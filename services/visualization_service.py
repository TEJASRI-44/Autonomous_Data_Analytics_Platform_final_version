from config.settings import (
    Settings
)


class VisualizationService:

    @staticmethod
    def get_visualization_path(
        filename
    ):

        return str(

            Settings.VISUALIZATION_DIR

            / filename
        )