#!/usr/bin/env python3

import urllib.request
import re
import json
import time
import random
import datetime
import collections

# Setup log
import traceback
import inspect
import logging
logging.basicConfig(filename=inspect.getfile(inspect.currentframe())[:-2]+"log", filemode="a", level=logging.INFO, format="[ %(asctime)s ] %(levelname)s : %(message)s")

resources = json.load(open("../../data/resources.json"))

TIME_TO_SLEEP = 900

def collect_video_comments(video_id):

    comments = []

    url_base = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&videoId={}&key={}".format(video_id, resources["API_KEY"])
    url = url_base
    
    page_num = 1

    while url:
    
        logging.info("[vid = {}] Page {}".format(video_id, page_num))

        req = urllib.request.urlopen(url, timeout=120).read()
        obj = json.loads(req.decode("utf-8"))

        new_comments = [ comment["snippet"] for comment in obj["items"] ]

        comments.extend(new_comments)

        if "nextPageToken" in obj:
            url = "{}&pageToken={}".format(url_base, obj["nextPageToken"])
            page_num += 1
        else:
            url = None

    return comments



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
                   if not os.path.exists("{}/data/videos/{}/comments.json".format(DIR_BASE, video_id))  ]
    logging.info("Videos to collect: {}".format(len(videos)))

    # Order videos by number of comments
    if os.path.exists("{}/data/videos.jsonl".format(DIR_BASE)):
        video_ncomments = collections.Counter()
        with open("{}/data/videos.jsonl".format(DIR_BASE), "r") as infile:
            for line in infile:
                obj = json.loads(line)
                video_ncomments[obj["video_id"]] = obj["comment_count"]
        videos = sorted(videos, key=lambda v: video_ncomments[v])
        logging.info("Videos sorted (min={:,}, max={:,})".format(video_ncomments[videos[0]], video_ncomments[videos[-1]]))
    else:
        random.shuffle(videos)
        logging.info("Videos shuffled".format(len(videos)))

    videos_queue = collections.deque((video_id, 1) for video_id in videos)

    #for video_id in videos:
    while len(videos_queue) > 0:
        video_id, tryrun = videos_queue.popleft()
        print("+ Collecting {} comments".format(video_id))

        logging.info("Remaining: {} videos".format(len(videos_queue)))
        logging.info("[vid = {}] Started".format(video_id))

        outdir = "{}/data/videos/{}".format(DIR_BASE, video_id)
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        
        outfile_name = "{}/comments.json".format(outdir)
        if not os.path.exists(outfile_name):

            logging.info("[vid = {}] Loading statistics".format(video_id))

            statistics = json.load(open("{}/statistics.json".format(outdir)))

            if "commentCount" in statistics and int(statistics["commentCount"]) > 0:

                if tryrun <= 3:

                    #if int(statistics["commentCount"]) <= 50000:
                    logging.info("[vid = {}] Comments: {}".format(video_id, statistics["commentCount"]))

                    #for tryrun in range(1, 4):
                    try:
                        logging.info("[vid = {}] Collecting comments (try {})".format(video_id, tryrun))
                        comments = collect_video_comments(video_id)

                        with open(outfile_name, "w", encoding="utf-8") as outfile:
                            outfile.write(json.dumps(comments))
                        logging.info("[vid = {}] Comments saved".format(video_id))

                        #break

                    except Exception as error:
                        logging.error("[vid = {}] Unknown error (try {}):\n{}".format(video_id, tryrun, traceback.format_exc()))
                        videos_queue.append((video_id, tryrun+1))

                else:
                    logging.error("[vid = {}] Last try (try {}):\n{}".format(video_id, tryrun))
                    #will_wake = datetime.datetime.today() + datetime.timedelta(seconds=TIME_TO_SLEEP) 
                    #logging.warning("[vid = {}] Sleeping {:,} seconds, will wake on {} (try {})".format(video_id, TIME_TO_SLEEP, will_wake, tryrun))
                    #time.sleep(TIME_TO_SLEEP)
                    #logging.warning("[vid = {}] Woke up (try {})".format(video_id, tryrun))

            else:
                logging.info("[vid = {}] No comments".format(video_id))
                comments = []
                with open(outfile_name, "w", encoding="utf-8") as outfile:
                    outfile.write(json.dumps(comments))

        else:
            logging.info("[vid = {}] Already collected".format(video_id))
            
        logging.info("[vid = {}] Finished".format(video_id))
