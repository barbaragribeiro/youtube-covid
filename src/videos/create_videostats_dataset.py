#!/usr/bin/env python3

import json
import csv

DIR_BASE = "../.."

with open("{}/data/videos-filtered.jsonl".format(DIR_BASE), "r") as infile,\
     open("{}/data/video_stats.tsv".format(DIR_BASE), "w") as outfile:

    fields = ["channel_type", "channel_id", "video_id", 
              "video_duration", "view_count", "comment_count",
              "favorite_count", "like_count", "dislike_count" ]


    csvw = csv.DictWriter(outfile, fieldnames=fields, delimiter="\t")

    csvw.writeheader()

    for line in infile:

        obj = json.loads(line)

        output = { k : obj[k] for k in fields }

        csvw.writerow(output)

