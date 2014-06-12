sentimentSourceClassCount = {
	"train": "select * from patientdischarge.ml_train_sentiment_source_class_count",
	"test": "select * from patientdischarge.ml_test_sentiment_source_class_count",
	"result": ("insert into patientdischarge.ml_result_sentiment_source_class_count(ID, Name) "
				"values (%s, %s)")
}

sentimentTypeCount = {
	"train": "select * from patientdischarge.ml_train_sentiment_type_count",
	"test": "select * from patientdischarge.ml_test_sentiment_type_count",
	"result": ("insert into patientdischarge.ml_result_sentiment_type_count(ID, NameClass, ClassGroup) "
				"values (%s, %s, '-')")
}