#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Unity UI Auto Slicer
- No OpenCV dependency. Only requires Pillow.
- Ask for an image path first.
- Output sliced PNG files under ./sliced_output/<image_name>_<timestamp>/
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

DISABLED_MESSAGE = (
    "Unity UI Auto Slicer is disabled for unity-ugui-ui-workflow. "
    "Provide pre-sliced element images instead."
)

if __name__ == "__main__":
    raise SystemExit(DISABLED_MESSAGE)

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception as exc:
    print("Pillow is not installed.")
    print("Please run: python -m pip install pillow")
    raise

Box = Tuple[int, int, int, int]  # left, top, right, bottom, right/bottom are exclusive


def safe_print(*args, **kwargs) -> None:
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        text = " ".join(str(a) for a in args)
        sys.stdout.buffer.write((text + "\n").encode("utf-8", errors="replace"))


def normalize_input_path(raw: str) -> Path:
    raw = raw.strip().strip('"').strip("'")
    # Windows drag-and-drop may append spaces. Keep internal spaces.
    return Path(raw).expanduser()


def prompt_path() -> Path:
    safe_print("============================================================")
    safe_print(" Unity UI Auto Slicer v2 - no cv2 / OpenCV")
    safe_print("============================================================")
    safe_print("Drag an image file here, or type the full image path, then press Enter.")
    raw = input("Image path: ").strip()
    if not raw:
        raise SystemExit("No image path provided.")
    p = normalize_input_path(raw)
    if not p.exists():
        raise SystemExit(f"Image not found: {p}")
    if not p.is_file():
        raise SystemExit(f"Not a file: {p}")
    return p


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    ans = input(f"{prompt} {suffix}: ").strip().lower()
    if not ans:
        return default
    return ans in ("y", "yes", "1", "true")


def ask_int(prompt: str, default: int, min_value: int = 0) -> int:
    ans = input(f"{prompt} [{default}]: ").strip()
    if not ans:
        return default
    try:
        return max(min_value, int(ans))
    except ValueError:
        safe_print(f"Invalid number. Use default: {default}")
        return default


def ask_settings() -> Dict[str, int]:
    settings = {
        "padding": 8,
        "group_gap": 18,
        "min_area": 120,
        "min_width": 8,
        "min_height": 8,
        "bg_threshold": 18,
        "alpha_threshold": 8,
        "chroma_threshold": 8,
    }
    if ask_yes_no("Use default slicing settings?", True):
        return settings
    safe_print("")
    safe_print("Advanced settings. Press Enter to keep the default value.")
    safe_print("Tip: if one asset is cut into small pieces, increase group_gap.")
    safe_print("Tip: if small icons are missed, decrease min_area.")
    safe_print("Tip: if background remains, increase bg_threshold a little.")
    settings["padding"] = ask_int("padding", settings["padding"], 0)
    settings["group_gap"] = ask_int("group_gap", settings["group_gap"], 0)
    settings["min_area"] = ask_int("min_area", settings["min_area"], 1)
    settings["min_width"] = ask_int("min_width", settings["min_width"], 1)
    settings["min_height"] = ask_int("min_height", settings["min_height"], 1)
    settings["bg_threshold"] = ask_int("bg_threshold", settings["bg_threshold"], 0)
    settings["chroma_threshold"] = ask_int("chroma_threshold", settings["chroma_threshold"], 0)
    return settings


class DSU:
    def __init__(self) -> None:
        self.parent: List[int] = []
        self.rank: List[int] = []

    def make(self) -> int:
        i = len(self.parent)
        self.parent.append(i)
        self.rank.append(0)
        return i

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> int:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return ra
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return ra


def has_real_alpha(img: Image.Image, alpha_threshold: int = 250) -> bool:
    if img.mode not in ("RGBA", "LA"):
        return False
    alpha = img.getchannel("A")
    mn, mx = alpha.getextrema()
    return mn < alpha_threshold


