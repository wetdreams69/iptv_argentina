#!/usr/bin/python3

import requests
import os
import sys
import streamlink
#import json

banner = r'''
######################################################################
#  _       _                                          _              #
# (_)     | |                                        | |             # 
#  _ _ __ | |___   __  __ _  ___ _ __   ___ _ __ __ _| |_ ___  _ __  #
# | | '_ \| __\ \ / / / _` |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__| #
# | | |_) | |_ \ V / | (_| |  __/ | | |  __/ | | (_| | || (_) | |    #
# |_| .__/ \__| \_/   \__, |\___|_| |_|\___|_|  \__,_|\__\___/|_|    #
#   | |         ______ __/ |                                         #
#   |_|        |______|___/                                          #
#                                                                    #
#                                     >> https://github.com/osgioia  #
######################################################################
'''

def grab(url):
    try:
        if url.endswith('.m3u') or url.endswith('.m3u8') or ".ts" in url:
            return url

        session = streamlink.Streamlink()
        streams = session.streams(url)
        if "best" in streams:
            return streams["best"].url
        return None
    except streamlink.exceptions.NoPluginError:
        return url

def check_url(url):
    try:
        response = requests.head(url, timeout=15)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    
    try:
        response = requests.head(url, timeout=15, verify=False)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    
    return False

# Crear un array para almacenar los datos
channel_data = []

channel_info = os.path.abspath(os.path.join(os.path.dirname(__file__), '../channel_info.txt'))

with open(channel_info) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
            channel_data.append({
                'type': 'info',
                'ch_name': ch_name,
                'grp_title': grp_title,
                'tvg_logo': tvg_logo,
                'tvg_id': tvg_id,
                'url': ''
            })
            
        else:
            link = grab(line)
            if link and check_url(link):
                channel_data.append({
                    'type': 'link',
                    'url': link
                })

with open("playlist.m3u", "w") as f:
    f.write(banner)
    f.write(f'\n#EXTM3U')

    # Initialize a variable to keep track of the previous item
    prev_item = None

    for item in channel_data:
        if item['type'] == 'info':
            prev_item = item
        if item['type'] == 'link' and item['url']:
            f.write(f'\n#EXTINF:-1 group-title="{prev_item["grp_title"]}" tvg-logo="{prev_item["tvg_logo"]}" tvg-id="{prev_item["tvg_id"]}", {prev_item["ch_name"]}')
            f.write(item['url'])

#with open("playlist.json", "w") as f:

#json_data = json.dumps(channel_data, indent=2)

#print(json_data)

