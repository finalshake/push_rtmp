#!/usr/bin/env python3
# -*-coding: utf-8 -*-

__version__ = "0.0.1"
__aurthor__ = "Shake"

import optparse
import os
import ffmpeg
import json
from multiprocessing import cpu_count

cpus = cpu_count()
def main():
    with open('test.json', 'r') as f:
        js = json.load(f)
    if ('subtitle' in str(js)):
        print('yes')
    stream = js['format']['nb_streams']
    print(stream)
    for i in range(3):
        if js['streams'][i]['codec_type'] == 'subtitle':
            print(i)
    print(os.path.splitext('/video/1.mp3'))
    print(os.path.split('/video/1.mp3'))

    video = '/Video/CHD-The-Warlords.mkv'
    output = '/home/shake/test3.mkv'
    srt = 'Downloads/投名状.The.Warlords.2007.BluRay/投名状.The.Warlords.2007.BluRay.简中.srt'
    stream = ffmpeg.input(video)
    # stream = ffmpeg.filter(stream, 'video', subtitles=srt)
    stream = ffmpeg.output(stream, output, threads=cpus, vf='subtitles=%s'%srt)
    print(ffmpeg.compile(stream))
    # ffmpeg.run(stream)

    # split_soft_srt('test2.mkv')
    # add_srt_convert('1.avi', '1.srt', '/tmp')
    # convert('1.rm', '/tmp')
    add_soft_srt('/home/shake/video/kk.mp4', '/tmp.srt', '/home/shake/tmp')

def add_soft_srt(video, srt_exist, output):
    outputfile = os.path.join(output, os.path.split(video)[1])
    stream = ffmpeg.input(video)
    srt_stream = ffmpeg.input(srt_exist)
    stream = ffmpeg.output(stream, srt_stream, outputfile, scodec='srt')
    print(ffmpeg.compile(stream))
def convert(video, output):
    global cpus
    outputfile = os.path.join(output, os.path.split(video)[1])
    outputfile = os.path.splitext(outputfile)[0] + '.mp4'
    stream = ffmpeg.input(video)
    stream = ffmpeg.output(stream, outputfile, threads=cpus)
    print(ffmpeg.compile(stream))
def add_srt_convert(video, srt_exist, output):
    global cpus
    outputfile = os.path.join(output, os.path.split(video)[1])
    outputfile = os.path.splitext(outputfile)[0] + '.mp4'
    video_stream = ffmpeg.input(video)
    stream = ffmpeg.output(video_stream, outputfile, threads=cpus, vf='subtitles=%s'%srt_exist)
    print(ffmpeg.compile(stream))
def split_soft_srt(video):
    # ffmpeg -i test2.mkv -map 0:v -map 0:a -c copy test_video.mkv -map 0:s -c copy test_srt.srt
    stream = ffmpeg.input(video)
    srt = os.path.splitext(video)[0] + '.srt'
    srt = os.path.join('/tmp', os.path.split(srt)[1])
    nsvideo = os.path.join('/tmp', os.path.split(video)[1])
    
    out_srt = ffmpeg.output(stream['s'], srt)
    out_video = ffmpeg.output(stream['a'], stream['v'], nsvideo)
    stream = ffmpeg.merge_outputs(out_srt, out_video)
    print(ffmpeg.compile(stream))
    return srt, nsvideo
if __name__ == '__main__':
    main()
