insert into patientdischarge.ml_test_sentiment_source_class_count
select 
	sp.ID,
	case sentiment
		when 'positive' then 0
		when 'negative' then 1
		when 'neutral' then 2
		when 'both' then 3 
	end as 'Sentiment',
	case source
		when 'intuitive' then 0
		when 'textual' then 1
	end as Source,
	case class
		when 'Y' then 0
		when 'N' then 1
		when 'U' then 2
		when 'Q' then 3
	end as Class,
	sp.Count
from
	(`sentimentparagraph` `sp`
	join `recordclassification` `rc` ON ((`sp`.`ID` = `rc`.`ID`)))
where
	`sp`.`ID` in (select 
			`testids`.`ID`
		from
			`testids`)
order by `rc`.`Name` desc