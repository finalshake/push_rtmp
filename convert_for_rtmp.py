#!/usr/bin/env python3
# -*-coding: utf-8 -*-

__version__ = "0.0.1"
__aurthor__ = "Shake"
import ffmpeg
import optparse
import os
import json
from multiprocessing import cpu_count

cpus = cpu_count()

def main():
    parser = optparse.OptionParser('usage%pro ' + '-i <input folder>' + '-o <output folder>')
    parser.add_option('-i', dest='input', type='string', help='specify input folder')
    parser.add_option('-o', dest='output', type='string', help='specify output folder')
    (option, args) = parser.parse_args()
    input = option.input
    output = option.output
    if(input == None or output == None):
        print(parser.usage)
        exit(0)

    if not os.path.isdir(input) or not os.path.isdir(output):
        print("input/output must be a directory")
        exit(0)

    make_video(input, output)

    # js = ffmpeg.probe(video)
    # with open('test.json','w') as f:
        # json.dump(js, f, indent=2)

    # stream = ffmpeg.input('Video/阳光电影www.ygdy8.com. 骡子.BD.720p.中英双字幕.mkv', re=None)
    # stream = ffmpeg.output(stream, "rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_179138671_4350625&key=8495c3b70e5655ed2628b51044f47643&schedule=rtmp", vcodec='copy', acodec='aac', audio_bitrate='192k', format='flv')
    # print(ffmpeg.compile(stream))
    # ffmpeg.run(stream)
def make_video(input, output):
    # skip none video files
    for file in os.listdir(input):
        if not (file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.flv') or file.endswith('.avi') or file.endswith('.rmvb') or file.endswith('.rm') or file.endswith('.mpg')):
            continue

        srt_exist = None
        has_soft_srt = False
        soft_srt_stream = 0

        video = os.path.join(input, file)

        # check if there's subtitle file
        srt_exists = os.path.splitext(video)[0] + '.srt'
        if os.path.exists(srt_exists):
            srt_exist = srt_exists

        # check if there's soft subtitle stream
        js = ffmpeg.probe(video)
        if ('subtitle' in str(js)):
            has_soft_srt = True
            stream = js['format']['nb_streams']
            for i in range(stream):
                if js['streams'][i]['codec_type'] == 'subtitle':
                    soft_srt_stream = i
                    break

        # do convert video
        if video.endswith('.mkv'):
            if srt_exist is not None:
                burn_srt(video, srt_exist, output)
            elif has_soft_srt:
                srt, nsvideo = split_soft_srt(video, soft_srt_stream)
                burn_srt(nsvideo, srt, output)
            # else:
                # move(video, output)
        elif video.endswith('.rmvb') or video.endswith('.rm') or video.endswith('.avi'):
            if srt_exist is not None:
                add_srt_convert(video, srt_exist, output)
            else:
                convert(video, output)
        else:
            if srt_exist is not None:
                add_soft_srt(video, srt_exist, output)
            # else:
                # move(video, output)

def burn_srt(video, srt, output):
    # ffmpeg -i /Video/CHD-The-Warlords.mkv -vf subtitles=BluRay.简中.ass  output
    global cpus
    stream = ffmpeg.input(video)
    outputfile = os.path.join(output, os.path.split(video)[1])
    stream = ffmpeg.output(stream, outputfile, threads=cpus, vf='subtitles=%s'%srt)
    print(ffmpeg.compile(stream))
    ffmpeg.run(stream)

def split_soft_srt(video, soft_srt_stream):
    # ffmpeg -i test2.mkv -map 0:v -map 0:a -c copy test_video.mkv -map 0:s -c copy test_srt.srt
    stream = ffmpeg.input(video)
    srt = os.path.splitext(video)[0] + '.srt'
    srt = os.path.join('/tmp', os.path.split(srt)[1])
    nsvideo = os.path.join('/tmp', os.path.split(video)[1])
    
    out_srt = ffmpeg.output(stream[str(soft_srt_stream)], srt)
    out_video = ffmpeg.output(stream['a'], stream['v'], nsvideo)
    stream = ffmpeg.merge_outputs(out_srt, out_video)
    print(ffmpeg.compile(stream))
    ffmpeg.run(stream)
    return srt, nsvideo

def add_srt_convert(video, srt_exist, output):
    global cpus
    outputfile = os.path.join(output, os.path.split(video)[1])
    outputfile = os.path.splitext(outputfile)[0] + '.mp4'
    video_stream = ffmpeg.input(video)
    stream = ffmpeg.output(video_stream, outputfile, threads=cpus, vf='subtitles=%s'%srt_exist)
    print(ffmpeg.compile(stream))
    ffmpeg.run(stream)

def convert(video, output):
    global cpus
    outputfile = os.path.join(output, os.path.split(video)[1])
    outputfile = os.path.splitext(outputfile)[0] + '.mp4'
    stream = ffmpeg.input(video)
    stream = ffmpeg.output(stream, outputfile, threads=cpus)
    print(ffmpeg.compile(stream))
    ffmpeg.run(stream)

def add_soft_srt(video, srt_exist, output):
    outputfile = os.path.join(output, os.path.split(video)[1])
    stream = ffmpeg.input(video)
    srt_stream = ffmpeg.input(srt_exist)
    stream = ffmpeg.output(stream, srt_stream, outputfile, codec='copy', scodec='srt')
    print(ffmpeg.compile(stream))
    ffmpeg.run(stream)

if __name__ == '__main__':
    main()
