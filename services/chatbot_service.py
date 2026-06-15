"""
SAIFS - Chatbot Service
Expanded FAQ-style response system for Invertis SAIFS assistant.
"""


class ChatbotService:

    RESPONSES = {
        # Greetings
        "hello":      "👋 Hello! Welcome to Invertis SAIFS — Smart Academic Interaction & Feedback System. How can I help you today?",
        "hi":         "👋 Hi there! I'm your Invertis SAIFS assistant. Ask me anything about the portal!",
        "hey":        "👋 Hey! Welcome to Invertis SAIFS. What would you like to know?",
        "good morning": "🌅 Good morning! Hope you have a productive day. How can I assist you?",
        "good evening": "🌙 Good evening! How can I help you today?",

        # Features
        "feedback":    "⭐ You can submit teacher feedback from the Feedback Portal. Rate your teacher (1–5 stars) and leave comments. Your feedback can be anonymous!",
        "complaint":   "📋 Submit complaints via the Complaint Portal. Set priority (Low/Medium/High/Critical) and category. Track your complaint status in real-time.",
        "notes":       "📚 Access and download study notes in the Notes Section. Teachers upload notes subject-wise. You can search by subject!",
        "download":    "⬇️ To download notes, go to the Notes section and click the Download button next to any file.",
        "upload":      "⬆️ Teachers can upload notes from the Teacher Dashboard → Notes section. Supported formats: PDF, DOC, DOCX, PPT, PPTX.",
        "doubt":       "❓ Submit your doubts in the Doubt Portal. Teachers will respond with answers. Filter doubts by subject or status.",
        "attendance":  "📅 Attendance records are available in the Attendance section. Track Present, Absent, and Late statuses by subject and date.",
        "analytics":   "📊 Visit the Analytics Dashboard to see feedback trends, complaint categories, teacher performance charts, and monthly statistics.",
        "chatbot":     "🤖 I'm your SAIFS AI assistant! Ask me about any feature of the portal and I'll guide you.",
        "notification": "🔔 Check your Notification Center (bell icon in navbar) for system alerts, notes updates, and important announcements.",
        "dashboard":   "🏠 Your dashboard shows a summary of all your activity — feedback, complaints, attendance, notes, and notifications at a glance.",

        # Auth
        "login":       "🔐 To log in, go to the Login page and enter your registered email and password.",
        "signup":      "✍️ Register by clicking 'Sign Up' and filling in your name, email, password, role (student/teacher/parent), and department.",
        "password":    "🔑 If you've forgotten your password, please contact your institution's admin for a password reset.",
        "logout":      "👋 To log out, click your name in the top navbar and select 'Logout'.",

        # Roles
        "student":     "🎓 As a student you can: submit feedback, raise complaints, download notes, ask doubts, and view your attendance.",
        "teacher":     "👨‍🏫 As a teacher you can: upload notes, answer student doubts, view feedback ratings, and manage attendance.",
        "admin":       "🛡️ As an admin you can: manage all users, resolve complaints, view full analytics, and oversee the entire system.",
        "parent":      "👨‍👩‍👧 As a parent you can: view your child's attendance, feedback reports, complaints, and upcoming events.",

        # Help
        "help":        "🆘 I can help you with: Feedback, Complaints, Notes, Doubts, Attendance, Analytics, Notifications, Login/Signup, and more. Just ask!",
        "feature":     "✨ SAIFS Features: Feedback System, Complaint Management, Notes Portal, Doubt Forum, Attendance Tracker, Analytics Dashboard, Chatbot, and Notifications.",

        # Events
        "event":       "📅 Check the Events section in your dashboard for upcoming college events, PTMs, fests, and important dates.",

        # Contact
        "contact":     "📞 For technical support, contact your college admin or email support@saifs.edu",
    }

    @staticmethod
    def get_response(message: str) -> str:
        msg = message.lower().strip()

        for keyword, response in ChatbotService.RESPONSES.items():
            if keyword in msg:
                return response

        # Default
        return (
            "🤔 I'm not sure about that. You can ask me about: "
            "feedback, complaints, notes, doubts, attendance, analytics, "
            "login, signup, dashboard, notifications, or events. "
            "Type 'help' for a full list! 😊"
        )