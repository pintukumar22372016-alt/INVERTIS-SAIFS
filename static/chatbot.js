// Chatbot Frontend

function sendMessage() {

    const input =
        document.getElementById("chatInput");

    const chatBox =
        document.getElementById("chatBox");

    const message =
        input.value.trim();

    if (message === "") {

        return;
    }

    chatBox.innerHTML += `
        <div class="user-message">
            <b>You:</b> ${message}
        </div>
    `;

    let response =
        getBotResponse(message);

    setTimeout(() => {

        chatBox.innerHTML += `
            <div class="bot-message">
                <b>Bot:</b> ${response}
            </div>
        `;

        chatBox.scrollTop =
            chatBox.scrollHeight;

    }, 500);

    input.value = "";
}

function getBotResponse(message) {

    message = message.toLowerCase();

    if (message.includes("hello")) {

        return "Hello Student!";
    }

    if (message.includes("feedback")) {

        return "Visit Feedback Section.";
    }

    if (message.includes("complaint")) {

        return "Use Complaint Portal.";
    }

    if (message.includes("notes")) {

        return "Notes are available in Notes Module.";
    }

    if (message.includes("attendance")) {

        return "Attendance can be viewed in Dashboard.";
    }

    return "Sorry, I don't understand.";
}