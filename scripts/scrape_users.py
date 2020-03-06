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

url_fmt = 'https://fascistforge.com/index.php?app=core&module=members&controller=profile&id={}'
login_url = 'https://fascistforge.com/index.php?app=core&module=system&controller=login'

# I'm not sharing my username and password
username = os.getenv( 'FF_USERNAME' )
password = os.getenv( 'FF_PASSWORD' )

output_file = '../data/user_info'

# Field extraction routines (kinda sloppy but they work)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def get_name( soup ):
  return soup.find('h1', {'class' : 'ipsType_reset ipsPageHead_barText'}).get_text().replace('\n', '').replace( '\t', '')

def get_rep( soup ):
  return int(soup.find('span', {'class' : 'cProfileRepScore_points'}).get_text() )

def get_content_count( soup ):
  return int(soup.find_all('ul', {'class' : 'ipsList_inline ipsPos_left'})[0].find_all('li')[0].get_text().replace('\n', '').replace('\t', '').replace('Content Count', ''))

def get_joined( soup ):
  return soup.find_all('ul', {'class' : 'ipsList_inline ipsPos_left'})[0].find_all('li')[1].find('time')['datetime']

def get_last_visit( soup ):
  try:
    return soup.find_all('ul', {'class' : 'ipsList_inline ipsPos_left'})[0].find_all('li')[2].find('time')['datetime']
  except TypeError:
    return None

def get_days_won( soup ):
  try:
    return int(soup.find_all('ul', {'class' : 'ipsList_inline ipsPos_left'})[0].find_all('li')[3].get_text().replace('\n', '').replace('\t', '').replace('Days Won', ''))
  except IndexError:
    return 0

def get_followers( soup ):
  fa = soup.find_all('h2', {'class' : 'ipsWidget_title ipsType_reset'})
  if len(fa) == 4:
    return int(fa[0].get_text().replace('\n', '').replace('\t', '').replace('Followers', '').replace('Follower', ''))
  else:
    return 0

def get_age( soup ):
  fa = soup.find_all('div', {'class' : 'ipsWidget ipsWidget_vertical cProfileSidebarBlock ipsBox ipsSpacer_bottom'})
  if len( fa ) < 3:
    return None
  elif len( fa ) == 3:
    idx = 1
  else:
    idx = 2
  fa1 = fa[idx].find_all('div', {'class' : 'ipsDataItem_generic'})
  if len( fa1 ) == 2:
    return None
  else:
    return fa1[0].get_text().replace('\n', '').replace('\t', '')

def get_location( soup ):
  fa = soup.find_all('div', {'class' : 'ipsWidget ipsWidget_vertical cProfileSidebarBlock ipsBox ipsSpacer_bottom'})
  if len( fa ) < 3:
    return None
  elif len( fa ) == 3:
    idx = 1
  else:
    idx = 2
  fa1 = fa[idx].find_all('div', {'class' : 'ipsDataItem_generic'})
  if len( fa1 ) == 2:
    return None
  else:
    return fa1[1].get_text().replace('\n', '').replace('\t', '')

def get_ideology( soup ):
  fa = soup.find_all('div', {'class' : 'ipsWidget ipsWidget_vertical cProfileSidebarBlock ipsBox ipsSpacer_bottom'})
  if len( fa ) < 3:
    return None
  elif len( fa ) == 3:
    idx = 1
  else:
    idx = 2
  fa1 = fa[idx].find_all('div', {'class' : 'ipsDataItem_generic'})
  if len( fa1 ) == 2:
    return fa1[0].get_text().replace('\n', '').replace('\t', '')
  else:
    return fa1[2].get_text().replace('\n', '').replace('\t', '')

def get_religion( soup ):
  fa = soup.find_all('div', {'class' : 'ipsWidget ipsWidget_vertical cProfileSidebarBlock ipsBox ipsSpacer_bottom'})
  if len( fa ) < 3:
    return None
  elif len( fa ) == 3:
    idx = 1
  else:
    idx = 2
  fa1 = fa[idx].find_all('div', {'class' : 'ipsDataItem_generic'})
  if len( fa1 ) == 2:
    return fa1[1].get_text().replace('\n', '').replace('\t', '')
  else:
      return fa1[3].get_text().replace('\n', '').replace('\t', '')

def get_rank( soup ):
  return soup.find('span', {'class' : 'ipsPageHead_barText'}).get_text().replace('\n', '').replace('\t', '')

def get_cover_photo( soup ):
  return soup.find('div', {'class' : 'ipsCoverPhoto_container'}).find('img')['src']

def get_profile_photo( soup ):
  f = soup.find('div', {'class' : 'ipsColumn ipsColumn_fixed ipsColumn_narrow ipsPos_center'}).find('a')
  if f is None:
    return soup.find('div', {'class' : 'ipsColumn ipsColumn_fixed ipsColumn_narrow ipsPos_center'}).find('img')['src']
  else:
    return f['href']

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def get_dict( index, soup ):

  """Combine all field extraction routines into single function
  """

  d = dict( )
  d['user_index'] = index
  d['name'] = get_name( soup )
  d['rep'] = get_rep( soup )
  d['content_count'] = get_content_count( soup )
  d['joined'] = get_joined( soup )
  d['last_visit'] = get_last_visit( soup )
  d['days_won'] = get_days_won( soup )
  d['followers'] = get_followers( soup )
  d['age'] = get_age( soup )
  d['location'] = get_location( soup )
  d['ideology'] = get_ideology( soup )
  d['religion'] = get_religion( soup )
  d['rank'] = get_rank( soup )
  d['cover_photo'] = get_cover_photo( soup )
  d['profile_photo'] = get_profile_photo( soup )

  return d

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

if __name__ == '__main__':

  #----------------------------------------------------------------------------#

  # initialize list of user dicts
  dl = list()

  # login to website using credentials
  driver = webdriver.Chrome()
  driver.get(login_url)
  driver.find_element_by_id('auth').send_keys(username)
  driver.find_element_by_id('password').send_keys(password)
  driver.find_element_by_id('elSignIn_submit').click()

  # loop over all users
  for idx in range(1, 1152):

    # load website and convert to BeautifulSoup
    driver.get(url_fmt.format(idx))
    print(driver.status)
    soup = BeautifulSoup( driver.page_source )

    if ( ('2C138/1' in str(soup)) or ('2membertools' in str( soup )) ):
      # error code, user cannot be found, or member-only access
      pass
    else:
      # extract user fields and store in user dict, store user dict in
      # list of user dicts
      d = get_dict( index = idx, soup = soup)
      dl.append( d )

  #----------------------------------------------------------------------------#

  # convert list of user dicts into Pandas DataFrame and format it
  df = pd.DataFrame(dl)

  # write dataframe to pickle file
  df.to_pickle( output_file + '.df' )
  df.to_csv( output_file + '.csv', index = False )

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#