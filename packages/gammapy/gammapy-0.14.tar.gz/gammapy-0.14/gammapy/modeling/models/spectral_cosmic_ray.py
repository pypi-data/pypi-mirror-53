# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Simple models for cosmic ray spectra at Earth.

For measurements, the "Database of Charged Cosmic Rays (CRDB)" is a great resource:
http://lpsc.in2p3.fr/cosmic-rays-db/
"""
from astropy import units as u
from .spectral import LogGaussianSpectralModel, PowerLawSpectralModel


def create_cosmic_ray_spectral_model(particle="proton"):
    """Cosmic a cosmic ray spectral model at Earth.

    These are the spectra assumed in this CTA study:
    Table 3 in https://ui.adsabs.harvard.edu/abs/2013APh....43..171B

    The hadronic spectra are simple power-laws, the electron spectrum
    is the sum of  a power law and a log-normal component to model the
    "Fermi shoulder".

    Parameters
    ----------
    particle : {'electron', 'proton', 'He', 'N', 'Si', 'Fe'}
        Particle type

    Returns
    -------
    flux : `~astropy.units.Quantity`
        Cosmic ray flux in unit ``m^-2 s^-1 TeV^-1 sr^-1``
    """
    if particle == "proton":
        return PowerLawSpectralModel(
            amplitude=0.096 * u.Unit("1 / (m2 s TeV sr)"),
            index=2.70,
            reference=1 * u.TeV,
        )
    elif particle == "N":
        return PowerLawSpectralModel(
            amplitude=0.0719 * u.Unit("1 / (m2 s TeV sr)"),
            index=2.64,
            reference=1 * u.TeV,
        )
    elif particle == "Si":
        return PowerLawSpectralModel(
            amplitude=0.0284 * u.Unit("1 / (m2 s TeV sr)"),
            index=2.66,
            reference=1 * u.TeV,
        )
    elif particle == "Fe":
        return PowerLawSpectralModel(
            amplitude=0.0134 * u.Unit("1 / (m2 s TeV sr)"),
            index=2.63,
            reference=1 * u.TeV,
        )
    elif particle == "electron":
        return PowerLawSpectralModel(
            amplitude=6.85e-5 * u.Unit("1 / (m2 s TeV sr)"),
            index=3.21,
            reference=1 * u.TeV,
        ) + LogGaussianSpectralModel(
            norm=3.19e-3 * u.Unit("1 / (m2 s sr)"), mean=0.107 * u.TeV, sigma=0.776
        )
    else:
        raise ValueError(f"Invalid particle: {particle!r}")
