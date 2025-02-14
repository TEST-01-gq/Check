import os
import re
from deplog.config import TEST_DOCUMENT, LOG_PATH, LOG_FILE_NAME
from deplog.send import send_massage

logFile = os.path.join(LOG_PATH, LOG_FILE_NAME)

# 文件夹路径
path=os.getcwd()

#运行pathNow路径下的所有py文件
def run(document):
    if os.path.exists(logFile):
        with open(logFile, 'a+', encoding='utf-8') as documentLog:
            documentLog.truncate(0)
    pathNow=os.path.join(path,document)
    for file in os.listdir(pathNow):
        if os.path.splitext(file)[1]=='.py':
            absFilePath = os.path.join(pathNow, file)
            os.system('python "%s"' % absFilePath)
            # subprocess.run(['python', absFilePath], check=True)
    error_logs = get_record()
    send_massage(error_logs)

#读取log文件内容，获取error
def get_record():
    error_logs = []
    error_pattern = re.compile(r'.*ERROR.*', re.IGNORECASE)
    strip_pattern = re.compile(r'^error\s*', re.IGNORECASE)
    try:
        with open(logFile, encoding="utf-8") as f:
            for line in f:
                if error_pattern.search(line):
                    stripped_line = strip_pattern.sub('', line)
                    error_logs.append(stripped_line)  # 去除行尾的换行符并添加到列表中
    except FileNotFoundError:
        print(f"Error: The file '{logFile}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the log file: {e}")
        return []
    return error_logs

run(document=TEST_DOCUMENT)