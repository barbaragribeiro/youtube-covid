#!/usr/bin/env python3

import urllib.request
import re
import json
import codecs


def collect_closed_captions(video_id):

    url_video = "https://www.youtube.com/watch?v={}".format(video_id)
    html = urllib.request.urlopen(url_video, timeout=30).read().decode("utf-8")

    search_url = re.search("captionTracks\":\[\{\"baseUrl\":\"([^\"]+)\"",html)

    if search_url:
        url_partial = search_url.group(1).replace('\\u0026', '&')
        if len(url_partial) > 0:
            url_caption = "{}&fmt=srv3".format(url_partial)
            data_caption = urllib.request.urlopen(url_caption, timeout=30).read().decode("utf-8")
        else:
            data_caption = None
        
        if("name=" in url_partial):
            name = "subtitle"
        else:
            name = "transcript"

    else:
        data_caption = None
        name = None

    return data_caption, name


if __name__ == "__main__":

    import sys
    import os

    DIR_BASE = "../.."

    video_id = sys.argv[1]

    outdir = "{}/data/videos/{}".format(DIR_BASE, video_id)
    
    raw, name = collect_closed_captions(video_id)

    if (name):
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        outfile_name = "{}/".format(outdir) + name + ".xml"

        if not os.path.exists(outfile_name):

            with open(outfile_name, "w", encoding="utf-8") as outfile:
                outfile.write(raw)

