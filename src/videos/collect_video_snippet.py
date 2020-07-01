#!/usr/bin/env python3

import urllib.request
import re
import json

from collect_video_statistics import collect_video_info

resources = json.load(open("../../data/resources.json"))


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
                   if not os.path.exists("{}/data/videos/{}/snippet.json")  ]

    video_chunks = [videos[i:i+50] for i in range(0, len(videos), 50)] 

    print(len(video_chunks))

    for chunk_of_ids in video_chunks:

        videos_info = collect_video_info(chunk_of_ids, part="snippet")

        for video_id, statistics in videos_info:

            print("+ Collected {}".format(video_id))

            outdir = "{}/data/videos/{}".format(DIR_BASE, video_id)
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            
            outfile_name = "{}/snippet.json".format(outdir)
            if not os.path.exists(outfile_name):

                with open(outfile_name, "w", encoding="utf-8") as outfile:
                    outfile.write(json.dumps(statistics))

