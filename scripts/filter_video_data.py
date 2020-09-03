#!/usr/bin/env python3
import sys
import os
import json
import csv
import pandas as pd
import argparse

COLUMNS = ['id', 'uploader', 'uploader_id', 'channel_id', 'upload_date', 'license', 'title', 
          'description', 'categories', 'tags', 'duration', 'age_limit', 'view_count', 'like_count', 
          'dislike_count', 'average_rating', 'is_live', 'playlist', 'playlist_index']

def filter(args):   
    #Creates outdir if necessary 
    if os.sep in args.output:
        outdir = os.path.dirname(args.output)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    with open(args.output, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=COLUMNS)
        writer.writeheader() #Adds header to csv

        for root, dirs, files in os.walk(args.folder):
            for file in files:
                if file.endswith('info.json'):
                    print('Reading ' + file)
                    with open(os.path.join(root,file)) as json_file:
                        dic = json.load(json_file)
                    data = {key : dic[key] for key in COLUMNS} #Creates dict with selected fields
                    writer.writerow(data)
    if args.sort:
        df = pd.read_csv(args.output)
        df.sort_values('view_count', inplace=True)
        df.to_csv(args.output.split('.')[0] + '_sorted_views.csv', index=False)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', '-f', help='Path to folder with all video data')
    parser.add_argument('--output', '-o', help='Output filename')
    parser.add_argument('--sort', help='Create sorted csvs as well', action="store_true")

    args = parser.parse_args(argv)

    filter(args)

if __name__ == "__main__":
    main(sys.argv[1:])