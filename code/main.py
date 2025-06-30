#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《红海行动》评论分析主流程
"""
import os
import argparse
from data_crawler import DoubanCommentCrawler
from data_preprocessing import DataPreprocessor
from text_analysis import TextAnalyzer
from visualization import DataVisualizer

def main(do_crawl=False):
    """
    主函数
    do_crawl: 是否重新爬取数据，默认为False（使用已保存数据）
    """
    print("="*50)
    print("《红海行动》豆瓣评论数据分析项目启动")
    print("="*50)
    
    # 1. 数据采集
    if do_crawl:
        print("\n===== 开始爬取数据 =====")
        crawler = DoubanCommentCrawler()
        try:
            crawler.init_browser()
            crawler.crawl_comments(page_num=30)
            crawler.save_data()
        finally:
            crawler.close()
        print("数据爬取完成")
    else:
        print("\n===== 跳过数据爬取，使用已有数据 =====")
    
    # 2. 数据预处理
    print("\n===== 开始数据预处理 =====")
    preprocessor = DataPreprocessor()
    preprocessor.run()
    print("数据预处理完成")
    
    # 3. 文本分析
    print("\n===== 开始文本情感分析 =====")
    analyzer = TextAnalyzer()
    analyzer.run()
    print("文本分析完成")
    
    # 4. 数据可视化
    print("\n===== 开始数据可视化 =====")
    visualizer = DataVisualizer()
    visualizer.run()
    print("可视化完成")
    
    print("\n="*50)
    print("项目运行完成，结果已保存至docs文件夹")
    print("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="《红海行动》评论分析项目")
    parser.add_argument("--crawl", action="store_true", help="重新爬取数据")
    args = parser.parse_args()
    
    main(do_crawl=args.crawl)