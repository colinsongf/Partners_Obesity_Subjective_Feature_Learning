insert into patientdischarge.ml_disease_relationship
select 
	dn2.cname,
	dn1.cname
from
(select distinct 
	name,
	name as unKey
from recordclassification
union
select distinct 
	concat('Not ', name) as name,
	name as unKey
from recordclassification) b
join ml_disease_name dn1
	on b.name = dn1.name
join ml_disease_name dn2
	on b.unKey = dn2.name
where b.name != b.unKey