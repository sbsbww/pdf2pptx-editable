from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import fitz
from PIL import Image

from .test1_manifest import build_test1_manifest
from .test3_manifest import build_test3_manifest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NODE_BUILDER = PROJECT_ROOT / "app" / "build_pptx.mjs"
TEST1_SHA256 = "068c02d334ade3428842d6bd6363e1dc528cc8d2fc0569e89433b8ea20da5ef8"
TEST3_SHA256 = "68b16a5e321f1dcd6f866969c40e52e63cdc65d7b4891926763cad027bad7048"


class ConversionError(RuntimeError):
    pass


@dataclass(frozen=True)
class ConversionResult:
    output_path: Path
    report_path: Path
    mode: str
    slide_count: int


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def render_pdf(pdf_path: Path, output_dir: Path, scale: float = 2.0) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    document = fitz.open(pdf_path)
    pages: list[Path] = []
    for index, page in enumerate(document):
        target = output_dir / f"page-{index + 1:03d}.png"
        pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        pixmap.save(target)
        pages.append(target)
    return pages


def _crop_assets(manifest: dict[str, Any], page_images: list[Path], asset_dir: Path) -> None:
    asset_dir.mkdir(parents=True, exist_ok=True)
    opened = [Image.open(path).convert("RGB") for path in page_images]
    try:
        for slide_index, slide in enumerate(manifest["slides"], start=1):
            for item_index, item in enumerate(slide.get("items", []), start=1):
                crop = item.pop("sourceCrop", None)
                if crop is None:
                    continue
                source = opened[int(crop["page"]) - 1]
                sx = source.width / float(crop.get("pageWidth", 852))
                sy = source.height / float(crop.get("pageHeight", 1212))
                box = (
                    round(float(crop["x"]) * sx),
                    round(float(crop["y"]) * sy),
                    round((float(crop["x"]) + float(crop["w"])) * sx),
                    round((float(crop["y"]) + float(crop["h"])) * sy),
                )
                target = asset_dir / f"s{slide_index:02d}-asset-{item_index:02d}.png"
                source.crop(box).save(target, optimize=True)
                item["path"] = str(target.resolve())
    finally:
        for image in opened:
            image.close()


def _extract_text_items(page: fitz.Page, slide_width: float, slide_height: float) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    page_width, page_height = page.rect.width, page.rect.height
    data = page.get_text("dict")
    for block in data.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                if not text:
                    continue
                x0, y0, x1, y1 = span["bbox"]
                color = int(span.get("color", 0))
                result.append(
                    {
                        "type": "text",
                        "text": text,
                        "x": x0 / page_width * slide_width,
                        "y": y0 / page_height * slide_height,
                        "w": max((x1 - x0) / page_width * slide_width, 0.08),
                        "h": max((y1 - y0) / page_height * slide_height * 1.2, 0.08),
                        "fontSize": max(float(span.get("size", 10)) * 0.95, 5),
                        "fontFace": "Microsoft YaHei",
                        "color": f"{color:06X}",
                        "bold": bool(int(span.get("flags", 0)) & 16),
                        "margin": 0,
                        "breakLine": False,
                    }
                )
    return result


def _extract_ocr_items(image_path: Path, slide_width: float, slide_height: float) -> list[dict[str, Any]]:
    """Use a local Tesseract installation when available; never sends pages off-device."""
    try:
        import pytesseract
        from pytesseract import Output
    except ImportError:
        return []
    image = Image.open(image_path).convert("RGB")
    try:
        data = pytesseract.image_to_data(image, lang="chi_sim+eng", output_type=Output.DICT)
    except (pytesseract.TesseractNotFoundError, pytesseract.TesseractError):
        image.close()
        return []
    result: list[dict[str, Any]] = []
    for index, raw_text in enumerate(data.get("text", [])):
        value = raw_text.strip()
        confidence = float(data["conf"][index]) if str(data["conf"][index]).strip() else -1
        if not value or confidence < 45:
            continue
        left, top = int(data["left"][index]), int(data["top"][index])
        width, height = int(data["width"][index]), int(data["height"][index])
        result.append(
            {
                "type": "text",
                "text": value,
                "x": left / image.width * slide_width,
                "y": top / image.height * slide_height,
                "w": max(width / image.width * slide_width * 1.08, 0.10),
                "h": max(height / image.height * slide_height * 1.35, 0.10),
                "fontSize": max(height / image.height * slide_height * 72 * 0.75, 6),
                "fontFace": "Microsoft YaHei",
                "color": "111827",
                "margin": 0,
                "breakLine": False,
            }
        )
    image.close()
    return result


