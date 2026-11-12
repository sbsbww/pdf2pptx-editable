from __future__ import annotations

from typing import Any


NAVY = "07376D"
INK = "10182B"
GRAY = "6E7789"
CYAN = "11A9C7"
CYAN_2 = "56C8D8"
LIGHT_CYAN = "DDF7FA"
WHITE = "FFFFFF"


def text(
    value: str,
    x: float,
    y: float,
    w: float,
    h: float,
    size: float,
    color: str = INK,
    bold: bool = False,
    align: str = "left",
    valign: str = "mid",
    font: str = "Microsoft YaHei",
    **extra: Any,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "type": "text",
        "text": value,
        "x": x,
        "y": y,
        "w": w,
        "h": h,
        "fontSize": size,
        "fontFace": font,
        "color": color,
        "bold": bold,
        "align": align,
        "valign": valign,
        "margin": 0,
        "breakLine": False,
    }
    item.update(extra)
    return item


def shape(
    kind: str,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str = WHITE,
    line_color: str = CYAN,
    line_width: float = 1,
    **extra: Any,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "type": "shape",
        "shape": kind,
        "x": x,
        "y": y,
        "w": w,
        "h": h,
        "fill": fill,
        "line": {"color": line_color, "width": line_width},
    }
    item.update(extra)
    return item


def line(x: float, y: float, w: float, h: float = 0, color: str = CYAN, width: float = 1.1, **extra: Any) -> dict[str, Any]:
    item = shape("line", x, y, w, h, fill="FFFFFF", line_color=color, line_width=width)
    item.update(extra)
    return item


def image(page: int, crop: tuple[int, int, int, int], x: float, y: float, w: float, h: float, **extra: Any) -> dict[str, Any]:
    cx, cy, cw, ch = crop
    item: dict[str, Any] = {
        "type": "image",
        "sourceCrop": {
            "page": page,
            "x": cx,
            "y": cy,
            "w": cw,
            "h": ch,
            "pageWidth": 852,
            "pageHeight": 1212,
        },
        "x": x,
        "y": y,
        "w": w,
        "h": h,
    }
    item.update(extra)
    return item


def header(page: int, logo_crop: tuple[int, int, int, int], company: str = "郑州莱奥特科技") -> list[dict[str, Any]]:
    return [
        image(page, logo_crop, 0.45, 0.25, 0.42, 0.42),
        text(company, 0.92, 0.25, 2.0, 0.38, 12, NAVY, True),
        text("柯幻 · 让智能体有温度", 5.35, 0.27, 1.7, 0.32, 10, NAVY, True, "right"),
        line(0.45, 0.74, 6.60, 0, CYAN_2, 1.0),
    ]


def footer(page_number: str) -> list[dict[str, Any]]:
    return [
        line(0.45, 10.01, 6.62, 0, CYAN_2, 1.0),
        text("郑州莱奥特科技", 0.45, 10.08, 2.2, 0.28, 9.5, NAVY, True),
        text(page_number, 6.82, 10.08, 0.25, 0.28, 10, NAVY, True, "right"),
    ]


def section_rule(x: float, y: float, w: float = 0.34) -> dict[str, Any]:
    return line(x, y, w, 0, CYAN, 3.0)


