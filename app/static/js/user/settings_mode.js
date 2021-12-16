var list_of_exercises;
var list_of_workouts;

$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
    $('select').formSelect();
    $('.tooltipped').tooltip();
    userid = parseInt($('#userident').text());

    new Sortable(dnd_ex_in, {
        group: {
            name: 'shared',
            //pull: 'clone' // To clone: set pull to 'clone'
        },
        animation: 150,

        onAdd: function (evt) {
		    var buttons_to_hide = evt.item.getElementsByClassName("chunkbutton-holder-right");
		    $(buttons_to_hide).hide();
		    //list_of_exercises = document.getElementById('dnd_ex_in').getElementsByClassName('fragment-chunk')
		    //console.log(list_of_exercises);
	    },

	    onSort: function (/**Event*/evt) {
	        list_of_exercises = [];
		    var l_o_e = document.getElementById('dnd_ex_in').getElementsByClassName('fragment-chunk');
		    for (var e of l_o_e){list_of_exercises.push(e.getAttribute('data-exid'));};
		    if(l_o_e.length != 0){
		        $('#dnd-instruction').hide();
		    } else {
		        $('#dnd-instruction').show();
		    }
	    },

    });

    new Sortable(etc2_content, {
        group: {
            name: 'shared',
            pull: 'clone'
        },
        animation: 150,

        onAdd: function (evt) {
		    $(evt.item).remove();
	    },

    });

    new Sortable(dnd_wo_in, {
        group: {
            name: 'shared2',
            //pull: 'clone' // To clone: set pull to 'clone'
        },
        animation: 150,

        onAdd: function (evt) {
		    var buttons_to_hide = evt.item.getElementsByClassName("chunkbutton-holder-right");
		    $(buttons_to_hide).hide();
		    list_of_exercises = document.getElementById('dnd_wo_in').getElementsByClassName('fragment-chunk')
	    },

	    onSort: function (/**Event*/evt) {
	        list_of_workouts = [];
		    var l_o_w = document.getElementById('dnd_wo_in').getElementsByClassName('fragment-chunk');
		    for (var e of l_o_w){list_of_workouts.push(e.getAttribute('data-woid'));};
		    if(l_o_w.length != 0){
		        $('#dnd-instruction-wo').hide();
		    } else {
		        $('#dnd-instruction-wo').show();
		    }
	    },

    });

    new Sortable(etc1_content, {
        group: {
            name: 'shared2',
            pull: 'clone'
        },
        animation: 150,

        onAdd: function (evt) {
		    $(evt.item).remove();
	    },

    });

});


function showerror(message,errorplace){
    errorplace.text(message);
    errorplace.show();
}


function edit_exercise(exercise){
    $.ajax({
            url: '/API/getexercise',
            type: 'POST',
            dataType: "json",
            data: JSON.stringify({exid:exercise}),
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                ed_ex(result);
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
            }
    });
    return true;

}


function ed_ex(data){
    //fill inputs
    $('#addexerror').hide();
    $('#exer_name').val(data['name']);
    $('#exer_sname').val(data['short_name']);
    $('#exer_link').val(data['link']);
    $('#exer_maxrep').val(data['max_rep']);
    $('#exer_duration').val(data['duration']);
    $('#exer_type').val(data['type']);
    $("#ex_idholder").text(data['id']);
    //init inputs
    $('.tooltipped').tooltip();
    $('select').formSelect();
    M.updateTextFields();
    M.textareaAutoResize($('.materialize-textarea'));
    // modify button function and label
    //$('#man_ex_add').text('');
    $('#man_ex_add').attr('onClick','mod_exercise()');
    //show modal
    show_addexercise('ESEMÉNY SZERKESZTÉSE');
}


function mod_exercise(){
    //extract data from modal
    var name;
    if ($('#exer_name').val()){
        name = $('#exer_name').val()
    } else{
        showerror('Adjon nevet a gyakorlatnak!', $('#addexerror'));
        return;
    }

    var short_name;
    if ($('#exer_sname').val()){
        short_name = $('#exer_sname').val()
    } else{
        showerror('Határozza meg a megjelenítendő nevet!', $('#addexerror'));
        return;
    }

    var link = $('#exer_link').val();
    if ($('#exer_link').val()){
        link = $('#exer_link').val();
    } else{
        link = null
    }

    var type;
    if ($('#exer_type').val()){
        type = $('#exer_type').val();
    } else{
        showerror('Határozza meg a gyakorlat típusát!', $('#addexerror'));
        return;
    }

    var max_rep;
    if ($('#exer_maxrep').val()){
        max_rep = $('#exer_maxrep').val();
    } else{
        max_rep = null
    }

    var duration;
    if ($('#exer_duration').val()){
        duration = $('#exer_duration').val();
    } else{
        showerror('Határozza meg a gyakorlat időtartamát!', $('#addexerror'));
        return;
    }

    var uid;
    uid = userid;

    var id;
    id = $('#ex_idholder').text();

    //compose data to post
    var d;
    d = {id: id, name: name, short_name: short_name, link: link, type: type, max_rep:max_rep, duration:duration, user:uid};

    show_loader();
    //send ajax POST request
    $.ajax({
            url: '/API/modifyexercise',
            type: 'POST',
            dataType: "json",
            data: JSON.stringify(d),
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                hide_addexercise();
                $('#etc2_content').empty();
                $('#etc2_content').append(result['fragment']);
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                showerror(jqXhr['responseJSON']['message'], $('#addexerror'));
                return;
            }
    });
}


