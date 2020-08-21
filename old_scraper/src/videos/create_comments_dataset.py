#!/usr/bin/env python3

import os
import re
import json


DIR_BASE = "../.."

videos = []
with open("{}/data/videos.jsonl".format(DIR_BASE), "r") as infile:
    for line in infile:
        obj = json.loads(line)
        videos.append((obj["video_id"], obj["channel_id"], obj["channel_name"]))


with open("{}/data/comments.jsonl".format(DIR_BASE), "w") as outfile:

        for video_id, channel_id, channel_name in videos:
        
            dirvideo = "{}/data/videos/{}".format(DIR_BASE, video_id)
        
            if os.path.exists("{}/comments.json".format(dirvideo)):
                with open("{}/comments.json".format(dirvideo), "r") as infile:
                    comments = json.load(infile)
                    for comment in comments:
                        obj = {
                            "comment_id"          : comment["topLevelComment"]["id"],
                            "parent_id"           : None,
                            "video_id"            : comment["videoId"],
                            "channel_id"          : channel_id,
                            "author_id"           : comment["topLevelComment"]["snippet"]["authorChannelId"]["value"] 
                                                        if "authorChannelId" in comment["topLevelComment"]["snippet"] else 
                                                            comment["topLevelComment"]["snippet"]["authorChannelUrl"],
                            "author_name"         : comment["topLevelComment"]["snippet"]["authorDisplayName"],
                            "author_image"        : comment["topLevelComment"]["snippet"]["authorProfileImageUrl"],
                            "comment_date"        : comment["topLevelComment"]["snippet"]["publishedAt"],
                            "comment_text"        : comment["topLevelComment"]["snippet"]["textDisplay"],
                            "comment_reply_count" : comment["totalReplyCount"],
                            "comment_like_count"  : comment["topLevelComment"]["snippet"]["likeCount"],
                        }
                        outfile.write("{}\n".format(json.dumps(obj)))
            
        
            if os.path.exists("{}/comreplies.json".format(dirvideo)):
                with open("{}/comreplies.json".format(dirvideo), "r") as infile:
                    comreplies = json.load(infile)
                    for reply in comreplies:
                        obj = {
                            "comment_id"          : reply["id"],
                            "parent_id"           : reply["parentId"],
                            "video_id"            : reply["videoId"],
                            "channel_id"          : channel_id,
                            "author_id"           : reply["snippet"]["authorChannelId"]["value"] 
                                                        if "authorChannelId" in reply["snippet"] 
                                                            else reply["snippet"]["authorChannelUrl"],
                            "author_name"         : reply["snippet"]["authorDisplayName"],
                            "author_image"        : reply["snippet"]["authorProfileImageUrl"],
                            "comment_date"        : reply["snippet"]["publishedAt"],
                            "comment_text"        : reply["snippet"]["textDisplay"],
                            "comment_reply_count" : None,
                            "comment_like_count"  : reply["snippet"]["likeCount"],
                        }
                        outfile.write("{}\n".format(json.dumps(obj)))
                
