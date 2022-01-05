

$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
    $('select').formSelect();
    $('.tooltipped').tooltip();
});


function fetch_event(id){
    data = JSON.stringify({eid: id});
    $.post('/API/fetch_s_event', data ,function(data){
        console.log('FETCHED DATA: ', data['data']);
        app.data = data['data'];
        $('#select-workout').remove();
        $('#app').show();
    }, 'json')
}

//------------------Vue app---------------------
var app = new Vue({

    delimiters: ['##', '##'],

    el: '#app',

    data: {
        message: 'Hello Vue!',
        data: {},
    },

    created: function(){},

})


//----------------Components--------------------
Vue.component('button-counter', {

    name: 'counterbutton',

    data: function () {
        return {
        count: 0
        }
    },

    template: '<button v-on:click="count++">You clicked me {{ count }} times.</button>'

})

new Vue({ el: '#components-demo' })