function hide_error(){
    $('.errormessage').hide();
    return true;
}


function add_exercise(){
    //extract data from modal
    var name;
    if ($('#exer_name').val()){
        name = $('#exer_name').val();
    } else{
        showerror('Adjon nevet a gyakorlatnak!', $('#addexerror'));
        return;
    }

    var short_name;
    if ($('#exer_sname').val()){
        short_name = $('#exer_sname').val()
    } else{
        showerror('Határozza meg a megjelenítendő nevet!', $('#addexerror'));
        return;
    }

    var link = $('#exer_link').val();
    if ($('#exer_link').val()){
        link = $('#exer_link').val();
    } else{
        link = null
    }

    var type;
    if ($('#exer_type').val()){
        type = $('#exer_type').val();
    } else{
        showerror('Határozza meg a gyakorlat típusát!', $('#addexerror'));
        return;
    }

    var max_rep;
    if ($('#exer_maxrep').val()){
        max_rep = $('#exer_maxrep').val();
    } else{
        max_rep = null
    }

    var duration;
    if ($('#exer_duration').val()){
        duration = $('#exer_duration').val();
    } else{
        showerror('Határozza meg a gyakorlat időtartamát!', $('#addexerror'));
        return;
    }

    var uid;
    uid = userid;

    //compose data to post
    var d;
    d = {name: name, short_name: short_name, link: link, type: type, max_rep:max_rep, duration:duration, userid:uid};

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
                hide_addexercise();
                $('#etc2_content').empty();
                $('#etc2_content').append(result['fragment']);
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                showerror(jqXhr['responseJSON']['message'], $('#addexerror'));
                return;
            }
    });

}


function del_exercise(id){
    //extract data from modal
    var id;
    id = id;

    //compose data to post
    var d;
    d = {id:id, userid:userid};

    show_loader();
    //send ajax POST request
    $.ajax({

            url: '/API/delexercise',
            type: 'POST',
            dataType: "json",
            data: JSON.stringify(d),
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                //closemodal($('#addexercise_modalback'));
                //$('#etc2_content').empty();
                //$('#etc2_content').append(result['fragment']);
                location.reload();
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                closemodal($('#addexercise_modalback'));
                showerror(jqXhr['responseJSON']['message'], $('#addexerciseerror'))
            }

    });
}


function show_addworkout(title='ÚJ VERSENYSZÁM'){
    //hide event chunk holder
    $('.event-holder').hide();
    //fade workout plain
    $('#wo_fader').show();
    //change title and hide button
    $('#active_title').text(title);
    $('#active_button').hide();
    //hide add exercise button
    $('#etc2_button').hide();
    //hide exercises manipulate buttons
    $('#etc2_content .chunkbutton-holder-right').hide();

    M.updateTextFields();
    M.textareaAutoResize($('.materialize-textarea'));

    //display workout dashboard
    $('.manipulate-workout-container').show();
}


function add_workout(){

    //extract data from form
    var name = $('#wo_sname').val();
    var description = $('#wo_description').val();
    var uid;
    uid = userid;

    //compose json
    console.log(list_of_exercises);
    var data = JSON.stringify({ short_name: name, description: description, exercises: list_of_exercises, user: uid });

    //post AJAX request
    $.ajax({
            url: '/API/addworkout',
            type: 'POST',
            dataType: "json",
            data: data,
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                hide_addworkout();
                $('#etc1_content').empty();
                $('#etc1_content').append(result['fragment']);
                $('.tooltipped').tooltip();
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                closemodal($('#addexercise_modalback'));
                showerror(jqXhr['responseJSON']['message'], $('#addexerciseerror'))
            }
    });

}


function del_workout(id){

    //extract data from modal
    var id;
    id = id;

    //compose data to post
    var d;
    d = JSON.stringify({id:id, userid:userid});

    show_loader();
    //send ajax POST request
    $.ajax({

            url: '/API/delworkout',
            type: 'POST',
            dataType: "json",
            data: (d),
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                //$('#etc1_content').empty();
                //$('#etc1_content').append(result['fragment']);
                location.reload();
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                closemodal($('#addexercise_modalback'));
                showerror(jqXhr['responseJSON']['message'], $('#addexerciseerror'))
            }

    });

}


