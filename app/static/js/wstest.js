socket = io();

function send_message(message, event_name='general'){
    socket.emit(event_name, message);
};


function echo(){
    message = document.getElementById("echoinput").value;
    send_message(message);
}