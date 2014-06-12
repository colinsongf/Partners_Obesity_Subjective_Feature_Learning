insert into patientdischarge.ml_test_sentiment_type_count
select 
	t.ID,
	mp.cname as Sentiment,
	mpt.cname as Type,
	count(*) as Count
from historywordposnormalized hwpn
join testidtable t
	on hwpn.ID = t.ID
join subjectivelexicon sl
	on hwpn.Word = sl.Word and hwpn.PosNormalized = sl.Pos
join ml_polarity mp
	on mp.name = sl.priorpolarity
join ml_polaritytype mpt
	on mpt.name = sl.type
group by t.ID, sl.PriorPolarity, sl.Type