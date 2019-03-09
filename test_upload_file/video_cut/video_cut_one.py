import moviepy.editor as mpy

file_path = "F:\BaiduNetdiskDownload\哈尔的移动城堡.mkv"
# file_path="res1.mp4"

# 视频文件的本地路径
content = mpy.VideoFileClip(file_path)
# 剪辑78分55秒到79分6秒的片段。注意：不使用resize则不会修改清晰度
clip = content.subclip((0, 5), (0, 9))
# 将片段保存为gif图到python的默认路径，可保存到"C:\Users\Administrator\Desktop"
clip.write_gif("dog.gif", program='ffmpeg')
