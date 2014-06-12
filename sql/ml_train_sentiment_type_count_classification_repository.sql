insert into patientdischarge.ml_train_sentiment_type_count_classification_repository
select 
	dn.cname as name,
	b.Sentiment,
	b.Type,
	b.Count,
	concat(mld.cname, '-', mld.oppositeCname) as g
from
	(select 
	t.ID,
	mp.cname as Sentiment,
	mpt.cname as Type,
	count(*) as Count
from historywordposnormalized hwpn
join trainidtable t
	on hwpn.ID = t.ID
join subjectivelexicon sl
	on hwpn.Word = sl.Word and hwpn.PosNormalized = sl.Pos
join ml_polarity mp
	on mp.name = sl.priorpolarity
join ml_polaritytype mpt
	on mpt.name = sl.type
group by t.ID, sl.PriorPolarity, sl.Type) b
join recordclassification rc
	on b.ID = rc.ID and rc.Class = 'Y'
join ml_disease_name dn
	on rc.name = dn.name
join ml_disease_relationship mld
	on dn.cname = mld.cname or dn.cname = mld.oppositeCname