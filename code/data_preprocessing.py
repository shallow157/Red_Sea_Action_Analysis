"""
《红海行动》评论数据预处理
"""
import re
import pandas as pd
import jieba
import numpy as np

class DataPreprocessor:
    def __init__(self, data_path="../data/raw_comments.csv"):
        """初始化数据预处理"""
        self.data_path = data_path
        self.df = self._load_data()
        self.stopwords = self._load_stopwords()
        self.military_dict = "../data/military_words.txt"  # 军事术语词典路径
        jieba.load_userdict(self.military_dict)  # 加载自定义词典
    
    def _load_data(self):
        """加载原始数据"""
        try:
            df = pd.read_csv(self.data_path)
            print(f"加载数据成功，共{len(df)}条记录")
            return df
        except Exception as e:
            print(f"加载数据失败: {e}")
            return pd.DataFrame()
    
    def _load_stopwords(self):
        """加载停用词表"""
        stopwords = set([
            '红海', '行动', '电影', '这部', '片子', '一个', '的', '了', '是', '我', '有',
            '看', '觉得', '这个', '非常', '很', '也', '就', '都', '还', '没有', '说',
            '要', '去', '你', '会', '着', '没有', '不是', '什么', '时候'
        ])
        # 可选：从文件加载更多停用词
        try:
            with open("../data/stopwords.txt", "r", encoding="utf-8") as f:
                extra_stopwords = f.read().splitlines()
            stopwords.update(extra_stopwords)
        except:
            pass
        return stopwords
    
    def clean_data(self):
        """清洗基础数据"""
        if self.df.empty:
            return pd.DataFrame()
        
        # 1. 处理评分：提取数字并标准化
        self.df['score'] = self.df['score'].apply(lambda x: int(x) if pd.notna(x) else 0)
        self.df['score_numeric'] = self.df['score']
        
        # 2. 处理城市：去除方括号等符号
        self.df['city'] = self.df['city'].apply(lambda x: re.sub(r'[\[\]]', '', str(x)))
        self.df['city'] = self.df['city'].replace('未知', np.nan)
        
        # 3. 处理时间：提取日期部分
        self.df['date'] = self.df['time'].apply(lambda x: re.findall(r'\d{4}-\d{1,2}-\d{1,2}', str(x))[0] if re.findall(r'\d{4}-\d{1,2}-\d{1,2}', str(x)) else np.nan)
        self.df['hour'] = self.df['time'].apply(lambda x: re.findall(r'(\d{1,2}):\d{1,2}', str(x))[0] if re.findall(r'(\d{1,2}):\d{1,2}', str(x)) else np.nan)
        
        # 4. 去除空值评论
        self.df = self.df[self.df['content'].notna() & (self.df['content'] != '')]
        print(f"数据清洗完成，剩余{len(self.df)}条记录")
        return self.df
    
    def tokenize_text(self):
        """文本分词与去停用词"""
        if self.df.empty:
            return pd.DataFrame()
        
        # 定义分词函数
        def tokenize(content):
            words = jieba.lcut(content)
            return [word for word in words if word not in self.stopwords and len(word) > 1]
        
        # 应用分词
        self.df['tokens'] = self.df['content'].apply(tokenize)
        
        # 过滤空分词记录
        self.df = self.df[self.df['tokens'].apply(lambda x: len(x) > 0)]
        print(f"文本分词完成，剩余{len(self.df)}条有效记录")
        return self.df
    
    def save_processed_data(self, file_path="../data/cleaned_data.csv"):
        """保存处理后的数据"""
        if self.df.empty:
            print("没有数据可保存")
            return
        
        # 保存必要字段
        save_cols = ['score', 'score_numeric', 'content', 'tokens', 'date', 'hour', 'city', 'votes']
        self.df[save_cols].to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"处理后数据已保存至 {file_path}")
    
    def run(self):
        """执行完整预处理流程"""
        self.clean_data()
        self.tokenize_text()
        self.save_processed_data()
        return self.df

if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    preprocessor.run()