socket = io();

function send_message(message_text, event_code=100, event_name='general'){
    var m = {event: event_code, message: message_text}
    socket.emit(event_name, m);
};


function echo(){
    var message = document.getElementById("echoinput").value;
    send_message(message);
}


//Socket event dispatcher
socket.on('general', function(data){
    //print(data)
    switch (data['event']){
        case 100:  //ECHO receive function
            console.log(data['message']);
            break
    }
});