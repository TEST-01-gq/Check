import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from deplog.config import TABLE_PATH
from deplog.log import log, info


skip_rows = [0,2,3,4]

df = pd.read_excel(TABLE_PATH+'fragment~武将碎片表.xlsx', sheet_name='武将碎片道具',skiprows=skip_rows)
df_wujiang = pd.read_excel(TABLE_PATH+'hero_star~武将基础配置表.xlsx', sheet_name='数据表',skiprows=skip_rows,usecols=('hid','name','htype'))
df_wujiang_unique = df_wujiang.drop_duplicates()

#检查武将和道具的关联性

df_daoju = df[['fragment_id','beizhu','name','htype']]
merge_df = pd.merge(df_daoju,df_wujiang_unique,left_on='beizhu',right_on='hid',how='left')
merge_df['name_z'] = merge_df['name_y'] + '-碎片'

mismatched_rows = merge_df[merge_df['beizhu'] != (merge_df['fragment_id'] - 70000)]
if not mismatched_rows.empty:
    msg="不符合条件的行："+str(mismatched_rows)
    log.error(msg)
mismatched_rows_id  = merge_df[merge_df['beizhu'] != (merge_df['hid'])]
if not mismatched_rows_id.empty:
    msg="武将id对应不上的数据:"+str(mismatched_rows_id)
    log.error(msg)
else:
    msg="武将id和道具id一致性检查通过"
    info.info(msg)
mismatched_rows_type = merge_df[merge_df['htype_x'] != (merge_df['htype_y']) + 5]
if not mismatched_rows_type.empty:
    msg="武将兵种和碎片兵种对应不上的数据:"+str(mismatched_rows_type)
    log.error(msg)
else:
    msg="武将兵种和道具兵种一致性检查通过"
    info.info(msg)
mismatched_rows_name = merge_df[merge_df['name_x'] != (merge_df['name_z'])]
if not mismatched_rows_name.empty:
    msg="武将名称和碎片名称对应不上的数据:"+str(mismatched_rows_name)
    log.error(msg)
else:
    msg="武将名称和碎片名称一致性检查通过"
    info.info(msg)

correct_models = {1: '1|11|1', 2: '1|11|2', 3: '1|11|3',4:'1|11|20',5:'1|19|200'}
wrong_fenjie = 0
for index,row in df.iterrows():
    expected_model = correct_models[row['quality']]

    if row['smash_reward_goods'] != expected_model:
        wrong_fenjie += 1
        msg=str(row['name'])+str(row['fragment_id'])+"碎片品质对应不上分解的材料"
        log.error(msg)
if wrong_fenjie == 0:
    msg="武将碎片拆解道具检查通过"
    info.info(msg)
