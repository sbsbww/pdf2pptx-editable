import fs from "node:fs";
import path from "node:path";
import PptxGenJS from "pptxgenjs";

const [manifestArg, outputArg] = process.argv.slice(2);
if (!manifestArg || !outputArg) {
  throw new Error("Usage: node app/build_pptx.mjs <manifest.json> <output.pptx>");
}

const manifestPath = path.resolve(manifestArg);
const outputPath = path.resolve(outputArg);
const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
const pptx = new PptxGenJS();
pptx.defineLayout({
  name: "SOURCE_PORTRAIT",
  width: manifest.layout.width,
  height: manifest.layout.height,
});
pptx.layout = "SOURCE_PORTRAIT";
pptx.author = "pdf2pptx-editable";
pptx.company = "OpenAI Codex delivery";
pptx.subject = "Editable reconstruction from PDF page images";
pptx.title = "测试3 - 可编辑重建版";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  lang: "zh-CN",
};

const shapeMap = {
  rect: pptx.ShapeType.rect,
  roundRect: pptx.ShapeType.roundRect,
  ellipse: pptx.ShapeType.ellipse,
  line: pptx.ShapeType.line,
  chevron: pptx.ShapeType.chevron,
};

function shapeOptions(item) {
  const line = item.line || {};
  const options = {
    x: item.x,
    y: item.y,
    w: item.w,
    h: item.h,
    fill: { color: item.fill || "FFFFFF", transparency: item.fillTransparency || 0 },
    line: {
      color: line.color || "FFFFFF",
      width: line.width ?? 0,
      transparency: line.transparency ?? 0,
      dash: item.dash || line.dash,
    },
  };
  if (item.endArrow) options.line.endArrowType = item.endArrow;
  if (item.beginArrow) options.line.beginArrowType = item.beginArrow;
  return options;
}

function addText(slide, item) {
  const options = {
    x: item.x,
    y: item.y,
    w: item.w,
    h: item.h,
    fontFace: item.fontFace || "Microsoft YaHei",
    fontSize: item.fontSize || 12,
    color: item.color || "111827",
    bold: Boolean(item.bold),
    italic: Boolean(item.italic),
    align: item.align || "left",
    valign: item.valign || "mid",
    margin: item.margin ?? 0,
    breakLine: Boolean(item.breakLine),
    lineSpacingMultiple: item.lineSpacingMultiple,
    paraSpaceAfterPt: item.paraSpaceAfterPt || 0,
    isTextBox: true,
    transparency: item.transparency || 0,
  };
  if (item.fit) options.fit = item.fit;
  slide.addText(item.text, options);
}

function addChart(slide, item) {
  const type = item.chartType === "bar" ? pptx.ChartType.bar : pptx.ChartType.line;
  const data = item.series.map((series) => ({
    name: series.name,
    labels: item.categories,
    values: series.values,
    color: series.color,
  }));
  const options = {
    x: item.x,
    y: item.y,
    w: item.w,
    h: item.h,
    showLegend: Boolean(item.showLegend),
    showTitle: false,
    showValue: Boolean(item.showValue),
    showCatName: false,
    showSerName: false,
    showPercent: false,
    showMarker: item.chartType !== "bar",
    markerSize: 5,
    lineSize: 2,
    chartColors: item.series.map((series) => series.color || "11A9C7"),
    showCatName: false,
    dataLabelPosition: item.chartType === "bar" ? "outEnd" : "t",
    dataLabelColor: "07376D",
    dataLabelFormatCode: item.chartType === "bar" ? "0\"%\"" : "#,##0",
    barDir: item.chartType === "bar" ? "bar" : undefined,
    catAxisLabelFontFace: "Microsoft YaHei",
    catAxisLabelFontSize: 9,
    valAxisLabelFontFace: "Microsoft YaHei",
    valAxisLabelFontSize: 8,
    valAxisMinVal: item.minVal,
    valAxisMaxVal: item.maxVal,
    valAxisMajorUnit: item.majorUnit,
    showValAxisTitle: false,
    showCatAxisTitle: false,
    showValAxis: item.chartType !== "bar",
    showCatAxis: true,
    showValue: Boolean(item.showValue),
    showBorder: false,
    showGridLines: item.chartType !== "bar",
    showValue: true,
  };
  slide.addChart(type, data, options);
}

for (const slideSpec of manifest.slides) {
  const slide = pptx.addSlide();
  slide.background = { color: slideSpec.background || "FFFFFF" };
  for (const item of slideSpec.items || []) {
    if (item.type === "text") {
      addText(slide, item);
    } else if (item.type === "shape") {
      const shapeType = shapeMap[item.shape];
      if (!shapeType) throw new Error(`Unsupported shape: ${item.shape}`);
      slide.addShape(shapeType, shapeOptions(item));
    } else if (item.type === "image") {
      slide.addImage({
        path: path.resolve(item.path),
        x: item.x,
        y: item.y,
        w: item.w,
        h: item.h,
        transparency: item.transparency || 0,
      });
    } else if (item.type === "chart") {
      addChart(slide, item);
    } else {
      throw new Error(`Unsupported item type: ${item.type}`);
    }
  }
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
await pptx.writeFile({ fileName: outputPath, compression: true });
console.log(JSON.stringify({ output: outputPath, slides: manifest.slides.length }));

