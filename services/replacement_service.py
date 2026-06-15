class ReplacementService:

    common_replacements = {

        "wifi":
        "Please contact IT Department.",

        "attendance":
        "Contact your Class Coordinator.",

        "result":
        "Please visit Examination Cell.",

        "fees":
        "Please contact Accounts Department.",

        "library":
        "Visit Library Help Desk."
    }

    @staticmethod
    def get_solution(issue):

        issue = issue.lower()

        if issue in ReplacementService.common_replacements:

            return ReplacementService.common_replacements[
                issue
            ]

        return "No predefined solution available."