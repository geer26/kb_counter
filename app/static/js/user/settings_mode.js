$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
    $('select').formSelect();
});


function showerror(message,errorplace){
    errorplace.text(message);
    errorplace.show();
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


function hide_error(){
    $('.errormessage').hide();
}


function add_exercise(){
    //show_loader();

    //extract data from modal
    //var un = $('#uname').val();
    //var pw = $('#pw').val();
    //var mode = $("input[name='mode']:checked").attr('id');
    var name;
    $('#name').val() ? name = $('#name').val() : showerror('Adjon nevet a gyakorlatnak!', $('#addexerciseerror'));
    var short_name;
    $('#sname').val() ? sname = $('#sname').val() : showerror('Határozza meg a megjelenítendő nevet!', $('#addexerciseerror'));
    var link = $('#link').val();
    var type;
    console.log($('#type').val());
    var max_rep;
    var duration;
    var user;

    //compose data to post
    var d;
    //d = JSON.stringify({username:un, password:pw, mode:mode});

    //send ajax POST request
    /*
    $.ajax({
            url: '/API/addexercise',
            type: 'POST',
            dataType: "json",
            data: d,
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                //window.location.href = "/";
                //update exercise pane
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                showerror(jqXhr['responseJSON']['message'], $('#addexerciseerror'))
            }
    }); */
}