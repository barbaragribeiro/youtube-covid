#!/usr/bin/env python3

import re
import html
import json

import langid
lang_ident = langid.langid.LanguageIdentifier.from_modelstring(langid.langid.model, norm_probs=True)

import csv


def clean_text(raw_text):
    text = html.unescape(raw_text)
    text = re.sub("<.*?>", "", text)
    text = re.sub(r"https?://\S+", "", text)
    return text


DIR_BASE = "../.."

channel_type= {}
with open("{}/data/channels_names.tsv".format(DIR_BASE), "r") as infile:
    csvr = csv.DictReader(infile, delimiter="\t")
    for row in csvr:
        if row["channel_type"] != "ignored":
            channel_type[row["channel_id"]] = row["channel_type"]


selected_videos = set()

with open("{}/data/videos.jsonl".format(DIR_BASE), "r") as infile, \
     open("{}/data/videos-filtered.jsonl".format(DIR_BASE), "w") as outfile:

    for line in infile:

        obj = json.loads(line)

        if len(obj["subtitle"]) > 0:
            text_cleaned = clean_text(obj["subtitle"])
        else:
            text_cleaned = clean_text(obj["transcript"])

        lang, prob = lang_ident.classify(text_cleaned.lower())

        if len(text_cleaned) > 0 and lang == "en" and prob >= 0.8 and obj["channel_id"] in channel_type:

            selected_videos.add(obj["video_id"])

            obj["transcript"] = text_cleaned

            obj["channel_type"] = channel_type[obj["channel_id"]]

            outfile.write("{}\n".format(json.dumps(obj)))


with open("{}/data/comments.jsonl".format(DIR_BASE), "r") as infile, \
     open("{}/data/comments-filtered.jsonl".format(DIR_BASE), "w") as outfile:

    for line in infile:

        obj = json.loads(line)

        if obj["video_id"] in selected_videos:

            text_cleaned = clean_text(obj["comment_text"])

            lang, prob = lang_ident.classify(text_cleaned.lower())

            if lang == "en" and prob >= 0.8:

                obj["comment_text"] = text_cleaned

                obj["channel_type"] = channel_type[obj["channel_id"]]

                outfile.write("{}\n".format(json.dumps(obj)))

