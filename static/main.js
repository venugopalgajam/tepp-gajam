console.log('main.js is loading...')
tbl_div_ids = { '1': '#direct_div', '2': '#one_stop_div', '3': '#two_stops_div' }
tbl_ids = { '1': '#direct_tbl', '2': '#one_stop_tbl', '3': '#two_stops_tbl' }
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
function load_tables(response) {
	console.log('results are returned!');
	$('#results').html(response);
	$(document).ready(function () { $('#direct_tbl').DataTable(); });
	$(document).ready(function () { $('#one_stop_tbl').DataTable(); });
	// alert("we are running out of credits to get seat availability!! it will be back soon!!")
	$('#search').prop('disabled', false);
}
seat_cache = {};
cnt = 0;
function seat_avail_cb(res){
	// console.log(res)
	obj = JSON.parse(res);
	console.log(obj)
	cells = $(obj["id"]).html(obj["avail"]);
	$(obj["id"]).attr('class','availed')
	console.log(cells)
	// for ( var i=0 ; i< cells.length;i++){
	// 	$(cells[i]).html(res['avail'])
	// }
	if($('.avail').length==0){
		$(tbl_ids["1"]).DataTable();
		$(tbl_ids["2"]).DataTable();
		$(tbl_ids["3"]).DataTable();
		$('#search').prop('disabled',false);
	}
}
function load_seat_avails(){
	var cells =$(".avail")
	for (var i=0;i<cells.length;i++){
		console.log(cells[i])
		if($(cells[i]).attr('class')==undefined)
			continue;
		key = $(cells[i]).attr('class').substr(7)
		seat_cache[key] = "-1"
	}
	for(var key in seat_cache){
		cnt++;
		console.log(key)
		args = key.split('_')
		console.log(args)
		params = { jtrain:args[0],jsrc: args[1], jdst: args[2], jdate: args[3], jclass: cls_val,quota:quota_val }
		$.get('seatavail', params, seat_avail_cb)
	}
}
function load_table(response) {
	tbl_id = response.slice(0, 1)
	tbl = response.slice(2)
	console.log(tbl_id)
	// console.log(tbl)
	$(tbl_div_ids[tbl_id]).html(tbl)
	if(tbl_id=="2")load_seat_avails();
	// $(document).ready(function () { $(tbl_ids[tbl_id]).DataTable(); });
}
function query_submit() {
	$('#search').prop('disabled', true);
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
		$.get('direct_trains', params, load_table)
		$.get('one_stop', params, load_table)
		$.get('two_stops', params.load_table)
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
