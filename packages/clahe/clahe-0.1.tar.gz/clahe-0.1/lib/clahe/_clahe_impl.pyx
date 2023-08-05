#cython: binding=True
#cython: boundscheck=False
#cython: cdivision=True
#cython: initializedcheck=False
#cython: language_level=3
#cython: wraparound=False

# Adaptive Histogram Equalization and Its Variations, Pizer et al. (1987).

cimport numpy as np

import numpy as np


ctypedef fused dtype:
    np.npy_uint8
    np.npy_int8
    np.npy_uint16
    np.npy_int16
    np.npy_uint32
    np.npy_int32
    np.npy_uint64
    np.npy_int64


def clahe(dtype[:, :, :] img,
          size_t wx,
          size_t wy,
          size_t wz,
          double clip_limit,
          bint multiplicative=False):
    cdef:
        dtype[::1] orig_vals = np.unique(img)
        size_t[:, :, ::1] img_ord = np.searchsorted(orig_vals, img).view(np.uintp)
        size_t nx = img_ord.shape[0], ny = img_ord.shape[1], nz = img_ord.shape[2], \
            x0, y0, z0, x, y, z, \
            win_size = wx * wy * wz, \
            val, viter, nvals = orig_vals.shape[0]
        double count_clip = clip_limit * win_size / nvals, clip_sum, clip_psum
        size_t[::1] hist = np.zeros(nvals, np.uintp)
        double[:, :, ::1] out = np.zeros_like(img_ord, np.double)
    for z0 in range(nz - wz + 1):
        for y0 in range(ny - wy + 1):
            hist[:] = 0
            for z in range(z0, z0 + wz):
                for y in range(y0, y0 + wy):
                    for x in range(wx - 1):
                        hist[img_ord[x, y, z]] += 1
            for x0 in range(nx - wx + 1):
                # Update histogram.
                for z in range(z0, z0 + wz):
                    for y in range(y0, y0 + wy):
                        hist[img_ord[x0 + wx - 1, y, z]] += 1
                # Limit contrast.
                val = img_ord[
                    x0 + (wx - 1) // 2, y0 + (wy - 1) // 2, z0 + (wz - 1) // 2]
                clip_sum = 0
                for viter in range(val):
                    clip_sum += min(hist[viter], count_clip)
                clip_psum = clip_sum + min(hist[val], count_clip) / 2.
                for viter in range(val, nvals):
                    clip_sum += min(hist[viter], count_clip)
                out[x0 + (wx - 1) // 2, y0 + (wy - 1) // 2, z0 + (wz - 1) // 2] = (
                    # Multiplicative redistribution.
                    clip_psum / clip_sum
                    if multiplicative else
                    # Additive redistribution.
                    (clip_psum
                     + (win_size - clip_sum)
                     * (orig_vals[val] + .5) / (orig_vals[nvals - 1] + 1))
                    / win_size)
                # Update histogram.
                for z in range(z0, z0 + wz):
                    for y in range(y0, y0 + wy):
                        hist[img_ord[x0, y, z]] -= 1
    return np.asarray(out)
