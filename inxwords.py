#!/usr/bin/env python
# encoding: utf-8
"""
Find a trending topic along the lines of #YinXwords and
tweet a random X-word sentence from Project Gutenberg.
"""
from __future__ import print_function, unicode_literals

try:
    import resource
    mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024.0)
except ImportError:
    # resource not on Windows
    pass


import argparse
import os
import random
import re
import sys
import time
import twitter
import webbrowser
import yaml

from pprint import pprint
try:
    # http://stackoverflow.com/a/2282656/724176
    from timeout import timeout, TimeoutError
except (AttributeError, ImportError) as e:
    # Not on Windows or module not present
    timeout = None
    TimeoutError = None

REGEX = re.compile("[Ii]n([0-9]+|[Tt]hree|[Ff]our|[Ff]ive|[Ss]ix)[Ww]ords$")

# Dict of number of words in a sentence->all those sentences
BIG_OLD_CACHE = {}

HELSINKI_LAT = 60.170833
HELSINKI_LONG = 24.9375

# Limit to five locations to avoid rate limit:
#  * "GET trends/place" rate limit is 15 calls/15 minutes.
#  * We look for a new trend once every five minutes.
#  * If no hits found, all WOE_IDS are checked.
WOE_IDS = {
    "World":     1,
    "Australia": 23424748,
    "Canada":    23424775,
    # "France": 23424819,
    # "Sweden": 23424954,
    "UK":        23424975,
    "US":        23424977,
}

TWITTER = None

SEPERATORS = [" ", " ", " ", " ", "\n", "\n", "\n\n"]