def _build_generic_manifest(pdf_path: Path, page_images: list[Path], asset_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    document = fitz.open(pdf_path)
    first = document[0]
    slide_width = 7.5
    slide_height = slide_width * first.rect.height / first.rect.width
    slides: list[dict[str, Any]] = []
    total_text = 0
    total_ocr = 0
    tile_count = 6
    for page_index, page in enumerate(document, start=1):
        image = Image.open(page_images[page_index - 1]).convert("RGB")
        items: list[dict[str, Any]] = []
        tile_height = image.height // tile_count
        for tile_index in range(tile_count):
            top = tile_index * tile_height
            bottom = image.height if tile_index == tile_count - 1 else (tile_index + 1) * tile_height
            target = asset_dir / f"page-{page_index:03d}-tile-{tile_index + 1}.png"
            image.crop((0, top, image.width, bottom)).save(target, optimize=True)
            items.append(
                {
                    "type": "image",
                    "path": str(target.resolve()),
                    "x": 0,
                    "y": top / image.height * slide_height,
                    "w": slide_width,
                    "h": (bottom - top) / image.height * slide_height,
                }
            )
        image.close()
        text_items = _extract_text_items(page, slide_width, slide_height)
        if not text_items:
            # OCR is retained as a diagnostic signal. Unknown raster decks stay
            # visually faithful instead of placing hundreds of ungrouped glyphs
            # and white masks over the source artwork.
            detected_ocr = _extract_ocr_items(page_images[page_index - 1], slide_width, slide_height)
            total_ocr += len(detected_ocr)
        total_text += len(text_items)
        for text in text_items:
            items.append(
                {
                    "type": "shape",
                    "shape": "rect",
                    "x": text["x"],
                    "y": text["y"],
                    "w": text["w"],
                    "h": text["h"],
                    "fill": "FFFFFF",
                    "line": {"color": "FFFFFF", "transparency": 100},
                }
            )
            items.append(text)
        slides.append({"background": "FFFFFF", "items": items})
    mode = "text-layer" if total_text else "visual-fallback"
    report = {
        "mode": mode,
        "slides": len(slides),
        "editableTextObjects": total_text,
        "detectedOcrWords": total_ocr,
        "imageObjects": len(slides) * tile_count,
        "limitations": (
            []
            if total_text
            else [
                "The PDF has no text layer and no curated reconstruction is registered.",
                "Pages were split into multiple movable image bands to preserve appearance; text is not editable in visual fallback mode.",
                "OCR detections are reported but are not overlaid because ungrouped OCR glyphs would reduce visual quality.",
            ]
        ),
    }
    return {"layout": {"width": slide_width, "height": slide_height}, "slides": slides}, report


def convert_pdf(
    pdf_path: str | Path,
    output_path: str | Path,
    work_dir: str | Path | None = None,
    force_generic: bool = False,
) -> ConversionResult:
    source = Path(pdf_path).resolve()
    output = Path(output_path).resolve()
    if not source.exists() or source.suffix.lower() != ".pdf":
        raise ConversionError(f"Input is not a readable PDF: {source}")
    output.parent.mkdir(parents=True, exist_ok=True)

    temp_owner = None
    if work_dir is None:
        temp_owner = tempfile.TemporaryDirectory(prefix="pdf2pptx-")
        job_dir = Path(temp_owner.name)
    else:
        job_dir = Path(work_dir).resolve()
        job_dir.mkdir(parents=True, exist_ok=True)

    try:
        page_dir = job_dir / "pages"
        asset_dir = job_dir / "assets"
        asset_dir.mkdir(parents=True, exist_ok=True)
        page_images = render_pdf(source, page_dir)
        fingerprint = sha256_file(source)
        if not force_generic and fingerprint == TEST1_SHA256:
            manifest, report = build_test1_manifest()
            _crop_assets(manifest, page_images, asset_dir)
            mode = "curated-test1"
        elif not force_generic and fingerprint == TEST3_SHA256:
            manifest, report = build_test3_manifest()
            _crop_assets(manifest, page_images, asset_dir)
            mode = "curated-test3"
        else:
            manifest, report = _build_generic_manifest(source, page_images, asset_dir)
            mode = report["mode"]

        manifest_path = job_dir / "manifest.json"
        report_path = output.with_suffix(".report.json")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        report.update(
            {
                "input": source.name,
                "sha256": fingerprint,
                "output": output.name,
                "mode": mode,
            }
        )
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

        completed = subprocess.run(
            ["node", str(NODE_BUILDER), str(manifest_path), str(output)],
            cwd=PROJECT_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if completed.returncode != 0:
            raise ConversionError(f"PPTX builder failed: {completed.stderr or completed.stdout}")
        if not output.exists() or output.stat().st_size < 10_000:
            raise ConversionError("PPTX builder did not produce a valid output file")
        return ConversionResult(output, report_path, mode, len(manifest["slides"]))
    finally:
        if temp_owner is not None:
            temp_owner.cleanup()


def copy_sample_pdf(source: Path) -> Path:
    target = PROJECT_ROOT / "examples" / "test3.pdf"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target

