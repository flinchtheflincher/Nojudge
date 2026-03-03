(() => {
    const chatBox = document.getElementById("chat-box");
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message");
    const voiceButton = document.getElementById("voice-button");

    if (!chatBox || !chatForm || !messageInput || !voiceButton) {
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const keyStorageKey = "nojudge_owner_key";
    let recognition = null;
    let isListening = false;

    function getOwnerKey() {
        const existingKey = window.localStorage.getItem(keyStorageKey);
        if (existingKey) {
            return existingKey;
        }

        const enteredKey = window.prompt("Enter your Nojudge owner key");
        if (!enteredKey) {
            return "";
        }

        const trimmed = enteredKey.trim();
        if (trimmed) {
            window.localStorage.setItem(keyStorageKey, trimmed);
        }
        return trimmed;
    }

    let ownerKey = getOwnerKey();

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function addMessage(message, isUser) {
        const wrapper = document.createElement("div");
        wrapper.className = `message ${isUser ? "user-message" : "bot-message"}`;

        const content = document.createElement("div");
        content.className = "message-content";
        content.textContent = message;

        wrapper.appendChild(content);
        chatBox.appendChild(wrapper);
        scrollToBottom();
    }

    function speakText(text) {
        if (!("speechSynthesis" in window) || !text) {
            return;
        }
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1;
        utterance.pitch = 1;
        window.speechSynthesis.speak(utterance);
    }

    async function sendMessage(rawMessage) {
        const message = rawMessage.trim();
        if (!message) {
            return;
        }

        if (!ownerKey) {
            ownerKey = getOwnerKey();
        }

        if (!ownerKey) {
            addMessage("Owner key missing. Refresh and enter your key.", false);
            return;
        }

        addMessage(message, true);
        messageInput.value = "";

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Nojudge-Key": ownerKey,
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                if (response.status === 401) {
                    window.localStorage.removeItem(keyStorageKey);
                    ownerKey = "";
                    addMessage("Invalid owner key. Refresh and enter the correct key.", false);
                    return;
                }
                const errorData = await response.json().catch(() => ({}));
                const detail = errorData.detail || "Request failed.";
                addMessage(detail, false);
                return;
            }

            const data = await response.json();
            const aiReply = data.response || "Could not generate a response.";
            addMessage(aiReply, false);
            speakText(aiReply);
        } catch (_err) {
            addMessage("Network error. Please try again.", false);
        }
    }

    function updateVoiceButtonState() {
        if (isListening) {
            voiceButton.classList.add("listening");
            voiceButton.setAttribute("aria-label", "Stop listening");
        } else {
            voiceButton.classList.remove("listening");
            voiceButton.setAttribute("aria-label", "Start listening");
        }
    }

    function setupSpeechRecognition() {
        if (!SpeechRecognition) {
            return;
        }

        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            isListening = true;
            updateVoiceButtonState();
        };

        recognition.onend = () => {
            isListening = false;
            updateVoiceButtonState();
        };

        recognition.onerror = () => {
            addMessage("Could not capture voice. Try again.", false);
            isListening = false;
            updateVoiceButtonState();
        };

        recognition.onresult = (event) => {
            const transcript = event.results?.[0]?.[0]?.transcript || "";
            if (!transcript.trim()) {
                return;
            }
            messageInput.value = transcript;
            sendMessage(transcript);
        };
    }

    setupSpeechRecognition();
    updateVoiceButtonState();

    chatForm.addEventListener("submit", (event) => {
        event.preventDefault();
        sendMessage(messageInput.value);
    });

    voiceButton.addEventListener("click", () => {
        if (!recognition) {
            addMessage("This browser does not support voice recognition.", false);
            return;
        }

        if (isListening) {
            recognition.stop();
            return;
        }

        recognition.start();
    });
})();