def quantize_color(rgb: Tuple[int, int, int], step: int = 16) -> Tuple[int, int, int]:
    return tuple(int(v // step) for v in rgb)


def dequantize_color(q: Tuple[int, int, int], step: int = 16) -> Tuple[int, int, int]:
    return tuple(int(min(255, v * step + step // 2)) for v in q)


def dominant_edge_colors(img: Image.Image, max_colors: int = 8, sample_step: int = 8) -> List[Tuple[int, int, int]]:
    rgb = img.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    counts: Counter[Tuple[int, int, int]] = Counter()

    def add(x: int, y: int) -> None:
        counts[quantize_color(px[x, y])] += 1

    for x in range(0, w, sample_step):
        add(x, 0)
        add(x, h - 1)
    for y in range(0, h, sample_step):
        add(0, y)
        add(w - 1, y)

    # Make sure corners are included heavily.
    for xy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        for _ in range(20):
            add(*xy)

    colors = [dequantize_color(q) for q, _ in counts.most_common(max_colors)]
    # If the edge is checkerboard/solid, these are enough.
    return colors or [(255, 255, 255)]


def color_dist2(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> int:
    dr = a[0] - b[0]
    dg = a[1] - b[1]
    db = a[2] - b[2]
    return dr * dr + dg * dg + db * db


def build_foreground_mask(
    img: Image.Image,
    bg_threshold: int,
    alpha_threshold: int,
    chroma_threshold: int,
) -> Tuple[bytearray, bool, List[Tuple[int, int, int]]]:
    """Return mask bytearray of length w*h, 255 foreground, 0 background.
    Also returns whether original alpha was used as the main source.
    """
    rgba = img.convert("RGBA")
    w, h = rgba.size
    used_alpha = has_real_alpha(rgba)
    mask = bytearray(w * h)

    if used_alpha:
        alpha = rgba.getchannel("A").tobytes()
        for i, a in enumerate(alpha):
            if a > alpha_threshold:
                mask[i] = 255
        return mask, True, []

    bg_colors = dominant_edge_colors(rgba)
    rgb = rgba.convert("RGB")
    data = rgb.tobytes()
    thr2 = bg_threshold * bg_threshold

    # Foreground if color differs from the background OR is not neutral-gray enough.
    # This catches pale jade/gold UI plates on a white/gray checker background.
    for i in range(0, len(data), 3):
        r, g, b = data[i], data[i + 1], data[i + 2]
        chroma = max(r, g, b) - min(r, g, b)
        d2 = min(color_dist2((r, g, b), bg) for bg in bg_colors)
        if d2 > thr2 or chroma > chroma_threshold:
            mask[i // 3] = 255
    return mask, False, bg_colors


def connected_components_from_mask(
    mask: bytearray,
    w: int,
    h: int,
    min_area: int,
    min_width: int,
    min_height: int,
) -> List[Tuple[Box, int]]:
    """Connected components using run-length union-find. Fast enough without numpy/cv2."""
    dsu = DSU()
    runs: List[Tuple[int, int, int, int]] = []  # y, x1, x2 inclusive, id
    prev_runs: List[Tuple[int, int, int, int]] = []

    for y in range(h):
        row_start = y * w
        row = mask[row_start:row_start + w]
        cur_runs: List[Tuple[int, int, int, int]] = []
        x = 0
        while x < w:
            while x < w and row[x] == 0:
                x += 1
            if x >= w:
                break
            x1 = x
            while x < w and row[x] != 0:
                x += 1
            x2 = x - 1
            cid = dsu.make()
            # Merge with previous-row runs if overlapping or touching.
            for py, px1, px2, pid in prev_runs:
                if px2 < x1 - 1:
                    continue
                if px1 > x2 + 1:
                    break
                dsu.union(cid, pid)
            cur_runs.append((y, x1, x2, cid))
        runs.extend(cur_runs)
        prev_runs = cur_runs

    bboxes: Dict[int, List[int]] = {}
    areas: Dict[int, int] = defaultdict(int)
    for y, x1, x2, cid in runs:
        r = dsu.find(cid)
        if r not in bboxes:
            bboxes[r] = [x1, y, x2 + 1, y + 1]
        else:
            box = bboxes[r]
            box[0] = min(box[0], x1)
            box[1] = min(box[1], y)
            box[2] = max(box[2], x2 + 1)
            box[3] = max(box[3], y + 1)
        areas[r] += (x2 - x1 + 1)

    comps: List[Tuple[Box, int]] = []
    image_area = w * h
    for r, box_list in bboxes.items():
        l, t, rr, bb = box_list
        area = areas[r]
        bw, bh = rr - l, bb - t
        # Ignore tiny specks and accidental full-canvas selections.
        if area < min_area or bw < min_width or bh < min_height:
            continue
        if bw * bh > image_area * 0.96:
            continue
        comps.append(((l, t, rr, bb), area))
    return comps


def expand_box(box: Box, pad: int, w: int, h: int) -> Box:
    l, t, r, b = box
    return (max(0, l - pad), max(0, t - pad), min(w, r + pad), min(h, b + pad))


def boxes_intersect_or_close(a: Box, b: Box, gap: int) -> bool:
    al, at, ar, ab = a
    bl, bt, br, bb = b
    return not (ar + gap < bl or br + gap < al or ab + gap < bt or bb + gap < at)


def box_contains(a: Box, b: Box) -> bool:
    al, at, ar, ab = a
    bl, bt, br, bb = b
    return al <= bl and at <= bt and ar >= br and ab >= bb


def union_box(a: Box, b: Box) -> Box:
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def merge_boxes(boxes: List[Box], group_gap: int) -> List[Box]:
    if not boxes:
        return []
    boxes = boxes[:]
    changed = True
    while changed:
        changed = False
        result: List[Box] = []
        used = [False] * len(boxes)
        for i, box in enumerate(boxes):
            if used[i]:
                continue
            merged = box
            used[i] = True
            local_changed = True
            while local_changed:
                local_changed = False
                for j, other in enumerate(boxes):
                    if used[j]:
                        continue
                    if boxes_intersect_or_close(merged, other, group_gap) or box_contains(merged, other) or box_contains(other, merged):
                        merged = union_box(merged, other)
                        used[j] = True
                        local_changed = True
                        changed = True
            result.append(merged)
        boxes = result
    return boxes


def flood_asset_mask(mask_crop: bytes, w: int, h: int) -> bytearray:
    """Given a rough foreground mask, return asset mask.
    False regions connected to crop edges are background.
    Everything else, including enclosed pale interior, is preserved as asset.
    """
    n = w * h
    outside = bytearray(n)
    q: deque[int] = deque()

    def push(idx: int) -> None:
        if mask_crop[idx] == 0 and outside[idx] == 0:
            outside[idx] = 1
            q.append(idx)

    for x in range(w):
        push(x)
        push((h - 1) * w + x)
    for y in range(h):
        push(y * w)
        push(y * w + (w - 1))

    while q:
        idx = q.popleft()
        x = idx % w
        y = idx // w
        if x > 0:
            push(idx - 1)
        if x + 1 < w:
            push(idx + 1)
        if y > 0:
            push(idx - w)
        if y + 1 < h:
            push(idx + w)

    asset = bytearray(n)
    for i in range(n):
        if outside[i] == 0:
            asset[i] = 255
    return asset


def crop_mask_bytes(mask: bytearray, image_w: int, box: Box) -> bytes:
    l, t, r, b = box
    out = bytearray((r - l) * (b - t))
    pos = 0
    for y in range(t, b):
        start = y * image_w + l
        end = y * image_w + r
        row = mask[start:end]
        out[pos:pos + (r - l)] = row
        pos += (r - l)
    return bytes(out)


def sort_boxes_reading_order(boxes: List[Box]) -> List[Box]:
    if not boxes:
        return []
    heights = sorted((b[3] - b[1]) for b in boxes)
    median_h = heights[len(heights) // 2]
    row_tol = max(10, median_h // 2)
    boxes_sorted = sorted(boxes, key=lambda b: (b[1], b[0]))
    rows: List[List[Box]] = []
    for box in boxes_sorted:
        placed = False
        cy = (box[1] + box[3]) // 2
        for row in rows:
            row_cy = sum((b[1] + b[3]) // 2 for b in row) // len(row)
            if abs(cy - row_cy) <= row_tol:
                row.append(box)
                placed = True
                break
        if not placed:
            rows.append([box])
    rows.sort(key=lambda row: min(b[1] for b in row))
    result: List[Box] = []
    for row in rows:
        result.extend(sorted(row, key=lambda b: b[0]))
    return result


def save_preview(img: Image.Image, boxes: Sequence[Box], out_path: Path) -> None:
    preview = img.convert("RGBA")
    draw = ImageDraw.Draw(preview)
    for i, box in enumerate(boxes, 1):
        l, t, r, b = box
        # Red rectangle. Chosen for visibility in previews.
        draw.rectangle([l, t, r - 1, b - 1], outline=(255, 0, 0, 255), width=3)
        label = str(i)
        tx, ty = l + 4, max(0, t - 18)
        draw.rectangle([tx - 2, ty, tx + 8 * len(label) + 4, ty + 16], fill=(255, 255, 255, 220))
        draw.text((tx, ty), label, fill=(255, 0, 0, 255))
    preview.save(out_path)


def save_slices(
    img: Image.Image,
    mask: bytearray,
    boxes: Sequence[Box],
    out_dir: Path,
    used_alpha: bool,
) -> List[Dict[str, object]]:
    rgba = img.convert("RGBA")
    w, h = rgba.size
    manifest: List[Dict[str, object]] = []
    for index, box in enumerate(boxes, 1):
        l, t, r, b = box
        crop = rgba.crop(box)
        cw, ch = r - l, b - t
        if not used_alpha:
            rough = crop_mask_bytes(mask, w, box)
            alpha = flood_asset_mask(rough, cw, ch)
            crop.putalpha(Image.frombytes("L", (cw, ch), bytes(alpha)))
        filename = f"slice_{index:03d}_{l}_{t}_{cw}x{ch}.png"
        crop.save(out_dir / filename)
        manifest.append({
            "index": index,
            "file": filename,
            "x": l,
            "y": t,
            "width": cw,
            "height": ch,
            "bbox": [l, t, r, b],
        })
    return manifest


def run_once(image_path: Path, settings: Dict[str, int]) -> Path:
    script_dir = Path(__file__).resolve().parent
    output_root = script_dir / "sliced_output"
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_dir = output_root / f"{image_path.stem}_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    img = Image.open(image_path).convert("RGBA")
    w, h = img.size
    safe_print("")
    safe_print(f"Loaded image: {image_path}")
    safe_print(f"Image size: {w} x {h}")
    safe_print("Detecting foreground...")

    mask, used_alpha, bg_colors = build_foreground_mask(
        img,
        bg_threshold=settings["bg_threshold"],
        alpha_threshold=settings["alpha_threshold"],
        chroma_threshold=settings["chroma_threshold"],
    )

    if used_alpha:
        safe_print("Mode: transparent PNG alpha")
    else:
        safe_print(f"Mode: baked background removal, sampled background colors: {bg_colors}")

    comps = connected_components_from_mask(
        mask,
        w,
        h,
        min_area=settings["min_area"],
        min_width=settings["min_width"],
        min_height=settings["min_height"],
    )
    raw_boxes = [box for box, area in comps]
    safe_print(f"Raw components: {len(raw_boxes)}")

    boxes = merge_boxes(raw_boxes, settings["group_gap"])
    boxes = [expand_box(b, settings["padding"], w, h) for b in boxes]
    boxes = merge_boxes(boxes, 0)
    boxes = sort_boxes_reading_order(boxes)

    if not boxes:
        raise RuntimeError("No slices detected. Try advanced settings: lower min_area or lower bg_threshold.")

    manifest = save_slices(img, mask, boxes, out_dir, used_alpha)
    save_preview(img, boxes, out_dir / "preview_boxes.png")

    data = {
        "source_image": str(image_path),
        "image_width": w,
        "image_height": h,
        "settings": settings,
        "used_alpha": used_alpha,
        "count": len(manifest),
        "slices": manifest,
        "unity_import_recommendation": {
            "Texture Type": "Sprite (2D and UI)",
            "Sprite Mode": "Single",
            "Mesh Type": "Full Rect",
            "Compression": "None",
            "Filter Mode": "Bilinear"
        }
    }
    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    safe_print("")
    safe_print(f"Done. Slices: {len(manifest)}")
    safe_print(f"Output folder: {out_dir}")
    safe_print("Preview file: preview_boxes.png")
    return out_dir


def main() -> None:
    raise SystemExit(DISABLED_MESSAGE)
    try:
        if len(sys.argv) > 1:
            image_path = normalize_input_path(" ".join(sys.argv[1:]))
            if not image_path.exists():
                raise SystemExit(f"Image not found: {image_path}")
            settings = {
                "padding": 8,
                "group_gap": 18,
                "min_area": 120,
                "min_width": 8,
                "min_height": 8,
                "bg_threshold": 18,
                "alpha_threshold": 8,
                "chroma_threshold": 8,
            }
        else:
            image_path = prompt_path()
            settings = ask_settings()
        run_once(image_path, settings)
    except KeyboardInterrupt:
        safe_print("Cancelled.")
    except Exception as exc:
        safe_print("")
        safe_print("ERROR:", exc)
        safe_print("")
        safe_print("Try again with advanced settings:")
        safe_print("- Increase group_gap if one asset is split into many pieces.")
        safe_print("- Decrease min_area if small assets are missed.")
        safe_print("- Increase bg_threshold if the baked background remains.")
        raise


if __name__ == "__main__":
    main()
