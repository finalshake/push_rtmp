#!/usr/bin/env python3

__version__ = "0.0.1"
__aurthor__ = "Shake"

import ffmpeg
import optparse
import os

def main():
    parser = optparse.OptionParser('usage%pro' + '-i <input video folder>')
    parser.add_option('-i', dest='input', type='string', help='specify input video folder')
    (option, args) = parser.parse_args()
    input = option.input
    if (input == None):
        print(parser.usage)
        exit(0)

    while True:
        videos = os.listdir(input)
        print(videos)
        videos.sort()
        print(videos)
        for video in videos:
            video_to_push = os.path.join(input, video)
            stream = ffmpeg.input(video_to_push, re=None)
            stream = ffmpeg.output(stream, "rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_179138671_4350625&key=8495c3b70e5655ed2628b51044f47643&schedule=rtmp", vcodec='copy', acodec='aac', audio_bitrate='192k', format='flv')
            print(ffmpeg.compile(stream))
            ffmpeg.run(stream)
if __name__ == '__main__':
    main()
