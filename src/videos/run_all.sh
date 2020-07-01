#!/bin/bash

DIR_BASE="../.."

#find $DIR_BASE/data -iname "videos.txt" -exec cat {} \; > $DIR_BASE/data/videos/list.txt
rm $DIR_BASE/data/videos/list.txt
while read channel_id; do
    cat $DIR_BASE/data/channels/$channel_id/videos.txt >> $DIR_BASE/data/videos/list.txt
done < $DIR_BASE/data/channels/list.txt

./collect_video_subtitles.py
./collect_video_statistics.py
./collect_video_content.py
./collect_video_snippet.py

while read video_id; do
    echo "+ Collecting $video_id"
    ./collect_video_transcript.py $video_id
done < $DIR_BASE/data/videos/list.txt

./collect_video_comments.py
./collect_video_comreplies.py

