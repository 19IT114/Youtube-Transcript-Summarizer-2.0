import pytube
def Download_Video(url):
  YT_obj =pytube.YouTube(url=url)
  print(YT_obj.title)
  video = YT_obj.streams.get_by_itag('22')
  print('Video is downloading')
  video.download(filename='video.mp4')
  print('Done')

def Video_link(video):
    videos = []
    url = video
    videos.append(url)
    for video in videos:
        Download_Video(video)

# if __name__=="__main__":
#     print('helo')
#     vid = input()
#     Video_link(vid)
