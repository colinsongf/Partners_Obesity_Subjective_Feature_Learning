insert into patientdischarge.ml_train_sentiment_source_class_count
select 
	case name
		when 'Diabetes' then 0
		when 'Gout' then 1
		when 'CAD' then 2
		when 'Hypercholesterolemia' then 3
		when 'Depression' then 4
		when 'Venous Insufficiency' then 5
		when 'OSA' then 6
		when 'GERD' then 7
		when 'CHF' then 8
		when 'Hypertension' then 9
		when 'Hypertriglyceridemia' then 10
		when 'OA' then 11
		when 'PVD' then 12
		when 'Gallstones' then 13
		when 'Obesity' then 14
		when 'Asthma' then 15
	end as name,
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
			`trainids`.`ID`
		from
			`trainids`)
order by `rc`.`Name` desc