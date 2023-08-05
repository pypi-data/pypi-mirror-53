"""
Tools for aperture photometry with non native bg/error methods

This function serves to ease the computation of photometric magnitudes
and errors using PhotUtils by replicating DAOPHOT's photometry and
error methods.  The formula for DAOPHOT's error is:

err = sqrt (Poisson_noise / epadu + area * stdev**2 + area**2 * stdev**2 / nsky)

Which gives a magnitude error:

mag_err = 1.0857 * err / flux

Where epadu is electrons per ADU (gain), area is the photometric
aperture area, stdev is the uncertainty in the sky measurement
and nsky is the sky annulus area.  To get the uncertainty in the sky
we must use a custom background tool, which also enables computation of
the mean and median of the sky as well (more robust statistics).
All the stats are sigma clipped.  These are calculated by the
functions in aperture_stats_tbl.

.. note::
    Currently, the background computations will fully include a pixel that has ANY overlap with the background aperture (the annulus). This is to simplify the computation of the median, as a weighted median is nontrivial, and slower.
    Copied from https://grit.stsci.edu/HLA/software/blob/master/HLApipeline/HLApipe/scripts/photometry_tools.py
Authors
-------
    - Varun Bajaj, January 2018

Use
---

::

    from photometry_tools import iraf_style_photometry
    phot_aps = CircularAperture((sources['xcentroid'], sources['ycentroid']),r=10.)
    bg_aps = CircularAnnulus((sources['xcentroid'], sources['ycentroid']), r_in=13., r_out=15.)

Simplest call:

::

    photometry_tbl = iraf_style_photometry(phot_aps, bg_aps, data)

Pass in pixelwise error and set background to mean

::

    photometry_tbl = iraf_style_photometry(phot_aps, bg_aps, data, error_array=data_err, bg_method='mean')

Can also set the gain (if image units are DN)

::

    photometry_tbl = iraf_style_photometry(phot_aps, bg_aps, data, epadu=2.5)

Classes and Functions
---------------------
"""

import numpy as np
from astropy.table import Table
from background_median import aperture_stats_tbl
from photutils import aperture_photometry
import pdb


