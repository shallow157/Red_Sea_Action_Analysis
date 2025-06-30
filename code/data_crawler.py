#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《红海行动》豆瓣评论爬虫
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # 自动管理ChromeDriver

class DoubanCommentCrawler:
    def __init__(self):
        # 初始化浏览器配置
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # 无头模式
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        self.driver = None
        self.data = []
    
    def init_browser(self):
        """初始化浏览器驱动"""
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=self.options
            )
            self.driver.maximize_window()
            print("浏览器初始化成功")
        except Exception as e:
            print(f"浏览器初始化失败: {e}")
    
    def crawl_comments(self, movie_id="2675208", page_num=10):
        """
        爬取豆瓣电影评论
        movie_id: 豆瓣电影ID，《红海行动》ID为26861685
        page_num: 爬取页数，每页约20条评论
        """
        url = f"https://movie.douban.com/subject/26861685/comments?status=P"
        self.driver.get(url)
        time.sleep(3)  # 等待页面加载
        
        for page in range(page_num):
            try:
                # 等待评论元素加载
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.comment-item'))
                )
                
                # 滚动加载更多评论（模拟用户行为）
                for _ in range(3):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)  # 等待加载
                
                # 提取评论
                comment_items = self.driver.find_elements(By.CSS_SELECTOR, '.comment-item')
                for item in comment_items:
                    try:
                        # 评分
                        rating_ele = item.find_element(By.CSS_SELECTOR, '.rating')
                        score = rating_ele.get_attribute('class').split(' ')[-1]  # u评级格式
                        score = int(score.replace('rating', '')) * 10 if score else 0
                        
                        # 评论内容
                        content = item.find_element(By.CSS_SELECTOR, '.short').text.strip()
                        
                        # 评论时间
                        time_str = item.find_element(By.CSS_SELECTOR, '.comment-time').text.strip()
                        
                        # 评论城市
                        city_ele = item.find_elements(By.CSS_SELECTOR, '.comment-location')
                        city = city_ele[0].text.strip() if city_ele else "未知"
                        
                        # 点赞数
                        votes = item.find_element(By.CSS_SELECTOR, '.votes').text.strip()
                        
                        self.data.append({
                            'score': score,
                            'content': content,
                            'time': time_str,
                            'city': city,
                            'votes': votes
                        })
                    except Exception as e:
                        print(f"提取评论失败: {e}")
                
                print(f"已爬取第{page+1}页，累计{len(self.data)}条评论")
                
                # 点击下一页
                next_btn = self.driver.find_element(By.CSS_SELECTOR, '.next')
                if 'disabled' in next_btn.get_attribute('class'):
                    print("已到达最后一页")
                    break
                next_btn.click()
                time.sleep(3)  # 等待下一页加载
            except Exception as e:
                print(f"爬取第{page+1}页时出错: {e}")
                continue
    
    def save_data(self, file_path="../data/raw_comments.csv"):
        """保存数据到CSV"""
        if not self.data:
            print("没有数据可保存")
            return
        
        df = pd.DataFrame(self.data)
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"数据已保存至 {file_path}，共{len(df)}条记录")
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    crawler = DoubanCommentCrawler()
    try:
        crawler.init_browser()
        crawler.crawl_comments(page_num=30)  # 爬取30页，约600条评论
        crawler.save_data()
    finally:
        crawler.close()