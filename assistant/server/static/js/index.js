const canvas = document.getElementById('visualizer');
const canvasCtx = canvas.getContext('2d');
canvas.width = 150;
canvas.height = 150;

const socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', () => {
    console.log('Connected to WebSocket server');
});


socket.on('message', (data) => {
    console.log(data.data);
});

socket.on('canvas_update', (data) => {
    const radius = data.radius;
    const color = data.color
    drawCanvas(radius, color);
});


function drawCanvas(radius, color) {
    canvasCtx.clearRect(0, 0, canvas.width, canvas.height);


    canvasCtx.beginPath();
    canvasCtx.arc(canvas.width / 2, canvas.height / 2, radius, 0, 2 * Math.PI);
    canvasCtx.fillStyle = color ? color : 'rgba(0, 123, 255, 0.3)';
    canvasCtx.fill();
}


function sendMessage() {
    const message = document.getElementById('messageInput').value;
    if (message) {
        socket.emit('send_message', { message: message });
        document.getElementById('messageInput').value = ''; 
    }
}


document.getElementById('messageInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') { 
        sendMessage();
    }
});