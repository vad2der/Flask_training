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
    
	var new_collection = {
		"name": $('#new_col_name').val(),
		"col_id": '',
		"poi_ids": '',
		};
	
	$.ajax({
		type: 'POST',
		url: '/api/collections/',
		data: new_collection,
		success: function(newCollection) {	  
			$collections.append('<option value="' + new_collection.name + '">' + new_collection.name + '</option>');
			$('#new_col_name').val("Enter new collection name..")
		},
		error: function() {
			alert('error saving collection');
		}  
	});  
 });
 })