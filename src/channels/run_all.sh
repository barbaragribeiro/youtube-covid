#!/bin/bash

DIR_BASE="../.."

#cat $DIR_BASE/canais.txt | grep Link | awk '{print $4}' > $DIR_BASE/data/channels/list_urls.txt

cat $DIR_BASE/data/channels/list_urls.txt | xargs -n 1 -I {} ./collect_channel_id.py {} > $DIR_BASE/data/channels/list.txt

while read channel_id; do
    
    outdir=$DIR_BASE/data/channels/$channel_id
    mkdir -p $outdir

    echo "+ Collecting $channel_id"
    ./collect_channel_videos.py $channel_id > $outdir/videos.txt

done < $DIR_BASE/data/channels/list.txt
#done < $DIR_BASE/data/channels/list.txt.NEW

cat $DIR_BASE/data/channels/list.txt | xargs -n 1 -I {} ./collect_channel_subscribers.py {} > $DIR_BASE/data/channels/n_subscribers.txt
#cat $DIR_BASE/data/channels/list.txt.NEW | xargs -n 1 -I {} ./collect_channel_subscribers.py {} > $DIR_BASE/data/channels/n_subscribers.txt.NEW

echo -e "channel_id\tchannel_name" > $DIR_BASE/data/channels_names.tsv
cat $DIR_BASE/data/channels/n_subscribers.txt | awk -F '\t' '{print $1}' | paste -d $'\t' $DIR_BASE/data/channels/list.txt - >> $DIR_BASE/data/channels_names.tsv

