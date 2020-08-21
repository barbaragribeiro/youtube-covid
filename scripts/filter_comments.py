#!/usr/bin/env python3
import sys
import os
import pandas as pd

folder = sys.argv[1]
output = sys.argv[2]

if os.sep in output:
    outdir = os.path.dirname(output)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

with open(output, 'a') as csv:
    for i, file in enumerate(os.listdir(folder)):
        print(file)
        df = pd.read_json(folder + os.sep + file, lines=True, encoding="utf-8")
        df = df.drop(columns='photo')
        df['parent_id'] = df['cid'].apply(lambda x : x.split('.')[0] if '.' in x else None)
        df['video_id'] = file.split('.')[0]

        if i == 0:
            df.to_csv(csv, header=True, index = False)
        else:
            df.to_csv(csv, header=False, index = False)