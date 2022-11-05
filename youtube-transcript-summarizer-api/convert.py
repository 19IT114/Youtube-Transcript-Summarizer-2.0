import moviepy.editor
filename = "video.mp4"
obj = moviepy.editor.VideoFileClip(filename=filename)
obj.audio.write_audiofile(filename[:-4] + '.mp3')
obj.close()