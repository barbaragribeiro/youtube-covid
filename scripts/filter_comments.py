#!/usr/bin/env python3
import sys
import os
import json
import csv
import pandas as pd

#Files are expected to be in the format .comments.jsonl

COLUMNS = ['cid', 'text', 'time', 'author', 'channel', 'votes', 'video_id']
ORIGINAL_COLUMNS = ['cid', 'text', 'time', 'author', 'channel', 'votes', 'photo', 'video_id']

def toInt(n):
    n = n.replace(',', '.')
    if 'mil' in n:
        return int(float(n[:-4])*1000)
    elif 'mi' in n:
        return int(float(n[:-3])*1000000)
    else:
        return int(n)

def main():
    folder = sys.argv[1]
    output = sys.argv[2]
    video_data = sys.argv[3]

    if os.sep in output:
        outdir = os.path.dirname(output)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    with open(output, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=ORIGINAL_COLUMNS)
        writer.writeheader() #Add header to csv

        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('comments.jsonl'):
                    print('Reading ' + file)
                    video_id = file.split('.')[0]
                    with open(os.path.join(root,file)) as json_file:
                        dicts = [dict(json.loads(line), video_id=video_id) for line in json_file]
                    for dic in dicts:
                        writer.writerow(dic)
            
    #Post-processing
    df = pd.read_csv(output, usecols=COLUMNS, dtype={'votes':'str'})

    #Number of votes is in the form '999', '3,9 mil', '1,2 mi'
    df['votes'] = df['votes'].apply(lambda x : toInt(x)).astype('Int64')

    #Extract parent id for replies and adds replies count
    df['parent_id'] = df['cid'].apply(lambda x : x.split('.')[0] if '.' in x else None)
    replies_count = df.groupby('parent_id')['cid']\
                    .count()\
                    .rename('replies')\
                    .astype('Int64')
    df = df.join(replies_count, how='left', on='cid').fillna(0)

    #Adds video title
    videos = pd.read_csv(video_data, usecols=['id','title'])
    videos = videos.rename(columns={'id': 'video_id', 'title' : 'video_title'})
    df = pd.merge(df, videos, how='left', on='video_id')

    #Sorting
    df.sort_values('votes', ascending=False, inplace=True)
    df.to_csv(output.split('.')[0] + '_sorted_votes.csv', index=False)
    df.sort_values('replies', ascending=False, inplace=True)
    df.to_csv(output.split('.')[0] + '_sorted_replies.csv', index=False)

if __name__=='__main__':
    main()