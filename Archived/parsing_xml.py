# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 15:17:53 2016

@author: Tristan

run_this will load the Wikipedia xml file as an ElementTree,
find all the non-redirect articles with at least 300 characters,
take a reproducible random subset of 10000 articles,
get the titles and text of these articles,
and return a pandas dataframe including position in the file
"""

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy
import random
import pandas as pd

def xml_to_df(xmlname='simplewiki-20160701-pages-articles-multistream.xml', nsample=10000):
    # converts MediaWiki xml to dataframe of indices, titles, and text 
    root = parse_file(xmlname)
    indices = get_articles(root)
    random.seed(8685)
    indices = random.sample(indices,nsample)
    indices.sort()
    titles = get_titles(root,indices)
    text = get_text(root,indices)
    df = get_dataframe(indices,titles, text)
    return df

def parse_file(filename):
    tree = ET.parse(filename)
    return tree.getroot()

def get_titles(root,indices):
    return [root[i][0].text for i in indices ]

def get_articles(root):
    indices = []
    for i in range(1,len(root.getchildren())):
        # Remove non-articles (ie help pages, categories, etc.)
        if root[i][1].text == "0":
            # Remove redirect articles
            redirect = root[i].find('{http://www.mediawiki.org/xml/export-0.10/}redirect')
            if redirect is None:
                # Remove articles with fewer than 300 characters
                # Yes, this does slow it down a lot.
                if( len(root[i].find('{http://www.mediawiki.org/xml/export-0.10/}revision').find('{http://www.mediawiki.org/xml/export-0.10/}text').text) >= 300 ):
                    indices.append(i)
    return indices

def get_text(root,article_indices):
    text = []
    for child in [root[i] for i in article_indices]:
        for textnode in child.iter(tag ='{http://www.mediawiki.org/xml/export-0.10/}text'):
            text.append(textnode.text)
    return text

def get_dataframe(indices, title_list, text_list):
    data=pd.DataFrame(index=range(10000), columns=['index','title', 'text'])
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
