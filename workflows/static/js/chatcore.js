socket = new WebSocket("ws://" + window.location.host + "/chat/");

socket.onmessage = function(e) {
    var chatSection = document.getElementById("chat-section");
    var p = document.createElement('p');
    var node = document.createTextNode(e.data);
    p.appendChild(node);
    chatSection.appendChild(p);
};

if (socket.readyState == WebSocket.OPEN)
    socket.onopen();

var sendButton = document.getElementById("send-button");
    sendButton.onclick = function()
    {
        var msg = document.getElementById("textarea").value;
        socket.send(JSON.stringify({"username": msg}));
        document.getElementById("textarea").value = '';

};


