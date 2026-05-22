from repositories.analytics_repository import (
    AnalyticsRepository
)


class StorageService:

    @staticmethod
    def save_workflow_result(
        state
    ):

        AnalyticsRepository.save_workflow_result(
            state
        )

        print(
            "\nWorkflow Result Saved"
        )