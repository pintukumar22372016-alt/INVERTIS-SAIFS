"""
SAIFS - Chatbot Routes
Floating chatbot widget and API endpoint.
"""
from flask import Blueprint, render_template, request, jsonify
from services.chatbot_service import ChatbotService

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")


@chatbot_bp.route("/")
def chatbot_home():
    return render_template("features/chatbot.html")


@chatbot_bp.route("/message", methods=["POST"])
def chatbot_message():
    data = request.get_json()
    if not data:
        return jsonify({"response": "Please send a valid message."})

    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "I didn't catch that. Please type a message."})

    bot_response = ChatbotService.get_response(user_message)
    return jsonify({"response": bot_response})


@chatbot_bp.route("/health")
def health():
    return jsonify({"status": "success", "message": "SAIFS Chatbot Running ✅"})