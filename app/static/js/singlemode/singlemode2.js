$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
    $('select').formSelect();
    $('.tooltipped').tooltip();
});

function fetch_event(id){
    console.log('EID TO FETCH: ', id);
    data = JSON.stringify({eid: id});
    $.post('/API/fetch_s_event', data ,function(data){console.log(data['data']);}, 'json')
}