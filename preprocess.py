import string
import nltk
import csv
import re
import demoji

class preprocess():
    def __init__(self, df, contractions):
        self.df = df
        self.contractions = contractions
    
    def abbreviate(self, tweet):
        tweet = tweet.split(' ')
        j = 0
        for str_ in tweet:
            fileName = '/content/drive/My Drive/Covid 19 India/Abbreviations.txt'
            accessMode = 'r'
            with open(fileName, accessMode) as csvfile:
                dataFromFile = csv.reader(csvfile, delimiter = '=')
                str_ = re.sub('[^a-zA-Z0-9-_.]', '', str_)
                for row in dataFromFile:
                    if str_.upper() == row[0]:
                        tweet[j] = row[1]
                csvfile.close()
            j += 1
        return ' '.join(tweet)
    
    def expand(self, tweet):
        for word in tweet.split():
            if word in self.contractions.keys():
                tweet = tweet.replace(word, self.contractions[word])
        return tweet
    
    def emoji2text(self, tweet):
        emojis = demoji.findall(tweet)
        new_tweet = []
        for word in tweet.split():
            if word in emojis.keys():
                tweet = tweet.replace(word, emojis[word])
                new_tweet.append(emojis[word])
            wordmojis = demoji.findall(word)
            for char in word:
                if char in wordmojis.keys():
                    tweet = tweet.replace(word, wordmojis[char])
        
        return tweet
    
    def normalize(self, tweet):
        lem = WordNetLemmatizer()
        normalized_tweet = []
        for word in tweet.split():
            normalized_text = lem.lemmatize(word, 'v')
            normalized_tweet.append(normalized_text)
        return ' '.join(normalized_tweet)

    def remove_mentions(self, tweet):
        return re.sub(r'\@w+', '', tweet)
    
    def remove_hashtag(self, tweet):
        return re.sub(r'\#w+', '', tweet)

    def remove_punctuations(self, tweet):
        punct = string.punctuation
        trantab = str.maketrans(punct, len(punct)*' ')
        return tweet.translate(trantab)
    
    def preprocess_tweet(self, tweet):
        tweet = self.abbreviate(tweet)
        tweet = self.expand(tweet)
        tweet = self.emoji2text(tweet)
        tweet = self.normalize(tweet)
        tweet = self.remove_mentions(tweet)
        tweet = self.remove_hashtag(tweet)
        tweet = self.remove_punctuations(tweet)
        return tweet
