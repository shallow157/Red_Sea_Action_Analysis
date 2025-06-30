# 《红海行动》豆瓣评论数据分析项目
项目概述
基于豆瓣平台《红海行动》短评数据，通过爬虫获取、文本处理、多维分析与可视化，挖掘观众评分分布、情感倾向及时空特征，为军事题材电影市场分析提供数据支持。
技术栈
数据采集：Python + Selenium（突破豆瓣反爬机制）
数据处理：Pandas + Regex + Jieba（文本清洗与分词）
数据分析：Numpy + 统计模型
可视化：Matplotlib + Pyecharts + WordCloud
目录结构
plaintext
.
├── code/              # 核心代码

├── data/              # 原始数据与处理后数据

├── docs/              # 分析报告与可视化结果

├── requirements.txt   # 环境依赖

└── README.md          # 项目说明
快速开始
1. 环境配置
bash
# 克隆仓库
git clone https://github.com/shallow157/Red_Sea_Action_Analysis.git
cd Red_Sea_Action_Analysis

# 安装依赖
pip install -r requirements.txt

# 安装ChromeDriver（需与本地Chrome版本匹配）
# 可通过pip install webdriver-manager自动管理
2. 运行项目
bash
# 执行主脚本（默认跳过爬虫，使用已保存数据）
python code/main.py

# 如需重新爬取数据（建议谨慎操作，避免IP封禁）
python code/data_crawler.py
项目成果
1. 数据概况
爬取豆瓣短评 600 条，包含评分、评论内容、时间、城市等 7 个字段
数据清洗后有效样本率 98.3%，文本分词准确率达 92%
2. 核心发现
评分分布：4-5 星好评占比 66.78%，首映后一周评论量爆发
情感特征：好评集中于 “场面”“主旋律”，差评聚焦 “暴力”“剧情”
地域差异：北京、上海评论量占比超 30%，一线城市好评率显著更高
3. 可视化成果
评分饼图、评论时间趋势图（见docs/visualization_results/）
省份评论分布地图、好评 / 差评词云图
项目亮点
反爬策略：结合 Selenium 模拟滚动与动态等待，突破豆瓣评论加载限制
文本处理：自定义军事术语词典与停用词表，提升分词准确性
多维分析：融合时间序列、地域分布与情感挖掘，提供立体洞察
贡献指南
如需优化代码或补充分析，可提交 Pull Request
建议方向：
增加 LDA 主题模型分析评论主题分布
整合更多电影数据进行对比研究
开发交互式可视化仪表盘
联系方式
如有问题，可通过 README.md 中预留的邮箱或 Issue 反馈
四、注意事项
数据合规：爬取豆瓣数据需遵守平台规则，建议设置合理请求间隔（如time.sleep(3)）
图表显示：Obsidian 中 Mermaid 图表可正常渲染，GitHub 需通过插件或图片展示
代码可复现：确保requirements.txt包含所有依赖，数据路径配置统一