function edit_workout(workout){

    var woid = workout['id'];
    $('#wo_sname').val(workout['name']);
    $('#wo_description').val(workout['description']);

    if (workout['exercises'].length > 0) {
        $('#dnd-instruction').hide();
    }

    list_of_exercises = [];
    workout['exercises'].forEach(exercise => {
        var chunk = $('#etc2_content [data-exid=' + exercise.toString() + ']').clone();
        $('#dnd_ex_in').append(chunk);
        var buttons_to_hide = document.getElementById('dnd_ex_in').getElementsByClassName("chunkbutton-holder-right");
		$(buttons_to_hide).hide();
		list_of_exercises.push(exercise);
    });

    //change onclick target to update workout
    $('#man_wo_add').attr('onClick','update_workout('+ woid.toString() + ')');

    //show modal
    show_addworkout('VERSENYSZÁM SZERKESZTÉSE');
    return;
}


function update_workout(woid){
    //collect data and compose POST data
    var name = $('#wo_sname').val();
    var description = $('#wo_description').val();
    var data = JSON.stringify({ woid: woid, short_name: name, description: description, exercises: list_of_exercises, user: userid });

    //POST ajax request
    $.ajax({
            url: '/API/updateworkout',
            type: 'POST',
            dataType: "json",
            data: data,
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                hide_addworkout();
                $('#etc1_content').empty();
                $('#etc1_content').append(result['fragment']);
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                closemodal($('#addexercise_modalback'));
                showerror(jqXhr['responseJSON']['message'], $('#addexerciseerror'))
            }
    });
}


function hide_addworkout(){
    //show event chunk holder
    $('.event-holder').show();
    //unfade workout plain
    $('#wo_fader').hide();
    //change title and hide button
    $('#active_title').text('ESEMÉNYEK');
    $('#active_button').show();
    //hide workout dashboard
    $('.manipulate-workout-container').hide();
    //unhide add exercise button
    $('#etc2_button').show();
    //unhide exercises manipulate buttons
    $('#etc2_content .chunkbutton-holder-right').show();
    //clear inputs
    $('#addexerciseerror').hide();
    $('#wo_sname').val('');
    $('#wo_description').val('');
    $('#dnd_ex_in').empty();
    list_of_exercises = [];
    $('.tooltipped').tooltip();
    $('#dnd_ex_in').append('<p id="dnd-instruction">Húzza ide a gyakorlatokat!</p>');
    //TODO restore onclick attribute!
    $('#man_wo_add').attr('onClick','add_workout()')
}


function show_addevent(title='ÚJ ESEMÉNY'){
    //hide event chunk holder
    $('.event-holder').hide();
    //hide add workout button
    $('#etc1_button').hide();
    //hide add workout manipulate buttons
    $('#etc1_content .chunkbutton-holder-right').hide();
    //fade exercises plain
    $('#ex_fader').show();
    //change title and hide button
    $('#active_title').text(title);
    $('#active_button').hide();
    //init inputs
    $('select').formSelect();
    M.updateTextFields();
    M.textareaAutoResize($('.materialize-textarea'));
    //display workout dashboard
    $('.manipulate-event-container').show();
}


function show_addexercise(title='ÚJ GYAKORLAT'){
    //hide event chunk holder
    $('.event-holder').hide();
    //hide add workout button
    $('#active_button').hide();
    //fade unused chunks
    $('#ex_fader').show();
    $('#wo_fader').show();
    //change title
    $('#active_title').text(title);
    //init inputs
    $('select').formSelect();
    M.updateTextFields();
    M.textareaAutoResize($('.materialize-textarea'));
    //display workout dashboard
    $('.manipulate-exercises-container').show();
}


function hide_addevent(){
    //show event chunk holder
    $('.event-holder').show();
    //unhide add workout button
    $('#etc1_button').show();
    //unhide add workout manipulate buttons
    $('#etc1_content .chunkbutton-holder-right').show();
    //unfade exercises plain
    $('#ex_fader').hide();
    //change title and hide button
    $('#active_title').text('ESEMÉNYEK');
    $('#active_button').show();
    //hide workout dashboard
    $('.manipulate-event-container').hide();
    //clear inputs
    $('#addeventerror').hide();
    $('#ev_sname').val('');
    $('#ev_description').val('');
    $('#dnd_wo_in').empty();
    list_of_workouts = [];
    $('.tooltipped').tooltip();
    $('#dnd_wo_in').append('<p id="dnd-instruction-wo">Húzza ide a versenyszámokat!</p>');
    //restore SAVE button event
    $('#man_ev_add').attr('onClick','add_event()')
}


