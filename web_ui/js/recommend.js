var api_path = 'http://127.0.0.1:5002'

var cur_exif = {};
var prev_exposure = {};
var cur_exposure = {};
var exposure_id = -1;
var target_settings = {};
var manual_mode = false;
var cur_exp_val = null;
var target_exp_val = null;

var camera_id = -1;
var camera = null;
var image_id = 0;
var style = {};
var dof = {};

function recommend_style(image_id){
  var t0 = performance.now();
  $.ajax({
    url: api_path + '/recommend_style',
    type: 'GET',
    data: "image_id="+image_id,
    success: function(data){
      var t1 = performance.now();
      console.log("Recommend Style execution " + (t1 - t0) + "ms.")
      console.log(data);
      style = data;
    }
  });
}

//recommend functions
function rec_settings_wo_image(){}

function rec_settings_w_image(style, image_id){}

function recommend_filter(){}

// dof calc functions
function calc_dof(f_no, fl, subj_dist){
  $.ajax({
    url: api_path + '/calc_dof',
    type: 'GET',
    data: {
      'Aperture':f_no,
      'FocalLength':fl,
      'coc':"0.030",
      'SubjDist':subj_dist},
    dataType: 'json',
    success: function(data){
      console.log(data);
      dof = data;
    }
  });
}

function calc_coc(ff_fl, fl){
  $.ajax({
    url: api_path + '/calc_coc',
    type: 'GET',
    data: {
      'FFFocalLength':ff_fl,
      'FocalLength':fl},
    dataType: 'json',
    success: function(data){
      console.log(data);
    }
  });
}

//exif functions
function get_exif(image_id){
  //var t2 = performance.now();
  $.ajax({
    url: api_path + '/get_exif',
    type: 'GET',
    data: "image_id="+image_id,
    success: function(data){
      //var t3 = performance.now();
      //console.log("Get EXIF execution " + (t3 - t2) + "ms.")
      console.log(data);
      cur_exif = data;
    }
  });

}

// exposure functions
function set_manual_exposure(exp_id, exposure_time, iso, aperture){
  $.ajax({
    url: api_path + '/manual_exposure',
    type: 'PUT',
    data: {
      'exposure_id': exp_id,
      'ExposureTime': exposure_time,
      'ISO': iso,
      'Aperture': aperture
    },
    success: function(data){
      //var t3 = performance.now();
      //console.log("Get EXIF execution " + (t3 - t2) + "ms.")
      console.log(data);
      return data['EV'];
    }
  });  
}

function set_exposure(exposure_time, iso, aperture){
  $.ajax({
    url: api_path + '/exposure',
    type: 'PUT',
    data: {
      'ExposureTime': exposure_time,
      'ISO': iso,
      'Aperture': aperture
    },
    success: function(data){
      //var t3 = performance.now();
      //console.log("Get EXIF execution " + (t3 - t2) + "ms.")
      console.log(data);
      return data['exposure_id'];
    }
  });   
}

function get_exposure(exp_id){
  $.ajax({
    url: api_path + '/exposure',
    type: 'GET',
    data: {
      'exposure_id': exp_id
    },
    success: function(data){
      //var t3 = performance.now();
      //console.log("Get EXIF execution " + (t3 - t2) + "ms.")
      console.log(data);
      return data;
    }
  });    
}

function calc_exposure_value(exposure_time, iso, aperture){
  $.ajax({
    url: api_path + '/ev',
    type: 'GET',
    data: {
      'ExposureTime': exposure_time,
      'ISO': iso,
      'Aperture': aperture
    },
    success: function(data){
      //var t3 = performance.now();
      //console.log("Get EXIF execution " + (t3 - t2) + "ms.")
      console.log(data);
      return data['EV'];
    }
  });
}

function exposure_value_byid(exp_id){
  $.ajax({
    url: api_path + '/ev_by_id',
    type: 'GET',
    data: "exposure_id="+exp_id,
    success: function(data){
      //var t3 = performance.now();
      //console.log("Get EXIF execution " + (t3 - t2) + "ms.")
      console.log(data);
      return data['EV'];
    }
  });
}

function aperture(exp_id, aperture){
  $.ajax({
    url: api_path + '/aperture',
    type: 'POST',
    data: {
      'exposure_id': exp_id,
      'Aperture': aperture
    },
    success: function(data){
      //var t3 = performance.now();
      //console.log("Get EXIF execution " + (t3 - t2) + "ms.")
      console.log(data);
      return data; //returns exposure settings
    }
  });
}

function exposure_time(exp_id, exp_time){
  $.ajax({
    url: api_path + '/exposure_time',
    type: 'POST',
    data: {
      'exposure_id': exp_id,
      'ExposureTime': exp_time
    },
    success: function(data){
      //var t3 = performance.now();
      //console.log("Get EXIF execution " + (t3 - t2) + "ms.")
      console.log(data);
      return data; //returns exposure settings
    }
  });
}

