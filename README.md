# Rampage Image Viewer

A reusable Codex plugin for SVG and image previews with numbered comments and freehand drawing.

## Install in Codex

Install from this repository:

```sh
codex plugin marketplace add https://github.com/Charlie2k26/rampage-image-viewer.git
codex plugin add image-viewer@rampage
```

Start a new chat, attach an image, and ask: “Use Image Viewer to open this image.”

## Features

- Click to add numbered comments; hold the left mouse button and drag to draw.
- Compact popups, persistent numbers, hover previews and outside-click dismissal.
- Send one comment or right-click to send all comments to chat.
- SVG Preview, Code, Copy source and Download SVG.
- Raster previews and downloads; fresh comments for each new image.

## Requirements

Codex with inline visualizations and the visualize skill, Python 3, and Pillow for raster images. HEIC fallback uses macOS sips. This plugin is not a standalone browser application. Oversized images may use a reduced display copy; original artwork is preserved.

## Data handling

Images are embedded in the generated local viewer. Comments can be saved in Codex widget state and sent to the current chat only through explicit actions. The viewer loads Google Sans Flex from Google Fonts. No separate Rampage server is used.

Publisher: Rampage.
