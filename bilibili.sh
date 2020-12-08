#!/bin/sh

#视频文件目录
dir=$1

#如果参数不是目录，则提醒输入目录，结束 
if [ ! -d $dir ]; then
	echo "$dir is not a dir."
	exit -1
fi

#保证目录名后面以/结尾
if [ ${dir:-1} != '/' ]; then
	dir=$dir/
fi

#开始循环
while true
do
  for video in $dir*
  do
    if [ -d $video ];then
      continue
    fi
    if [[ $video =~ \.mp4$ || $video =~ \.mkv$ || $video =~ \.flv$ || $video =~ \.avi$ || $video =~ \.rmvb$ || $video =~ \.rm$ || $video =~ \.mpg$ ]];then
      echo $video
	    ffmpeg -re -i "$video" -vcodec copy -acodec aac -b:a 192k -f flv "rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_179138671_4350625&key=8495c3b70e5655ed2628b51044f47643&schedule=rtmp"
    fi
  done
done



