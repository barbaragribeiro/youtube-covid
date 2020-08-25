#!/usr/bin/env python3
import sys
import os
import json
import csv
import pandas as pd

COLUMNS = ['id', 'uploader', 'uploader_id', 'channel_id', 'upload_date', 'license', 'title', 
          'description', 'categories', 'tags', 'duration', 'age_limit', 'view_count', 'like_count', 
          'dislike_count', 'average_rating', 'is_live', 'playlist', 'playlist_index']

folder = sys.argv[1]
output = sys.argv[2]

if os.sep in output:
    outdir = os.path.dirname(output)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

with open(output, 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=COLUMNS)
    writer.writeheader() #Add header to csv

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('info.json'):
                print('Reading ' + file)
                with open(os.path.join(root,file)) as json_file:
                    dic = json.load(json_file)
                data = {key : dic[key] for key in COLUMNS}
                writer.writerow(data)

df = pd.read_csv(output)
df.sort_values('view_count', inplace=True)
df.to_csv(output.split('.')[0] + '_sorted_views.csv', index=False)