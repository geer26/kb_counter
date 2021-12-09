$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
    $('select').formSelect();
});


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


function hide_error(){
    $('.errormessage').hide();
}


function add_exercise(){
    show_loader();
    var un = $('#uname').val();
    var pw = $('#pw').val();

    var mode = $("input[name='mode']:checked").attr('id');

    d = JSON.stringify({username:un, password:pw, mode:mode});

    $.ajax({
            url: '/API/login',
            type: 'POST',
            dataType: "json",
            data: d,
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                window.location.href = "/";
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                //console.log(jqXhr);
                //console.log(jqXhr['responseJSON']['message']);
                $('#loginerror').text( jqXhr['responseJSON']['message'] );
                $('#loginerror').show();
            }
    });
}