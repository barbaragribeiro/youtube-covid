#!/usr/bin/env python3

import urllib.request
import re
import json
import time
import random

# Setup log
import traceback
import inspect
import logging
logging.basicConfig(filename=inspect.getfile(inspect.currentframe())[:-2]+"log", filemode="a", level=logging.INFO, format="[ %(asctime)s ] %(levelname)s : %(message)s")

def collect_subtitle(video_id, lang="pt"):

    url_video = "https://www.youtube.com/watch?v={}".format(video_id)
    html = urllib.request.urlopen(url_video, timeout=30).read().decode("utf-8")

    search_url = re.search("\'TTS_URL\': (.*),", html)

    if search_url:
        url_partial = json.loads(search_url.group(1))
        if (not ("kind=asr" in url_partial)) and len(url_partial) > 0:
            url_subtitle = "{}&lang={}&fmt=srv3".format(url_partial, lang)
            data_subtitle = urllib.request.urlopen(url_subtitle, timeout=30).read().decode("utf-8")
        else:
            data_subtitle = None
    else:
        data_subtitle = None

    return data_subtitle


if __name__ == "__main__":

    import sys
    import os

    DIR_BASE = "../.."


    logging.info("Starting to collect")

    # Read file with list of video ids
    file_videos = "{}/data/videos/list.txt".format(DIR_BASE)
    with open(file_videos, "r") as infile:
        videos = [ line.rstrip() for line in infile ]

    logging.info("Videos identified: {}".format(len(videos)))

    # Filter videos collected
    videos = [ video_id for video_id in videos 
                   if not os.path.exists("{}/data/videos/{}/subtitle.xml".format(DIR_BASE, video_id))  ]

    random.shuffle(videos)

    logging.info("Videos to collect: {}".format(len(videos)))

    for video_id in videos:

        logging.info("[vid = {}] Started".format(video_id))

        outdir = "{}/data/videos/{}".format(DIR_BASE, video_id)
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        
        outfile_name = "{}/subtitle.xml".format(outdir)
        if not os.path.exists(outfile_name):

            for tryrun in range(1, 4):

                try:
                    logging.info("[vid = {}] Collecting subtitle (try {})".format(video_id, tryrun))
                    #subtitle = collect_subtitle(video_id)
                    subtitle = collect_subtitle(video_id, lang="en")
                    
                    with open(outfile_name, "w", encoding="utf-8") as outfile:
                        if subtitle:
                            outfile.write(subtitle)
                            logging.info("[vid = {}] Subtitle saved".format(video_id))
                        else:
                            logging.info("[vid = {}] Subtitle not found".format(video_id))

                    break

                except Exception as error:
                    logging.error("[vid = {}] Unknown error (try {}):\n{}".format(video_id, tryrun, traceback.format_exc()))
                    logging.warning("[vid = {}] Sleeping (try {})".format(video_id, tryrun))
                    time.sleep(100)
                    logging.warning("[vid = {}] Woke up (try {})".format(video_id, tryrun))

        else:
            logging.info("[vid = {}] Already collected".format(video_id))
            
        logging.info("[vid = {}] Finished".format(video_id))
