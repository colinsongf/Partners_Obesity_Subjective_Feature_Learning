
select hwpn.ID, sl.PriorPolarity, sl.Type, count(*)
from historywordposnormalized hwpn
join trainidtable t
	on hwpn.ID = t.ID
join subjectivelexicon sl
	on hwpn.Word = sl.Word and hwpn.PosNormalized = sl.Pos
group by ID, sl.PriorPolarity, sl.Type


select hwpn.ID, sl.PriorPolarity, sl.Type, count(*)
from historywordposnormalized hwpn
join testidtable t
	on hwpn.ID = t.ID
join subjectivelexicon sl
	on hwpn.Word = sl.Word and hwpn.PosNormalized = sl.Pos
group by ID, sl.PriorPolarity, sl.Type