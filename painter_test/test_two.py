import sys
import os
import uuid

from flask import Flask, request

app = Flask(__name__)

uuid_dict = {}


# 上传文件
@app.route('/upload', methods=['POST'])
def upload_file():
    name = request.form.get("name")
    team = ''
    if name == 'c' or name == 'd':
        team = 'a'
    elif name == 'e':
        team = 'b'
    # 获取当前目录，创建目录
    currnet_pwd = os.getcwd()
    tmp_path = currnet_pwd + '/' + team + '/' + name + '/'
    isExists = os.path.exists(tmp_path)
    if not isExists:
        os.makedirs(tmp_path)
    one_file = request.files.get('file')
    file_name = one_file.filename
    file_path = tmp_path + file_name
    with open(file_path, 'wb') as f:
        f.write(one_file.read())
    file_uuid = uuid.uuid1()
    print(file_uuid)
    print(type(file_uuid))
    uuid_dict[file_uuid] = file_path
    print(uuid_dict)
    return "200"


if __name__ == '__main__':
    # 获取终端输入参数
    sys_list = sys.argv
    if len(sys_list) > 1:
        port = int(sys_list[1])
    else:
        port = 8011
    app.run(port=port)
