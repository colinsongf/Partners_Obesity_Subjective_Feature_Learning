diagnosis = read.table("../data/classifications.txt",header=TRUE,sep=",")
dim(diagnosis)
table(diagnosis[,1:2])
6451/727
ttt = table(diagnosis[,1:2])
ttt
cor(ttt)
barplot(t(ttt),beside=TRUE,cex.names=.55,main="Diagnoses Data",col=c(4,2));grid(col=1)


classes = read.table("../data/classes.txt",header=TRUE)
plot(hclust(dist(t(classes)),method="complete"))

