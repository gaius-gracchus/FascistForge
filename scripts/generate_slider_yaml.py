# -*- coding: UTF-8 -*-

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os
import pandas as pd

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

input_dir = '/home/tlee/Documents/blog/blog/assets/img/posts/2019-09-02-fascist-forge/gallery/'
user_df = '/home/tlee/Documents/blog/entries/fascist_forge/data/user_info.df'

output_file = '/home/tlee/Documents/blog/entries/fascist_forge/slider.yaml'

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

if __name__ == '__main__':

  df = pd.read_pickle( user_df )

  files = sorted(os.listdir(input_dir))

  with open(output_file, 'w') as f:

    for file in files:
      number, imagetype = file[:-4].split('_')
      number = int( number )

      user = df.loc[number]['name']

      capitalized_imagetype = imagetype[0].upper() + imagetype[1:].lower()
      alt = f'{capitalized_imagetype} image for user {user}'

      f.write(f"- src: /assets/img/posts/2019-09-02-fascist-forge/gallery/{file}\n")
      f.write(f"  href: /assets/img/posts/2019-09-02-fascist-forge/gallery/{file}\n")
      f.write('  alt: ' + alt + '\n')


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#