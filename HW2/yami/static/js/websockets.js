// $(function () {
    var ws;
    var canSendFile = false;

    $(document).ready(function () {
        connWebSocket();
    });

    function sendFileName(username) {
        // send filename to server through websocket
        ws.send(username);
        console.log('sent filename ' + username);
    }

    function connWebSocket() {
        var url = "ws://34.242.86.31:5000";

        ws = new WebSocket(url);
        ws.binaryType = "arraybuffer";
        ws.onopen = function () {
            console.log("Connected.");
        };

        ws.onmessage = function (evt) {
            if (evt.data === 'send file') {
                canSendFile = true;
                console.log("can send file...");
            } else {
                console.log(evt.data);
                canSendFile = false;
            }
        };

        ws.onclose = function () {
            console.log("Connection is closed...");
        };

        ws.onerror = function (e) {
            console.log(e.msg);
        }

    }

    function sendFile() {
        if (!canSendFile) {
            return;
        }

        var file = document.getElementById('filename').files[0];
        var reader = new FileReader();
        var rawData = new ArrayBuffer();
        reader.loadend = function () {
        };

        reader.onload = function (e) {
            rawData = e.target.result;
            ws.send(rawData);

            var sentFileMessage = document.getElementById('sentItemMessage');
            sentFileMessage.style.visibility = "visible";
        };

        reader.readAsArrayBuffer(file);
    }
// });