import os


def scan_path(ph):
    print(ph)
    file_list = os.listdir(ph)
    for obj in file_list:
        print(obj)
        obj_path = ph + "/" + obj
        if os.path.isfile(obj_path):
            # print(obj)
            pass
        elif os.path.isdir(obj_path):
            scan_path(obj_path)


if __name__ == '__main__':
    path = os.getcwd()
    scan_path(path)
