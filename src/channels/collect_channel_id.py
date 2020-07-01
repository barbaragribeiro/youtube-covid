#!/usr/bin/env python3

import urllib.request
import re
import json


def collect_channel_id(channel_url):

    html = urllib.request.urlopen(channel_url).read().decode("utf-8")

    channel_id = re.search("data-channel-external-id=\"([^\"]+)\"", html).group(1)

    return channel_id


if __name__ == "__main__":

    import sys

    channel_url = sys.argv[1]

    channel_id = collect_channel_id(channel_url)

    print(channel_id)

