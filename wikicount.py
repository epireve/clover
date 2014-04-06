# -*- coding: utf-8 -*-
import urllib2
import codecs
from scrapy.selector import Selector
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
import math
import json
from nltk.stem import WordNetLemmatizer
stopwords = nltk.corpus.stopwords.words('english')
tokenizer = RegexpTokenizer("[\w’]+", flags=re.UNICODE)
#st = LancasterStemmer()
wnl = WordNetLemmatizer()
keywords=[]
with open('keywords.txt','r') as f:
    for i in f:
        keywords.append(i.strip())    

with open('stopwords.txt','r') as f:
    for i in f:
        stopwords.append(i.strip())          
def freq(word, doc):
    return doc.count(word)
 
 
def word_count(doc):
    return len(doc)
 
 
def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))
    
 
def calcu_tf(keyword):
    url = "http://en.wikipedia.com/wiki/"+keyword
    content = urllib2.urlopen(url).read()

    vocabulary = []
 
    all_tips = []
    sel=Selector(text=content)
 
    #text="".join(sel.xpath('.//div[@id="mw-content-text"]/*[self::p or self::ul]//text()').extract())
    text="".join(sel.xpath('.//div[@id="mw-content-text"]//text()').extract())
    if text.find(keyword+' may refer to:') >=0 :
    #if text.find(keyword+' may refer to:') or text.find('Wikipedia does not have an article with this exact name') >=0 :
    #if text.find('Wikipedia does not have an article with this exact name') >=0 :
        return #[]
    tokens = tokenizer.tokenize(text)
 
    tokens = [token.lower() for token in tokens if len(token) > 2]
    tokens = [wnl.lemmatize(token)  for token in tokens if token not in stopwords]
 
   
    docs = { 'tf': {}, 'tokens': []}
    for token in tokens:
 
        docs['tf'][token] = tf(token, tokens)
 
    tops=sorted(docs['tf'].items(), key=lambda x: x[1], reverse=True)[:15]
    #print tops
    return [ i[0] for i in tops ]
      
       
 
 
 
        


 
with codecs.open('links.txt','ab+','utf-8') as f1:      
    with codecs.open('tf.json','ab+','utf-8') as f:  
        j=0
        for i in f :
            print i
            j+=1
        print j
        for keyword in keywords[j:] : 
                print "processing : %s "% keyword
                list=[]
                try:
                    list=calcu_tf(keyword)
                except urllib2.HTTPError, err:
                    if err.code == 404:
                        pass
                    else:
                        raise
                f.write(json.dumps({keyword:list})+'\n')
                f1.write("http://en.wikipedia.com/wiki/"+keyword+"\n")
                print json.dumps({keyword:list})
                #break
            
raw_input()
    