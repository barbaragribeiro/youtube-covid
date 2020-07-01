#!/usr/bin/env python3

import urllib.request
import re
import json
import codecs


def collect_closed_captions(video_id, lang="pt"):

    url_caption = "http://video.google.com/timedtext?lang={}&v={}".format(lang, video_id)
    #Also works
    #url_caption = "https://www.youtube.com/api/timedtext?lang={}&v={}".format(lang, video_id)
    data_caption = urllib.request.urlopen(url_caption, timeout=30).read().decode("utf-8")

    return data_caption



if __name__ == "__main__":

    import sys
    import os

    DIR_BASE = "../.."

    video_id = sys.argv[1]

    outdir = "{}/data/videos/{}".format(DIR_BASE, video_id)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    outfile_name = "{}/transcript.xml".format(outdir)
    if not os.path.exists(outfile_name):

        with open(outfile_name, "w", encoding="utf-8") as outfile:
            
            raw = collect_closed_captions(video_id)
            #raw = collect_closed_captions(video_id, lang="en")

            if raw:
                outfile.write(raw)

