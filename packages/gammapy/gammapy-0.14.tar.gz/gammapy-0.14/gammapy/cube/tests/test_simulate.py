# Licensed under a 3-clause BSD style license - see LICENSE.rst
import numpy as np
from numpy.testing import assert_allclose
import astropy.units as u
from astropy.coordinates import SkyCoord
from gammapy.cube import MapDataset, simulate_dataset
from gammapy.irf import load_cta_irfs
from gammapy.maps import MapAxis, WcsGeom
from gammapy.modeling.models import (
    GaussianSpatialModel,
    PowerLawSpectralModel,
    SkyModel,
    SkyModels,
)
from gammapy.utils.testing import requires_data


@requires_data()
def test_simulate():
    irfs = load_cta_irfs(
        "$GAMMAPY_DATA/cta-1dc/caldb/data/cta/1dc/bcf/South_z20_50h/irf_file.fits"
    )

    # Define sky model to simulate the data
    spatial_model = GaussianSpatialModel(
        lon_0="0 deg", lat_0="0 deg", sigma="0.2 deg", frame="galactic"
    )
    spectral_model = PowerLawSpectralModel(
        index=2, amplitude="1e-11 cm-2 s-1 TeV-1", reference="1 TeV"
    )
    sky_model_simu = SkyModel(
        spatial_model=spatial_model, spectral_model=spectral_model
    )

    # Define map geometry
    axis = MapAxis.from_edges(
        np.logspace(-1, 1.0, 20), unit="TeV", name="energy", interp="log"
    )
    geom = WcsGeom.create(
        skydir=(0, 0), binsz=0.025, width=(1, 1), coordsys="GAL", axes=[axis]
    )

    # Define some observation parameters
    pointing = SkyCoord(0 * u.deg, 0 * u.deg, frame="galactic")

    dataset = simulate_dataset(
        sky_model_simu, geom, pointing, irfs, livetime=10 * u.h, random_state=42
    )

    assert isinstance(dataset, MapDataset)
    assert isinstance(dataset.model, SkyModels)

    assert dataset.counts.data.dtype is np.dtype("int")
    assert_allclose(dataset.counts.data[5, 20, 20], 5)
    assert_allclose(dataset.exposure.data[5, 20, 20], 16122681639.856329)
    assert_allclose(dataset.background_model.map.data[5, 20, 20], 0.976554, rtol=1e-5)
    assert_allclose(dataset.psf.data[5, 32, 32], 0.044402823)
    assert_allclose(dataset.edisp.data.data[10, 10], 0.662208, rtol=1e-5)
