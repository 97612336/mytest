file_path = "F:\BaiduNetdiskDownload\哈尔的移动城堡.mkv"

with open(file_path, "rb") as f:
    while 1:
        data = f.read(102400)
        print(len(data))
        # 对data进行操作
        with open("a.mkv", "ab+") as f2:
            f2.write(data)

        if len(data) == 0:
            break
