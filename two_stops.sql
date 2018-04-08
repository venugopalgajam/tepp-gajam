
select train1.train_name as Train1,train1.train_name as Train1_name, hp1.stn_code Source1, date("2018-04-09") as hp1
from
(
	trains train1
	join hops hp1
		on train1.train_no = hp1.train_no 
        and (train1.jday & (1<<weekday(date("2018-04-09") + interval (1- hp1.day) day))) >0
        and hp1.stn_code="MUGR" 
        and train1.SL = '1'
	

	join hops hp2
		on train1.train_no = hp2.train_no 
		and hp2.stn_code in (Select stn_code from top_stns) 
		and hp1.hop_index < hp2.hop_index


    join trains train2
		on train2.SL='1'
	join hops as hp3
		on train2.train_no = hp3.train_no
        and hp3.stn_code = hp2.stn_code
        and 
        (
			((train2.jday & (1<<weekday(date("2018-04-09") + interval (hp2.sday- hp1.day) day))) >0 and hp3.dept_time > hp2.arr_time)
            or
            ((train2.jday & (1<<weekday(date("2018-04-09") + interval (hp2.sday- hp1.day+1) day))) >0 and hp3.dept_time < hp2.arr_time)
        )
	join hops as hp4
		on train2.train_no=hp4.train_no
        and hp4.stn_code in (select stn_code from top_stns)
        and hp4.hop_index > hp3.hop_index

    join trains train3
		on train3.SL='1'
	join hops as hp5
		on train3.train_no = hp5.train_no
        and hp5.stn_code = hp4.stn_code
        and
        (
			((train3.jday & (1<<weekday(date("2018-04-09") + interval (hp2.sday- hp1.day+1*(hp3.dept_time<hp2.arr_time)+hp4.sday-hp3.day) day))) >0 and hp5.dept_time > hp4.arr_time)
            or
            ((train2.jday & (1<<weekday(date("2018-04-09") + interval (hp2.sday- hp1.day+1*(hp3.dept_time<hp2.arr_time)+hp4.sday-hp3.day+1) day))) >0 and hp5.dept_time < hp4.arr_time)
		)
	join hops as hp6
		on train3.train_no=hp6.train_no
        and hp6.stn_code in (select stn_code from top_stns)
        and hp6.hop_index < hp5.hop_index
	
	
)
