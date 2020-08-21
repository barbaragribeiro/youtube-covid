#!/usr/bin/env python3

import os
import re
import json


def clean_caption(raw):
    if raw:
        text = re.sub("<[^>]+>", "", raw)
        text = re.sub("\s*\n\s*\n", "\n", text)
        text = text.strip()
    else:
        text = ""
    return text


def decode_duration(duration_str):

    s = re.search("PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_str)

    hours, minutes, seconds = map(lambda a: int(a) if a else 0, s.groups())

    total_seconds = 3600*hours + 60*minutes + seconds

    return total_seconds



DIR_BASE = "../.."

file_videos = "{}/data/videos/list.txt".format(DIR_BASE)
with open(file_videos, "r") as infile:
    videos = [ line.rstrip() for line in infile ]


for video_id in videos:

    outdir = "{}/data/videos_filtered/{}".format(DIR_BASE, video_id)
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    outfile_name = "{}/data.json".format(outdir)
    with open(outfile_name, "w") as outfile:

        try:

            dirvideo = "{}/data/videos/{}".format(DIR_BASE, video_id)
        
            with open("{}/statistics.json".format(dirvideo), "r") as infile:
                statistics = json.load(infile)
            
            with open("{}/snippet.json".format(dirvideo), "r") as infile:
                snippet = json.load(infile)

            try:
                with open("{}/content.json".format(dirvideo), "r") as infile:
                    content = json.load(infile)
            except:
                content = None

            try:
                with open("{}/transcript.xml".format(dirvideo), "r", encoding="utf-8") as infile:
                    transcript = infile.read()           
            except:
                transcript = None

            try:
                with open("{}/subtitle.xml".format(dirvideo), "r", encoding="utf-8") as infile:
                    subtitle = infile.read()
            except:
                subtitle = None

            obj = {
                "video_id"       : video_id,

                "video_title"    : snippet["title"],
                "video_desc"     : snippet["description"],
                "video_duration" : decode_duration(content["duration"]) if content else None,
                "video_tags"     : snippet["tags"] if "tags" in snippet else None,
                "video_date"     : snippet["publishedAt"],
                #"video_language" : snippet["defaultAudioLanguage"],

                "channel_id"     : snippet["channelId"],
                "channel_name"   : snippet["channelTitle"],

                "view_count"     : int(statistics["viewCount"]) if "viewCount" in statistics else 0,
                "comment_count"  : int(statistics["commentCount"]) if "commentCount" in statistics else 0,
                "favorite_count" : int(statistics["favoriteCount"]),
                "like_count"     : int(statistics["likeCount"]) if "likeCount" in statistics else 0,
                "dislike_count"  : int(statistics["dislikeCount"]) if "dislikeCount" in statistics else 0,

                "transcript"     : clean_caption(transcript),
                "subtitle"       : clean_caption(subtitle),

            }

            total_likedislike = obj["like_count"] + obj["dislike_count"]
            obj["like_prop"] =  obj["like_count"]/total_likedislike if total_likedislike > 0 else None

            outfile.write(json.dumps(obj))

        except:
            print("ERROR: {}".format(video_id))

