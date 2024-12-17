const socket = io.connect('http://' + document.domain + ':' + location.port);



function openURL(link){
    socket.emit('open_link', { url: link });
}