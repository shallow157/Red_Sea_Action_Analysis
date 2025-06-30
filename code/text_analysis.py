#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《红海行动》评论文本分析
"""
import pandas as pd
from collections import Counter
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

class TextAnalyzer:
    def __init__(self, data_path="../data/cleaned_data.csv"):
        """初始化文本分析"""
        self.data_path = data_path
        self.df = self._load_data()
        self.output_dir = "../docs/visualization_results/wordclouds/"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _load_data(self):
        """加载预处理后的数据"""
        try:
            df = pd.read_csv(self.data_path)
            print(f"加载处理后数据成功，共{len(df)}条记录")
            return df
        except Exception as e:
            print(f"加载数据失败: {e}")
            return pd.DataFrame()
    
    def classify_comments(self, threshold=30):
        """将评论分为好评和差评"""
        if self.df.empty:
            return {}, {}
        
        # 以30分为阈值分类
        good_comments = self.df[self.df['score_numeric'] >= threshold]['tokens']
        bad_comments = self.df[self.df['score_numeric'] < threshold]['tokens']
        
        print(f"好评数: {len(good_comments)}, 差评数: {len(bad_comments)}")
        return good_comments, bad_comments
    
    def extract_keywords(self, comments, top_n=50):
        """提取高频关键词"""
        all_words = []
        for tokens in comments:
            all_words.extend(tokens)
        
        word_counter = Counter(all_words)
        return word_counter.most_common(top_n)
    
    def generate_wordcloud(self, keywords, title, mask_path=None):
        """生成词云图"""
        # 转换关键词为字典格式
        word_dict = dict(keywords)
        
        # 配置词云
        wc = WordCloud(
            font_path="C:/Windows/Fonts/simhei.ttf",  # 中文黑体字体路径
            background_color="white",
            width=800,
            height=600,
            max_words=100,
            mask=plt.imread(mask_path) if mask_path else None
        )
        
        # 生成词云
        wc.generate_from_frequencies(word_dict)
        
        # 保存图片
        plt.figure(figsize=(10, 8))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title(title, fontsize=15)
        plt.savefig(f"{self.output_dir}/{title}.png", dpi=300, bbox_inches="tight")
        plt.close()
        print(f"词云图已保存至 {self.output_dir}/{title}.png")
    
    def analyze_sentiment(self):
        """执行情感分析全流程"""
        if self.df.empty:
            return
        
        # 分类评论
        good_comments, bad_comments = self.classify_comments()
        
        if not good_comments.empty and not bad_comments.empty:
            # 提取关键词
            good_keywords = self.extract_keywords(good_comments)
            bad_keywords = self.extract_keywords(bad_comments)
            all_keywords = self.extract_keywords(self.df['tokens'])
            
            # 生成词云
            self.generate_wordcloud(all_keywords, "总体评论词云")
            self.generate_wordcloud(good_keywords, "好评词云")
            self.generate_wordcloud(bad_keywords, "差评词云")
            
            return {
                "good_keywords": good_keywords,
                "bad_keywords": bad_keywords,
                "all_keywords": all_keywords
            }
        return {}
    
    def run(self):
        """执行文本分析主流程"""
        print("开始文本情感分析...")
        result = self.analyze_sentiment()
        print("文本分析完成")
        return result

if __name__ == "__main__":
    analyzer = TextAnalyzer()
    analyzer.run()