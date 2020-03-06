# -*- coding: UTF-8 -*-

"""Extracts all user data from a fascist website, stores in Pandas DataFrame
"""

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os

from selenium import webdriver
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

url_fmt = 'https://fascistforge.com/index.php?app=forums&module=forums&controller=topic&id={}&do=showReactionsComment&comment={}'
login_url = 'https://fascistforge.com/index.php?app=core&module=system&controller=login'

# I'm not sharing my username and password
username = os.getenv( 'FF_USERNAME' )
password = os.getenv( 'FF_PASSWORD' )

output_file = '../data/reaction_info'

# dict mapping image url to reaction name
reaction_dict = {
 'https://fascistforge.com/uploads/reactions/swastikaWhite300x300.png': 'Like',
 'https://fascistforge.com/uploads/reactions/gas.png': 'Gas',
 'https://fascistforge.com/uploads/reactions/Antifascist300x300.png': 'Anti-Fascist',
 'https://fascistforge.com/uploads/reactions/60704641_Mason1.png': 'Mason +1',
 'https://fascistforge.com/uploads/reactions/shlomo(300x257).png': 'Shlomo',
 'https://fascistforge.com/uploads/reactions/SneakyNazi(300x300).png': 'Sneaky Nazi',
 'https://fascistforge.com/uploads/reactions/RockwellThumbingNose.png': 'Rockwell Salute',
 'https://fascistforge.com/uploads/reactions/hitlerthumbsup.png': 'Hitler Approves'}

# Field extraction routines (kinda sloppy but they work)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_reactors( fa ):
  return [ float(f.find('a', {'class' : 'ipsUserPhoto ipsUserPhoto_mini'})['href'].split('=')[-1]) for f in fa]

def get_reactions( fa ):
  return [reaction_dict[f.find_all('img')[1]['src']] for f in fa]

def get_reaction_info( soup ):

  d = dict( )
  fa = (soup.find('section', {'class' : 'ipsTabs_panels'}).find_all('li', {'class' : 'ipsGrid_span6 ipsPhotoPanel ipsPhotoPanel_mini ipsClearfix'}))

  return get_reactors( fa ), get_reactions( fa )

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

if __name__ == '__main__':

  #----------------------------------------------------------------------------#

  # read in thread info DataFrame
  df = pd.read_pickle('data/comment_info.df')

  # login to website using credentials
  driver = webdriver.Chrome()
  driver.get(login_url)
  driver.find_element_by_id('auth').send_keys(username)
  driver.find_element_by_id('password').send_keys(password)
  driver.find_element_by_id('elSignIn_submit').click()

  # initialize field lists
  author_list = []
  cidx_list = []
  tidx_list = []
  reactor_list = []
  reaction_list = []

  # loop over all comments
  for author, cidx, tidx in zip( df['author'], df['comment_index'], df['thread_index']):

    # load page containing reaction data
    reaction_url = url_fmt.format(tidx, cidx)
    driver.get( reaction_url )

    # read html from page into BeautifulSoup
    soup = BeautifulSoup( driver.page_source )

    # extract info from page, store in lists
    reactors, reactions = get_reaction_info( soup )
    N = len( reactors )

    author_list.extend( [author] * N )
    cidx_list.extend( [cidx] * N )
    tidx_list.extend( [tidx] * N )
    reactor_list.extend(reactors)
    reaction_list.extend(reactions)

  # put all field lists into DataFrame
  rdf = pd.DataFrame()
  rdf['thread_index'] = tidx_list
  rdf['comment_index'] = cidx_list
  rdf['author'] = author_list
  rdf['reactor'] = reactor_list
  rdf['reaction'] = reaction_list

  #----------------------------------------------------------------------------#

  # write dataframe to pickle file
  rdf.to_pickle( output_file + '.df' )
  rdf.to_csv( output_file + '.csv', index = False )

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#