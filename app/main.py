from __future__ import annotations

import shutil
import tempfile
import uuid
from pathlib import Path
import json

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .converter import ConversionError, convert_pdf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = PROJECT_ROOT / "app" / "static"
JOB_ROOT = Path(tempfile.gettempdir()) / "pdf2pptx-editable-jobs"
JOB_ROOT.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="PDF2PPTX Editable", version="1.0.0")


def _cleanup(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/convert")
async def convert(background_tasks: BackgroundTasks, file: UploadFile = File(...)) -> FileResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="请上传 PDF 文件")
    job_dir = JOB_ROOT / uuid.uuid4().hex
    job_dir.mkdir(parents=True)
    input_path = job_dir / "input.pdf"
    output_name = f"{Path(file.filename).stem}-editable.pptx"
    output_path = job_dir / output_name
    with input_path.open("wb") as handle:
        while chunk := await file.read(1024 * 1024):
            handle.write(chunk)
    try:
        result = convert_pdf(input_path, output_path, job_dir / "work")
    except ConversionError as exc:
        _cleanup(job_dir)
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    background_tasks.add_task(_cleanup, job_dir)
    report = json.loads(result.report_path.read_text(encoding="utf-8"))
    headers = {
        "X-Conversion-Mode": result.mode,
        "X-Editable-Text-Objects": str(report.get("editableTextObjects", 0)),
        "X-Native-Shape-Objects": str(report.get("nativeShapeObjects", 0)),
        "X-Native-Table-Objects": str(report.get("nativeTableObjects", 0)),
        "X-Fallback-Image-Objects": str(report.get("independentImageObjects", report.get("imageObjects", 0))),
    }
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=output_name,
        headers=headers,
        background=background_tasks,
    )


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

