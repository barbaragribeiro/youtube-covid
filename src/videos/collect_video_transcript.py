#!/usr/bin/env python3

import urllib.request
import re
import json
import codecs


def collect_closed_captions(video_id, lang="pt"):

    url_video = "https://www.youtube.com/watch?v={}".format(video_id)
    html = urllib.request.urlopen(url_video, timeout=30).read().decode("utf-8")

    search_url = re.search("\'TTS_URL\': (.*),", html)

    if search_url:
        url_partial = json.loads(search_url.group(1))
        if len(url_partial) > 0:
            url_caption = "{}&kind=asr&lang={}&fmt=srv3".format(url_partial, lang)
            data_caption = urllib.request.urlopen(url_caption, timeout=30).read().decode("utf-8")
        else:
            data_caption = None
    else:
        data_caption = None

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
            
            #raw = collect_closed_captions(video_id)
            raw = collect_closed_captions(video_id, lang="en")

            if raw:
                outfile.write(raw)

