function userMessage(text,sender){
    const bubble = document.createElement("div");
    bubble.classList.add("message",sender);
    bubble.textContent = text;
    const chatWindow = document.getElementById("chat-window");
    chatWindow.appendChild(bubble);
    console.log("scrollHeight:", chatWindow.scrollHeight, "clientHeight:", chatWindow.clientHeight);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function answer(prompt, text){
    prompt.textContent = text;
    const chatWindow = document.getElementById("chat-window");
    console.log("scrollHeight:", chatWindow.scrollHeight, "clientHeight:", chatWindow.clientHeight);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(){
    const inputBox = document.getElementById("query-input");
    const userInput = inputBox.value;
    inputBox.value = "";    
    userMessage(userInput,"user");
    const prompt = document.createElement("div");
    prompt.classList.add("message", "LLM");
    prompt.textContent = "Waiting for response...";
    const chatWindow = document.getElementById("chat-window");
    chatWindow.appendChild(prompt);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    const response = await fetch("/ask",{
        method: "POST",
        headers: {"Content-type": "application/json"},
        body: JSON.stringify({query:userInput})
    });
    const data = await response.json();
    answer(prompt, data.answer);
}

const sendBtn = document.getElementById("send-btn");
sendBtn.addEventListener("click",sendMessage);
