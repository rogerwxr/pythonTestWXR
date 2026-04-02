import pandas as pd
import matplotlib.pyplot as plt

# --- 1. 数据读取 ---
# 修改点：添加 skiprows=1，跳过第一行垃圾数据
df = pd.read_csv('xbx.csv', encoding='gbk', skiprows=1)

# 打印前几行看看读取是否正确
print("前5行数据预览：")
print(df.head())

# 获取列名（防止列名有空格）
# 注意：跳过行之后，列名的索引可能会变，建议打印出来确认
print("实际列名：", df.columns.tolist())

# 假设跳过一行后，"交易日期" 变成了第3列（索引2），"收盘价" 是第8列（索引7）
date_col = df.columns[2]
close_col = df.columns[7]

# --- 2. 数据处理 ---
# 指定 format='%Y/%m/%d'
df['Date'] = pd.to_datetime(df[date_col], format='%Y/%m/%d')

df['年月'] = df['Date'].dt.to_period('M')

# 计算每月平均收盘价
monthly_avg = df.groupby('年月')[close_col].mean().reset_index()
monthly_avg['年月'] = monthly_avg['年月'].dt.start_time

# --- 3. 保存与绘图 ---
monthly_avg.to_csv('monthly_avg_close.csv', index=False, encoding='utf-8-sig')
print("✅ 统计完成")

plt.figure(figsize=(14, 7))
plt.plot(monthly_avg['年月'], monthly_avg[close_col], marker='o', linestyle='-')
plt.title('月度平均收盘价趋势图')
plt.xlabel('时间')
plt.ylabel('平均收盘价')
plt.gcf().autofmt_xdate()
plt.show()