# Only get a trend every five minutes
counter = 0


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def load_yaml(filename):
    """
    File should contain:
    consumer_key: TODO_ENTER_YOURS
    consumer_secret: TODO_ENTER_YOURS
    access_token: TODO_ENTER_YOURS
    access_token_secret: TODO_ENTER_YOURS
    If it contains last_number or last_mention_id, don't change it
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {
            'access_token', 'access_token_secret',
            'consumer_key', 'consumer_secret'}:
        sys.exit("Twitter credentials missing from YAML: " + filename)

    return data


def ends_with_in_x_words(text):
    """
    If "inXwords" found at the end of the text, return the X.
    Otherwise return 0.
    """
    if not text:
        return 0
    found = REGEX.findall(text, re.IGNORECASE)
    if found:
        found = found[0]
        try:
            return int(found)
        except ValueError:
            if found.lower() == "three":
                return 3
            elif found.lower() == "four":
                return 4
            elif found.lower() == "five":
                return 5
            elif found.lower() == "six":
                return 6
    return 0


def get_trending_topic_from_twitter():
    global TWITTER, counter

    # "This information is cached for 5 minutes. Requesting more frequently
    # than that will not return any more data, and will count against your
    # rate limit usage."
    if counter <= 0 or ends_with_in_x_words(args.trend) == 0:
        counter = 4
        print("Get fresh trend")
    else:
        counter -= 1
        print("Use cached trend")
        return args.trend, ends_with_in_x_words(args.trend)

    # Create and authorise an app with (read and) write access at:
    # https://dev.twitter.com/apps/new
    # Store credentials in YAML file
    if TWITTER is None:
        TWITTER = twitter.Twitter(auth=twitter.OAuth(
            data['access_token'],
            data['access_token_secret'],
            data['consumer_key'],
            data['consumer_secret']))

    # Returns the locations that Twitter has trending topic information for.
    # world_locations = TWITTER.trends.available()
    # pprint(world_locations)
    # print("*"*80)

    # Shuffle list of WOE_IDS, and go through each until a match is found
    pprint(WOE_IDS)
    woe_ids = WOE_IDS.items()
    random.shuffle(woe_ids)
    pprint(woe_ids)

    for woe_id in woe_ids:
        print(woe_id)

        print("GET trends/place")
        trends = TWITTER.trends.place(_id=woe_id[1])[0]

        for trend in trends['trends']:
            print("-"*80)
            pprint(trend)
            print_it(trend['name'])

            how_many_words = ends_with_in_x_words(trend['name'])
            print(how_many_words)

            if (not trend['promoted_content'] and
                    how_many_words >= 3 and
                    how_many_words <= 6):
                args.trend = trend['name']
                return trend['name'], how_many_words

    print("No fresh trend found, use cached")
    return args.trend, ends_with_in_x_words(args.trend)


def get_random_sentence_from_pg(number_of_words):
    infile = os.path.join(args.sendir,
                          str(number_of_words) + "-word-sentences.txt")

    print(number_of_words in BIG_OLD_CACHE)
    if number_of_words not in BIG_OLD_CACHE:
        with open(infile) as f:
            BIG_OLD_CACHE[number_of_words] = f.read().splitlines()

    return random.choice(BIG_OLD_CACHE[number_of_words])


def tweet_it(string, in_reply_to_status_id=None):
    global TWITTER

    if len(string) <= 0:
        print("ERROR: trying to tweet an empty tweet!")
        return

    # Create and authorise an app with (read and) write access at:
    # https://dev.twitter.com/apps/new
    # Store credentials in YAML file
    if TWITTER is None:
        TWITTER = twitter.Twitter(auth=twitter.OAuth(
            data['access_token'],
            data['access_token_secret'],
            data['consumer_key'],
            data['consumer_secret']))

    print_it("TWEETING THIS: " + string)

    if args.test:
        print("(Test mode, not actually tweeting)")
    else:
        print("POST statuses/update")
        result = TWITTER.statuses.update(
            status=string,
            # lat=HELSINKI_LAT, long=HELSINKI_LONG,
            display_coordinates=True,
            in_reply_to_status_id=in_reply_to_status_id)
        url = "http://twitter.com/" + \
            result['user']['screen_name'] + "/status/" + result['id_str']
        print("Tweeted: " + url)
        if not args.no_web:
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


# @timeout(30)
def inxwords():
    """
    Main stuff callable in  loop
    """
    print("Get a topic from Twitter")
    trend, how_many_words = get_trending_topic_from_twitter()
    pprint(trend)
    print("How many words?", how_many_words)

    if not trend:
        print("Nowt found, try later")
        return

    # Find a matching sentence from PG
    random_sentence = get_random_sentence_from_pg(how_many_words)
    print(random_sentence)

    # 1 in 4 chance to add quotes
    if random.randint(0, 3) == 0:
        random_sentence = '"' + random_sentence + '"'
    # Random order of text and hashtag
    things = [trend, random_sentence]
    random.shuffle(things)
    print(">"+" ".join(things)+"<")
    # Random separator between text and hashtag
    tweet = random.choice(SEPERATORS).join(things)
    print(">"+tweet+"<")

    print("Tweet this:\n", tweet)
    try:
        tweet_it(tweet)

    except twitter.api.TwitterHTTPError as e:
        print("*"*80)
        print(e)
        print("*"*80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find a trending topic along the lines of #YinXwords and "
                    "tweet a random X-word sentence from Project Gutenberg.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        # default='/Users/hugo/Dropbox/bin/data/inxwords.yaml',
        default='E:/Users/hugovk/Dropbox/bin/data/inxwords.yaml',
        help="YAML file location containing Twitter keys and secrets")
    parser.add_argument(
        '-s', '--sendir',
        # default='/Users/hugo/Dropbox/txt/gutenberg/',
        default='E:/Users/hugovk/Dropbox/txt/gutenberg',
        help="Directory of files containing sentences from Project Gutenberg")
    parser.add_argument(
        '-t', '--trend', default=None,
        help="Default trend to use if none found")
    parser.add_argument(
        '-l', '--loop', action='store_true',
        help="Run repeatedly with a minute delay")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    parser.add_argument(
        '-x', '--test', action='store_true',
        help="Test mode: go through the motions but don't update anything")
    args = parser.parse_args()

    data = load_yaml(args.yaml)

    if args.loop:
        while(True):
            try:
                inxwords()
                print("Sleep for a minute")
                time.sleep(60)
            except TimeoutError as e:
                print("*"*80)
                print(e)
                print("*"*80)
                print("Sleep for 30 seconds")
                time.sleep(30)
            except twitter.api.TwitterHTTPError as e:
                print("*"*80)
                print(e)
                print("*"*80)
                print("Sleep for at least 60 seconds")
                time.sleep(61)
    else:
        inxwords()

    try:
        mem1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024.0)
        print(mem0)
        print(mem1)
        print(mem1-mem0)
    except NameError:
        # resource not on Windows
        pass

#      TODO call from a .sh/.bat looping as well, in case of exceptions

# End of file
