from __future__ import annotations

from typing import Any

from .test3_manifest import line, shape, text


BLUE = "0874CB"
DEEP_BLUE = "073A75"
INK = "10182B"
GRAY = "667085"
LIGHT_BLUE = "EAF4FC"
WHITE = "FFFFFF"


def t(value: str, x: float, y: float, w: float, h: float, size: float, color: str = INK, bold: bool = False, **extra: Any) -> dict[str, Any]:
    return text(value, x, y, w, h, size, color, bold, **extra)


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


def header(page: int, logo_crop: tuple[int, int, int, int] = (45, 25, 62, 52)) -> list[dict[str, Any]]:
    return [
        image(page, logo_crop, 0.38, 0.20, 0.45, 0.42),
        t("郑州莱奥特科技", 0.90, 0.22, 2.15, 0.36, 12.5, DEEP_BLUE, True),
        line(2.32, 0.50, 3.55, 0, "8CB8DF", 0.8),
        t("柯幻熊猫 · AI 智能体", 5.60, 0.22, 1.42, 0.32, 9.3, DEEP_BLUE, True, align="right"),
    ]


def footer(page_number: str) -> list[dict[str, Any]]:
    return [
        line(0.40, 10.03, 6.62, 0, "76B7E5", 0.9),
        t("Zhengzhou Lai'aote Technology Co., Ltd.   |   柯幻熊猫 · AI 智能体", 0.40, 10.10, 5.70, 0.25, 8.2, GRAY),
        t(page_number, 6.82, 10.08, 0.22, 0.26, 9.2, GRAY, False, align="right"),
    ]


def section_title(prefix: str, suffix: str, y: float = 1.32) -> list[dict[str, Any]]:
    prefix_w = max(1.15, len(prefix) * 0.42)
    return [
        t(prefix, 0.42, y, prefix_w, 0.58, 27, BLUE, True),
        t(f"· {suffix}", 0.42 + prefix_w, y, 6.20 - prefix_w, 0.58, 27, INK, True),
    ]


