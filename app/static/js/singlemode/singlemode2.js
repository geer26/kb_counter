

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
        app.$forceUpdate();
    }, 'json')
}


//----------------Components--------------------
Vue.component('button-counter', {

    data: function () {
        return {
        count: 0,
        }
    },

    template: `
        <button v-on:click="count++">
                You clicked me {{ count }} times.
        </button>
    `,

})


Vue.component('downcounter', {
    data: function(){
        return {
            secs: 30,
        }
    },
    props: [],
    template: `

    `,
})


Vue.component('sidebar', {
    name: 'sidebar',
    data: function(){
        return { content: 'SIDEBAR'}
    },
    props: [],
    template: `
        <ul>
            <li v-for="player in data"> ## player.cname ## </li>
        </ul>
    `,
})




//------------------Vue app---------------------
var app = new Vue({

    delimiters: ['##', '##'],

    el: '#app',

    data: function() {
        return {
            message: 'Hello Vue!',
            data: {},

            playerIndex: 0,
            currentPlayer: null
        }
    },

    props: {
        dt: {},
    },

    created() {},

    computed: {},

    methods: {
        nextPlayer: function() {
            this.playerIndex++;
            if (this.playerIndex >= this.data.length) {
                // VÉGE
            }
        },

        showCurrentPlayer: function() {
            this.currentPlayer = this.data[this.playerIndex];
        }
    },

    mounted(){
        console.log('HELLO, VUE HERE!');
    },

    updated() {
        this.message = "Started";
        this.playerIndex = 0;
        // Show current player info
        this.showCurrentPlayer();
    }

})




