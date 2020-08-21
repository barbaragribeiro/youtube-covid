#!/usr/bin/env python3

import urllib.request
import re
import json

resources = json.load(open("../../data/resources.json"))

def collect_channel_videos(channel_id):

    videos = []

    url_base = "https://www.googleapis.com/youtube/v3/search?part=id&maxResults=50&type=video&channelId={}&key={}".format(channel_id, resources["API_KEY"])
    url = url_base

    while url:

        req = urllib.request.urlopen(url).read()
        obj = json.loads(req.decode("utf-8"))

        new_videos = [ video["id"]["videoId"] 
                           for video in obj["items"] 
                               if video["id"]["kind"] == "youtube#video" ]

        videos.extend(new_videos)

        if "nextPageToken" in obj:
            url = "{}&pageToken={}".format(url_base, obj["nextPageToken"])
        else:
            url = None

    return videos


if __name__ == "__main__":

    import sys

    channel_id = sys.argv[1]

    videos = collect_channel_videos(channel_id)

    for video in videos:
        print(video)

