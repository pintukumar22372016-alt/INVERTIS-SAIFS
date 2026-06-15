from models.complaint_model import ComplaintModel


class ComplaintService:

    @staticmethod
    def submit_complaint(
        title,
        description
    ):

        ComplaintModel.add_complaint(
            title,
            description
        )

        return {
            "status": True,
            "message": "Complaint Submitted"
        }

    @staticmethod
    def get_all_complaints():

        return ComplaintModel.get_all_complaints()

    @staticmethod
    def resolve_complaint(
        complaint_id
    ):

        ComplaintModel.update_status(
            complaint_id,
            "Resolved"
        )

        return {
            "status": True,
            "message": "Complaint Resolved"
        }

    @staticmethod
    def reject_complaint(
        complaint_id
    ):

        ComplaintModel.update_status(
            complaint_id,
            "Rejected"
        )

        return {
            "status": True,
            "message": "Complaint Rejected"
        }