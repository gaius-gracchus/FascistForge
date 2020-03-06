# -*- coding: UTF-8 -*-

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

from datetime import datetime as dt

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
plt.style.use('plotstyle')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def get_utc( s ):
  fmt = '%Y-%m-%dT%H:%M:%S%z'
  if s is None:
    return None
  else:
    return dt.strptime(s,fmt).timestamp()

def get_utc_user( s ):
  fmt = '%Y-%m-%dT%H:%M:%SZ'
  if s is None:
    return None
  else:
    return dt.strptime(s,fmt).timestamp()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

df_paths = [
  '../data/user_info.df',
  '../data/thread_info.df',
  '../data/comment_info.df' ]

names_list = [
  'New Users',
  'New Threads',
  'New Comments' ]

output_fname = 'activity.svg'

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

if __name__ == '__main__':

  # load in dataframes
  df_list = [pd.read_pickle( df_path ) for df_path in df_paths]

  # create ticks and ticklabels for x axis
  time_ticks = []
  time_ticklabels = []
  for year in [2018, 2019]:
      for month, monthname in zip( [3, 6, 9, 12], ['Mar', 'June', 'Sept', 'Dec'] ):
          time_ticks.append( dt( year, month, 1, 1, 1, 1).timestamp())
          time_ticklabels.append(f'{monthname} {year}')

  time_ticks = time_ticks[:-1]
  time_ticklabels = time_ticklabels[:-1]

  #----------------------------------------------------------------------------#

  # get timestamps for all activity
  times_list = [
    df_list[0]['joined'].apply( get_utc_user ),
    df_list[1]['created'].apply( get_utc ),
    df_list[2]['date'].apply( get_utc ) ]

  start_time = min( [np.min(time) for time in times_list] )
  stop_time = max( [np.max(time) for time in times_list])

  # one bin per week
  step = 60 * 60 * 24 * 7

  # generate array of bin edges and bin centers
  bins = np.arange(start_time, stop_time, step)
  bins_c = 0.5 * (bins[1:] + bins[:-1])

  hist_list = [np.histogram( time, bins = bins)[0] for time in times_list]
  hist_list = [a / np.max(a) for a in hist_list]

  fig, ax = plt.subplots()

  for hist, name in zip( hist_list, names_list):
    ax.plot(bins_c, hist, label = name)

  ax.set_xticks(time_ticks)
  ax.set_xticklabels(time_ticklabels)

  ax.set_xlim(start_time, time_ticks[-1])

  ax.set_ylabel('Normalized Weekly Activity')

  legend = ax.legend( loc = 1)
  legend.get_frame().set_linewidth(1.0)

  plt.tight_layout()
  plt.savefig(output_fname)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
