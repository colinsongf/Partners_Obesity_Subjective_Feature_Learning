insert into patientdischarge.ml_polarity
select 
	name,
	@rowid:=@rowid+1 as cname
	from 
(select 
distinct 
	priorpolarity as name
from subjectivelexicon) b, (select @rowid:=0) as init