function iso(exp_id, iso, change){
  $.ajax({
    url: api_path + '/iso',
    type: 'POST',
    data: {
      'exposure_id': exp_id,
      'ISO': iso,
      'change': change
    },
    success: function(data){
      //var t3 = performance.now();
      //console.log("Get EXIF execution " + (t3 - t2) + "ms.")
      console.log(data);
      return data; //returns exposure settings
    }
  });
}

/*
ff_fl="50", orig_fl = "50", model="Nikon D750", sensor_size="FF", 
max_aperture = 20, min_aperture = 2.8, max_shutter_speed = 30, min_shutter_speed = 1/4000,
max_iso = 6400, min_iso = 100, max_fl = 70, min_fl = 28, multiplier=1
*/
function set_camera(camera){
    $.ajax({
    url: api_path + '/camera_config',
    type: 'PUT',
    data: camera,
    success: function(data){
      //var t3 = performance.now();
      //console.log("Get EXIF execution " + (t3 - t2) + "ms.")
      console.log(data);
      return data['camera_id']; //returns exposure settings
    }
  });
}

function get_camera(camera_id){

}

//wIP

$(function () {
    $('#fileupload').fileupload({
        dataType: 'json',
        done: function (e, data) {
            console.log(data['result']['image_id']);
            console.log("Get style.")
            image_id = data['result']['image_id']
            recommend_style(image_id);
            get_exif(image_id);

            // DISPLAY EXIF
        },

        progressall: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#progress .bar').css(
            'width',
            progress + '%'
        );
      }
    });
});

// CAMERA
$( '#camera_form' ).submit(function( event ) {
  /*
ff_fl="50", orig_fl = "50", model="Nikon D750", sensor_size="FF", 
        max_aperture = 20, min_aperture = 2.8, max_shutter_speed = 30, min_shutter_speed = 1/4000,
        max_iso = 6400, min_iso = 100, max_fl = 70, min_fl = 28, multiplier=1
  */
  event.preventDefault();
  form_status = check_form_filled('#camera_form');
  console.log(form_status);
  if(form_status){
    camera = {
    ff_fl: $('#ff_fl').val(),
    orig_fl: $('#orig_fl').val(),
    model: $('#model').val(),
    sensor_size: $('#sensor_size').val(),
    max_aperture: $('#max_aperture').val(),
    min_aperture: $('#min_aperture').val(),
    max_shutter_speed: $('#max_shutter_speed').val(),
    min_shutter_speed: $('#min_shutter_speed').val(),
    max_iso: $('#max_iso').val(),
    min_iso: $('#min_iso').val(),
    max_fl: $('#max_fl').val(),
    min_fl: $('#min_fl').val(),
    multiplier: $('#multiplier').val()

    }
    camera_id = set_camera(camera);
    $('#camera_sub_status').html('<br><span class="badge badge-pill badge-success">Submission Complete.</span>');
  }else{
    $('#camera_sub_status').html('<br><span class="badge badge-pill badge-danger">Form not complete.</span>')
  }
  

});

// check all exposure values set

function check_form_filled(elem){
  var isFilled = true;
  $(elem + ' input').each(function() {
    if($(this).val() === '' )
      isFilled = false;
  } );
  return isFilled;
}

// EXPOSURE WIP

$("#ExposureTime").change(function() {
  var exp_time = $('#ExposureTime').val();
  console.log(exp_time);
  if(check_form_filled('#exp_settings')){
    if(manual_mode){
      // just updated value.
    }
    console.log("Exp filled");
  }else{
    console.log(check_form_filled('#exp_settings'));
  }
});

$("#Aperture").change(function(){
  var f_no = $('#Aperture').val();
  console.log(f_no);
  if(check_form_filled('#exp_settings')){
    if(manual_mode){
      // just updated value.
    }
    console.log("Exp filled");
  }else{
    console.log(check_form_filled('#exp_settings'));
  }
});

$('#ISO').change(function(){
  var iso = $('#ISO').val();
  console.log(iso);
  if(check_form_filled('#exp_settings')){
    if(manual_mode){
      // just updated value.
    }
    console.log("Exp filled");
  }else{
    console.log(check_form_filled('#exp_settings'));
  }
});

$('#exp_clear').click(function(){
  exposure_id = -1;
  $('#exp_settings input').each(function(){
    $(this).val("");
  });
});

$('#manual_mode').change(function(){
  if(this.checked){
    manual_mode = true;
    $('#exposure_val').html("lol")
  }else{
    manual_mode = false;
    $('#exposure_val').html("no")
  }

});

