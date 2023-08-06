import numpy as np
import scipy.ndimage as ndi

from florin.ndnt import integral_image, integral_image_sum, ndnt


def hausdorff(a, b, mode='max'):
    """Approximation of the pixel-wise Hausdorff distance.

    Given two arrays of image segmentations, find the maximum (or mean) minimum
    distance from any positive pixel in ``a`` to the nearest positive pixel in
    ``b``.

    Parameters
    ----------
    a : array_like
    b : array_like
        The binary segmentation arrays to compare.
    mode : {'max','mean'}

    Returns
    -------
    distance : float
        The
    """
    if a.shape[0] == 0 or b.shape[0] == 0 and not a.shape[0] == b.shape[0]:
            return np.inf
    # elif a.shape[0] == 0 and b.shape[0] == 0:
    #     return 0
    else:
        a_mesh, b_mesh = np.meshgrid(
            np.arange(a.shape[0], dtype=np.int16),
            np.arange(b.shape[0], dtype=np.int16),
            indexing='ij', sparse=True)
        dists = np.abs(
            np.subtract(a[a_mesh], b[b_mesh], dtype=np.int16),
            dtype=np.int16)

        del a_mesh, b_mesh

        if mode == 'mean':
            dist = max(np.mean(np.min(dists, axis=1)),
                       np.mean(np.min(dists.T, axis=1)))
        else:
            dist = max(np.max(np.min(dists, axis=1)),
                       np.max(np.min(dists.T, axis=1)))
        return dist


def match_histogram(img, ref):
    """Match the histogram of an image to a reference image.

    Parameters
    ----------
    img : array_like
        The image to match.
    ref : array_like
        The image to map ``img`` to.

    Returns
    -------
    matched : array_like
        ``img`` with its histogram matched to ``ref``.
    """
    def _cumsum(arr):
        summed = np.zeros(arr.shape)
        summed[0] += arr[0]
        for i in range(1, summed.shape[0]):
            summed[i] += arr[i] + summed[i - 1]
        return summed

    matched = np.zeros(img.shape, dtype=img.dtype)

    ref_hist, bins = np.histogram(ref.ravel(), bins=np.arange(256),
                                  range=(0, 255), density=True)
    ref_cdf = _cumsum(ref_hist)
    ref_cdf = (255 * ref_cdf / ref_cdf[-1])

    img_hist, _ = np.histogram(img.ravel(), bins=np.arange(256),
                               range=(0, 255), density=True)
    img_cdf = _cumsum(img_hist)
    img_cdf = (255 * img_cdf / img_cdf[-1])

    new = np.interp(img, bins[:-1], img_cdf)
    matched += np.interp(new, ref_cdf, bins[:-1]).astype(img.dtype)
    return matched


def autotuning(img, proxy_img, proxy_seg, shape=None, delta=0.1, decay=0.1,
               min_delta=1e-3):
    """Automatically optimize the threshold parameter of NDNT using RCA.

    This method is based on the Reverse Classification Accuracy (RCA)
    introduced by ... , which uses labeled proxy data from a similar dataset as
    a placeholder for annotations.

    Parameters
    ----------
    img : array_like
        The image to tune the threshold value for.
    proxy_img : array_like
        Proxy image data from a similar dataset of a simlar size to ``img``.
    proxy_seg : array_like
        Segmentation labels of ``proxy_img``.
    shape : array-like, optional
        The dimensions of the local neighborhood around each pixel/voxel.
    delta : float, optional
        The step between threshold values to search.
    decay : float, optional
        The decay between steps in rounds of the grid search.
    min_delta : float, optional
        The minimum delta to search.
    """
    if img.size == 0 or np.mean(img) <= 30:
        return 1.0

    max_size = np.product(np.asarray(shape)) * 0.666

    center = int(proxy_seg.shape[0] / 2)

    proxy_img = match_histogram(proxy_img, img)

    lo = 0.0
    hi = 1.0

    sel = ndi.generate_binary_structure(3, 1)
    sel[0] = 0
    sel[2] = 0

    ref_ccs = np.logical_xor(proxy_seg,
                             ndi.binary_erosion(proxy_seg, structure=sel))
    ref_coords = np.asarray(np.nonzero(ref_ccs)).T.astype(np.int16)

    int_img = integral_image(proxy_img)
    sums, counts = integral_image_sum(int_img, np.asarray(shape))
    del int_img, ref_ccs

    while (hi - lo) > min_delta:
        t_vals = np.arange(lo, hi, delta)
        h_dists = np.zeros(t_vals.shape)

        for i, val in enumerate(t_vals):
            if val == 0:
                val += 1e-7
            thresh = ndnt(proxy_img, shape=shape, threshold=val,
                          sums=sums, counts=counts)
            seg = np.logical_xor(thresh,
                                 ndi.binary_erosion(thresh, structure=sel))
            h_dists[i] += hausdorff(
                np.asarray(seg.nonzero()).T.astype(np.int16), ref_coords)

        idx = np.argsort(h_dists)[0]

        if idx == 0:
            lo = t_vals[idx]
            hi = t_vals[idx + 1]
        elif idx == t_vals.shape[0] - 1:
            lo = t_vals[idx - 1]
            hi = t_vals[idx]
        else:
            if t_vals[idx - 1] < t_vals[idx + 1]:
                lo = t_vals[idx - 1]
                hi = t_vals[idx]
            elif t_vals[idx + 1] < t_vals[idx - 1]:
                lo = t_vals[idx]
                hi = t_vals[idx + 1]
            else:
                lo = t_vals[idx - 1]
                hi = t_vals[idx + 1]
        delta *= decay

    t = (hi + lo) / 2.0
    return ndnt(img, shape=shape, threshold=t)
