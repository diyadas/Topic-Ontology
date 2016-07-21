# -*- coding: utf-8 -*-
"""
Created on 21 Jul

@author: Diya

run_this will parse the Wikipedia xml file,
find all the non-redirect articles,
take a reproducible random subset of 10000 articles,
get the titles and text of these articles,
and return a pandas dataframe
"""

#import xml.etree.ElementTree as ET
from lxml import etree
import matplotlib.pyplot as plt
import numpy
import random
import pandas as pd

def xml_to_df(xmlname='enwiki-20160701-pages-articles-multistream.xml', nsample=100000):
    # converts MediaWiki xml to dataframe of indices, titles, and text 
    #root = parse_file(xmlname)
    indices = [int(index) for index in get_articles(xmlname)]
    random.seed(8685)
    indices = random.sample(indices,nsample)
    indices.sort()
    titles = get_titles(xmlname,indices)
    text = get_text(xmlname,indices)
    df = get_dataframe(indices,titles, text)
    return df

#def parse_file(filename):
#    tree = ET.parse(filename)
#    return tree.getroot()

def get_titles(xmlname,indices):
    return [root[i][0].text for i in indices ]

def get_articles(xmlname):
    indices = []
    for event, element in etree.iterparse(xmlname, tag="{http://www.mediawiki.org/xml/export-0.10/}page"):
        if element.find("{http://www.mediawiki.org/xml/export-0.10/}ns").text=='0':
            redirect = element.find('{http://www.mediawiki.org/xml/export-0.10/}redirect')
            if redirect is None:
                indices.append(element.find("{http://www.mediawiki.org/xml/export-0.10/}id").text) #yes, this will be a string corresponding to the id of the article
        element.clear()
    return indices

def get_text(root,article_indices):
    text = []
    for child in [root[i] for i in article_indices]:
        for textnode in child.iter(tag ='{http://www.mediawiki.org/xml/export-0.10/}text'):
            text.append(textnode.text)
    return text

def get_dataframe(indices, title_list, text_list):
    data=pd.DataFrame(index=len(indices), columns=['index','title', 'text'])
    data['index']=indices
    data['title']=title_list
    data['text']=text_list
    return data

"""A few additional functions to characterize the articles"""
def get_length(text):
    #to execute:
    #(char_count, log_char, word_count, log_word) = get_length(text)
    char_count = [len(a) for a in text]
    log_char = numpy.log10(char_count)
    word_count = [len(a.split()) for a in text]
    log_word = numpy.log10(word_count)
    plt.hist(log_word)
    plt.ylabel("Number articles")
    plt.xlabel("Log number words")
    return char_count, log_char, word_count, log_word
