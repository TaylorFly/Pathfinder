import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. 准备数据 (来源于您提供的实验结果文件)
data = {
    'Benchmark': ['450.soplex', '482.sphinx3', 'bfs-10', '605.mcf', 'cc-5'],
    'No Prefetch': [0.304502, 0.711897, 0.250297, 0.152961, 0.243320],
    'Best Offset': [0.353193, 1.172670, 0.395311, 0.152961, 0.243320],
    'SISB':        [0.384485, 1.264830, 0.394685, 0.153593, 0.247524],
    'Pathfinder':  [0.398401, 1.245940, 0.326901, 0.153593, 0.247524] 
    # 注: 这里假设 sisb_bo 组合即为您的 Pathfinder 实验组
}

df = pd.DataFrame(data)

# 2. 计算加速比 (Speedup = 当前IPC / No Prefetch IPC)
df['Speedup_BO'] = df['Best Offset'] / df['No Prefetch']
df['Speedup_SISB'] = df['SISB'] / df['No Prefetch']
df['Speedup_Pathfinder'] = df['Pathfinder'] / df['No Prefetch']

# 3. 设置绘图风格
# 使用 seaborn-darkgrid 风格会让图表更专业，适合学术 PPT
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    plt.style.use('ggplot') # 如果没有 seaborn 风格，回退到 ggplot

# ==========================================
# 图表 1: 加速比 (Speedup) - 推荐用于 PPT
# ==========================================
fig, ax = plt.subplots(figsize=(12, 6))

benchmarks = df['Benchmark']
x = np.arange(len(benchmarks))
width = 0.25  # 柱状图宽度

# 绘制柱子
rects1 = ax.bar(x - width, df['Speedup_BO'], width, label='Best Offset', color='#A9A9A9') # 灰色作为基准
rects2 = ax.bar(x, df['Speedup_SISB'], width, label='SISB', color='#87CEEB') # 浅蓝作为强力对手
rects3 = ax.bar(x + width, df['Speedup_Pathfinder'], width, label='Pathfinder (Ours)', color='#CD5C5C') # 红色突出您的工作

# 添加标签和标题
ax.set_ylabel('IPC Speedup (Normalized to Baseline)', fontsize=12)
ax.set_title('Performance Speedup: Pathfinder vs State-of-the-Art', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=11)
ax.legend(fontsize=10)
ax.axhline(y=1.0, color='black', linestyle='--', linewidth=1.5, alpha=0.7) # 基准线

# 在柱子上方添加数值标签函数
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}x',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 垂直偏移
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()
plt.savefig('pathfinder_speedup.png', dpi=300) # 保存高清图片
plt.show()

# ==========================================
# 图表 2: 原始 IPC 数值 - 备用
# ==========================================
fig2, ax2 = plt.subplots(figsize=(12, 6))

# 调整宽度以容纳4个柱子
width_ipc = 0.2

rects1_ipc = ax2.bar(x - 1.5*width_ipc, df['No Prefetch'], width_ipc, label='No Prefetch', color='black', alpha=0.3)
rects2_ipc = ax2.bar(x - 0.5*width_ipc, df['Best Offset'], width_ipc, label='Best Offset', color='#A9A9A9')
rects3_ipc = ax2.bar(x + 0.5*width_ipc, df['SISB'], width_ipc, label='SISB', color='#87CEEB')
rects4_ipc = ax2.bar(x + 1.5*width_ipc, df['Pathfinder'], width_ipc, label='Pathfinder', color='#CD5C5C')

ax2.set_ylabel('Instructions Per Cycle (IPC)', fontsize=12)
ax2.set_title('Raw IPC Performance Comparison', fontsize=14, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(benchmarks, fontsize=11)
ax2.legend()

plt.tight_layout()
plt.savefig('pathfinder_raw_ipc.png', dpi=300)
plt.show()