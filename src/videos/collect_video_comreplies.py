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

TIME_TO_SLEEP = 300

def collect_comment_replies(comment_id):

    replies = []

    url_base = "https://www.googleapis.com/youtube/v3/comments?part=snippet&maxResults=100&parentId={}&key={}".format(comment_id, resources["API_KEY"])
    url = url_base
    
    page_num = 1

    while url:
    
        #logging.info("[cid = {}] Page {}".format(comment_id, page_num))

        req = urllib.request.urlopen(url, timeout=30).read()
        obj = json.loads(req.decode("utf-8"))

        #new_replies = [dict(parentId=comment_id, **reply) for reply in obj["items"]]
        new_replies = obj["items"]

        replies.extend(new_replies)

        if "nextPageToken" in obj:
            url = "{}&pageToken={}".format(url_base, obj["nextPageToken"])
            page_num += 1
        else:
            url = None

    return replies


def collect_video_comreplies(video_str, video_id, comments_file):

    logging.info("[{}] Loading comments".format(video_str))

    comments = json.load(open(comments_file))
    logging.info("[{}] Comments: {}".format(video_str, len(comments)))

    comments_with_reply = [ comment["topLevelComment"]["id"] for comment in comments if comment["totalReplyCount"] > 0 ]
    logging.info("[{}] Comments with reply: {}".format(video_str, len(comments_with_reply)))

    comreplies = []

    #for i, comment_id in enumerate(comments_with_reply, 1):
    #For test purposes only
    for i, comment_id in enumerate(comments_with_reply[:2], 1):
        #logging.info("[{}] Collecting replies for comment {} ({}/{}) (try {})".format(video_str, comment_id, i, len(comments_with_reply)))

        #comment_replies = collect_comment_replies(comment_id)
        #comment_replies = [ dict(videoId=video_id, parentId=comment_id, **reply) for reply in comment_replies ]

        #comreplies.extend(comment_replies)

        for tryrun in range(1, 4):

            try:
                logging.info("[{}] Collecting replies for comment {} ({}/{}) (try {})".format(video_str, comment_id, i, len(comments_with_reply), tryrun))
                comment_replies = collect_comment_replies(comment_id)
                comment_replies = [ dict(videoId=video_id, parentId=comment_id, **reply) for reply in comment_replies ]

                comreplies.extend(comment_replies)

                break

            except Exception as error:
                logging.error("[{}] Unknown error (try {}):\n{}".format(video_str, tryrun, traceback.format_exc()))
                will_wake = datetime.datetime.today() + datetime.timedelta(seconds=TIME_TO_SLEEP) 
                logging.warning("[vid = {}] Sleeping {:,} seconds, will wake on {} (try {})".format(video_str, TIME_TO_SLEEP, will_wake, tryrun))
                time.sleep(TIME_TO_SLEEP)
                logging.warning("[{}] Woke up (try {})".format(video_str, tryrun))

    return comreplies


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
                   if not os.path.exists("{}/data/videos/{}/comreplies.json".format(DIR_BASE, video_id))  ]

    random.shuffle(videos)

    logging.info("Videos to collect: {}".format(len(videos)))

    for i, video_id in enumerate(videos, 1):

        video_str = "vid = {} ({}/{})".format(video_id, i, len(videos))

        logging.info("[{}] Started".format(video_str))

        outdir = "{}/data/videos/{}".format(DIR_BASE, video_id)

        outfile_name = "{}/comreplies.json".format(outdir)
        if not os.path.exists(outfile_name):

            comments_filename = "{}/comments.json".format(outdir)
            if os.path.exists(comments_filename):

                for tryrun in range(1, 4):

                    try:
                        logging.info("[{}] Collecting replies (try {})".format(video_str, tryrun))
                        comreplies = collect_video_comreplies(video_str, video_id, comments_filename)

                        with open(outfile_name, "w", encoding="utf-8") as outfile:
                            outfile.write(json.dumps(comreplies))
                        logging.info("[{}] Replies saved".format(video_str))

                        break

                    except Exception as error:
                        logging.error("[{}] Unknown error (try {}):\n{}".format(video_str, tryrun, traceback.format_exc()))
                        will_wake = datetime.datetime.today() + datetime.timedelta(seconds=TIME_TO_SLEEP) 
                        logging.warning("[vid = {}] Sleeping {:,} seconds, will wake on {} (try {})".format(video_str, TIME_TO_SLEEP, will_wake, tryrun))
                        time.sleep(TIME_TO_SLEEP)
                        logging.warning("[{}] Woke up (try {})".format(video_str, tryrun))

            else:
                logging.warning("[{}] No comments".format(video_str))

        else:
            logging.info("[{}] Already collected".format(video_str))
            
        logging.info("[{}] Finished".format(video_str))
