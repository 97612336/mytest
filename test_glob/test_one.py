import glob

log_file_list = glob.glob("/var/log/nginx/mylog*.log")

for one in log_file_list:
    print(one)