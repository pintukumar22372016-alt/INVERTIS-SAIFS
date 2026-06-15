from models.feedback_model import FeedbackModel


class FeedbackService:

    @staticmethod
    def submit_feedback(
        teacher_name,
        subject,
        rating,
        comments
    ):

        FeedbackModel.add_feedback(
            teacher_name,
            subject,
            rating,
            comments
        )

        return {
            "status": True,
            "message": "Feedback Submitted Successfully"
        }

    @staticmethod
    def get_feedback_list():

        return FeedbackModel.get_all_feedback()

    @staticmethod
    def delete_feedback(
        feedback_id
    ):

        FeedbackModel.delete_feedback(
            feedback_id
        )

        return {
            "status": True,
            "message": "Feedback Deleted"
        }