def build_test3_manifest() -> tuple[dict[str, Any], dict[str, Any]]:
    slides: list[dict[str, Any]] = []

    # 1. Cover: editable title copy plus separately movable artwork crops.
    slides.append(
        {
            "background": "002A64",
            "items": [
                image(1, (250, 0, 602, 1212), 2.20, 0, 5.30, 10.669),
                shape("rect", 0, 0, 4.08, 10.669, "002A64", "002A64", 0),
                image(1, (55, 75, 200, 110), 0.43, 0.53, 1.75, 0.95),
                text("柯幻熊猫 AI 智能体", 0.70, 1.93, 4.25, 0.55, 25, WHITE, False),
                text("郑州莱奥特科技", 0.70, 2.63, 3.30, 0.38, 16, "C7D8EE"),
            ],
        }
    )

    # 2. Intro page.
    items = header(2, (57, 35, 110, 65))
    items += [
        text("柯幻熊猫 AI 智能体", 0.55, 1.58, 4.70, 0.58, 26, NAVY, True),
        text("郑州莱奥特科技", 0.55, 2.18, 3.30, 0.40, 18, NAVY),
        section_rule(0.55, 2.87, 0.38),
        text("以人工智能技术为核心，构建有温度、\n可进化、可落地的智能体解决方案，\n让智能体走进更多场景，创造更美好的未来。", 0.55, 3.15, 3.75, 1.16, 15, NAVY, False, valign="top", breakLine=True, lineSpacingMultiple=1.15),
        section_rule(0.55, 4.74, 0.28),
        text("柯幻熊猫，让技术更有温度，让智能更贴近生活。", 0.55, 4.92, 4.20, 0.32, 10.5, NAVY, True),
        image(2, (650, 185, 202, 535), 5.72, 1.63, 1.78, 4.71),
        image(2, (420, 325, 432, 650), 3.70, 2.86, 3.80, 5.72),
        image(2, (245, 650, 607, 325), 2.16, 5.72, 5.34, 2.86),
    ]
    items += footer("01")
    slides.append({"background": WHITE, "items": items})

    # 3. Contents.
    items = header(3, (57, 35, 110, 65))
    items += [
        text("目录", 0.55, 1.98, 1.10, 0.50, 25, NAVY, True),
        line(1.58, 2.04, 0, 0.32, CYAN, 1.4),
        text("CONTENTS", 1.78, 2.03, 2.0, 0.36, 17, CYAN),
        section_rule(0.55, 2.73, 0.38),
    ]
    contents = [
        ("01", "关于柯幻熊猫 AI智能体", "03", 0.55, 3.35),
        ("02", "核心技术与产品体系", "07", 0.55, 4.18),
        ("03", "应用场景与行业解决方案", "11", 4.02, 3.35),
        ("04", "未来规划与社会价值", "15", 4.02, 4.18),
    ]
    for number, label, page_no, x, y in contents:
        items += [
            text(number, x, y, 0.47, 0.40, 19, CYAN, True),
            text(label, x + 0.48, y + 0.02, 2.20, 0.34, 11.5, NAVY, False),
            line(x + 2.30, y + 0.20, 0.63, 0, CYAN_2, 0.9, dash="dash"),
            text(page_no, x + 2.88, y + 0.02, 0.22, 0.34, 11.5, NAVY, False, "right"),
        ]
    items += footer("02")
    slides.append({"background": WHITE, "items": items})

    # 4. Strategy timeline.
    items = header(4, (48, 35, 50, 48))
    items += [
        text("柯幻熊猫智能体战略路线", 0.68, 1.40, 6.1, 0.62, 27, INK, True),
        text("以人为本，让 AI 智能体走进更多真实场景", 0.70, 2.02, 5.5, 0.42, 17, GRAY),
        line(0.88, 3.40, 6.00, 0, CYAN_2, 1.4, endArrow="triangle"),
    ]
    steps = [
        ("01", "技术筑基", "构建多模态能力\n打磨核心算法"),
        ("02", "场景深耕", "聚焦行业应用\n推动落地实践"),
        ("03", "生态共建", "开放平台能力\n连接更多伙伴"),
        ("04", "价值普惠", "让智能体走进生活\n创造更大社会价值"),
    ]
    for index, (num, title_value, body) in enumerate(steps):
        x = 0.82 + index * 1.70
        items += [
            shape("roundRect", x, 3.31, 0.20, 0.20, CYAN_2, CYAN_2, 0.5, radius=0.04),
            text(num, x, 3.66, 0.48, 0.35, 16, CYAN, True),
            text(title_value, x, 4.00, 1.28, 0.36, 14, INK, True),
            text(body, x, 4.42, 1.45, 0.72, 11.3, GRAY, valign="top", breakLine=True),
        ]
    items += [image(4, (0, 610, 852, 440), 0, 5.55, 7.50, 3.88)]
    items += footer("01")
    slides.append({"background": WHITE, "items": items})

    # 5. Core capabilities.
    items = header(5, (48, 35, 50, 48))
    items += [
        text("核心能力", 0.68, 1.40, 3.5, 0.62, 27, INK, True),
        text("以技术与场景双轮驱动，打造更有温度的 AI 智能体", 0.70, 2.02, 6.1, 0.42, 17, GRAY),
        image(5, (0, 850, 420, 245), 0, 7.48, 3.70, 2.16),
    ]
    capability_rows = [
        ("多模态理解与生成", "支持文本、图像、语音等多模态融合，\n实现更自然的交互体验。"),
        ("行业场景适配", "面向多行业深度优化，快速适配真实业务\n场景，提升应用价值。"),
        ("智能决策与执行", "具备自主规划与任务执行能力，\n持续学习迭代，提供高效可靠的服务。"),
        ("开放生态能力", "提供灵活接口与平台能力，\n携手伙伴共建智能体生态。"),
    ]
    for index, (title_value, body) in enumerate(capability_rows):
        y = 3.00 + index * 1.14
        items += [
            section_rule(3.25, y + 0.15, 0.34),
            text(title_value, 3.78, y, 2.8, 0.37, 15, INK, True),
            text(body, 3.78, y + 0.40, 2.95, 0.80, 10.3, GRAY, valign="top", breakLine=True),
        ]
    items += [text("让智能体更懂行业、更懂人，\n用 AI 创造更美好的未来。", 5.35, 8.70, 1.65, 0.72, 10, GRAY, True, valign="top", breakLine=True)]
    items += footer("02")
    slides.append({"background": WHITE, "items": items})

    # 6. Security and compliance cards.
    items = header(6, (48, 35, 62, 48))
    items += [
        text("安全与合规", 0.48, 1.30, 4.2, 0.62, 29, NAVY, True),
        text("构建可信赖的智能体服务体系", 0.50, 1.95, 5.4, 0.42, 18, GRAY),
    ]
    cards = [
        ("数据安全保护", "全链路数据加密，完善的权限管控\n机制，保障数据安全与隐私。", (90, 365, 140, 145)),
        ("合规规范管理", "遵循国家法律法规与行业标准，\n建立健全的合规管理体系。", (430, 365, 140, 145)),
        ("内容安全审核", "多维度内容识别与风险过滤，\n杜绝有害信息，守护健康生态。", (90, 730, 140, 145)),
        ("责任可追溯", "完整的日志审计与追溯机制，\n确保使用过程可监管、可追溯。", (430, 730, 140, 145)),
    ]
    positions = [(0.47, 2.92), (3.86, 2.92), (0.47, 6.16), (3.86, 6.16)]
    for (title_value, body, crop), (x, y) in zip(cards, positions):
        items += [
            shape("rect", x, y, 3.18, 2.92, WHITE, CYAN_2, 1.0),
            image(6, crop, x + 0.33, y + 0.34, 0.80, 0.80),
            section_rule(x + 0.35, y + 1.32, 0.32),
            text(title_value, x + 0.35, y + 1.53, 2.4, 0.38, 16, NAVY, True),
            text(body, x + 0.35, y + 2.02, 2.42, 0.66, 11, GRAY, valign="top", breakLine=True),
        ]
    items += footer("3")
    slides.append({"background": WHITE, "items": items})

    # 7. Application scenarios.
    items = header(7, (48, 35, 62, 48))
    items += [
        text("应用场景", 0.48, 1.30, 4.2, 0.62, 29, NAVY, True),
        text("三大场景落地，赋能千行百业", 0.50, 1.95, 5.4, 0.42, 18, GRAY),
        image(7, (25, 325, 420, 760), 0.35, 2.88, 3.70, 6.70),
        line(3.80, 2.90, 0, 6.40, CYAN_2, 1.0),
    ]
    scenarios = [
        ("企业办公", "智能助理、知识管理、流程协同，\n提升组织效率，助力企业数字化转型。", (480, 330, 125, 125)),
        ("政务服务", "智能问答、事项办理、信息整合，\n提升政务服务效能与公众体验。", (480, 590, 125, 125)),
        ("教育科研", "智能教学、个性化学习、科研辅助，\n促进教育公平与创新发展。", (480, 845, 125, 125)),
    ]
    for index, (title_value, body, crop) in enumerate(scenarios):
        y = 2.98 + index * 2.22
        items += [
            image(7, crop, 4.30, y, 0.78, 0.78),
            section_rule(4.32, y + 0.92, 0.28),
            text(title_value, 4.32, y + 1.12, 2.3, 0.42, 16, NAVY, True),
            text(body, 4.32, y + 1.56, 2.55, 0.66, 10.6, GRAY, valign="top", breakLine=True),
        ]
    items += [text("注：以上为典型应用场景示例，具体落地方案可根据实际需求定制。", 0.46, 9.63, 6.3, 0.30, 8.5, GRAY)]
    items += footer("4")
    slides.append({"background": WHITE, "items": items})

    # 8. Market trends with native editable charts.
    items = header(8, (48, 35, 62, 48))
    items += [
        shape("rect", 0.43, 1.54, 0.11, 0.42, CYAN, CYAN, 0),
        text("市场趋势", 0.70, 1.45, 4.4, 0.62, 28, NAVY, True),
        text("AI 智能体加速渗透，行业应用进入规模化落地阶段", 0.72, 2.08, 6.1, 0.42, 17, NAVY),
        shape("rect", 0.43, 3.08, 3.18, 4.15, WHITE, CYAN_2, 0.9),
        shape("rect", 3.78, 3.08, 3.30, 4.15, WHITE, CYAN_2, 0.9),
        text("中国 AI 智能体市场规模（亿元）", 0.58, 3.38, 2.8, 0.34, 13, NAVY, True),
        text("企业引入 AI 智能体的核心动因", 3.95, 3.38, 2.8, 0.34, 13, NAVY, True),
        {
            "type": "chart",
            "chartType": "line",
            "x": 0.62,
            "y": 3.95,
            "w": 2.75,
            "h": 2.72,
            "categories": ["2023", "2024", "2025", "2026", "2027"],
            "series": [{"name": "市场规模", "values": [320, 680, 1120, 1680, 2360], "color": CYAN}],
            "showValue": True,
            "showLegend": False,
            "minVal": 0,
            "maxVal": 2500,
            "majorUnit": 500,
        },
        {
            "type": "chart",
            "chartType": "bar",
            "x": 3.92,
            "y": 3.95,
            "w": 2.88,
            "h": 2.72,
            "categories": ["提升运营效率", "优化客户体验", "降低人力成本"],
            "series": [{"name": "占比", "values": [62, 48, 36], "color": CYAN}],
            "showValue": True,
            "showLegend": False,
            "minVal": 0,
            "maxVal": 70,
            "majorUnit": 10,
        },
        text("图1  中国 AI 智能体市场规模及预测\n数据来源：行业公开资料整理", 0.58, 7.45, 3.00, 0.62, 9.4, NAVY, valign="top", breakLine=True),
        text("图2  企业引入 AI 智能体的核心动因占比\n数据来源：行业调研统计", 3.95, 7.45, 3.00, 0.62, 9.4, NAVY, valign="top", breakLine=True),
        section_rule(0.43, 8.54, 0.73),
        text("结论：", 0.43, 8.77, 0.70, 0.42, 15, NAVY, True),
        text("AI 智能体市场保持高速增长，企业应用意愿持续提升，\n未来将在更多行业实现规模化落地，释放更大价值。", 1.10, 8.77, 5.72, 0.85, 14, NAVY, valign="top", breakLine=True),
    ]
    items += footer("5")
    slides.append({"background": WHITE, "items": items})

    # 9. Collaboration scope.
    items = header(9, (48, 35, 62, 48))
    items += [
        shape("rect", 0.43, 1.54, 0.11, 0.42, CYAN, CYAN, 0),
        text("合作范围", 0.70, 1.45, 4.4, 0.62, 28, NAVY, True),
        text("开放多元合作，共建智能化未来", 0.72, 2.08, 6.1, 0.42, 17, NAVY),
        image(9, (0, 315, 470, 770), 0, 2.78, 4.14, 6.79),
    ]
    collaborations = [
        ("行业解决方案合作", "面向政务、教育、医疗、金融、制造、\n文旅等行业，提供定制化 AI 智能体\n解决方案。"),
        ("技术与平台合作", "开放能力接口，开展技术共建、平台\n对接与模型应用合作。"),
        ("场景落地合作", "联合探索典型业务场景，推动 AI 智能体\n在实际业务中的规模化应用。"),
        ("生态共建合作", "与合作伙伴共同打造产业生态，分享\n资源、联合创新，实现长期共赢。"),
    ]
    for index, (title_value, body) in enumerate(collaborations):
        y = 3.16 + index * 1.58
        items += [
            section_rule(4.24, y + 0.12, 0.34),
            text(title_value, 4.68, y, 2.30, 0.40, 15, NAVY, True),
            text(body, 4.68, y + 0.48, 2.28, 0.86, 10.4, GRAY, valign="top", breakLine=True),
        ]
    items += [text("注：以上合作范围可根据具体需求进一步沟通。", 4.68, 9.42, 2.22, 0.32, 8.4, GRAY)]
    items += footer("6")
    slides.append({"background": WHITE, "items": items})

    # 10. Closing page.
    slides.append(
        {
            "background": "062A5B",
            "items": [
                text("郑州莱奥特科技", 0.82, 5.00, 3.8, 0.38, 16, "DCE7F3"),
                text("柯幻熊猫 AI 智能体", 0.82, 5.52, 4.5, 0.42, 17, "DCE7F3"),
                text("智启未来  融合创新", 0.82, 6.05, 3.8, 0.38, 15, "DCE7F3"),
                text("让 AI 更懂世界  更懂人", 0.82, 6.58, 4.2, 0.38, 15, "DCE7F3"),
                text("郑州莱奥特科技", 0.82, 9.48, 2.8, 0.30, 11, "DCE7F3"),
                text("柯幻熊猫 AI 智能体", 0.82, 9.88, 3.2, 0.30, 11, "DCE7F3"),
            ],
        }
    )

    report = {
        "slides": 10,
        "editableTextObjects": sum(1 for slide in slides for item in slide["items"] if item["type"] == "text"),
        "nativeShapeObjects": sum(1 for slide in slides for item in slide["items"] if item["type"] == "shape"),
        "nativeChartObjects": sum(1 for slide in slides for item in slide["items"] if item["type"] == "chart"),
        "independentImageObjects": sum(1 for slide in slides for item in slide["items"] if item["type"] == "image"),
        "reconstruction": {
            "text": "Recreated as editable PowerPoint text boxes.",
            "charts": "Slide 8 charts are native editable PowerPoint charts.",
            "linesAndCards": "Recreated as native PowerPoint shapes.",
            "illustrations": "Complex panda/city/icon artwork is preserved as independently movable cropped image objects.",
        },
        "limitations": [
            "The source PDF contains one raster image per page and no text/vector layer.",
            "Complex line-art illustrations cannot be losslessly vectorized and remain image objects.",
            "Font metrics may vary if Microsoft YaHei is unavailable on the viewing system.",
        ],
    }
    return {"layout": {"width": 7.5, "height": 10.669}, "slides": slides}, report

