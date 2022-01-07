

$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
    $('select').formSelect();
    $('.tooltipped').tooltip();
    $('#app').hide();
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


Vue.component('downcounter', {
    name: '',
    data: function(){
        return {
            secs: 30
        }
    },
    props: [],
    template: ''
})


Vue.component('sidebar', {
    name: 'sidebar',
    data: function(){
        return { content: 'SIDEBAR'}
    },
    props: [],
    template: '<div><p>{{content}}</p></div>'
})



//------------------Vue app---------------------
var app = new Vue({

    delimiters: ['##', '##'],

    components: {
        //'counterbutton',
    },

    el: '#app',

    data: {
        message: 'Hello Vue!',
        data: {},
    },

    created() {},

    computed: {},

    methods: {},

})




