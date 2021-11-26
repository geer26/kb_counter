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