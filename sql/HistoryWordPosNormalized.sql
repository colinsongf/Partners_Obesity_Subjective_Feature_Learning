insert into patientdischarge.historywordposnormalized
select
	ID,
	SentenceID,
	Word,
	Pos,
	case
		when Pos = 'JJ' or Pos = 'JJS' or Pos = 'JJR' then 'adj' 
		when Pos = 'NN' or Pos = 'NNP' or Pos = 'NNPS' or Pos = 'NNS' then 'noun'
		when Pos = 'VB' or Pos = 'VBD' or Pos = 'VBG' or Pos = 'VBN' or Pos = 'VBP' or Pos = 'VBZ' then 'verb'
		when Pos = 'RB' or Pos = 'RBR' or Pos = 'RBS' then 'adverb'
		else 'none' end as NormalizedPos
	from historywordpos

