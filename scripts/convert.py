from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.converter import ConversionError, convert_pdf  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert PDF pages to an editable PPTX deck")
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pptx", type=Path)
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--force-generic", action="store_true")
    args = parser.parse_args()
    try:
        result = convert_pdf(args.input_pdf, args.output_pptx, args.work_dir, args.force_generic)
    except ConversionError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "ok": True,
                "output": str(result.output_path),
                "report": str(result.report_path),
                "mode": result.mode,
                "slides": result.slide_count,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

