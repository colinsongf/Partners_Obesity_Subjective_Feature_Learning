insert into patientdischarge.ml_polaritytype
select 
	name,
	@rowid:=@rowid+1 as cname
	from 
(select 
distinct 
	concat(type) as name
from subjectivelexicon) b, (select @rowid:=0) as init