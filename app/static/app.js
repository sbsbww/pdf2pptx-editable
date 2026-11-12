const form = document.querySelector("#upload-form");
const input = document.querySelector("#pdf-file");
const label = document.querySelector("#file-label");
const button = document.querySelector("#convert-button");
const status = document.querySelector("#status");
const progress = document.querySelector("#progress");
const health = document.querySelector("#health");

fetch("/api/health")
  .then((response) => response.ok ? response.json() : Promise.reject())
  .then(() => { health.textContent = "服务可用"; health.classList.add("ok"); })
  .catch(() => { health.textContent = "服务不可用"; });

input.addEventListener("change", () => {
  label.textContent = input.files[0]?.name || "选择 PDF 文件";
  status.textContent = input.files[0] ? "已选择文件" : "等待文件";
});

for (const eventName of ["dragenter", "dragover"]) {
  form.addEventListener(eventName, (event) => { event.preventDefault(); form.classList.add("dragging"); });
}
for (const eventName of ["dragleave", "drop"]) {
  form.addEventListener(eventName, (event) => { event.preventDefault(); form.classList.remove("dragging"); });
}
form.addEventListener("drop", (event) => {
  const file = event.dataTransfer.files[0];
  if (file?.type === "application/pdf" || file?.name.toLowerCase().endsWith(".pdf")) {
    const transfer = new DataTransfer();
    transfer.items.add(file);
    input.files = transfer.files;
    input.dispatchEvent(new Event("change"));
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!input.files[0]) return;
  button.disabled = true;
  status.textContent = "正在解析并重建对象…";
  progress.classList.add("active");
  const data = new FormData();
  data.append("file", input.files[0]);
  try {
    const response = await fetch("/api/convert", { method: "POST", body: data });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(payload.detail || "转换失败");
    }
    const blob = await response.blob();
    const disposition = response.headers.get("content-disposition") || "";
    const match = disposition.match(/filename\*?=(?:UTF-8''|\")?([^\";]+)/i);
    const filename = match ? decodeURIComponent(match[1].replace(/\"$/, "")) : "editable.pptx";
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    anchor.click();
    URL.revokeObjectURL(url);
    status.textContent = "转换完成，PPTX 已下载";
  } catch (error) {
    status.textContent = error.message;
  } finally {
    button.disabled = false;
    progress.classList.remove("active");
  }
});

