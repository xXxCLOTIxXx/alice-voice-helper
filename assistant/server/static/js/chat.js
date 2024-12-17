
        const socket = io.connect('http://' + document.domain + ':' + location.port);

        const chatContainer = document.getElementById('chat');
        const userInput = document.getElementById('userInput');
        const internetStatus = document.getElementById('internet-status');
        const botStatus = document.getElementById('bot-status');


        function addMessage(content, sender, color) {
            const message = document.createElement('div');
            message.className = `message ${sender}`;
            message.textContent = content;
            message.style.backgroundColor = color;
            chatContainer.appendChild(message);
            window.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: 'smooth'
            });
        }

        function sendMessage() {
            const userMessage = userInput.value.trim();

            if (userMessage) {
                socket.emit('send_message', {
                    message: userMessage
                });
                userInput.value = '';
            }
        }

        socket.on('new_message', (data) => {
            const { message, sender, color } = data;
            addMessage(message, sender, color);
        });


        window.onload = () => {
            addMessage("Добро пожаловать в чат!", "system", "dark magenta")
            getChatHistory();
        };

        function getChatHistory() {
            socket.emit('get_history');
        }

        function clear_chat(){
            socket.emit('chat_clear');
            location.reload(true);
        }

        socket.on('history', (history) => {
            history.forEach((msg) => {
                addMessage(msg.message, msg.sender, msg.color);
            });
        });


document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') { 
        sendMessage();
    }
});






async function checkInternetConnection() {
    try {
        const response = await fetch('https://www.google.com/favicon.ico', { method: 'HEAD', mode: 'no-cors' });
        if (response.ok || response.status === 200 || response.type === 'opaque') {
            setInternetStatus(true);
        } else {
            setInternetStatus(false);
        }
    } catch (error) {
        setInternetStatus(false);
    }
}


function setInternetStatus(isOnline) {
    if (isOnline) {
        internetStatus.textContent = "Подключено";
        internetStatus.classList.remove('offline');
        internetStatus.classList.add('online');
    } else {
        internetStatus.textContent = "Нет соединения";
        internetStatus.classList.remove('online');
        internetStatus.classList.add('offline');
    }
}


function startInternetMonitoring() {
    checkInternetConnection();
    setInterval(checkInternetConnection, 5000);
}


function setBotStatus(text, color) {
    botStatus.textContent = text;
    if (color) {
        botStatus.style.color = color;
    }
}

socket.on('ai_status', (data) => {
    const {text, color} = data;
    setBotStatus(text, color);
});




startInternetMonitoring();