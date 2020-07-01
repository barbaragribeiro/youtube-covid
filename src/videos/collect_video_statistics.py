#!/usr/bin/env python3

import urllib.request
import re
import json

resources = json.load(open("../../data/resources.json"))

def collect_video_info(video_id, part="statistics"):

    if isinstance(video_id, list):
        video_id = ",".join(video_id)

    url = "https://www.googleapis.com/youtube/v3/videos?part={}&id={}&key={}".format(part, video_id, resources["API_KEY"])

    req = urllib.request.urlopen(url, timeout=120).read()
    obj = json.loads(req.decode("utf-8"))

    video_info = [ (video["id"], video[part]) for video in obj["items"] ]
    #print(video_id, video_info)
    
    return video_info


if __name__ == "__main__":

    import sys
    import os

    DIR_BASE = "../.."

    # Read file with list of video ids
    file_videos = "{}/data/videos/list.txt".format(DIR_BASE)
    with open(file_videos, "r") as infile:
        videos = [ line.rstrip() for line in infile ]

    # Filter videos collected
    videos = [ video for video in videos 
                   if not os.path.exists("{}/data/videos/{}/statistics.json")  ]

    video_chunks = [videos[i:i+50] for i in range(0, len(videos), 50)] 

    print(len(video_chunks))

    for chunk_of_ids in video_chunks:

        videos_info = collect_video_info(chunk_of_ids)

        for video_id, statistics in videos_info:

            print("+ Collected {}".format(video_id))

            outdir = "{}/data/videos/{}".format(DIR_BASE, video_id)
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            
            outfile_name = "{}/statistics.json".format(outdir)
            if not os.path.exists(outfile_name):

                with open(outfile_name, "w", encoding="utf-8") as outfile:
                    outfile.write(json.dumps(statistics))
            
