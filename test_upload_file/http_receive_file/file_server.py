import sys
import time
import os

from flask import Flask, request

app = Flask(__name__)


@app.route('/upload', methods=["POST","GET"])
def receive_file():
    if request.method == 'GET':
        return "this is a get method"
    # 获取罪行的静态文件目录
    static_path = "/static_dir"
    # static_path = "F:\Python_project\/test_upload_file\http_receive_file"
    now_time = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    now_time_list = now_time.split(".")
    new_time_str = "/upload_file/" + now_time_list[0] + '_' + now_time_list[1] + '_' + now_time_list[2] + '/'
    # 判断上传文件目录是否存在，不存在则创建
    tmp_static_path = static_path + new_time_str
    isExists = os.path.exists(tmp_static_path)
    print(tmp_static_path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(tmp_static_path)
    # 获取相关参数
    code = request.form.get('code')
    # 判断code是否正确
    if code != "wangkun_123":
        return "error"
    # 获取具体的文件字节
    file = request.files.get("file")
    data = file.read()
    # 获取文件名
    file_name = request.form.get("file_name")
    # 获取文件扩展
    ext = request.form.get("ext")
    # 对参数进行写入操作
    tmp_file_name = file_name + ext  # 拼接文件名
    tmp_file_path = new_time_str + tmp_file_name  # 获取文件相对于upload_file的目录位置
    path_file_name = static_path + tmp_file_path  # 获取文件相对于整个系统的目录位置
    print(path_file_name)
    with open(path_file_name, "ab+") as f:
        f.write(data)
    # https://file.bigbiy.com/upload_file/2018-10-18/f3b9c8e6b3da10d1a5ddcf9dea9b56f3.jpg
    # 返回图片的链接
    print(tmp_file_path)
    return "https://file.bigbiy.com" + tmp_file_path


if __name__ == '__main__':
    # 获取终端输入参数
    sys_list = sys.argv
    if len(sys_list) > 1:
        port = int(sys_list[1])
    else:
        port = 8011
    app.run(port=port)
