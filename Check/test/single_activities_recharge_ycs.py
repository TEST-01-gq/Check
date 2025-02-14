import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from deplog.config import TABLE_PATH
from deplog.log import log, info

skip_rows = [0,2,3,4]

df = pd.read_excel(TABLE_PATH+'activities_turntable_recharge~锦鲤池累积充值.xlsx', sheet_name='Sheet1',skiprows=skip_rows)

# 检查第一列是否为自增
def check_auto_increment(df) -> None:
    for i in range(1, len(df)):
        if i < 399:
            if df.iloc[i, 0] != df.iloc[i - 1, 0] + 1:
                msg = "锦鲤池累计充值表：" + str(i + 6) + "\t检查完毕，该行自增有误,与上述值相比并未加1\n" + str(df.iloc[i,0])
                log.error(msg)
            elif df.iloc[i + 1, 0] != df.iloc[i, 0] + 1:
                msg = "锦鲤池累计充值表：" + str(i + 6) + "\t检查完毕，该行自增有误,与上述值相比并未加1\n" + str(df.iloc[i,0])
                log.error(msg)

check_auto_increment(df)

# 检查第二列是否只有 1 和 2
def check_type_column(df) -> None:
    column_name = df.columns[1]  # 获取第二列的列名
    invalid_values = df[~df[column_name].isin([1, 2])]
    if not invalid_values.empty:
        for index, row in invalid_values.iterrows():
            msg = "锦鲤池累计充值表：" + str(index + 1) + "\t检查完毕，该行存在除1和2之外的值\n" + str(row[column_name])
            log.error(msg)
    else:
        msg = "未发现除1和2以外的值"
        log.error(msg)

check_type_column(df)

# 检查第三列是否为数字
def check_price_column(df) -> None:
    column_name = df.columns[2]  # 获取第三列的列名
    for i in range(1, 399):
        if df.loc[df.index[i], column_name] != df.loc[df.index[i - 1], column_name] + 30:
            msg = "锦鲤池累计充值表：" + str(i + 6) + "\t检查完毕，该行逐行增加未达30\n" + str(df.loc[df.index[i - 1], column_name] + 30)
            log.error(msg)

    for i in range(400, 409):
        if df.loc[df.index[i + 1], column_name] != df.loc[df.index[i], column_name] + 10:
            msg = "锦鲤池累计充值表：" + str(i + 6) + "\t检查完毕，该行逐行增加未达10\n" + str(df.loc[df.index[i - 1], column_name] + 30)
            log.error(msg)

    for i in range(410, 414):
        if df.loc[df.index[i], column_name] != df.loc[df.index[i - 1], column_name] + 20:
            msg = "锦鲤池累计充值表：" + str(i + 6) + "\t检查完毕，该行逐行增加未达20\n" + str(df.loc[df.index[i - 1], column_name] + 30)
            log.error(msg)

    for i in range(415, 419):
        if df.loc[df.index[i], column_name] != df.loc[df.index[i - 1], column_name] + 20:
            msg = "锦鲤池累计充值表：" + str(i + 6) + "\t检查完毕，该行逐行增加未达20\n" + str(df.loc[df.index[i - 1], column_name] + 30)
            log.error(msg)

    for i in range(420, 424):
        if df.loc[df.index[i], column_name] != df.loc[df.index[i - 1], column_name] + 20:
            msg = "锦鲤池累计充值表：" + str(i + 6) + "\t检查完毕，该行逐行增加未达20\n" + str(df.loc[df.index[i - 1], column_name] + 30)
            log.error(msg)

check_price_column(df)

# 检查第四列是否符合 道具类型|道具ID|ID 格式
def check_packet_id_column(df, valid_items) -> None:
    column_name = df.columns[3]  # 获取第四列的列名
    invalid_rows = []  # 记录无效的行

    for index, row in df.iterrows():
        value = row[column_name]
        if not isinstance(value, str):
            msg = "锦鲤池累计充值表：" + str(index + 1) + "\t道具类型不在已知类型内\n" + str(value)
            log.error(msg)
            invalid_rows.append(index + 1)
            continue

        parts = value.split("|")
        if len(parts) != 3:
            msg = "锦鲤池累计充值表：" + str(index + 1) + "\t道具ID不在已知道具ID内\n" + str(value)
            log.error(msg)
            invalid_rows.append(index + 1)
            continue

        item_type, item_id, id_value = parts
        if (item_type, item_id, id_value) not in valid_items:
            msg = "锦鲤池累计充值表：" + str(index + 1) + "\tID不在已知ID内\n" + str(value)
            log.error(msg)
            invalid_rows.append(index + 1)

    if not invalid_rows:
        info(f"列 '{column_name}' 检查通过: 所有值均有效")
    else:
        info(f"列 '{column_name}' 检查失败: 无效行号 {invalid_rows}")

check_packet_id_column()