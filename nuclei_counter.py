import cv2 as cv
import numpy as np
import tifffile as tiff

def count_nuclei(
    img_path: str,
    channel: int = 2,                 # default = red channel
    min_area: int = 40,
    max_area: int = 20000,
    blur_ksize: int = 3,
    maxima_ksize: int = 7,
    peak_thresh_frac: float = 0.35,
    dilate_iters: int = 2,
    do_seed_supplement: bool = True
):
    """
    Counts nuclei in a max projection image using:
    channel selection -> normalize -> blur -> Otsu -> distance -> local maxima seeds
    -> (optional) seed supplementation -> watershed -> area filtering.

    Returns:
        count (int)
        numbered_overlay (BGR uint8 image)
        debug (dict of intermediate images)
    """

    # --- Load image ---
    img = tiff.imread(img_path)
    if img.ndim == 2:
        nuclei = img
    elif img.ndim == 3 and img.shape[2] == 3:
        nuclei = img[:, :, channel]
    else:
        raise ValueError(f"Unsupported image shape: {img.shape}")

    # --- Normalize ---
    nuclei_norm = cv.normalize(nuclei, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)

    # --- Gentle blur ---
    if blur_ksize % 2 == 0:
        blur_ksize += 1
    blur = cv.GaussianBlur(nuclei_norm, (blur_ksize, blur_ksize), 0)

    # --- Otsu threshold ---
    otsu_val, binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # --- Distance transform ---
    dist = cv.distanceTransform(binary, cv.DIST_L2, 5)
    dist_blur = cv.GaussianBlur(dist, (3, 3), 0)

    # --- Local maxima seeds ---
    if maxima_ksize % 2 == 0:
        maxima_ksize += 1
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (maxima_ksize, maxima_ksize))
    dist_dil = cv.dilate(dist_blur, kernel)
    local_max = (dist_blur == dist_dil)

    peak_thresh = peak_thresh_frac * dist.max()
    seeds = (local_max & (dist_blur > peak_thresh) & (binary > 0)).astype(np.uint8) * 255

    # --- Optional seed supplementation (adds 1 seed to components with 0 seeds) ---
    if do_seed_supplement:
        num_cc, cc_labels, cc_stats, _ = cv.connectedComponentsWithStats(binary, connectivity=8)
        supp_seeds = seeds.copy()

        for i in range(1, num_cc):
            area = cc_stats[i, cv.CC_STAT_AREA]
            if area < min_area or area > max_area:
                continue

            comp_mask = (cc_labels == i)
            if np.count_nonzero(seeds[comp_mask]) == 0:
                dist_in_comp = dist.copy()
                dist_in_comp[~comp_mask] = 0
                y, x = np.unravel_index(np.argmax(dist_in_comp), dist_in_comp.shape)
                cv.circle(supp_seeds, (int(x), int(y)), 1, 255, -1)

        seeds = supp_seeds

    # --- Build markers and run watershed ---
    _, markers = cv.connectedComponents(seeds)
    markers = markers + 1

    k3 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    sure_bg = cv.dilate(binary, k3, iterations=dilate_iters)
    unknown = cv.subtract(sure_bg, seeds)
    markers[unknown == 255] = 0

    base_for_ws = cv.cvtColor(nuclei_norm, cv.COLOR_GRAY2BGR)
    markers_ws = cv.watershed(base_for_ws, markers.copy())

    # --- Filter by area ---
    obj_ids = np.unique(markers_ws)
    obj_ids = obj_ids[(obj_ids != 1) & (obj_ids != -1) & (obj_ids != 0)]

    kept = []
    for oid in obj_ids:
        area = np.count_nonzero(markers_ws == oid)
        if min_area <= area <= max_area:
            kept.append(oid)

    # --- Number overlay ---
    vis_numbers = base_for_ws.copy()
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.35
    thickness = 1
    color = (0, 255, 255)

    label_id = 1
    for oid in kept:
        mask = (markers_ws == oid).astype(np.uint8)
        M = cv.moments(mask)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv.putText(vis_numbers, str(label_id), (cx, cy), font, font_scale, color, thickness, cv.LINE_AA)
        label_id += 1

    debug = {
        "nuclei_norm": nuclei_norm,
        "blur": blur,
        "binary": binary,
        "dist": dist,
        "seeds": seeds,
        "markers_ws": markers_ws,
        "otsu_value": otsu_val
    }

    return len(kept), vis_numbers, debug