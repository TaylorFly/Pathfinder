# 北京工业大学多核体系结构大作业Repo
__小组成员__: 尚凡胜、李高飞

# 实验流程
克隆Pathfinder仓库 
``` git clone https://github.com/linjiaty/Pathfinder.git ```
创建conda环境
```
cd ChampSim
conda env create -f environment.yml
conda activate snn-champ_test
```
编译 pathfinder
```
./ml_prefetch_sim.py build
```

准备数据, 数据将下载到ChampSim/gap_spec_traces中
```
bash download.sh
```

运行
```
run_pathfinder_gap_spec.sh
```

运行结果位于```ChampSim/results```中，如```ChampSim/results/450.soplex-s0.trace.gz-hashed_perceptron-no-no-no-bo-lru-1core.txt```
表示不同的benchmark上Baseline、两个对比组、pathfinder的结果，结果包括IPC,预取准确率,预取覆盖率