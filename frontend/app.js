const API_URL = "http://127.0.0.1:8000";

let sessionId = "session-" + Date.now();
let selectedSource = null;


// Load documents when page opens
document.addEventListener("DOMContentLoaded", () => {
    loadDocuments();
});


// -----------------------------
// Load Documents
// -----------------------------

async function loadDocuments() {

    const container = document.getElementById("documents");

    try {

        const response = await fetch(`${API_URL}/documents`);

        if (!response.ok) {
            throw new Error("Failed to load documents");
        }

        const data = await response.json();

        container.innerHTML = "";

        if (!data.documents || data.documents.length === 0) {

            container.innerHTML =
                '<p class="empty">No documents uploaded.</p>';

            return;
        }

        data.documents.forEach(doc => {

    const div = document.createElement("div");

    div.className = "document";

    div.textContent =
        `${doc.name} (${doc.chunks} chunks)`;

    div.title = "Click to use this document";

    div.onclick = () => selectDocument(doc.name);

    container.appendChild(div);

});

    } catch (error) {

        console.error(error);

        container.innerHTML =
            '<p class="empty">Backend unavailable.</p>';
    }
}


// -----------------------------
// Select Document
// -----------------------------

function selectDocument(filename) {

    selectedSource = filename;

    addAssistantMessage(
        `Selected document: <strong>${escapeHtml(filename)}</strong><br>
         Future questions will use this document.`
    );
}


// -----------------------------
// Send Message
// -----------------------------

async function sendMessage() {

    const input = document.getElementById("messageInput");

    const message = input.value.trim();

    if (!message) {
        return;
    }

    input.value = "";

    removeWelcome();

    addUserMessage(message);

    const button = document.getElementById("sendButton");

    button.disabled = true;

    const loadingId = addAssistantMessage("Thinking...");

    try {

        const response = await fetch(`${API_URL}/chat`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                message: message,

                source: selectedSource,

                session_id: sessionId

            })

        });

        const data = await response.json();

        removeMessage(loadingId);

        if (!response.ok) {

            addAssistantMessage(
                `Error: ${escapeHtml(data.detail || "Something went wrong.")}`
            );

            return;
        }

        addAssistantMessage(
            formatResponse(data.response),
            data.sources
        );

    } catch (error) {

        console.error(error);

        removeMessage(loadingId);

        addAssistantMessage(
            "Unable to connect to the FastAPI server. Make sure Uvicorn is running."
        );

    } finally {

        button.disabled = false;

        input.focus();
    }
}


// -----------------------------
// User Message
// -----------------------------

function addUserMessage(message) {

    const chat = document.getElementById("chat");

    const div = document.createElement("div");

    div.className = "message user";

    div.innerHTML = `
        <div class="message-content">
            ${escapeHtml(message)}
        </div>
    `;

    chat.appendChild(div);

    scrollToBottom();
}


// -----------------------------
// Assistant Message
// -----------------------------

function addAssistantMessage(message, sources = []) {

    const chat = document.getElementById("chat");

    const id =
        "message-" +
        Date.now() +
        "-" +
        Math.random().toString(36).substring(2, 8);

    const div = document.createElement("div");

    div.id = id;

    div.className = "message assistant";

    let sourcesHTML = "";

    if (sources && sources.length > 0) {

        sourcesHTML = `
            <div class="sources">
                📄 Source: ${sources
                    .map(source => escapeHtml(source))
                    .join(", ")}
            </div>
        `;
    }

    div.innerHTML = `
        <div class="message-content">
            ${message}
            ${sourcesHTML}
        </div>
    `;

    chat.appendChild(div);

    scrollToBottom();

    return id;
}


// -----------------------------
// Remove Message
// -----------------------------

function removeMessage(id) {

    const message = document.getElementById(id);

    if (message) {
        message.remove();
    }
}


// -----------------------------
// New Chat
// -----------------------------

function newChat() {

    sessionId = "session-" + Date.now();

    selectedSource = null;

    const chat = document.getElementById("chat");

    chat.innerHTML = `
        <div class="welcome">

            <div class="welcome-icon">✦</div>

            <h2>How can I help you?</h2>

            <p>
                Upload your enterprise documents and ask questions
                using natural language.
            </p>

            <div class="suggestions">

                <button onclick="useSuggestion('What position is mentioned?')">
                    What position is mentioned?
                </button>

                <button onclick="useSuggestion('Summarize this document')">
                    Summarize this document
                </button>

                <button onclick="useSuggestion('What skills are mentioned?')">
                    What skills are mentioned?
                </button>

            </div>

        </div>
    `;

    document.getElementById("messageInput").focus();
}


// -----------------------------
// Suggestions
// -----------------------------

function useSuggestion(text) {

    const input = document.getElementById("messageInput");

    input.value = text;

    input.focus();

    sendMessage();
}


// -----------------------------
// Enter Key
// -----------------------------

function handleKey(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }
}


// -----------------------------
// Remove Welcome Screen
// -----------------------------

function removeWelcome() {

    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }
}


// -----------------------------
// Format Response
// -----------------------------

function formatResponse(text) {

    if (!text) {
        return "";
    }

    return escapeHtml(text)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");
}


// -----------------------------
// Escape HTML
// -----------------------------

function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// -----------------------------
// Scroll Chat
// -----------------------------

function scrollToBottom() {

    const chat = document.getElementById("chat");

    chat.scrollTop = chat.scrollHeight;
}
// -----------------------------
// Upload Document
// -----------------------------

async function uploadDocument(input) {

    const file = input.files[0];

    if (!file) {
        return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {

        alert("Please select a PDF file.");

        input.value = "";

        return;
    }

    const uploadButton = document.querySelector(".upload-button");

    uploadButton.disabled = true;
    uploadButton.textContent = "Uploading...";

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch(
            `${API_URL}/documents/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Failed to upload document."
            );
        }

        addAssistantMessage(
            `Document <strong>${escapeHtml(data.filename)}</strong> uploaded successfully.<br>
             ${data.chunks} chunks processed.`
        );

        await loadDocuments();

    } catch (error) {

        console.error(error);

        addAssistantMessage(
            `Upload failed: ${escapeHtml(error.message)}`
        );

    } finally {

        uploadButton.disabled = false;
        uploadButton.textContent = "+ Upload PDF";

        input.value = "";
    }
}