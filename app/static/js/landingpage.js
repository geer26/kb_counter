$(document).ready(function(){
    $('.tooltipped').tooltip();
  });


function closemodal(modal){
    modal.hide();
    return true;
}


function openmodal(modal){
    var inputs = modal.find("input");
    inputs.each(function(){
        $(this).val('');
    });

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
                hide_loader();
                window.location.href = "/";
                /*
                $('#main').empty();
                $('#main').append(result['html']);
                $("[data-target="+visible_tab.toString()+"]").click();
                get_logs();
                */
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                console.log(jqXhr);
            }
    });
}



function login(){
    //show_loader();
    console.log('HELLO WORLD!')
    d = {username:'test', password: 'qwertz'};
    $.ajax({
            url: '/API/login',
            type: 'POST',
            dataType: "json",
            //update data content!
            data: d,
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
            }
    });
}