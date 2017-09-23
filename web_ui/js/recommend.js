var api_path = 'http://127.0.0.1:5002'

function recommend_style(image_id){
  $.ajax({
    url: api_path + '/recommend_style',
    type: 'GET',
    data: "image_id="+image_id,
    success: function(data){
      console.log(data);
    }
  });
}

//recommend functions
function rec_settings_wo_image(){}

function rec_settings_w_image(style, image_id){}

function recommend_filter(){}

// dof calc functions
function calc_dof(f_no, fl, coc, subj_dist){
  $.ajax({
    url: api_path + '/calc_dof',
    type: 'GET',
    data: {
      'Aperture':f_no,
      'FocalLength':fl,
      'coc':coc,
      'SubjDist':subj_dist},
    dataType: 'json',
    success: function(data){
      console.log(data);
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
  $.ajax({
    url: api_path + '/get_exif',
    type: 'GET',
    data: "image_id="+image_id,
    success: function(data){
      console.log(data);
    }
  });

}

// exposure functions
function manual_exposure(){}

function exposure(){}

function exposure_value(){}

function exposure_value_byid(){}

function aperture(){}

function exposure_time(){}

function iso(){}





$(function () {
    $('#fileupload').fileupload({
        dataType: 'json',
        done: function (e, data) {
            console.log(data['result']['image_id']);
            console.log("Get style.")
            recommend_style(data['result']['image_id']);
            get_exif(data['result']['image_id']);

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