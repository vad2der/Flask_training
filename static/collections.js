$(function (){
  
  var $collections = $('#collections');
  
  $.ajax({  
    type: 'GET',
	url: '/api/collections',
	success: function(collections) {
	  $.each(collections, function (i, collection){
	    $collections.append('<option value="' + collection.name + '">' + collection.name + '</option>')
	});
  },
  error: function() {
    alert('error loading collections');
  }
  });
  
  $('#add-collection').on('click', function() {
    
	var new_collection_name = $('#new_col_name')
	
	$.ajax({
		type: 'POST',
		url: '/api/collections',
		data: new_collection_name,
		success: function(newCollection) {	  
			$collections.append('<option value="' + new_collection_name + '">' + new_collection_name + '</option>')
		},
		error: function() {
			alert('error saving collection');
		}  
	});  
 });
 })