def build_test1_manifest() -> tuple[dict[str, Any], dict[str, Any]]:
    slides: list[dict[str, Any]] = []

    # 1. Architectural cover. The photo and logo remain independent image objects.
    slides.append(
        {
            "background": WHITE,
            "items": [
                image(1, (640, 15, 185, 70), 5.62, 0.13, 1.63, 0.62),
                t("BUILD A BETTER TOMORROW", 0.42, 0.82, 2.85, 0.25, 7.8, "6F7882"),
                line(2.52, 0.95, 1.15, 0, "A5AEB7", 0.7),
                t("匠心筑造  美好未来", 0.42, 1.13, 4.85, 0.55, 25, "142B45", True),
                t("建筑城市价值  创享品质生活", 0.42, 1.73, 4.55, 0.30, 10.8, "546272"),
                t("CONSTRUCTION CREATES URBAN VALUE\nAND SHARES A BETTER LIFE", 0.42, 2.08, 3.6, 0.46, 7.5, "87919B", breakLine=True, valign="top"),
                image(1, (0, 250, 852, 720), 0, 2.20, 7.50, 6.34),
                t("专业  |  责任  |  创新  |  共赢", 5.15, 9.35, 1.80, 0.28, 8.4, GRAY, False, align="center"),
                t("PROFESSIONAL  RESPONSIBLE  INNOVATIVE  WIN-WIN", 5.15, 9.62, 1.80, 0.22, 5.1, "9AA3AD", False, align="center"),
            ],
        }
    )

    # 2. Product opening page.
    items = header(2, (48, 30, 65, 48))
    items += [
        t("柯幻熊猫", 0.45, 1.48, 4.5, 0.66, 31, INK, True),
        line(0.48, 2.28, 0.48, 0, BLUE, 2.4),
        t("让 AI 更懂行业  让智能更近人心", 0.48, 2.48, 5.55, 0.42, 18, INK),
        t("以人工智能为引擎，连接场景与价值，\n为行业数字化转型提供更可靠的智能伙伴。", 0.48, 3.03, 4.75, 0.76, 13.5, GRAY, breakLine=True, valign="top"),
        image(2, (0, 350, 852, 690), 0, 3.08, 7.50, 6.08),
        t("AI\nCREATES\nA BETTER\nTOMORROW", 6.18, 2.55, 0.82, 1.20, 10.5, "6F86A0", breakLine=True, valign="top"),
        line(6.20, 3.82, 0.34, 0, BLUE, 2),
    ]
    items += footer("01")
    slides.append({"background": "F5FAFF", "items": items})

    # 3. Fully editable contents page.
    items = header(3, (48, 30, 65, 48))
    items += [
        t("目录", 0.48, 1.30, 2.05, 0.72, 31, INK, True),
        t("C O N T E N T S", 0.50, 2.06, 2.55, 0.34, 15, "56718E"),
        line(0.50, 2.55, 0.62, 0, BLUE, 2.4),
        line(3.55, 1.80, 0, 7.68, "C6D8E8", 0.8),
        shape("ellipse", 3.51, 4.02, 0.08, 0.08, BLUE, BLUE, 0),
        shape("ellipse", 3.51, 6.45, 0.08, 0.08, BLUE, BLUE, 0),
    ]
    sections = [
        ("01", "关于我们", "01", ["公司简介", "发展历程", "核心优势", "企业文化"], 0.48, 3.42),
        ("02", "产品与解决方案", "07", ["产品体系", "核心功能", "行业解决方案", "应用场景"], 0.48, 6.38),
        ("03", "技术实力", "15", ["技术架构", "核心算法", "数据安全", "研发创新"], 4.08, 1.93),
        ("04", "行业应用", "21", ["智慧政务", "智慧教育", "智慧医疗", "企业服务", "更多行业场景"], 4.08, 4.55),
        ("05", "客户案例", "27", ["典型案例", "客户价值", "合作伙伴"], 4.08, 7.05),
        ("06", "未来展望", "33", ["发展战略", "生态布局", "与您共建智能未来"], 4.08, 8.82),
    ]
    for number, title_value, page_no, bullets, x, y in sections:
        items += [
            t(number, x, y, 0.60, 0.44, 21, "0067D9", True),
            shape("ellipse", x + 0.50, y - 0.11, 0.28, 0.28, "DCEFFF", "DCEFFF", 0),
            t(title_value, x + 0.18, y + 0.55, 2.20, 0.35, 15, INK, True),
            t(page_no, x + 2.24, y + 0.55, 0.28, 0.32, 9.5, INK, False, align="right"),
            line(x + 0.18, y + 0.94, 2.34, 0, "BAC6D2", 0.7),
        ]
        for bullet_index, bullet in enumerate(bullets):
            by = y + 1.14 + bullet_index * 0.31
            items += [shape("ellipse", x + 0.19, by + 0.10, 0.07, 0.07, "6CA9EA", "6CA9EA", 0), t(bullet, x + 0.38, by, 2.1, 0.25, 10.6, GRAY)]
    items += footer("02")
    slides.append({"background": WHITE, "items": items})

    # 4. Manufacturing process: editable headings, independent process regions.
    items = header(4)
    items += [
        t("P20  |  制造工艺 · 生产流程", 0.43, 0.92, 3.45, 0.34, 13.5, GRAY),
        line(0.44, 1.31, 2.35, 0, "A8C6DF", 0.7),
    ]
    items += section_title("制造工艺", "生产流程", 1.43)
    items += [
        t("从原材料到成品的全流程品控体系，确保每一件产品的稳定与可靠。", 0.44, 2.10, 6.40, 0.36, 14, GRAY),
        image(4, (45, 330, 420, 665), 0.40, 2.90, 3.70, 5.86),
        image(4, (505, 270, 305, 755), 4.45, 2.38, 2.68, 6.65),
    ]
    items += footer("20")
    slides.append({"background": WHITE, "items": items})

    # 5. Case studies: two separately movable image grids with editable descriptions.
    items = header(5)
    items += [t("P10  |  案例合集 · 多图网格", 0.43, 0.92, 3.45, 0.34, 13.5, GRAY), line(0.44, 1.31, 2.40, 0, "A8C6DF", 0.7)]
    items += section_title("案例合集", "多图网格", 1.43)
    items += [
        t("覆盖多行业应用场景，以可靠品质和定制化方案，助力客户实现更大价值。", 0.44, 2.10, 6.45, 0.36, 13.5, GRAY),
        shape("ellipse", 0.42, 2.66, 0.48, 0.48, BLUE, BLUE, 0),
        t("01", 0.42, 2.70, 0.48, 0.30, 15, WHITE, True, align="center"),
        t("工业自动化生产线", 1.12, 2.72, 2.75, 0.32, 14.5, DEEP_BLUE, True),
        image(5, (90, 350, 720, 275), 0.80, 3.08, 6.34, 2.42),
        t("为某知名制造企业提供定制化自动化生产线解决方案，实现生产效率提升 40%，\n产品不良率降低 60%，得到客户高度认可。", 0.82, 5.58, 6.25, 0.64, 11.3, GRAY, breakLine=True, valign="top"),
        shape("ellipse", 0.42, 6.32, 0.48, 0.48, BLUE, BLUE, 0),
        t("02", 0.42, 6.36, 0.48, 0.30, 15, WHITE, True, align="center"),
        t("新能源行业应用", 1.12, 6.38, 2.75, 0.32, 14.5, DEEP_BLUE, True),
        image(5, (90, 760, 720, 270), 0.80, 6.70, 6.34, 2.38),
        t("为新能源领域客户提供核心部件及系统集成方案，产品广泛应用于储能、光伏等领域，\n助力客户实现绿色低碳发展。", 0.82, 9.18, 6.25, 0.62, 11.2, GRAY, breakLine=True, valign="top"),
    ]
    items += footer("10")
    slides.append({"background": WHITE, "items": items})

    # 6. Quality management: complex diagram preserved as two independent regions.
    items = header(6)
    items += [t("P21  |  质量管理 · 闭环图", 0.43, 0.92, 3.30, 0.34, 13.5, DEEP_BLUE), line(2.36, 1.13, 3.08, 0, "A8C6DF", 0.7)]
    items += section_title("质量管理", "全流程闭环", 1.42)
    items += [
        t("以标准化体系保障产品与服务质量，持续改进，形成可追溯的闭环管理。", 0.55, 2.08, 6.25, 0.36, 13.5, GRAY),
        image(6, (35, 280, 780, 440), 0.30, 2.47, 6.87, 3.88),
        image(6, (35, 730, 780, 340), 0.30, 6.42, 6.87, 3.00),
    ]
    items += footer("3")
    slides.append({"background": WHITE, "items": items})

    # 7. Team page: portraits and advantages remain separately movable blocks.
    items = header(7)
    items += [t("P14  |  团队介绍 · 人物卡", 0.43, 0.92, 3.20, 0.34, 13.5, DEEP_BLUE), line(2.28, 1.13, 3.18, 0, "A8C6DF", 0.7)]
    items += section_title("核心团队", "专业创新", 1.42)
    items += [
        t("多元化的专业团队，深耕 AI 技术与行业应用，持续创造客户价值。", 0.55, 2.08, 6.2, 0.36, 13.5, GRAY),
        image(7, (35, 300, 780, 425), 0.30, 2.64, 6.87, 3.74),
        image(7, (35, 735, 780, 345), 0.30, 6.47, 6.87, 3.04),
    ]
    items += footer("4")
    slides.append({"background": WHITE, "items": items})

    # 8. Product matrix with a native editable table.
    items = header(8)
    items += [
        t("P25  |  产品参数 · 规格表", 0.45, 0.92, 3.35, 0.34, 13.5, GRAY),
        line(0.47, 1.31, 0.30, 0, BLUE, 2),
        t("产品参数 · 规格表", 0.45, 1.43, 5.35, 0.62, 29, DEEP_BLUE, True),
        t("多形态可选，满足不同场景需求", 0.47, 2.10, 4.8, 0.36, 15, GRAY),
        image(8, (80, 280, 700, 330), 0.70, 2.46, 6.16, 2.91),
        {
            "type": "table",
            "x": 0.35,
            "y": 5.55,
            "w": 6.80,
            "h": 4.10,
            "fontSize": 8.2,
            "colW": [1.18, 1.40, 1.40, 1.40, 1.42],
            "headerFill": "0874CB",
            "headerColor": WHITE,
            "firstColFill": "EAF3FB",
            "bodyFill": "F8FBFE",
            "borderColor": "CAD7E3",
            "rows": [
                ["项目", "Mini Panda", "Standard", "Pro", "Custom"],
                ["产品定位", "桌面陪伴", "通用服务", "行业应用", "定制开发"],
                ["整机尺寸", "280×220×220 mm", "900×420×380 mm", "1320×520×480 mm", "按需定制"],
                ["整机重量", "3.5 kg", "18 kg", "32 kg", "按需定制"],
                ["屏幕尺寸", "7 英寸", "10.1 英寸", "21.5 英寸", "按需定制"],
                ["分辨率", "1024×600", "1280×800", "1920×1080", "按需定制"],
                ["AI 交互", "语音/视觉/触控", "语音/视觉/触控", "语音/视觉/触控", "按需定制"],
                ["移动方式", "固定桌面", "轮式移动", "轮式移动/电梯", "按需定制"],
                ["续航时间", "6 小时", "8-10 小时", "8-12 小时", "按需定制"],
                ["网络连接", "Wi-Fi/蓝牙", "Wi-Fi/蓝牙", "Wi-Fi/蓝牙", "按需定制"],
                ["适用场景", "家庭/个人", "展厅/商业/教育", "政务/医疗/金融", "按需定制"],
            ],
        },
    ]
    items += footer("5")
    slides.append({"background": WHITE, "items": items})

    # 9. Logo wall plus editable partnership cards.
    items = header(9)
    items += [
        t("P16  |  合作伙伴 · Logo墙", 0.45, 0.92, 3.35, 0.34, 13.5, GRAY),
        line(0.47, 1.31, 0.30, 0, BLUE, 2),
        t("合作伙伴 · Logo墙", 0.45, 1.43, 5.35, 0.62, 29, DEEP_BLUE, True),
        t("携手行业领先伙伴，共建 AI 智能新生态", 0.47, 2.10, 5.4, 0.36, 15, GRAY),
        image(9, (30, 310, 545, 730), 0.26, 2.73, 4.80, 6.43),
    ]
    partner_cards = [
        ("战略合作", "共建 AI 产业生态"),
        ("技术共创", "联合研发创新"),
        ("场景落地", "行业解决方案"),
        ("生态互联", "开放平台合作"),
        ("共赢发展", "携手创造更大价值"),
    ]
    for index, (title_value, body) in enumerate(partner_cards):
        y = 2.80 + index * 1.28
        items += [
            shape("roundRect", 5.20, y, 1.88, 1.02, LIGHT_BLUE, LIGHT_BLUE, 0, radius=0.06),
            shape("ellipse", 5.34, y + 0.29, 0.35, 0.35, WHITE, BLUE, 1.2),
            t(str(index + 1), 5.34, y + 0.32, 0.35, 0.22, 9.5, BLUE, True, align="center"),
            t(title_value, 5.83, y + 0.20, 1.05, 0.30, 13.5, DEEP_BLUE, True),
            t(body, 5.83, y + 0.55, 1.05, 0.26, 9.5, GRAY),
        ]
    items += footer("6")
    slides.append({"background": WHITE, "items": items})

    # 10. Closing page.
    slides.append(
        {
            "background": WHITE,
            "items": [
                t("建筑更美好的城市生活", 0.62, 0.93, 4.05, 0.34, 13.5, "55616C"),
                t("BUILD A BETTER\nURBAN LIFE", 0.62, 1.30, 2.20, 0.52, 10, "6F7C88", breakLine=True, valign="top"),
                line(0.62, 1.91, 0.34, 0, "7A8792", 1.2),
                image(10, (55, 260, 530, 570), 0.48, 2.28, 4.66, 5.02),
                t("城市\n建筑\n人居\n未来", 5.34, 3.35, 0.75, 1.42, 14, "48545F", breakLine=True, valign="top"),
                line(5.34, 4.88, 0.34, 0, "6A7580", 1.2),
                t("CITY\nCONSTRUCTION\nHABITAT\nFUTURE", 5.34, 5.25, 1.25, 1.10, 9.5, "7D8791", breakLine=True, valign="top"),
                line(5.34, 6.51, 0.38, 0, BLUE, 2),
                t("宏远建设有限公司", 0.62, 8.06, 3.45, 0.42, 18, "22364A", True),
                t("HONGYUAN CONSTRUCTION CO., LTD.", 0.62, 8.52, 3.65, 0.28, 9.5, "65717C"),
                line(3.45, 8.65, 2.10, 0, "9AA5AF", 0.8),
                t("◉  400-888-1234      ✉  info@hongyuan.com", 0.62, 8.98, 5.10, 0.30, 11, "53616E"),
                t("●  中国·北京市朝阳区未来科技城创新路8号", 0.62, 9.38, 5.15, 0.30, 11, "53616E"),
                t("◎  www.hongyuan.com", 0.62, 9.78, 3.10, 0.30, 11, "53616E"),
                image(10, (680, 900, 115, 145), 5.95, 7.92, 1.02, 1.28),
                t("关注我们\n了解更多", 6.08, 9.24, 0.76, 0.52, 9.5, GRAY, breakLine=True, align="center", valign="top"),
            ],
        }
    )

    report = {
        "slides": 10,
        "editableTextObjects": sum(1 for slide in slides for item in slide["items"] if item["type"] == "text"),
        "nativeShapeObjects": sum(1 for slide in slides for item in slide["items"] if item["type"] == "shape"),
        "nativeTableObjects": sum(1 for slide in slides for item in slide["items"] if item["type"] == "table"),
        "nativeChartObjects": 0,
        "independentImageObjects": sum(1 for slide in slides for item in slide["items"] if item["type"] == "image"),
        "reconstruction": {
            "text": "Titles, subtitles, contents, descriptions, partnership cards, contact information, headers and footers are editable text boxes.",
            "tables": "The product specification matrix on slide 8 is a native editable PowerPoint table.",
            "shapes": "Lines, bullets, badges and partnership cards are native PowerPoint shapes.",
            "images": "Photos, portraits, robots, diagrams and logo walls are preserved as independently movable region images.",
        },
        "limitations": [
            "The source PDF contains only one raster image per page and has no recoverable original object structure.",
            "Complex process diagrams, portraits and brand logos remain image regions to preserve visual fidelity.",
            "The source itself mixes company identities and page numbering; the reconstruction preserves the visible content.",
        ],
    }
    return {"layout": {"width": 7.5, "height": 10.669}, "slides": slides}, report

