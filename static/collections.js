$(function (){
    var $collections = $('#collections');
    // fill colections list
    var getCollectionNames = function() {
    $.ajax({
        type: 'GET',
	    url: '/api/collections',
	    success: function(collections) {
	    $('#collections').find('option').remove()
	    $collections.append('<option disabled selected>..select a collection..</option>'),
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
		    url: '/api/collections/',
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
		
		$.ajax({  
			type: 'GET',
			url: '/api/pois/'+the_collection,
			success: function(pois) {
				$('#poi_list').empty();
				$poi_list.append(JSON.stringify(pois));
				$('#poi_list_show').empty();
				$poi_list_show.append('<tr><th>#</th><th>Name</th><th>longitude</th><th>Latitude</th><th>Type</th><th>SubType</th></tr>');
				$.each(pois, function (i, poi){					
					$poi_list_show.append('<tr>><td>'+i+'</td><td>'+poi.poi_name+'</td><td>'+poi.lng+'</td><td>'+poi.lat+'</td><td>'+poi.type+'</td><td>'+poi.subtype+'</td></tr>')
				});
				initMap(JSON.stringify(pois));
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
	 $('#del-collection').click('click', function() {

	    var del_collection_name = $('#new_col_name');

	    $.ajax({
		    type: 'DELETE',
		    url: '/api/collections/',
		    success: function() {

		    },
		    error: function() {
			    alert('error deleting collection');
		    }
	    });
    });

    // add point
    $('#del-poi').on('click', function() {

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
    });
 })