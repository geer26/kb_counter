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
    //extract data from modal
    var name;
    if ($('#name').val()){
        name = $('#name').val()
    } else{
        showerror('Adjon nevet a gyakorlatnak!', $('#addexerciseerror'));
        return;
    }

    var short_name;
    if ($('#sname').val()){
        short_name = $('#sname').val()
    } else{
        showerror('Határozza meg a megjelenítendő nevet!', $('#addexerciseerror'));
        return;
    }

    var link = $('#link').val();
    if ($('#link').val()){
        link = $('#link').val();
    } else{
        link = null
    }

    var type;
    if ($('#type').val()){
        type = $('#type').val();
    } else{
        showerror('Határozza meg a gyakorlat típusát!', $('#addexerciseerror'));
        return;
    }

    var max_rep;
    if ($('#maxrep').val()){
        max_rep = $('#maxrep').val();
    } else{
        max_rep = null
    }

    var duration;
    if ($('#duration').val()){
        duration = $('#duration').val();
    } else{
        showerror('Határozza meg a gyakorlat időtartamát!', $('#addexerciseerror'));
        return;
    }

    var userid;
    userid = parseInt($('#userident').text());

    //compose data to post
    var d;
    d = {name: name, short_name: short_name, link: link, type: type, max_rep:max_rep, duration:duration, userid:userid};

    show_loader();
    //send ajax POST request
    $.ajax({
            url: '/API/addexercise',
            type: 'POST',
            dataType: "json",
            data: JSON.stringify(d),
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                //window.location.href = "/";
                //update exercise pane
                console.log(result);
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                showerror(jqXhr['responseJSON']['message'], $('#addexerciseerror'))
            }
    });
}