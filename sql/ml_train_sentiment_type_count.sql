insert into patientdischarge.ml_train_sentiment_type_count
select 
	case 
		when ml.NameClass = 1 then 1
		else 17
	end as NameClass,
	ml.Sentiment,
	ml.Type,
	ml.Count
from ml_train_sentiment_type_count_classification_repository ml