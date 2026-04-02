'''
邢不行 | 量化小讲堂系列
《Python量化神秘信号，15年来一旦出现，市场就变天！【量化投资邢不行】》
https://www.bilibili.com/video/BV1FQ4y1Q7qf?spm_id_from=333.999.0.0
获取更多量化文章，请联系邢不行个人微信：xbx971
'''

from datetime import datetime
import os
from multiprocessing import Pool

import matplotlib.pyplot as plt
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 获取文件路径
_ = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径
root_path = os.path.abspath(os.path.join(_, ''))  # 返回根目录文件夹
file_location = root_path + '/股票数据'
file_list = []

# 遍历股票交易数据（stock）文件夹，读取文件
for root, dirs, files in os.walk(file_location):
    for filename in files:
        if filename.endswith('.csv'):
            file_path = os.path.join(root, filename)
            file_path = os.path.abspath(file_path)
            file_list.append(file_path)

all_data = pd.DataFrame()

# 定义函数
def read_c_c(fp):
    print(fp)
    df = pd.read_csv(fp, skiprows=1, encoding='gbk')
    df['交易日期'] = pd.to_datetime(df['交易日期'])
    #  将数据合成月度数据
    rule_type = '1M'
    df = df.resample(rule=rule_type, on='交易日期', label='left', closed='left').agg(
        {
            '股票名称': 'first',
            '股票代码': 'first',
            '成交额': 'sum',
        }
    )
    df = df.reset_index()
    # 限定时间段
    df = df[df['交易日期'] >= pd.to_datetime('20061130')]
    df = df[df['交易日期'] <= pd.to_datetime('20240731')]
    return df

# 绘制策略曲线函数
def draw_equity_curve(df, time, data_dict, pic_size=[18, 9], dpi=72, font_size=25):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(pic_size[0], pic_size[1]), dpi=dpi)
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    for key in data_dict:
        plt.plot(df[time], df[data_dict[key]], label=key)
    plt.legend(fontsize=font_size)
    plt.tick_params(axis='x', labelsize=30)
    plt.show()

# 入口函数
if __name__ == '__main__':
    start_time = datetime.now()
    # 多进程
    with Pool(processes=4) as pool:

        df_list = pool.map(read_c_c, file_list)

        print('读入完成, 开始合并', datetime.now() - start_time)
        # 合并为一个大的DataFrame
        all_data = pd.concat([all_data] + df_list, ignore_index=True)

    all_data.sort_values(by='交易日期')
    all_data = all_data[all_data['成交额'] > 0]
    all_df = pd.DataFrame()

    # 计算总成交额及筛选成交额前5%个股
    for code, group in all_data.groupby('交易日期'):
        group['成交额排名'] = group['成交额'].rank(pct=True, ascending=False)
        group['总成交额'] = group['成交额'].sum()
        group = group[group['成交额排名'] <= 0.05]
        group['前5%成交额'] = group['成交额'].sum()
        all_df = pd.concat([all_df, group.iloc[[0]]])

    all_df.set_index(inplace=True, keys=['交易日期'])

    # 计算前5%个股成交额占比
    all_df['前5%个股成交额占比'] = all_df['前5%成交额'] / all_df['总成交额']
    all_df = all_df[['前5%成交额']+['总成交额']+['前5%个股成交额占比']]

    # 输出数据
    all_df.to_csv(root_path + '/前5%个股成交额占比.csv')
    print(all_df)

    # 绘制指标曲线
    all_df.reset_index(inplace=True)
    draw_equity_curve(all_df, '交易日期', {'前5%个股成交额占比': '前5%个股成交额占比'})

