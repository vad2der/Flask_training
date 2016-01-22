$(function (){
  
  var $collections = $('#collections');
  var $col_id = $('#col_id');
  
  $.ajax({
  
    type: 'GET',
	url: '/api/collections',
	success: function(collections) {
	  $.each(collections, function (i, collection){
	    $collections.append('<option>' + collection.name+'</option>')
	});
  },
  error: function() {
    alert('error loading collections');
  }
  });
  
 });