def iraf_style_photometry(phot_apertures,bg_apertures,data,platescale,
                          error_array=None,bg_method='mode',epadu=1.0,zero_point=0.0):
    """
    Computes photometry with PhotUtils apertures, with IRAF formulae

    Parameters
    ----------
    phot_apertures : photutils PixelAperture object (or subclass)
        The PhotUtils apertures object to compute the photometry. i.e. the object returned via CirularAperture.

    bg_apertures : photutils PixelAperture object (or subclass)
        The phoutils aperture object to measure the background in. i.e. the object returned via CircularAnnulus.

    data : array
        The data for the image to be measured.

    platescale : float
        instrument platescale in arcseconds per pixel.

    error_array : array
        (Optional) The array of pixelwise error of the data.  If none, the Poisson noise term in the error computation
        will just be the square root of the flux/epadu. If not none, the aperture_sum_err column output by
        aperture_photometry (divided by epadu) will be used as the Poisson noise term.

    bg_method: string
        {'mean', 'median', 'mode'}, optional. The statistic used to calculate the background. All measurements are
        sigma clipped. Default value is 'mode'. NOTE: From DAOPHOT, mode = 3 * median - 2 * mean.

    epadu : float
        (optional) Gain in electrons per adu (only use if image units aren't e-). Default value is 1.0

    zero_point: float
        (optional) Photometric zeropoint used to compute magnitude values from flux values. Default value is 0.0

    Returns
    -------
        An astropy Table with 'XCENTER', 'YCENTER', 'ID', 'FLUX_0.05', 'FERR_0.05', 'MAG_0.05', 'MERR_0.05',
        'FLUX_0.15', 'FERR_0.15', 'MAG_0.15', 'MERR_0.15', 'MSKY', and 'STDEV' values for each of the sources.
    """
    if bg_method not in ['mean', 'median', 'mode']:
        raise ValueError('Invalid background method, choose either \
                          mean, median, or mode')

    phot = aperture_photometry(data, phot_apertures, error=error_array)
    bg_phot = aperture_stats_tbl(data, bg_apertures, sigma_clip=True)

    names = ['XCENTER', 'YCENTER', 'ID']
    X, Y = phot_apertures[0].positions.T
    finalStacked = np.stack([X, Y, phot["id"].data], axis=1)
    nAper = 0
    nameList = 'FLUX', 'FERR', 'MAG', 'MERR'
    for item in list(phot.keys()):
        if item.startswith("aperture_sum_") and not item.startswith("aperture_sum_err_"):
            aperSize_arcsec = phot_apertures[nAper].r * platescale
            for name in nameList:
                names.append("{}_{}".format(name, aperSize_arcsec))
            nAper += 1

    for aperCtr in range(0, nAper):
        ap_area = phot_apertures[aperCtr].area()
        bg_method_name = 'aperture_{}'.format(bg_method)

        flux = phot['aperture_sum_{}'.format(aperCtr)] - bg_phot[bg_method_name] * ap_area

        # Need to use variance of the sources
        # for Poisson noise term in error computation.
        #
        # This means error needs to be squared.
        # If no error_array error = flux ** .5

        if error_array is not None:
            flux_error = compute_phot_error(phot['aperture_sum_err_{}'.format(aperCtr)] ** 2.0, bg_phot, bg_method,
                                            ap_area, epadu)
        else:
            flux_error = compute_phot_error(flux, bg_phot, bg_method, ap_area, epadu)

        mag = zero_point - 2.5 * np.log10(flux)
        mag_err = 1.0857 * flux_error / flux

        # Build the final data table
        stacked = np.stack([flux, flux_error, mag, mag_err], axis=1)
        finalStacked = np.concatenate([finalStacked, stacked], axis=1)
    # Build final output table
    final_tbl = Table(data=finalStacked, names=names,
                      dtype=[np.float64, np.float64, np.int64, np.float64, np.float64, np.float64, np.float64,
                             np.float64, np.float64, np.float64, np.float64])

    # add sky and std dev columns from background calculation subroutine
    final_tbl.add_column(bg_phot[bg_method_name])
    final_tbl.rename_column(bg_method_name, 'MSKY')
    final_tbl.add_column(bg_phot['aperture_std'])
    final_tbl.rename_column('aperture_std', 'STDEV')

    # # Add some empty columns to match the current final output DAOPHOT
    # emptyTotMag = MaskedColumn(name="TotMag(0.15)", fill_value=None, mask=True, length=len(final_tbl['X-CENTER'].data),
    #                            dtype=np.int64)
    # emptyTotMagErr = MaskedColumn(name="TotMagErr(0.15)", fill_value=None, mask=True,
    #                               length=len(final_tbl['X-CENTER'].data), dtype=np.int64)
    # final_tbl.add_column(emptyTotMag)
    # final_tbl.add_column(emptyTotMagErr)

    return final_tbl

def compute_phot_error( flux_variance, bg_phot, bg_method, ap_area, epadu=1.0):
    """Computes the flux errors using the DAOPHOT style computation

    Parameters
    ----------
    flux_variance : array
        flux values

    bg_phot : array
        background brightness values.

    bg_method : string
        background method

    ap_area : array
        the area of the aperture in square pixels

    epadu : float
        (optional) Gain in electrons per adu (only use if image units aren't e-). Default value is 1.0

    Returns
    -------
    flux_error : array
        an array of flux errors
    """
    bg_variance_terms = (ap_area * bg_phot['aperture_std'] ** 2. ) \
                        * (1. + ap_area/bg_phot['aperture_area'])
    variance = flux_variance / epadu + bg_variance_terms
    flux_error = variance ** .5
    return flux_error
