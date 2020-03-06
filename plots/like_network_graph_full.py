# -*- coding: UTF-8 -*-

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

from collections import Counter
import random

import pandas as pd
import numpy as np
import networkx as nx

import holoviews as hv
from holoviews import opts
from holoviews.operation.datashader import datashade, bundle_graph

from bokeh.io import show, output_file

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# input Pandas DataFrames
reaction_df_path = '../data/reaction_info.df'
user_df_path = '../data/user_info.df'

# output html document
output_fpath = 'bundled_like_graph'

# if user has less than `thr` likes, or has been liked less than `thr` times,
# user is not considered
thr = 0

# random seed for networkx graph layout
seed = 1312
random.seed(seed)
np.random.seed(seed)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

if __name__ == '__main__':

  # load in reaction data, convert user indices to integer
  df = pd.read_pickle(reaction_df_path)
  df['author'] = df['author'].apply(int)
  df['reactor'] = df['reactor'].apply(int)

  # load in user data, create dict that maps user index to username
  udf = pd.read_pickle(user_df_path)
  udf = udf[['user_index', 'name']]
  udf = udf.dropna()
  user_dict = dict(zip(udf['user_index'], udf['name']))

  # filter entries in reaction dataframe
  #----------------------------------------------------------------------------#

  # only looking at Likes (swastikas)
  ldf = df[df['reaction'] == 'Like']
  authors = Counter(ldf['author'])
  reactors = Counter(ldf['reactor'])

  # # filter users with less than `thr` likes
  # authors = {k:v for k, v in authors.items() if v > thr}
  # reactors = {k:v for k, v in reactors.items() if v > thr}

  # # propagate user filter to dataframe
  users = set(authors.keys()) | set(reactors.keys())
  print(len(users))
  # ldf = ldf[((ldf['author'].isin(users)) & (ldf['reactor'].isin(users)))]

  # get lists of user numbers and usernames: some usernames are nans so ignore those.
  usernames = []
  usernums = []
  for user in users:
    try:
      usernames.append(user_dict[user])
      usernums.append(user)
    except KeyError:
      pass

  ldf = ldf[((ldf['author'].isin(usernums)) & (ldf['reactor'].isin(usernums)))]

  edge_dict = dict()
  for author, reactor in zip(ldf['author'], ldf['reactor']):
    t = ( author, reactor)
    if t in edge_dict.keys():
      edge_dict[t] += 1
    else:
      edge_dict[t] = 1

  # create list of weighted edge tuples
  edges = [(k[0], k[1], v) for k, v in edge_dict.items() ]

  # initialize networkx graph
  G = nx.Graph()
  for user, username in zip(users, usernames):
    G.add_node(user, name = str(username), user_index = str(user))
  G.add_weighted_edges_from(edges)

  # configure holoviews
  #----------------------------------------------------------------------------#

  hv.extension('bokeh')
  renderer = hv.renderer('bokeh')

  kwargs = dict(width=800, height=800, xaxis=None, yaxis=None)
  opts.defaults(opts.Nodes(**kwargs), opts.Graph(**kwargs))

  # create filtered DataFrames
  #----------------------------------------------------------------------------#

  pos = nx.spring_layout( G )

  nl = []
  for k, v in pos.items():
    try:
      d = dict()
      d['x'] = v[0]
      d['y'] = v[1]
      d['user index'] = k
      d['username'] = user_dict[k]
      d['log degree'] = np.log10(df[((df['author'] == k) | (df['reactor'] == k))].shape[0])
      nl.append(d)
    except KeyError:
      print(k, v)

  ndf = pd.DataFrame(nl)
  ndf = ndf[['x', 'y', 'user index', 'username', 'log degree']]
  ndf = ndf[((ndf['user index'] != 299) & (ndf['user index'] != 680) & (ndf['user index'] != 373))]
  el = []
  for u, v, w in edges:
    d = dict()
    d['start'] = u
    d['stop'] = v
  #   d['weight'] = w
    el.append(d)

  edf = pd.DataFrame(el)

  edf = edf[((edf['start'].isin(ndf['user index'])) & (edf['stop'].isin(ndf['user index'])))]

  # create graph and save
  #----------------------------------------------------------------------------#

  kwargs = dict(width=800, height=800, xaxis=None, yaxis=None)
  opts.defaults(opts.Nodes(**kwargs), opts.Graph(**kwargs))

  hv_nodes = hv.Nodes(ndf).sort()
  hv_graph = hv.Graph((edf, hv_nodes))
  hv_graph.opts(
    node_color = 'log degree',
    node_size=10,
    edge_line_width=1,
    node_line_color='gray',
    edge_hover_line_color = '#DF0000')

  bundled = bundle_graph(hv_graph)
  renderer.save(bundled, 'graph_bundled_full')
  renderer.save(hv_graph, 'graph_full')

  #----------------------------------------------------------------------------#

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
