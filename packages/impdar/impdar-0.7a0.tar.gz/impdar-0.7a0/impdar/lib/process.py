#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 dlilien <dlilien@berens>
#
# Distributed under terms of the GNU GPL3.0 license.

"""
Define generic processing functions to ease calls from executables.
"""
import os.path
import numpy as np

from .load import load
from .gpslib import interp as interpdeep


def process_and_exit(fn, cat=False, filetype='mat', **kwargs):
    """Perform one or more processing steps, save, and exit

    Parameters
    ----------
    fn: list of strs
        The filename(s) to process. Assumed to be .mat files unless gssi or pe is True.
    cat: bool, optional
        If True, concatenate files before processing rather than running through each individually
    filetype: str, optional
        The type of input file. Default is .mat.
    kwargs:
        These are the processing arguments for `process`
    """

    radar_data = load(filetype, fn)

    # first we do the quirky one
    if cat:
        radar_data = concat(radar_data)
        bn = os.path.splitext(fn[0])[0]
        if bn[-4:] == '_raw':
            bn = bn[:-4]
        fn = [bn + '_cat.mat']

    processed = process(radar_data, **kwargs)
    if not processed and not cat:
        print('No processing steps performed. Not saving!')
        return

    if 'o' in kwargs and kwargs['o'] is not None:
        if len(radar_data) > 1:
            for d, f in zip(radar_data, fn):
                bn = os.path.split(os.path.splitext(f)[0])[1]
                if bn[-4:] == '_raw':
                    bn = bn[:-4]
                out_fn = os.path.join(kwargs['o'], bn + '_proc.mat')
                d.save(out_fn)
        else:
            out_fn = kwargs['o']
            radar_data[0].save(out_fn)
    else:
        for d, f in zip(radar_data, fn):
            bn = os.path.splitext(f)[0]
            if bn[-4:] == '_raw':
                bn = bn[:-4]
            if cat:
                out_fn = bn + '.mat'
            else:
                out_fn = bn + '_proc.mat'
            d.save(out_fn)


def process(RadarDataList, interp=None, rev=False, vbp=None, hfilt=None, ahfilt=False, nmo=None, crop=None, hcrop=None, restack=None, denoise=None, migrate=None, **kwargs):
    """Perform one or more processing steps on a list of RadarData objects

    Parameters
    ----------
    RadarDataList: list of strs
        The `~impdar.RadarData` objects to process
    rev: bool, optional
        Reverse the profile orientation. Default is False.
    vbp: 2-tuple, optional
        Vertical bandpass between (vbp1, vbp2) MHz. Default None (no filtering).
    hfilt: 2-tuple, optional
        Horizontal filter subtracting average trace between (hfilt1, hfilt2). Default is None (no hfilt).
    ahfilt: bool, optional
        Adaptively horizontally filter the data.
    denoise: bool, optional
        denoising filter (only wiener for now).
    migrate: string, optional
        Migrates the data.

    Returns
    -------
    processed: bool
        If True, we did something, if False we didn't
    """

    # first some argument checking so we don't crash later
    if crop is not None:
        try:
            if crop[1] not in ['top', 'bottom']:
                raise ValueError('First element of crop must be in ["top", "bottom"]')
            if crop[2] not in ['snum', 'twtt', 'depth']:
                raise ValueError('Second element of crop must be in ["snum", "twtt", "depth"]')
            try:
                crop = (float(crop[0]), crop[1], crop[2])
            except ValueError:
                raise ValueError('Third element of crop must be convertible to a float')
        except TypeError:
            raise TypeError('Crop must be subscriptible')

    if hcrop is not None:
        try:
            if crop[1] not in ['left', 'right']:
                raise ValueError('First element of crop must be in ["left", "right"]')
            if crop[2] not in ['tnum', 'dist']:
                raise ValueError('Second element of crop must be in ["tnum", "dist"]')
            try:
                crop = (float(crop[0]), crop[1], crop[2])
            except ValueError:
                raise ValueError('Third element of crop must be convertible to a float')
        except TypeError:
            raise TypeError('Crop must be subscriptible')

    done_stuff = False
    # hcrop first to reduce computation
    if hcrop is not None:
        for dat in RadarDataList:
            dat.hcrop(*hcrop)
        done_stuff = True

    if restack is not None:
        for dat in RadarDataList:
            if type(restack) in [list, tuple]:
                restack = int(restack[0])
            dat.restack(restack)
        done_stuff = True

    if rev:
        for dat in RadarDataList:
            dat.reverse()
        done_stuff = True

    if vbp is not None:
        for dat in RadarDataList:
            dat.vertical_band_pass(*vbp)
        done_stuff = True

    if hfilt is not None:
        for dat in RadarDataList:
            dat.hfilt(ftype='hfilt', bounds=hfilt)
        done_stuff = True

    if ahfilt:
        for dat in RadarDataList:
            dat.hfilt(ftype='adaptive')
        done_stuff = True

    if nmo is not None:
        if type(nmo) == float:
            print('One nmo value given. Assuming that this is the separation. Uice=1.6')
            nmo = (nmo, 1.6)
        for dat in RadarDataList:
            dat.nmo(*nmo)
        done_stuff = True

    if denoise is not None:
        for dat in RadarDataList:
            dat.denoise(*denoise)
        done_stuff = True

    if interp is not None:
        interpdeep(RadarDataList, float(interp[0]), interp[1])
        done_stuff = True

    # Crop after nmo so that we have nmo_depth available for cropping if desired
    if crop is not None:
        for dat in RadarDataList:
            dat.crop(*crop)
        done_stuff = True

    if migrate is not None:
        dat.migrate(mtype='stolt')
        done_stuff = True

    if not done_stuff:
        return False
    return True


def concat(radar_data):
    """Concatenate all radar data input

    Parameters
    ----------
    radar_data: list of RadarData
        Objects to concatenate

    Returns
    -------
    RadarData
        A single, concatenated output.
    """
    from copy import deepcopy
    # let's do some checks to make sure we are consistent here
    out = deepcopy(radar_data[0])

    for dat in radar_data[1:]:
        if out.snum != dat.snum:
            raise ValueError('Need the same number of vertical samples in each file')
        if not np.all(out.travel_time == dat.travel_time):
            raise ValueError('Need matching travel time vectors')

    out.data = np.hstack([dat.data for dat in radar_data])
    tnums = np.hstack((np.array([0]), np.cumsum([dat.tnum for dat in radar_data])))
    out.tnum = out.data.shape[1]
    out.trace_num = np.hstack([dat.trace_num + tnum for dat, tnum in zip(radar_data, tnums)])
    dists = np.hstack((np.array([0]), np.cumsum([dat.dist[-1] for dat in radar_data])))
    out.dist = np.hstack([dat.dist + dist for dat, dist in zip(radar_data, dists)])
    for attr in ['pressure', 'trig_level', 'lat', 'long', 'x_coord', 'y_coord', 'elev', 'decday', 'trace_int']:
        setattr(out, attr, np.hstack([getattr(dat, attr) for dat in radar_data]))
    print('Objects concatenated')
    return [out]
