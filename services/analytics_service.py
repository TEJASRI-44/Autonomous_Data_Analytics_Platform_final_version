from graph.workflow import graph

from services.storage_service import (
    StorageService
)


class AnalyticsService:

    @staticmethod
    def stream_workflow(
        initial_state
    ):

        final_result = None

        for event in graph.stream(
            initial_state
        ):

            final_result = event

            yield event

        # ----------------------------------------
        # SAVE FINAL RESULT
        # ----------------------------------------

        if final_result:

            final_state = list(
                final_result.values()
            )[-1]

            StorageService.save_workflow_result(
                final_state
            )