function hide_addexercise(){
    //unhide event chunk holder
    $('.event-holder').show();
    //unhide add workout button
    $('#active_button').show();
     //unfade unused chunks
    $('#ex_fader').hide();
    $('#wo_fader').hide();
    //change title
    $('#active_title').text('ESEMÉNYEK');
    //hide workout dashboard
    $('.manipulate-exercises-container').hide();
    //clear inputs
    $('#addexerror').hide();
    $('#exer_name').val('');
    $('#exer_sname').val('');
    $('#exer_link').val('');
    $('#exer_maxrep').val('');
    $('#exer_duration').val('');
    $('#exer_type').val('');
    $("#ex_idholder").text('');
    $('.tooltipped').tooltip();
    //restore SAVE button event
    $('#man_ex_add').attr('onClick','add_exercise()')
}


function add_event(){

    //extract data from form
    var name = $('#ev_sname').val();
    var description = $('#ev_description').val();
    var uid;
    uid = userid;

    //compose json
    var data = JSON.stringify({ short_name: name, description: description, workouts: list_of_workouts, user: uid });
    console.log(data);

    //post AJAX request
    $.ajax({
            url: '/API/addevent',
            type: 'POST',
            dataType: "json",
            data: data,
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                hide_addevent();
                $('#event_window').empty();
                $('#event_window').append(result['fragment']);
                $('.tooltipped').tooltip();
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                //closemodal($('#addexercise_modalback'));
                showerror(jqXhr['responseJSON']['message'], $('#addeventerror'))
            }
    });

}


function mod_event(id){
    // collect data and compose json to post
    var short_name = $('#ev_sname').val();
    var description = $('#ev_description').val();
    var d = JSON.stringify({short_name: short_name, description: description, list_of_workouts: list_of_workouts, userid: userid, id: id});
    //console.log(d);
    $.ajax({
        url: '/API/editevent',
        type: 'POST',
        dataType: "json",
        data: (d),
        contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                hide_addevent();
                $('#event_window').empty();
                $('#event_window').append(result['fragment']);
                $('.tooltipped').tooltip();
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                showerror(jqXhr['responseJSON']['message'], $('#eventerror'))
            }

    });
}


function del_event(id){
    //compose data to post
    var id;
    id = id;
    var d;
    d = JSON.stringify({id:id, userid:userid});
    show_loader();
    //send ajax POST request
    $.ajax({

            url: '/API/delevent',
            type: 'POST',
            dataType: "json",
            data: (d),
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                $('#event_window').empty();
                $('#event_window').append(result['fragment']);
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                showerror(jqXhr['responseJSON']['message'], $('#eventerror'))
            }

    });

}


function swap_enable(id){
    //compose data to post
    var id;
    id = id;
    var d;
    d = JSON.stringify({id:id, userid:userid});
    show_loader();
    //send ajax POST request
    $.ajax({

            url: '/API/swapenable',
            type: 'POST',
            dataType: "json",
            data: (d),
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                $('#event_window').empty();
                $('#event_window').append(result['fragment']);
                $('.tooltipped').tooltip();
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                showerror(jqXhr['responseJSON']['message'], $('#eventerror'))
            }

    });
}


function edit_event(event){
    // collect data and compose json to post
    var id;
    id = event;
    var d;
    d = JSON.stringify({id:id, userid:userid});
    show_loader();

    //send ajax POST request
    $.ajax({

            url: '/API/geteventdata',
            type: 'POST',
            dataType: "json",
            data: (d),
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();

                //fill inputs
                $('#addeventerror').hide();
                $('#ev_sname').val(result['data']['ev_sname']);
                $('#ev_description').val(result['data']['ev_description']);
                $('#ev_ident').text('IDENT: ' + result['data']['ev_ident']);
                $('#dnd_wo_in').empty();
                list_of_workouts = [];
                //add workout chunks
                result['data']['ev_workouts'].forEach(workout => {
                    var chunk = $('#etc1_content [data-woid=' + workout.toString() + ']').clone();
                    $('#dnd_wo_in').append(chunk);
                    var buttons_to_hide = document.getElementById('dnd_wo_in').getElementsByClassName("chunkbutton-holder-right");
		            $(buttons_to_hide).hide();
		            list_of_workouts.push(workout);
                });
                var temp = 'mod_event(' + result['data']['ev_id'] + ')';
                $('#man_ev_add').attr('onClick',temp);
                show_addevent('ESEMÉNY SZERKESZTÉSE');

                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                showerror(jqXhr['responseJSON']['message'], $('#eventerror'))
            }

    });

}


function edit_competitors(){
    console.log('EDIT COMPETITORS');
}