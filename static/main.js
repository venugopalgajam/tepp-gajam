console.log('main.js is loading...')
tbl_div_ids = { '1': '#direct_div', '2': '#one_stop_div', '3': '#two_stops_div' }
tbl_ids = { '1': '#direct_tbl', '2': '#one_stop_tbl', '3': '#two_stops_tbl' }
names = {'1': 'direct_tbl', '2': 'one_stop_tbl', '3': 'two_stops_tbl'};
var cls_val,quota_val;
function reg_submit() {
	alert("we are running out of credits to get seat availability!! it will be back soon!!")
}
function date_format(date_obj) {
	var month = (date_obj.getMonth() + 1);
	var day = date_obj.getDate();
	if (month < 10)
		month = "0" + month;
	if (day < 10)
		day = "0" + day;
	return date_obj.getFullYear() + '-' + month + '-' + day;
}
seat_cache = {};
cnt = 0;
function seat_avail_cb(res){
	obj = JSON.parse(res);
	cells = $(obj["id"]).html(obj["avail"]);
	$(obj["id"]).attr('class','availed');
	if($('.avail').length==0){
		var tb = $('.table').DataTable({
			'retrieve':true,
			'bJQueryUI':true,
		});
		tb
		 .column( 1 ).search( 'VSKP' )
		 .draw();
		$('#search').prop('disabled',false);
	}
}
function load_seat_avails(){
	var cells = $(".avail");
	for (var i=0;i<cells.length;i++){
		if($(cells[i]).attr('class')==undefined)
			continue;
		var key = $(cells[i]).attr('class').substr(6);
		seat_cache[key] = "-1";
	}
	for(var key in seat_cache){
		cnt++;
		args = key.split('_');
		params = { jtrain:args[0],jsrc: args[1], jdst: args[2], jdate: args[3], jclass: cls_val,quota:quota_val }
		$.get('seatavail', params, seat_avail_cb)
	}
}
function load_table(response1) {
	response = JSON.parse(response1);
	tbl_id = response['type'];
	if(tbl_id=='1'){
		main = '<table class="table table-bordered table-hover table-striped table-condensed" id="'+names[tbl_id]+'">';
		main += '<thead><tr>';
		main += '<th>S.No.</th>';
		main += '<th>' + response['head'][0] + '<br>' + response['head'][1] + '</th>';
		main += '<th>' + response['head'][2] + '<br>' + response['head'][3] + '</th>';
		main += '<th>' + response['head'][4] + '<br>' + response['head'][5] + '</th>';
		main += '<th>SEAT AVAILABILITY</th>';
		main += '</tr></thead><tbody>';
		for(var j=0;j<response['body'].length;j++){
			header = '<tr><td></td>';
			header += '<td>' + response['body'][j][0] + '<br>' + response['body'][j][1] + '</td>';
			header += '<td>' + response['body'][j][2] + '<br>' + response['body'][j][3] + '</td>';
			header += '<td>' + response['body'][j][4] + '<br>' + response['body'][j][5] + '</td>';
			data = [response['body'][j][0],response['body'][j][2],response['body'][j][4],response['body'][j][3].substr(0,10)].join('_');
			header += '<td><span class="avail ' + data + '">loading...</span></td>';
			header += '</tr>';
			main += header;
		}
		main += '</tbody></table>';
	}

	else if(tbl_id=='2'){
		main = '<table class="table table-bordered table-hover table-striped table-condensed display compact" id="'+names[tbl_id]+'">';
		main += '<thead><tr>';
		main += '<th>S.No.</th>';
		main += '<th>' + response['head'][0] + '<br>' + response['head'][1] + '</th>';
		main += '<th>' + response['head'][2] + '<br>' + response['head'][3] + '</th>';
		main += '<th>' + response['head'][4] + '<br>' + response['head'][5] + '</th>';
		main += '<th>SEAT AVAILABILITY1</th>';
		main += '<th>' + response['head'][6] + '</th>';
		main += '<th>' + response['head'][7] + '<br>' + response['head'][8] + '</th>';
		main += '<th>' + response['head'][9] + '<br>' + response['head'][10] + '</th>';
		main += '<th>' + response['head'][11] + '<br>' + response['head'][12] + '</th>';
		main += '<th>SEAT AVAILABILITY2</th>';
		main += '</tr></thead><tbody>';
		for(var j=0;j<response['body'].length;j++){
			header = '<tr><td></td>';
			header += '<td>' + response['body'][j][0] + '<br>' + response['body'][j][1] + '</td>';
			header += '<td>' + response['body'][j][2] + '<br>' + response['body'][j][3] + '</td>';
			header += '<td>' + response['body'][j][4] + '<br>' + response['body'][j][5] + '</td>';
			data = [response['body'][j][0],response['body'][j][2],response['body'][j][4],response['body'][j][3].substr(0,10)].join('_');
			header += '<td><span class="avail ' + data + '">loading...</span></td>';
			header += '<td>' + response['body'][j][6] + '</td>';
			header += '<td>' + response['body'][j][7] + '<br>' + response['body'][j][8] + '</td>';
			header += '<td>' + response['body'][j][9] + '<br>' + response['body'][j][10] + '</td>';
			header += '<td>' + response['body'][j][11] + '<br>' + response['body'][j][12] + '</td>';
			data = [response['body'][j][7],response['body'][j][9],response['body'][j][11],response['body'][j][10].substr(0,10)].join('_');
			header += '<td><span class="avail ' + data + '">loading...</span></td>';
			header += '</tr>';
			main += header;
		}
		main += '</tbody></table>';
	}
		
	// main += "<input type='hidden' id='json_"+tbl_id+"' value='"+response1+"'>";
	$(tbl_div_ids[tbl_id]).html(main);
	load_seat_avails();
}
function query_submit() {
	$('#search').prop('disabled', true);
	$('#stxt').innerHTML = 'Searching..';
	src_val = $('#src').val();
	dst_val = $('#dst').val();
	jdate_val = $('#date').val();
	cls_val = $('#cls').val();
	quota_val = $('#quota').val();
	if (src_val.length == 0 || dst_val.length == 0 || jdate_val.length == 0) {
		window.alert('All fields are mandatory!!')
		$('#search').prop('disabled', false);
	}
	else {
		params = { src: src_val, dst: dst_val, jdate: jdate_val, cls: cls_val }
		$.get('direct_trains', params, load_table);
		$.get('one_stop', params, load_table);
		// $.get('two_stops', params.load_table)
		// $.get('get_paths', params, load_tables)
	}
}

$(document).ready(function () {
	var arp = 120;
	var today = date_format(new Date())
	var arpday = new Date((new Date()).getTime() + (arp * 24 * 60 * 60 * 1000));
	var maxday = date_format(arpday)
	$('#date').val(today);
	$("#date").attr("min", today);
	$('#date').attr("max", maxday);

	$('#src').autocomplete({
		source: stations,
		minLength: 2
	});

	$('#dst').autocomplete({
		source: stations,
		minLength: 2
	});
	console.log("stations are loaded:" + stations.length);
});
