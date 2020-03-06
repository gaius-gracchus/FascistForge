# -*- coding: UTF-8 -*-

"""Downloads and saves all unique profile and cover images from Fascist Forge
"""

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os
from collections import Counter
import pandas as pd

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# user data DataFrame file
input_file = 'user_info.df'

# directory to save images to
output_dir = 'images'

# image number format
fmt = '{:04d}'

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

if __name__ == '__main__':

  # create output directory if it doesn't already exist
  os.makedirs( output_dir, exist_ok = True )

  # read in user data DataFrame
  df = pd.read_pickle(input_file)

  # determine the Fascist Forge default images (so we don't download
  # extraneous copies)
  default_cover = Counter(df['cover_photo']).most_common(1)[0][0]
  default_profile = Counter(df['profile_photo']).most_common(1)[0][0]

  # loop over rows in DataFrame
  for idx in df.index:

    # extract image URLs for a given user
    cover_url = df.loc[idx]['cover_photo']
    profile_url = df.loc[idx]['profile_photo']

    # download cover image and save to file using wget, if image isn't the
    # default Fascist Forge cover photo
    if cover_url != default_cover:

      cover_ext = cover_url.split('.')[-1]
      cover_fname = os.path.join(
        output_dir,
        fmt.format(idx) + f'_cover.{cover_ext}' )
      os.system(f'wget {cover_url} -O {cover_fname}')

    # download profile image and save to file using wget, if image isn't the
    # default Fascist Forge profile photo
    if profile_url != default_profile:

      profile_ext = profile_url.split('.')[-1]
      profile_fname = os.path.join(
        output_dir,
        fmt.format(idx) + f'_profile.{profile_ext}' )
      os.system(f'wget {profile_url} -O {profile_fname}')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#