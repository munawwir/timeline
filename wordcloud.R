library(wordcloud)
library(RColorBrewer)
library(wordcloud2)
library(tm)
library(magrittr)
library(dplyr)
library(stringr)

set.seed(1234)

text <- readChar("57. Prophet Of Mercy By Shaykh Abul Hasan Ali Nadwi content.txt", file.info("57. Prophet Of Mercy By Shaykh Abul Hasan Ali Nadwi content.txt")$size)
text %<>% str_remove_all("https://nmusba.wordpress.com/")
text %<>% str_remove_all("PROPHET OF MERCY")
text %<>% str_remove_all("The Age of Ignorance")
text %<>% str_remove_all("Selection of Arabia for Prophethood")
text %<>% str_remove_all("Makkah Before the Prophet")
text %<>% str_remove_all("Makkah, The Prophet’s Birth Place")
text %<>% str_remove_all("From Birth to Prophethood")
text %<>% str_remove_all("The Dawn of Prophethood")
text %<>% str_remove_all("Yathrib before Islam")
text %<>% str_remove_all("In Madinah")
text %<>% str_remove_all("The Decisive Battle of Badr")
text %<>% str_remove_all("The Battle of Uhud")
text %<>% str_remove_all("The Battle of Trenches")
text %<>% str_remove_all("Action against Banu Qurayzah")
text %<>% str_remove_all("The Truce of Hudaybiyyah")
text %<>% str_remove_all("ibn")
text %<>% str_remove_all("abu")
text %<>% str_remove_all("httpsnmusbawordpresscom")
text %<>% str_remove_all("also")
text %<>% str_remove_all("vol")
# text %<>% str_remove_all("said")
# text %<>% str_remove_all("came")
text %<>% str_remove_all("‘")
text %<>% str_remove_all("’")
text %<>% str_remove_all("”")
text %<>% str_remove_all("“")
text %<>% str_remove_all("ing")
text %<>% str_remove_all("dhu")
text %<>% str_remove_all("ths")
test %<>% str_replace_all("Madlnah", "Madinah")

docs <- Corpus(VectorSource(text))

docs <- docs %>%
  tm_map(removeNumbers) %>%
  tm_map(removePunctuation) %>%
  tm_map(stripWhitespace)
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeWords, stopwords("english"))

dtm <- TermDocumentMatrix(docs) 
matrix <- as.matrix(dtm) 
words <- sort(rowSums(matrix),decreasing=TRUE) 
df <- data.frame(word = names(words),freq=words)

wordcloud(words = df$word, freq = df$freq, min.freq = 1, max.words=200, random.order=FALSE, rot.per=0.35, colors=brewer.pal(8, "Dark2"), scale=c(3,0.25))
wordcloud2(data=df, size=1, color='random-dark')
