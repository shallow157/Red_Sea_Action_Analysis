#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《红海行动》评论数据可视化
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pyecharts import options as opts
from pyecharts.charts import Map, Line, Pie
from pyecharts.globals import ThemeType
import os

class DataVisualizer:
    def __init__(self, data_path="../data/cleaned_data.csv"):
        """初始化可视化"""
        self.data_path = data_path
        self.df = self._load_data()
        self.output_dir = "../docs/visualization_results/"
        os.makedirs(self.output_dir, exist_ok=True)
        plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
        plt.rcParams["axes.unicode_minus"] = False
    
    def _load_data(self):
        """加载处理后的数据"""
        try:
            df = pd.read_csv(self.data_path)
            print(f"加载数据成功，共{len(df)}条记录")
            return df
        except Exception as e:
            print(f"加载数据失败: {e}")
            return pd.DataFrame()
    
    def plot_rating_distribution(self):
        """绘制评分分布饼图"""
        if self.df.empty:
            return
        
        # 计算评分分布
        rating_counts = self.df['score_numeric'].value_counts(bins=5, sort=False)
        labels = ['1星(10分)', '2星(20分)', '3星(30分)', '4星(40分)', '5星(50分)']
        
        # 绘制饼图
        plt.figure(figsize=(8, 8))
        wedges, texts, autotexts = plt.pie(
            rating_counts, 
            labels=labels, 
            autopct="%1.2f%%", 
            startangle=140,
            explode=[0.1 if i in [3, 4] else 0 for i in range(5)]  # 突出好评
        )
        
        # 调整标签字体
        for text in texts + autotexts:
            text.set_fontsize(10)
        
        plt.title("《红海行动》豆瓣评分分布", fontsize=15)
        plt.savefig(f"{self.output_dir}/rating_pie_chart.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("评分饼图已保存")
    
    def plot_comment_time_series(self):
        """绘制评论时间序列图"""
        if self.df.empty:
            return
        
        # 按日期统计评论数
        date_counts = self.df['date'].value_counts().sort_index()
        
        # 绘制趋势图
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=date_counts.index, y=date_counts.values, marker='o', color='red')
        plt.title("评论数量随时间变化趋势", fontsize=15)
        plt.xlabel("日期", fontsize=12)
        plt.ylabel("评论数量", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # 标记首映周
        first_week = date_counts.index[:7]
        plt.fill_between(first_week, date_counts[first_week], alpha=0.3, color='lightcoral')
        
        plt.savefig(f"{self.output_dir}/comment_time_trend.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("评论时间趋势图已保存")
    
    def plot_hourly_comment_distribution(self):
        """绘制按小时评论分布"""
        if self.df.empty:
            return
        
        # 按小时统计评论数
        hour_counts = self.df['hour'].value_counts().sort_index()
        hours = list(range(24))
        counts = [hour_counts.get(str(h), 0) for h in hours]
        
        # 绘制柱状图
        plt.figure(figsize=(10, 6))
        plt.bar(hours, counts, color='skyblue', alpha=0.7)
        plt.title("评论数量按小时分布", fontsize=15)
        plt.xlabel("小时", fontsize=12)
        plt.ylabel("评论数量", fontsize=12)
        plt.xticks(hours)
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        plt.savefig(f"{self.output_dir}/hourly_comment_distribution.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("按小时评论分布图已保存")
    
    def plot_province_comment_map(self):
        """绘制省份评论分布地图"""
        if self.df.empty:
            return
        
        # 处理城市到省份的映射（简化版，实际需更完整的映射表）
        city_to_province = {
            '北京': '北京', '上海': '上海', '广州': '广东', '深圳': '广东',
            '杭州': '浙江', '南京': '江苏', '成都': '四川', '重庆': '重庆',
            '武汉': '湖北', '西安': '陕西', '长沙': '湖南', '天津': '天津',
            '青岛': '山东', '济南': '山东', '郑州': '河南', '沈阳': '辽宁'
        }
        
        # 统计各省份评论数
        province_counts = {}
        for city in self.df['city'].dropna():
            province = city_to_province.get(city, "其他")
            province_counts[province] = province_counts.get(province, 0) + 1
        
        # 准备Pyecharts地图数据
        map_data = [(k, v) for k, v in province_counts.items() if v > 0]
        
        # 创建地图
        map_chart = (
            Map(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1200px", height="800px"))
            .add("评论数量", map_data, "china", is_map_symbol_show=False)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="各省份评论数量分布"),
                visualmap_opts=opts.VisualMapOpts(
                    min_=0, max_=max(province_counts.values()) if province_counts else 100,
                    range_text=["高", "低"], range_color=["lightcoral", "lightskyblue"]
                ),
                toolbox_opts=opts.ToolboxOpts(is_show=True)
            )
        )
        
        # 保存为HTML
        map_chart.render(f"{self.output_dir}/province_comment_map.html")
        print("省份评论地图已保存为HTML")
    
    def run(self):
        """执行可视化主流程"""
        print("开始数据可视化...")
        self.plot_rating_distribution()
        self.plot_comment_time_series()
        self.plot_hourly_comment_distribution()
        self.plot_province_comment_map()
        print("可视化完成")

if __name__ == "__main__":
    visualizer = DataVisualizer()
    visualizer.run()