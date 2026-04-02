import pandas as pd
import matplotlib.pyplot as plt

# --- 1. 数据读取 ---
# 使用 gbk 编码读取
df = pd.read_csv('xbx.csv', encoding='gbk')

# ⚡ 核心修复：使用列的整数位置索引来选取“交易日期”列
# df.columns[2] 代表第 3 列（Python 索引从0开始）
date_column_name = df.columns[2]
close_column_name = df.columns[7] # 收盘价是第 8 列

# --- 2. 数据处理 ---
# 重命名方便后续操作，或者直接使用变量
df['Date'] = pd.to_datetime(df[date_column_name])
df['年月'] = df['Date'].dt.to_period('M')

# 计算每月平均收盘价
monthly_avg = df.groupby('年月')[close_column_name].mean().reset_index()
monthly_avg['年月'] = monthly_avg['年月'].dt.start_time

# --- 3. 保存结果 ---
monthly_avg.to_csv('monthly_avg_close.csv', index=False, encoding='utf-8-sig')
print("✅ 数据已保存")

# --- 4. 绘图 ---
plt.figure(figsize=(14, 7))
plt.plot(monthly_avg['年月'], monthly_avg[close_column_name], marker='o', linestyle='-')
plt.title('月度平均收盘价趋势图')
plt.xlabel('月份')
plt.ylabel('平均价格')
plt.gcf().autofmt_xdate()
plt.savefig('monthly_trend.png', dpi=200, bbox_inches='tight')
plt.show()