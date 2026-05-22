class InsightReviewService:

    @staticmethod
    def approve(state):

        state[
            "insights_approved"
        ] = True

        state[
            "waiting_for_insight_review"
        ] = False

        state[
            "workflow_complete"
        ] = False

        return state

    @staticmethod
    def regenerate(

        state,

        feedback
    ):

        state[
            "insight_feedback"
        ] = feedback

        state[
            "waiting_for_insight_review"
        ] = False

        state[
            "insights"
        ] = {}

        return state