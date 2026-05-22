import os

from reportlab.platypus import (
    SimpleDocTemplate
)

from reportlab.lib.pagesizes import (
    letter
)

from config.settings import (
    Settings
)


class ReportRepository:

    @staticmethod
    def create_document(
        filename
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

        return document, report_path