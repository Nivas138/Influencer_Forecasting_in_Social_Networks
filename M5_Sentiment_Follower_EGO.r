setwd('C:\\Users\\Nivas\\')
getwd()
#install.packages("ggplot2")
#install.packages("tm")
#install.packages("wordcloud")
#install.packages("syuzhet")
#install.packages('SnowballC')
#?tm

library(SnowballC)
library(ggplot2)
library(tm)
library(wordcloud)
library(syuzhet)
#texts = readLines("_chat.txt")
texts=read.csv("m5_follower_max_text.csv")
print(texts)
#text<-rm(texts$X0)
docs = Corpus(VectorSource(texts$STOP.EVERYTHING....I.have.an.update........ahhhhh..alopecia..growingback.ðY.OðY..ðY.OðY..ðY.SðY.SðY.SðY.S.https...t.co.2AnXOKsIlt.https...t.co.rkpLl5vrpl ))
docs

trans=content_transformer(function(x,pattern) gsub(pattern," ",x))
trans
docs=tm_map(docs,trans,"/")
docs=tm_map(docs,trans,"@")
docs=tm_map(docs,trans,"\\|")
docs=tm_map(docs,content_transformer(tolower))
docs=tm_map(docs,removeNumbers)
docs=tm_map(docs,removeWords,stopwords("english"))
docs=tm_map(docs,removePunctuation)
docs=tm_map(docs,stripWhitespace)
docs=tm_map(docs,stemDocument)

docs

dtm=TermDocumentMatrix(docs)
dtm
mat=as.matrix(dtm)
mat

v=sort(rowSums(mat),decreasing=TRUE)
print(v)


d = data.frame(word=names(v),freq=v)
head(d)
set.seed(1056)
#wordcloud(words=d$word,freq=d$freq,min.freq=1,max.words=200,random.order=TRUE,
#rot.per=0.45,colors=brewer.pal(8,"Dark2"))
#type.convert(text)
#?get_nrc_sentiment
texts<-as.character(texts$STOP.EVERYTHING....I.have.an.update........ahhhhh..alopecia..growingback.ðY.OðY..ðY.OðY..ðY.SðY.SðY.SðY.S.https...t.co.2AnXOKsIlt.https...t.co.rkpLl5vrpl )
sentiment=get_nrc_sentiment(texts)
print(sentiment)
text=cbind(texts,sentiment)
head(text)
TotalSentiment = data.frame(colSums(text[,c(2:11)])) 
TotalSentiment

names(TotalSentiment)="count"
TotalSentiment=cbind("sentiment" = rownames(TotalSentiment),TotalSentiment)
print(TotalSentiment)
rownames(TotalSentiment)
ggplot(data=TotalSentiment, aes(x = sentiment,y=count)) + geom_bar(aes(fill=sentiment),stat="identity")+theme(legend.position="none")+xlab("Tweet Analysis")+ylab("Total Count")+ggtitle("Total Tweet Analysis Score - follower Influencer")

