from moviepy.editor import VideoFileClip, concatenate_videoclips

file_path1 = "F:\BaiduNetdiskDownload\c1.mp4"
file_path2 = "F:\BaiduNetdiskDownload\c2.mp4"


clip1 = VideoFileClip(file_path1)
clip3 = VideoFileClip(file_path2)
final_clip = concatenate_videoclips([clip1, clip3])
final_clip.write_videofile("res1.mp4")
