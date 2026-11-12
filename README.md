# PDF2PPTX Editable

将 PDF 页面重建为可编辑的 PPTX。项目包含命令行工具、FastAPI 上传下载 Demo、测试3的高保真重建清单、Open XML 验证脚本和 Docker 部署配置。

本仓库不是把每页 PDF 直接作为一张背景图塞进 PPT。转换器优先生成独立文本框、原生形状和原生图表；无法可靠结构化的复杂插图才保留为可独立移动、缩放的局部图片对象。

## 已交付结果

测试素材：`examples/test3.pdf`，共 10 页，所有页面均为单张栅格图，没有 PDF 文字层或矢量对象。

输出文件：`examples/test3-editable.pptx`

| 对象类型 | 数量 | 编辑方式 |
| --- | ---: | --- |
| 文本框 | 121 | 可选中、修改文字、字体、字号和位置 |
| 原生形状 | 55 | 可调整颜色、线宽、尺寸和位置 |
| 原生图表 | 2 | 可编辑系列、类别和数值 |
| 局部图片 | 24 | 可独立移动、缩放和替换 |

转换结果已用 WPS 12.0 实际打开，并重新导出 10 页 PDF 做逐页视觉检查。验证详情见 [docs/editability-report.md](docs/editability-report.md)。

## 转换策略

转换器按以下顺序选择路径：

1. `curated`：已知测试素材使用经过人工校验的结构清单，获得确定性高保真结果。
2. `text-layer`：PDF 有文字层时，使用 PyMuPDF 提取文本、字号、颜色和坐标，并重建为文本框。
3. `ocr`：扫描件且本机安装 Tesseract 时，使用 `chi_sim+eng` 识别文字并生成文本框。
4. `segmented-image`：没有文字层且 OCR 不可用时，将页面切成多个独立图像带，保证文件可打开并避免单张整页背景，但会在报告中明确标记文字不可编辑。

复杂线稿、照片和无法可靠解析的装饰区域不会伪装成原生图形，而是按内容区域裁切为独立图片对象。测试3中的时间轴、卡片边框、分隔线和两张数据图均为 PPT 原生对象。

## 本地运行

要求：Python 3.11+、Node.js 20+。PowerPoint/WPS 仅用于人工验收，不是转换依赖。

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
npm ci --ignore-scripts --no-audit --no-fund

.\.venv\Scripts\python scripts\convert.py `
  examples\test3.pdf `
  examples\test3-editable.pptx
```

Linux/macOS：

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
npm ci --ignore-scripts --no-audit --no-fund
.venv/bin/python scripts/convert.py examples/test3.pdf examples/test3-editable.pptx
```

扫描件 OCR 为可选依赖：

```bash
pip install -r requirements-ocr.txt
# 另需安装 Tesseract 及 chi_sim 语言包
```

## 启动 Demo

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

打开 `http://localhost:8000`，上传 PDF 后服务会直接返回可下载的 PPTX。健康检查地址为 `GET /api/health`。

也可直接调用 API：

```bash
curl -F "file=@examples/test3.pdf" http://localhost:8000/api/convert -o test3-editable.pptx
```

## Docker 与在线部署

Docker 镜像包含中文 Tesseract OCR：

```bash
docker build -t pdf2pptx-editable .
docker run --rm -p 8000:8000 pdf2pptx-editable
```

仓库根目录的 `render.yaml` 可由 Render Blueprint 直接部署。部署后平台会调用 `/api/health` 做健康检查。其他支持 Docker 的平台（Railway、Fly.io、云托管容器）也可直接使用同一镜像。

服务不依赖第三方 API，不需要 API Key。上传文件与转换中间文件写入系统临时目录，响应结束后自动删除。

## 验证

```bash
python -m unittest discover -s tests -v
python scripts/validate_pptx.py examples/test3-editable.pptx
```

验证脚本会检查：

- PPTX 是否为有效 Open XML 包；
- 幻灯片、媒体与原生图表部件数量；
- 每页是否包含结构化对象；
- 是否存在仅由一张图片构成的页面。

CI 工作流位于 `.github/workflows/ci.yml`，会安装依赖、运行单元测试、重新转换测试3并验证输出结构。

## 项目结构

```text
app/
  converter.py          PDF 解析、OCR、素材裁切与任务编排
  test3_manifest.py     测试3的高保真结构重建清单
  build_pptx.mjs        PptxGenJS 原生对象生成器
  main.py               FastAPI 上传下载服务
  static/               Demo 前端
scripts/
  convert.py            CLI 入口
  validate_pptx.py      Open XML 结构验证
examples/
  test3.pdf
  test3-editable.pptx
docs/
  editability-report.md
```

## 主要依赖

- PyMuPDF：PDF 页面渲染、文字层与页面对象读取。
- Pillow：区域裁切和图像资产处理。
- PptxGenJS：生成 Office Open XML PPTX、原生文本框、形状与图表。
- FastAPI/Uvicorn：上传下载服务。
- Tesseract/pytesseract：可选的本地中文 OCR。

## 已知限制

- 栅格 PDF 已经丢失原 PPT 的语义结构，无法无损恢复原始分组、动画、母版和字体嵌入信息。
- 复杂熊猫/城市线稿无法可靠矢量化，按局部图片对象保留，仍可独立移动和缩放。
- 不同系统缺少 `Microsoft YaHei` 时，Office/WPS 会替换字体，可能造成轻微换行变化。
- 通用 OCR 的识别准确率取决于分辨率、语言包和页面噪声；生产环境应保留人工校验环节。

## 安全

项目没有硬编码密钥、令牌或密码。转换过程默认不联网，也不会把文档发送到外部服务。

