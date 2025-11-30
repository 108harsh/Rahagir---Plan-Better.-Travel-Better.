const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Auto-scroll to bottom
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Add Message to UI
function addMessage(text, isUser = false) {
    const div = document.createElement('div');
    div.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    // Simple markdown parsing for bold and newlines
    let formattedText = text.replace(/\n/g, '<br>');
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    div.innerHTML = formattedText;
    chatContainer.appendChild(div);
    scrollToBottom();
}

// Send Request to Backend
async function handleSend() {
    const text = userInput.value.trim();
    if (!text) return;

    // 1. Add User Message
    addMessage(text, true);
    userInput.value = '';
    userInput.disabled = true;

    // 2. Show Loading State
    const loadingId = 'loading-' + Date.now();
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message';
    loadingDiv.id = loadingId;
    loadingDiv.textContent = 'Thinking...';
    chatContainer.appendChild(loadingDiv);
    scrollToBottom();

    // Get or Create User ID
    let userId = localStorage.getItem('rahagir_user_id');
    if (!userId) {
        userId = "web_user_" + Date.now();
        localStorage.setItem('rahagir_user_id', userId);
    }

    try {
        // 3. Call API
        const response = await fetch('/plan_trip', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                raw_user_input: text,
                user_id: userId
            })
        });

        const data = await response.json();

        // 4. Remove Loading and Show Response
        document.getElementById(loadingId).remove();

        if (data.status === "Success") {
            addMessage(data.message);
            // If there's a trip ID or other details, we could show them here
        } else {
            addMessage("Sorry, I encountered an error: " + data.detail);
        }

    } catch (error) {
        document.getElementById(loadingId).remove();
        addMessage("Network error. Please try again.");
        console.error(error);
    } finally {
        userInput.disabled = false;
        userInput.focus();
    }
}

// Event Listeners
sendBtn.addEventListener('click', handleSend);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});
