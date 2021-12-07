$(document).ready(function(){
    $('.tooltipped').tooltip();
  });


function hide_error(){
    $('.errormessage').hide();
}


function closemodal(modal){
    var inputs = modal.find("input");
    inputs.each(function(){
        $(this).val('');
    });
    hide_error();
    modal.hide();
    return true;
}


function openmodal(modal){
    var inputs = modal.find("input");
    inputs.each(function(){
        $(this).val('');
    });
    hide_error();
    modal.show();
    return true;
}



function join(){
    //show_loader();
    $.ajax({
            url: '/API/login',
            type: 'POST',
            dataType: "json",
            //update data content!
            //data: JSON.stringify({id: id}),
            contentType: "application/json; charset=utf-8",

            success: result => {
                //console.log(result);
                //hide_loader();
                window.location.href = "/";
                /*
                $('#main').empty();
                $('#main').append(result['html']);
                $("[data-target="+visible_tab.toString()+"]").click();
                get_logs();
                */
            },

            error: (jqXhr, textStatus, errorMessage) => {
                //hide_loader();
                console.log(jqXhr);
                console.log(jqXhr['responseJSON']);
            }
    });
}



function login(){
    //show_loader();
    console.log('HELLO WORLD!')
    un = $('#uname').val();
    pw = $('#pw').val();
    d = JSON.stringify({username:un, password:pw});
    $.ajax({
            url: '/API/login',
            type: 'POST',
            dataType: "json",
            data: d,
            contentType: "application/json; charset=utf-8",

            success: result => {
                //hide_loader();
                window.location.href = "/";
            },

            error: (jqXhr, textStatus, errorMessage) => {
                //hide_loader();
                //console.log(jqXhr);
                //console.log(jqXhr['responseJSON']['message']);
                $('#loginerror').text( jqXhr['responseJSON']['message'] );
                $('#loginerror').show();
            }
    });
}