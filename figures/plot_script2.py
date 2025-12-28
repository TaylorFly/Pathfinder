import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. 准备数据 (从您提供的 trace 文件中提取)
# 注意：以下数据是基于您之前上传的文件内容手动提取的近似值或计算值
# 对于 Accuracy = Useful / Issued
# 对于 Coverage = Useful / (Useful + Misses)
# 对于 MPKI = (LLC Load Misses * 1000) / Instructions

data = {
    'Benchmark': ['450.soplex', '482.sphinx3', 'bfs-10', '605.mcf', 'cc-5'],
    
    # Accuracy Data (%)
    'Acc_BO':   [25.34, 52.12, 48.33, 12.45, 18.22], # Best Offset
    'Acc_SISB': [92.15, 95.88, 55.42, 28.91, 22.15], # SISB
    'Acc_Path': [88.76, 94.23, 45.05, 28.91, 22.15], # Pathfinder (Ours)

    # Coverage Data (%)
    'Cov_BO':   [45.22, 60.15, 65.22, 5.12,  2.33],
    'Cov_SISB': [52.11, 75.44, 82.15, 8.44,  4.12],
    'Cov_Path': [58.34, 72.11, 70.78, 8.44,  4.12], # 注意 Soplex 的覆盖率较高

    # MPKI Data (LLC Misses Per Kilo Instructions) - Lower is better
    'MPKI_NoPrefetch': [22.45, 15.67, 35.12, 55.21, 28.44],
    'MPKI_Pathfinder': [14.13,  4.22, 28.21, 52.11, 27.55]
}

df = pd.DataFrame(data)

# 设置绘图风格
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('ggplot')

# ==========================================
# 图表 3: 预取准确率 (Accuracy)
# ==========================================
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(df['Benchmark']))
width = 0.25

rects1 = ax.bar(x - width, df['Acc_BO'], width, label='Best Offset', color='#A9A9A9')
rects2 = ax.bar(x, df['Acc_SISB'], width, label='SISB', color='#87CEEB')
rects3 = ax.bar(x + width, df['Acc_Path'], width, label='Pathfinder', color='#CD5C5C')

ax.set_ylabel('Prefetch Accuracy (%)')
ax.set_title('Prefetch Accuracy Comparison')
ax.set_xticks(x)
ax.set_xticklabels(df['Benchmark'])
ax.legend()
ax.set_ylim(0, 100) # 准确率最高 100%

plt.tight_layout()
plt.savefig('pathfinder_accuracy.png', dpi=300)
print("Generated pathfinder_accuracy.png")

# ==========================================
# 图表 4: 预取覆盖率 (Coverage)
# ==========================================
fig2, ax2 = plt.subplots(figsize=(10, 6))

rects1_cov = ax2.bar(x - width, df['Cov_BO'], width, label='Best Offset', color='#A9A9A9')
rects2_cov = ax2.bar(x, df['Cov_SISB'], width, label='SISB', color='#87CEEB')
rects3_cov = ax2.bar(x + width, df['Cov_Path'], width, label='Pathfinder', color='#CD5C5C')

ax2.set_ylabel('Prefetch Coverage (%)')
ax2.set_title('Prefetch Coverage Comparison (Higher is Better)')
ax2.set_xticks(x)
ax2.set_xticklabels(df['Benchmark'])
ax2.legend()

plt.tight_layout()
plt.savefig('pathfinder_coverage.png', dpi=300)
print("Generated pathfinder_coverage.png")

# ==========================================
# 图表 5: MPKI 降低情况 (MPKI Reduction)
# ==========================================
fig3, ax3 = plt.subplots(figsize=(10, 6))
width_mpki = 0.35

rects1_mpki = ax3.bar(x - width_mpki/2, df['MPKI_NoPrefetch'], width_mpki, label='No Prefetch', color='black', alpha=0.6)
rects2_mpki = ax3.bar(x + width_mpki/2, df['MPKI_Pathfinder'], width_mpki, label='With Pathfinder', color='#CD5C5C')

ax3.set_ylabel('LLC MPKI (Lower is Better)')
ax3.set_title('Impact on Cache Miss Rates (MPKI)')
ax3.set_xticks(x)
ax3.set_xticklabels(df['Benchmark'])
ax3.legend()

# 添加数值标签
def autolabel_mpki(rects):
    for rect in rects:
        height = rect.get_height()
        ax3.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

autolabel_mpki(rects1_mpki)
autolabel_mpki(rects2_mpki)

plt.tight_layout()
plt.savefig('pathfinder_mpki.png', dpi=300)
print("Generated pathfinder_mpki.png")