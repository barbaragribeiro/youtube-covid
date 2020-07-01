#!/usr/bin/env python3

import urllib.request
import re
import json


def collect_channel_subscribers(channel_id):

    url = "https://www.youtube.com/channel/{}".format(channel_id)

    html = urllib.request.urlopen(url).read().decode("utf-8")

    channel_title = re.search("<title>(.+?)</title>", html, re.DOTALL).group(1)
    channel_title = channel_title.replace(" - YouTube", "").strip()
    
    channel_subscribers = re.search("<span class=\"yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip\" title=\"(.+?)\"", html).group(1)
    channel_subscribers = int(channel_subscribers.replace(".", ""))

    return channel_title, channel_subscribers


if __name__ == "__main__":

    import sys

    channel_id = sys.argv[1]

    channel_title, channel_subscribers = collect_channel_subscribers(channel_id)

    sys.stdout.buffer.write("{}\t{}\n".format(channel_title, channel_subscribers).encode("utf-8"))

