---
name: image-region-picker
description: Use when the user wants to pick exact pixel coordinates or a region on an image (upload, click four points, confirm a box) and then edit only that area.
---

# Image region picker

Help the user mark a precise region on an image, then edit only that region and composite the result back onto the original.

## Helper

Open the bundled helper `picker.html` in this skill folder (the same directory as this SKILL.md).

On macOS, open it in the default browser. Use the path that exists:

```bash
# installed for every project
open ~/.cursor/skills/image-region-picker/picker.html

# this repository is the open workspace
open .cursor/skills/image-region-picker/picker.html
```

The page lets the user upload or drop an image, click exactly 4 points with a crosshair, draws numbered arrows and coordinates on the image (in the image's real pixel space, origin at the top-left), shows the bounding box, and on Confirm copies a region message to the clipboard (it does not download a file).

Coordinates must be computed from `naturalWidth` / `naturalHeight`, never from the on-screen scaled size.

Region message shape:

```
Selected region for image "photo.png" (1920×1080):
bounding box: x=120, y=80, x2=340, y2=200 (width 220, height 120)
points: (120, 80), (340, 80), (340, 200), (120, 200)

Please edit only this region and keep every pixel outside it unchanged.
```

JSON shape in `region.json`:

```json
{
  "image": "photo.png",
  "imageWidth": 1920,
  "imageHeight": 1080,
  "points": [{"x": 120, "y": 80}, {"x": 340, "y": 80}, {"x": 340, "y": 200}, {"x": 120, "y": 200}],
  "boundingBox": {"x": 120, "y": 80, "x2": 340, "y2": 200, "width": 220, "height": 120}
}
```

## Steps

1. If the user has not attached an image, they can still upload it in the picker. Ask them to also keep the original file available in the chat or workspace so you can edit it later.
2. Open `picker.html` for the user. Do not ask them to install anything.
3. Tell them to upload the image, click 4 points around the area to change, then click Confirm. They can Undo last or Reset points if needed.
4. The picker cannot type into the Cursor chat input by itself (a local web page is not allowed to control Cursor). Confirm copies the region message to the clipboard only — no file download. Ask the user to click the Cursor chat input and press ⌘V (Ctrl+V on Windows) to paste it.
5. When you have the region, remember the bounding box (and the 4 points as a polygon if the area is not a perfect rectangle).
6. When they ask to edit that area, do **not** regenerate the whole image. Crop or mask only the selected region, generate or edit that patch, then paste it back into the original image so pixels outside the region stay identical to the source. Feather the edge slightly if needed so the join is less obvious.
7. Be honest: this keeps the rest of the image unchanged by compositing, but the patched area is still a regeneration. Edges, lighting, or texture inside and just around the cut may not match perfectly. If they need exact typography or pixel-perfect fixes, recommend a professional editor (for example Photoshop) after the patch.
8. Show the result and keep the original plus the pasted region message so they can try again without re-picking points.
