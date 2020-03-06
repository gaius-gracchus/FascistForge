# -*- coding: UTF-8 -*-

"""Extracts all thread and comment data from a fascist website, stores in
Pandas DataFrames
"""

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os
import json

from selenium import webdriver
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

url_fmt = 'https://fascistforge.com/index.php?app=forums&module=forums&controller=topic&id={0}&page={1}&app=forums&module=forums&id={0}'
login_url = 'https://fascistforge.com/index.php?app=core&module=system&controller=login'


# I'm not sharing my username and password
username = os.getenv( 'FF_USERNAME' )
password = os.getenv( 'FF_PASSWORD' )

thread_output_file = '../data/thread_info'
comment_output_file = '../data/comment_info'

# Field extraction routines (kinda sloppy but they work)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def get_headline( dr ):
  return d['headline']

def get_date_created( d ):
  return d['dateCreated']

def get_author( d ):
  try:
    return int(d['author']['url'].split('=')[-1])
  except KeyError:
    return None
def get_start_page( d ):
  return d['pageStart']

def get_end_page( d ):
  return d['pageEnd']

def get_category( soup ):
  return soup.find('li', {'id' : 'elMobileBreadcrumb'}).get_text().replace('\n', '')

def get_comment_index( c ):
  return int(c['url'].split('=')[-1])

def get_comment_date_created( c ):
  return c['dateCreated']

def get_comment_author( c ):
  try:
    return int(c['author']['url'].split('=')[-1])
  except KeyError:
    return None

def get_comment_text( c ):
#   return c['text'].replace('\n', '').replace('\t', '')
  return c['text']

def get_comment_dict( index, c ):

  """Dict of information for a single comment
  """

  d = dict()
  d['thread_index'] = index
  d['comment_index'] = get_comment_index( c )
  d['author'] = get_comment_author( c )
  d['date'] = get_comment_date_created( c )
  d['text'] = get_comment_text( c )

  return d

def get_thread_dict( index, d, soup ):

  """Dict of information for a single thread, not including comments
  """

  di = dict()
  di['thread_index'] = index
  di['headline'] = get_headline( d )
  di['author'] = get_author( d )
  di['created'] = get_date_created( d )
  di['pages'] = get_end_page( d ) - get_start_page( d ) + 1
  di['category'] = get_category( soup )

  return di

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

if __name__ == '__main__':

  # initialize list of thread and comment dicts, respectively
  tdl = list()
  cdl = list()

  # login to website using credentials
  driver = webdriver.Chrome()
  driver.get(login_url)
  driver.find_element_by_id('auth').send_keys(username)
  driver.find_element_by_id('password').send_keys(password)
  driver.find_element_by_id('elSignIn_submit').click()

  # loop over all threads
  for idx in range(1, 1162):

    # load first page of thread and convert to BeautifulSoup
    driver.get(url_fmt.format(idx, 1))
    soup = BeautifulSoup( driver.page_source )

    if ( ('2F173' in str(soup)) or ('2membertools' in str( soup )) ):
      # error code, don't have permission to access page
      pass
    else:

      # load json into dict because it's way easier than parsing the html
      d = json.loads( soup.find('script', {'type' : 'application/ld+json'}).get_text() )

      # extract info fields for the given thread specified by `idx`, store in
      # list of thread dicts
      td = get_thread_dict( index = idx, d = d, soup = soup)
      tdl.append( td )

      # determine how many pages needed to loop over
      last_page = get_end_page( d )

      # loop over all pages of thread
      for page in range(1, last_page + 1):

        # load first page of thread and convert to BeautifulSoup
        driver.get(url_fmt.format(idx, page))
        soup = BeautifulSoup( driver.page_source )

        # load json into dict
        d = json.loads( soup.find('script', {'type' : 'application/ld+json'}).get_text() )
        try:
          # if type of post is not `question`, extract all comments, stores
          # fields in comment dict, stores comment dict in list of
          # comment dicts.
          comments = d['comment']
          for comment in comments:
            cdl.append( get_comment_dict( idx, comment))
        except KeyError:
          # if type of post is `question`, only extract top comment.
          #TODO figure out how to extract all answers, not just top answer.
          try:
            answer = d['acceptedAnswer']
            cdl.append( get_comment_dict( idx, answer))
          except KeyError:
            pass

  #----------------------------------------------------------------------------#

  # convert list of thread dicts into Pandas DataFrame and format it
  tdf = pd.DataFrame(tdl)

  # write thread DataFrame to pickle file
  tdf.to_pickle( thread_output_file + '.df' )
  tdf.to_csv( thread_output_file + '.csv', index = False )

  #----------------------------------------------------------------------------#

  # convert list of thread dicts into Pandas DataFrame and format it
  cdf = pd.DataFrame(cdl)

  # write thread DataFrame to pickle file
  cdf.to_pickle( comment_output_file + '.df' )
  cdf.to_csv( comment_output_file + '.csv', index = False )
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#