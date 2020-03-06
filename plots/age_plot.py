# -*- coding: UTF-8 -*-

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
plt.style.use('plotstyle')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# path to user DataFrame pickle
df_path = '../data/user_info.df'

# path to output plot to
output_fname = 'age.svg'

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

if __name__ == '__main__':

  # load in DataFrame
  df = pd.read_pickle( df_path )

  # only use ages than can be coerced into integer datatyoe
  ages = []
  for e in df['age']:
      try:
          ages.append(int(e))
      except:
          pass
  ages = np.array( ages )

  # restrict to reasonable range of ages
  bins = np.arange(0, 100)

  # bin centers
  bins_c = 0.5 * (bins[1:] + bins[:-1])

  # generate histogram of age distribution, normalize by number of users to get
  # probability distribution
  h, _ = np.histogram(ages, bins = bins)
  h = h / ages.size

  # plot data
  fig, ax = plt.subplots()
  ax.bar(bins_c, h, width = 1)
  ax.set_xlabel('Age')
  ax.set_ylabel('Probability')

  plt.tight_layout()
  plt.savefig(output_fname)
  plt.close()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#