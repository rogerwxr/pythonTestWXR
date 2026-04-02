import pandas as pd
import matplotlib.pyplot as plt

# --- 1. 数据读取与预处理 ---
# 读取CSV文件
# 注意：根据你提供的数据，第一行是标题，但前面有无关行，header=0 表示使用第一行作为列名
df = pd.read_csv('xbx.csv', header=0, encoding='gbk')#encoding='cp936'

# 将 '交易日期' 列转换为 datetime 类型
df['交易日期'] = pd.to_datetime(df['交易日期'])
date_column_name = df.columns[2]
close_column_name = df.columns[7] # 收盘价是第 8 列
# 提取 '年-月' 作为新的列用于分组
df['年月'] = df['交易日期'].dt.to_period('M')

# --- 2. 计算每月平均收盘价 ---
# 按 '年月' 分组，计算 '收盘价' 的平均值
monthly_avg = df.groupby('年月')['收盘价'].mean().reset_index()

# 将 Period 转换回 datetime 以便绘图显示更美观
monthly_avg['年月'] = monthly_avg['年月'].dt.start_time

# --- 3. 保存结果到新CSV ---
monthly_avg.to_csv('monthly_avg_close.csv', index=False, encoding='utf-8-sig')
print("✅ 月度平均收盘价已保存到 'monthly_avg_close.csv'")

# --- 4. 绘制折线图 ---
plt.figure(figsize=(14, 7))
plt.plot(monthly_avg['年月'], monthly_avg['收盘价'], marker='o', linestyle='-', color='b')

# 设置图表标题和标签
plt.title('星昊医药月度平均收盘价趋势图 (2023-2025)', fontsize=16, fontweight='bold')
plt.xlabel('交易月份', fontsize=12)
plt.ylabel('平均收盘价 (元)', fontsize=12)

# 优化日期显示格式
plt.gcf().autofmt_xdate() # 旋转日期标签
plt.grid(True, alpha=0.3)

# 显示数值 (可选，数据点多时可能拥挤)
for i, row in monthly_avg.iterrows():
    plt.annotate(f"{row['收盘价']:.2f}",
                 (row['年月'], row['收盘价']),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center', fontsize=9)

# 保存图片
plt.savefig('monthly_trend.png', dpi=200, bbox_inches='tight')
print("✅ 折线图已保存为 'monthly_trend.png'")
plt.show()