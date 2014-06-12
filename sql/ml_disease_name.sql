insert into patientdischarge.ml_disease_name
select 
	name,
	@rowid:=@rowid+1 as cname
from
(select distinct 
	name
from recordclassification
union
select distinct 
	concat('Not ', name) as name
from recordclassification) b, (select @rowid:=0) as init