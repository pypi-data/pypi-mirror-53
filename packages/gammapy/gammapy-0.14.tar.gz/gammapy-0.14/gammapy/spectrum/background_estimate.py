# Licensed under a 3-clause BSD style license - see LICENSE.rst


__all__ = ["BackgroundEstimate"]


class BackgroundEstimate:
    """Container class for background estimate.

    This container holds the result from a region based background estimation
    for one observation.

    Created e.g. by `~gammapy.spectrum.ReflectedRegionsBackgroundEstimator`.

    Parameters
    ----------
    on_region : `~regions.SkyRegion`
        Signal extraction region
    on_events : `~gammapy.data.EventList`
        Signal events
    off_region : `~regions.SkyRegion`
        Background extraction region
    off_events : `~gammapy.data.EventList`
        Background events
    a_on : float
        Relative background exposure of the on region
    a_off : float
        Relative background exposure of the off region
    method : str
        Background estimation method
    """

    def __init__(
        self,
        on_region,
        on_events,
        off_region,
        off_events,
        a_on,
        a_off,
        method="default",
    ):
        self.on_region = on_region
        self.on_events = on_events
        self.off_region = off_region
        self.off_events = off_events
        self.a_on = a_on
        self.a_off = a_off
        self.method = method

    def __str__(self):
        ss = self.__class__.__name__
        ss += f"\n Method: {self.method}"
        ss += "\n on region"
        ss += f"\n {self.on_region}"
        ss += f"\n {self.on_events}"
        ss += "\n off region"
        ss += f"\n {self.off_region}"
        ss += f"\n {self.off_events}"
        return ss
