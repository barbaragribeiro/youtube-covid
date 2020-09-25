#!/usr/bin/env python3
import sys
import os
import json
import pandas as pd
import argparse

#Files are expected to be in the format .comments.jsonl

COLUMNS = ['cid', 'text', 'time', 'author', 'channel', 'votes', 'video_id']

def toInt(n):
    n = n.replace(',', '.')
    if 'mil' in n:
        return int(float(n[:-4])*1000)
    elif 'mi' in n:
        return int(float(n[:-3])*1000000)
    else:
        return int(n)

def dicts_generator(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.comments.jsonl'):
                print('Reading ' + file)
                video_id = file.split('.')[0]
                with open(os.path.join(root,file)) as json_file:
                    for line in json_file:
                        dic = json.loads(line)
                        dic['video_id'] = video_id
                        del dic['photo']
                        yield(dic)

def filter(args):
    if os.sep in args.output:
        outdir = os.path.dirname(args.output)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    comments_gen = dicts_generator(args.folder)

    #Post-processing
    df = pd.DataFrame(comments_gen)
    #Change number of votes from '3,9 mil' or '1,2 mi' to 3900 or 1200000
    df['votes'] = df['votes'].apply(lambda x : toInt(x)).astype('Int64')

    #Extracts parent id and add replies count
    df['parent_id'] = df['cid'].apply(lambda x : x.split('.')[0] if '.' in x else None)
    replies_count = df.groupby('parent_id')['cid']\
                    .count()\
                    .rename('replies')\
                    .astype('Int64')
    df = df.join(replies_count, how='left', on='cid')
    df = df.fillna({'replies_count':0})

    #Adds video and channel info
    videos = pd.read_csv(args.video_info, usecols=['id','title','uploader','uploader_id'])
    videos = videos.rename(columns={'id': 'video_id', 'title' : 'video_title'})
    df = pd.merge(df, videos, how='left', on='video_id')

    df.to_csv(args.output, index=False)

    if args.sort:
        #Sorting
        df.sort_values('votes', ascending=False, inplace=True)
        df.to_csv(args.output.split('.')[0] + '_sorted_votes.csv', index=False)
        df.sort_values('replies', ascending=False, inplace=True)
        df.to_csv(args.output.split('.')[0] + '_sorted_replies.csv', index=False)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', '-f', help='Path to folder with all video data')
    parser.add_argument('--output', '-o', help='Output filename')
    parser.add_argument('--video-info', help='File with video info')
    parser.add_argument('--sort', help='Create sorted csvs as well', action="store_true")

    args = parser.parse_args(argv)

    filter(args)

if __name__=='__main__':
    main(sys.argv[1:])