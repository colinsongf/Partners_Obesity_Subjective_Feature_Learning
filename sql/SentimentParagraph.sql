insert into patientdischarge.sentimentparagraph
select ID, count(*), sl.PriorPolarity
from historywordposnormalized hwpn
join subjectivelexicon sl
	on hwpn.Word = sl.Word and hwpn.PosNormalized = sl.Pos
group by ID, sl.PriorPolarity
order by count(*) desc