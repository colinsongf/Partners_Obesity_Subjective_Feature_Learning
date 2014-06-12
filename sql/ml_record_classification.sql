insert into patientdischarge.ml_record_classification
select distinct
	rc.ID,
	rc.Name,
	dn.CName
from recordclassification rc
join ml_disease_name dn
	on rc.name = dn.name
where rc.class = 'Y'
order by ID