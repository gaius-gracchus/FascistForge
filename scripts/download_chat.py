# -*- coding: UTF-8 -*-

"""Downloads chat data from public Fascist Forge Matrix Riot chat room.

Package used is `matrix-dl`, clone and install from
https://gitlab.gnome.org/thiblahute/matrix-dl

"""

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# url of matrix chat
matrix_url = "https://matrix.org"

# room internal ID
room = "\!ycCscfsOQiaubPktZu:matrix.org"

# I'm not sharing my username and password
username = os.getenv( 'FF_MATRIX_USERNAME' )
password = os.getenv( 'FF_MATRIX_PASSWORD' )

# file name to save output data to
output_fname = 'chat.txt'

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

if __name__ == '__main__':

  print(f'matrix-dl --matrix-url {matrix_url} --password {password} {username} {room} > {output_fname}')

  # call command-line interface
  os.system( f'matrix-dl --matrix-url {matrix_url} --password {password} {username} {room} > {output_fname}')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#