$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
    $('select').formSelect();
    userid = parseInt($('#userident').text());


    var list_of_exercises;

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
    //console.log(data);

    $('#exer_name').val(data['name']);
    $('#exer_sname').val(data['short_name']);
    $('#exer_link').val(data['link']);
    var t = '#exer_type option[value=' + data['type'] + ']';
    $(t).attr('selected', true);
    $('#exer_maxrep').val(data['max_rep']);
    $('#exer_duration').val(data['duration']);

    $('select').formSelect();

    $('#ex_idholder').text(data['id']);

    $('#addexercise_modalback').show();
    $('#add_e').hide();
    $('#mod_e').show();

    return true;
}


function mod_exercise(){
    //extract data from modal
    var name;
    if ($('#exer_name').val()){
        name = $('#exer_name').val()
    } else{
        showerror('Adjon nevet a gyakorlatnak!', $('#addexerciseerror'));
        return;
    }

    var short_name;
    if ($('#exer_sname').val()){
        short_name = $('#exer_sname').val()
    } else{
        showerror('Határozza meg a megjelenítendő nevet!', $('#addexerciseerror'));
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
        showerror('Határozza meg a gyakorlat típusát!', $('#addexerciseerror'));
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
        showerror('Határozza meg a gyakorlat időtartamát!', $('#addexerciseerror'));
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
                closemodal($('#addexercise_modalback'));
                $('#etc2_content').empty();
                $('#etc2_content').append(result['fragment']);
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                closemodal($('#addexercise_modalback'));
                showerror(jqXhr['responseJSON']['message'], $('#addexerciseerror'))
            }
    });
}


function hide_error(){
    $('.errormessage').hide();
    return true;
}


function adde(modal){
    $('#add_e').show();
    $('#mod_e').hide();
    openmodal(modal);
}


function add_exercise(){
    //extract data from modal
    var name;
    if ($('#exer_name').val()){
        name = $('#exer_name').val()
    } else{
        showerror('Adjon nevet a gyakorlatnak!', $('#addexerciseerror'));
        return;
    }

    var short_name;
    if ($('#exer_sname').val()){
        short_name = $('#exer_sname').val()
    } else{
        showerror('Határozza meg a megjelenítendő nevet!', $('#addexerciseerror'));
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
        showerror('Határozza meg a gyakorlat típusát!', $('#addexerciseerror'));
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
        showerror('Határozza meg a gyakorlat időtartamát!', $('#addexerciseerror'));
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
                closemodal($('#addexercise_modalback'));
                $('#etc2_content').empty();
                $('#etc2_content').append(result['fragment']);
                return;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                closemodal($('#addexercise_modalback'));
                showerror(jqXhr['responseJSON']['message'], $('#addexerciseerror'))
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
                $('#etc2_content').empty();
                $('#etc2_content').append(result['fragment']);
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
    //display workout dashboard
    $('.manipulate-workout-container').show();
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
    //TODO zeroize!!!
}