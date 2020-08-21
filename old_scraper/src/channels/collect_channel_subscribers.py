#!/usr/bin/env python3

import urllib.request
import re
import json


def collect_channel_subscribers(channel_id):

    url = "https://www.youtube.com/channel/{}".format(channel_id)

    html = urllib.request.urlopen(url).read().decode("utf-8")

    channel_title = re.search("<meta name=\"title\" content=\"([^\"]+)\"", html).group(1)
    
    channel_subscribers = re.search("subscriberCountText\":{\"runs\":\[\{\"text\":\"([^\"]+)\"", html).group(1)

    if "mil" in channel_subscribers:
        mult = 1000

    elif "mi" in channel_subscribers:
        mult = 1000000

    else:
        mult = 1

    channel_subscribers = int(float(re.sub("[^0-9,]", "", channel_subscribers).replace(",",".")) * mult)

    return channel_title, channel_subscribers


if __name__ == "__main__":

    import sys

    channel_id = sys.argv[1]

    channel_title, channel_subscribers = collect_channel_subscribers(channel_id)

    sys.stdout.buffer.write("{}\t{}\n".format(channel_title, channel_subscribers).encode("utf-8"))

