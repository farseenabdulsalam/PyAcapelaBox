#!/bin/python3

# License
#
# Wrote by farzeen on May 19 of 2016 to ease off
# the heat of JEE Advance exam ;)
#
#  * This script is written for educational purposes.
#  * You are free to do whatever with this script
#    as long as you attribute the original work to me.
#  * I am not responsible for anything this script or its user does.

import signal
import requests
import argparse
import subprocess
import sys

signal.signal(signal.SIGINT,lambda signal,frame:exit(130))

parser = argparse.ArgumentParser(
    description='Convert a text to high quality realistic human speech using acapela-box.com'
)

parser.add_argument('--print-url','-p',
                    action='store_true',
                    help='Only print the url to tts mp3 file. '\
                    'If not specified mplayer will automatically play the mp3'\
                   )

parser.add_argument('--quiet','-q',
                    action='store_true',
                    help='Don\'t print fancy status to stderr. '\
                    '--print-url will still work')

# store every argument other than above -args in a list.
# we assume it to be completely our tts text
parser.add_argument('text',nargs='+',
                    help='The text to speak. Use - to read from stdin')
args = parser.parse_args()

flag_print_url_only = args.print_url
flag_quiet = args.quiet
if args.text[0]=='-':
    tts_text = sys.stdin.read()
else:
    tts_text = ' '.join(args.text)


def info(info_str):
    if not flag_quiet:
        print(info_str,file=sys.stderr)

# urls
home_url=r'https://acapela-box.com/AcaBox/index.php'
post_url=r'https://acapela-box.com/AcaBox/dovaas.php'

# some params
speed='180'
vct='100' # voice shaping
# headers are simply included in the 'text' field of post data as \key=value\
header=r'\vct='+vct+'\ \spd='+speed+'\ '
# The text i'm gonna make him speak

# the post data
data={
    'text':header+tts_text,
    'voice':'rod22k',
    'listen':'1',
    'format':'MP3',
    'codecMP3':'1',
    'spd':speed,
    'vct':vct
}

session = requests.session()
# Just load the home page to initialize cookies
info('Initializing..')
session.get(home_url)
info('Connecting..')
# Now the real fun
request = session.post(post_url,data=data)

mp3_url = request.json()['snd_url']

if flag_print_url_only:
    print(mp3_url)
else:
    info('Playing..')
    subprocess.run(['mplayer','-really-quiet',mp3_url])

