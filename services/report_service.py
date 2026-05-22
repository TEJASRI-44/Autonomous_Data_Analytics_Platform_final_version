import os
import re

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.pagesizes import (
    letter
)
from reportlab.lib.enums import (
    TA_JUSTIFY
)

from config.settings import (
    Settings
)


class ReportService:

    @staticmethod
    def save_report(
        report_content,
        filename="final_report.pdf"
    ):

        os.makedirs(
            Settings.REPORT_DIR,
            exist_ok=True
        )

        report_path = (
            Settings.REPORT_DIR
            / filename
        )


        document = SimpleDocTemplate(
            str(report_path),
            pagesize=letter,
            leftMargin=60,
            rightMargin=60,
            topMargin=60,
            bottomMargin=60
        )

        base = getSampleStyleSheet()

        heading1 = ParagraphStyle(
            "heading1",
            parent=base["Heading1"],
            fontSize=16,
            leading=22,
            spaceBefore=18,
            spaceAfter=6,
            fontName="Helvetica-Bold"
        )

        heading2 = ParagraphStyle(
            "heading2",
            parent=base["Heading2"],
            fontSize=13,
            leading=18,
            spaceBefore=14,
            spaceAfter=4,
            fontName="Helvetica-Bold"
        )

        heading3 = ParagraphStyle(
            "heading3",
            parent=base["Heading3"],
            fontSize=11,
            leading=16,
            spaceBefore=10,
            spaceAfter=3,
            fontName="Helvetica-Bold"
        )

        body = ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontSize=10,
            leading=15,
            spaceBefore=2,
            spaceAfter=4,
            fontName="Helvetica",
            alignment=TA_JUSTIFY
        )

        bullet = ParagraphStyle(
            "bullet",
            parent=base["BodyText"],
            fontSize=10,
            leading=15,
            spaceBefore=2,
            spaceAfter=3,
            fontName="Helvetica",
            leftIndent=16
        )


        elements = []

        for line in report_content.splitlines():

            stripped = line.strip()

            # blank line
            if not stripped:
                elements.append(Spacer(1, 6))
                continue

            # heading 1  (#)
            if stripped.startswith("# "):
                text = stripped[2:].strip()
                text = _inline(text)
                elements.append(Paragraph(text, heading1))
                elements.append(
                    HRFlowable(
                        width="100%",
                        thickness=0.5,
                        spaceAfter=4
                    )
                )
                continue

            # heading 2  (##)
            if stripped.startswith("## "):
                text = stripped[3:].strip()
                text = _inline(text)
                elements.append(Paragraph(text, heading2))
                continue

            # heading 3  (###)
            if stripped.startswith("### "):
                text = stripped[4:].strip()
                text = _inline(text)
                elements.append(Paragraph(text, heading3))
                continue

            # bullet  (- or *)
            if re.match(r"^[-*]\s+", stripped):
                text = re.sub(r"^[-*]\s+", "", stripped)
                text = _inline(text)
                elements.append(
                    Paragraph(f"\u2022  {text}", bullet)
                )
                continue

            # numbered list  (1. 2. ...)
            num = re.match(r"^(\d+)\.\s+(.+)$", stripped)
            if num:
                text = _inline(num.group(2))
                elements.append(
                    Paragraph(
                        f"<b>{num.group(1)}.</b>  {text}",
                        bullet
                    )
                )
                continue

            # horizontal rule  (---)
            if re.match(r"^-{3,}$", stripped):
                elements.append(
                    HRFlowable(
                        width="100%",
                        thickness=0.5,
                        spaceAfter=4
                    )
                )
                continue

            # plain body text
            text = _inline(stripped)
            if text:
                elements.append(Paragraph(text, body))

        document.build(elements)

        print(f"\nReport Saved At: {report_path}")

        return str(report_path)


def _inline(text: str) -> str:
    """Convert **bold** and *italic* markdown to ReportLab XML tags."""

    # bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

    # italic
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)

    return text