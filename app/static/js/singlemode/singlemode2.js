

$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
    $('select').formSelect();
    $('.tooltipped').tooltip();
});


function fetch_event(id){
    data = JSON.stringify({eid: id});
    $.post('/API/fetch_s_event', data ,function(data){
        console.log('FETCHED DATA: ', data['data']);
        $('#select-workout').hide();
        $('#app').show();
    }, 'json')
}


Vue.component('button-counter', {
  data: function () {
    return {
      count: 0
    }
  },
  template: '<button v-on:click="count++">You clicked me {{ count }} times.</button>'
})

new Vue({ el: '#components-demo' })

