from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path


def validate(path: Path) -> dict[str, object]:
    if not zipfile.is_zipfile(path):
        raise ValueError("Not a valid ZIP/Open XML package")
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        required = {"[Content_Types].xml", "ppt/presentation.xml"}
        missing = sorted(required - names)
        if missing:
            raise ValueError(f"Missing required package parts: {missing}")
        slide_names = sorted(
            (name for name in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)),
            key=lambda name: int(re.search(r"\d+", Path(name).stem).group()),
        )
        slides = []
        for name in slide_names:
            xml = archive.read(name).decode("utf-8", errors="replace")
            text_objects = len(re.findall(r"<p:sp>", xml))
            images = len(re.findall(r"<p:pic>", xml))
            groups = len(re.findall(r"<p:graphicFrame>", xml))
            text_runs = len(re.findall(r"<a:t(?:\s[^>]*)?>", xml))
            tables = len(re.findall(r"<a:tbl>", xml))
            slides.append(
                {
                    "slide": len(slides) + 1,
                    "shapeObjects": text_objects,
                    "imageObjects": images,
                    "graphicFrames": groups,
                    "textRuns": text_runs,
                    "tables": tables,
                    "notSinglePageImage": not (images == 1 and text_objects == 0 and groups == 0),
                    "objectCountReasonable": text_runs <= 120,
                }
            )
        chart_parts = sorted(name for name in names if re.fullmatch(r"ppt/charts/chart\d+\.xml", name))
        media_parts = sorted(name for name in names if name.startswith("ppt/media/") and not name.endswith("/"))
        return {
            "file": str(path.resolve()),
            "bytes": path.stat().st_size,
            "slides": len(slides),
            "charts": len(chart_parts),
            "mediaFiles": len(media_parts),
            "allSlidesStructured": all(item["notSinglePageImage"] for item in slides),
            "objectDensityReasonable": all(item["objectCountReasonable"] for item in slides),
            "perSlide": slides,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.pptx)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    result["ok"] = True
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload)
    return 0 if result["allSlidesStructured"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

