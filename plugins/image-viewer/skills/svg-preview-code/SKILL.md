---
name: svg-preview-code
description: Show SVGs, photos, screenshots and other images in an inline viewer with numbered popup comments and downloads. SVGs also provide Code and Copy source. Use for image viewing or annotation; this skill does not design or revise the source artwork.
---

# Image viewer with SVG Preview / Code

Present the selected SVG using the user's reusable viewing format:
- One viewer with Preview selected initially and a Code tab.
- Copy source and Download SVG controls.
- Direct commenting: click the preview to place serial numbered pins and open a nearby comment popover, with the input focused. Retain pins and comments, show the comment on pin hover and close the hover popup when the pointer leaves both pin and popup; allow a short delay to cross between them. Clicking a pin or focusing its input opens editing mode, which retains the existing outside-click, Close and Escape dismissal. Reopen on pin click, and persist them in widgetState scoped to the source. Keep the popup concise: numbered title, Close, input, Send comment to chat and Copy for chat. No activation button, dropdown, visible coordinates or redundant labels. Pins do not modify the exported artwork.
- Offer Send comment to chat and Copy for chat. Send uses the documented `window.openai.sendFollowUpMessage({prompt,title})` only on the user's explicit button click or Enter in the comment input; Enter confirms and sends; Shift+Enter inserts a newline. Ignore Enter during IME composition and do not send empty comments. Never send on ordinary typing, closing or copying. Copy includes the filename, pin number, coordinates, quoted label and comment for manual pasting. The user restored the Send button after trying copy-only.
- A separate, clearly labeled Download SVG Markdown link to the standalone SVG beside the viewer in the final response.

Use the latest relevant image from the current task unless the user specifies another. If no SVG or source is available, ask for it; never reuse another task's artwork or invent a sample as the requested result. Do not change geometry, layers, dimensions, artwork, typography or revision status merely to display it. This is independent of any cup artwork or packaging workflow.

Read the available `visualize` skill in full and follow its current inline-fragment delivery contract. Use a durable task-owned visualization directory from the current writable roots; do not copy an old task's absolute paths. Keep the standalone SVG in the current task's user-facing output directory. If inline visualization is unavailable, explain the limitation and provide a raster preview plus the standalone SVG download.

## Build

The reusable [viewer fragment](assets/viewer.html) and [builder](scripts/build_viewer.py) implement the controls. Run:

```sh
python3 <skill-directory>/scripts/build_viewer.py <standalone.svg> <absolute-viewer.html> --label "SVG artwork preview"
```

The builder preserves the SVG source and inserts it as escaped JSON; Preview, Code, copying and downloading all use that same source. Preview uses an image context rather than executable inline SVG. Native tabs use the visualize runtime. Copy falls back to selecting source if clipboard access is unavailable. Always keep the external Markdown download link, since sandbox download support varies.

The asset assumes white paper, as in the original approved viewer. For an SVG whose intended transparency or background differs, adapt the preview surface without changing the SVG itself. Use Google Sans Flex for viewer controls, preserving original artwork typography. Verify font loading; do not silently replace a required font.

The builder rejects fragments over 1 MB. If embedded fonts cause this, subset fonts to actual glyphs while preserving styles, weights and editable text, preferably in a separately named portable SVG. Verify the resulting file, and use that exact file for all viewer operations and the download link. Never strip a required font or quietly substitute a raster. Keep the original source.

## Verify and deliver

Check the final fragment using the visualize preview wrapper when available. Verify initial Preview, switching both tabs, rendered image, source equality, copy or its selection fallback, and download source equality. Ensure controls fit at narrow widths. Inspect the rendered artwork and font loading after any font or SVG transformation. Do not claim physical or manufacturing verification from a visual preview.

Emit the visualization reference in the final response and the standalone SVG download link. Do not link the viewer HTML unless the user asks to export the viewer itself.

## New viewer state

Every newly generated viewer starts with no comments or pins and index 1, even when displaying the same SVG. Scope saved state to a unique viewer-instance identifier as well as the source fingerprint. Restore comments only within that same viewer. Build a fresh fragment with the builder when the user requests a new viewer; do not seed it with another viewer’s widgetState or reuse an old viewer reference when a clean viewer is requested. Existing viewers retain their own comments.

## Compact comment popup

Keep all existing popup functions while using a compact layout: about 240 px maximum width, 8 px padding, 5 px internal gaps and a two-row input. Use concise Send to chat and Copy button labels. Preserve Enter/Shift+Enter, hover preview, click-to-edit, outside/Close/Escape dismissal, persistent comment numbers, clipboard fallback and explicit chat submission. Do not reduce font size or remove functions to save space.

## Photos and raster images

Use the same comment behaviors for PNG, JPEG, WebP, GIF and other browser-displayable images. Raster previews show Preview and Download image; hide SVG Code and Copy source. The builder accepts these inputs with Pillow installed. HEIC/HEIF can use macOS sips; TIFF/BMP and other Pillow-decodable still images can be converted to a separate PNG/JPEG display copy. Explain unavailable decoders rather than claiming every format is supported.

For oversized or non-browser formats, pass `--preview-output <task-output>/image-preview.jpg` (PNG when transparency is present). Preserve the original, honor orientation, and disclose reduced display resolution; inline annotations refer to display-pixel coordinates. The viewer download is the displayed copy. Link the original separately when available. Never silently flatten animation or multipage images: preserve animation when it fits or explicitly select a requested frame/page. Keep existing approved text/artwork unchanged. No image generation is required for viewing or format conversion.

For raster work replace the final Download SVG link with a clearly labeled image download. For SVG work continue linking the exact standalone SVG.

Position the comment popup to the right of the numbered badge, raised so the pin sits alongside the text-entry area: default x = point + 44 px, y = point - 54 px. Flip left near the right edge and clamp vertically within the preview. Keep a visible gap after the badge. Keep the compact number beside its dot; this spacing applies only to the popup.

## Freehand annotation

Holding the left mouse button and moving draws a freehand stroke directly over the image. On release, open the comment popup at its endpoint and associate the stroke and its bounds with the numbered comment. A simple click still places a point pin. Preserve drawings with their comments in widgetState and include stroke coordinates in the submitted context. Drawings remain review overlays and never change the original image or SVG download. Right-click must not draw. Discard unannotated draft strokes on dismissal without consuming an index.

Popup placement must avoid the full bounding area of the active freehand drawing and its pin. Try right, left, above, then below with a clear gap. If there is no clear space inside the image, show the popup below the image and reserve layout space for it rather than covering the drawing. Recalculate on resize; preserve all existing popup interactions.

## Batch comments

Right-click anywhere on the image to open a compact context menu with Send all comments to chat. Right-click itself must never send or draw. The menu action sends one message containing every nonempty comment, including previously sent ones, with stable numbers, source filename, coordinate bounds, points, selections and strokes. Disable it when empty. Preserve all pins after sending. Dismiss the menu with an outside click or Escape; report failures without marking unsent comments as sent.

## Template reuse

For every new image, run the packaged builder against the packaged viewer template. Do not reconstruct the viewer HTML or interaction code. Generate only a fresh instance populated with the selected image and no existing comments. This plugin requires the visualize skill/runtime for inline rendering and Python with Pillow for raster inputs.
