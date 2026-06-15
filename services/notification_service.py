from datetime import datetime


class NotificationService:

    notifications = []

    @staticmethod
    def add_notification(message):

        NotificationService.notifications.append({

            "message": message,

            "time":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        })

    @staticmethod
    def get_notifications():

        return NotificationService.notifications

    @staticmethod
    def clear_notifications():

        NotificationService.notifications.clear()