import requests
import logging
from deplog.config import LOG_FILE_NAME, URL

#日志配置
logging.basicConfig(filename='send.log', level=logging.INFO)
logger = logging.getLogger('send_massage')

#发送钉钉消息
def send_massage(error_log):
    error = ""
    n = 0
    for error_log in error_log:
        if n < 10:
           error += error_log + "\n"
           n += 1
        else:
           error = error+"....\n\n\n错误消息过多"
           break
    data = {
        "msgtype": "text",
        "text": {
            "content": f"测试异常：检测到{n}条错误消息，请查看日志"
        }
    }
    try:
        if URL != '':
            response = requests.post(URL, json=data)
            response.raise_for_status()
            logger.info(f"发送钉钉消息成功，状态码：{response.status_code}")
        else:
            logger.info("未配置钉钉机器人URL，不发送消息")
    except requests.exceptions.RequestException as e:    
            logger.error(f"发送钉钉消息失败，错误信息：{e}")
