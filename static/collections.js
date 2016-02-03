$(function (){
    var $collections = $('#collections');
    // fill colections list
    var getCollectionNames = function() {
    $.ajax({
        type: 'GET',
	    url: '/api/collections/all',
	    success: function(collections) {
	    $('#collections').find('option').remove()
	    $collections.append('<option disabled selected>..select a collection..</option>'),
			$('#del-collection').hide(500);
	        $.each(collections, function (i, collection){
	            $collections.append('<option value="' + collection.name + '">' + collection.name + '</option>')
	        });
        },
        error: function() {
            alert('error loading collections');
        }
    });
  };
  $(window).load(getCollectionNames);
  //$('#collections').change(getCollectionNames);

// add a colleciton
    $('#add-collection').on('click', function() {
    
	    var new_collection = {
		    "name": $('#new_col_name').val(),
		    "col_id": '',
		    "poi_ids": '',
		};
	
	    $.ajax({
		    type: 'POST',
		    url: '/api/collections/'+new_collection,
		    data: new_collection,
		    success: function(newCollection) {
			    $collections.append('<option value="' + new_collection.name + '"selected>' + new_collection.name + '</option>');
			    $('#new_col_name').val("Enter new collection name..")
			    updatePOIList();
			    $('#new_poi').show(500);
		    },
		    error: function() {
			    alert('error saving collection');
		    }
	    });
    });
 
 // change poi_list on collection click
    var updatePOIList = function() {
		var the_collection = $('#collections').val();
		var $poi_list = $('#poi_list');
		var $poi_list_show = $('#poi_list_show');
		var index = 0;
		var nextIndex = function(){
			var newIndex = index + 1;
			return newIndex}
		var pointTemplate = "<tr>"+
			"<td>{{index}}</td>"+
			"<td>{{poi_name}}</td>"+
			"<td>{{lat}}</td>"+
			"<td>{{lng}}</td>"+
			"<td>{{type}}</td>"+
			"<td>{{subtype}}</td>"+
			"<th><button data-id='{{id}}'class='edit'>E</button></th>"+
			"<th><button data-id='{{id}}'class='remove'>D</button></th></tr>";
		
		$.ajax({  
			type: 'GET',
			url: '/api/pois/'+the_collection,
			success: function(pois) {
				//$('#poi_list').empty();
				//$poi_list.append(JSON.stringify(pois));
				$('#poi_list_show').empty();
				$poi_list_show.append('<tr><th>#</th><th>Name</th><th>Latitude</th><th>Longitude</th><th>Type</th><th>SubType</th><th>Edit</th><th>Delete</th></tr>');
				$.each(pois, function (i, poi){
					poi.index = i+1;
					$poi_list_show.append(Mustache.render(pointTemplate, poi));
				});
				setMapView(JSON.stringify(pois));
				$('#del-collection').show(500);
				$('#new_poi').show(500);
			},
			error: function() {
				alert('error loading pois from collection');
			}
		});
	};
	$('#collections').change(updatePOIList);

	// delete collection
	 var deleteCollection = function() {
	    var del_collection = {
		    name: $('#collections').val()
		};		
	    $.ajax({
		    type: 'DELETE',
		    url: '/api/collections/'+del_collection.name,
		    success: function() {
				getCollectionNames();
		    },
		    error: function() {
			    alert('error deleting collection');
		    }
	    });
    };
	$('#del-collection').click(deleteCollection);
	
    // add point
    var addPoint = function() {

	    var new_poi = {
	        "name": $('#new_col_name'),
	    }

	    $.ajax({
		    type: 'POST',
		    url: '',
		    data: new_poi,
		    success: function() {

		    },
		    error: function() {
			    alert('error adding point');
		    }
	    });
    };
	$('#add-poi').click(addPoint);
		
    // delete point
    var deletePoint = function() {

	    var new_poi = {
	        "name": $('#new_col_name'),
	    }

	    $.ajax({
		    type: 'DELETE',
		    url: 'api/pois'+$(this).attr('data-id'),
		    data: new_poi,
		    success: function() {

		    },
		    error: function() {
			    alert('error adding point');
		    }
	    });
    };
	$('.remove').click(deletePoint); 
 })