#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Danbooru图片爬虫
用于爬取指定标签下的图片
"""

import requests
import json
import os
import time
from urllib.parse import urljoin
import sys
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DanbooruScraper:
    def __init__(self):
        self.base_url = "https://danbooru.donmai.us"
        self.api_url = f"{self.base_url}/posts.json"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # 禁用SSL验证以避免证书问题
        self.session.verify = False
        # 禁用代理
        self.session.proxies = {}
        # 设置超时时间
        self.session.timeout = 10
        
    def search_posts(self, tags, limit=2):
        """
        搜索指定标签的帖子
        
        Args:
            tags (str): 搜索标签
            limit (int): 返回结果数量限制
            
        Returns:
            list: 帖子列表
        """
        params = {
            'tags': tags,
            'limit': limit,
            'random': 'true'  # 随机获取结果
        }
        
        try:
            print(f"正在搜索标签: {tags}")
            response = self.session.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            
            posts = response.json()
            print(f"找到 {len(posts)} 个结果")
            return posts
            
        except requests.exceptions.RequestException as e:
            print(f"搜索请求失败: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"解析JSON失败: {e}")
            return []
    
    def download_image(self, post, download_dir="downloads"):
        """
        下载单张图片
        
        Args:
            post (dict): 帖子信息
            download_dir (str): 下载目录
            
        Returns:
            bool: 下载是否成功
        """
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            
        # 获取图片URL
        file_url = post.get('file_url')
        if not file_url:
            print(f"帖子 {post.get('id')} 没有文件URL")
            return False
            
        # 构建完整URL
        if file_url.startswith('http'):
            image_url = file_url
        else:
            image_url = urljoin(self.base_url, file_url)
            
        # 获取文件扩展名
        file_ext = post.get('file_ext', 'jpg')
        post_id = post.get('id')
        
        # 生成文件名
        filename = f"danbooru_{post_id}.{file_ext}"
        filepath = os.path.join(download_dir, filename)
        
        # 如果文件已存在，跳过下载
        if os.path.exists(filepath):
            print(f"文件已存在，跳过: {filename}")
            return True
            
        try:
            print(f"正在下载: {filename}")
            response = self.session.get(image_url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            print(f"下载完成: {filename}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"下载失败 {filename}: {e}")
            return False
    
    def scrape_images(self, tags, count=2, download_dir="downloads"):
        """
        爬取指定标签的图片
        
        Args:
            tags (str): 搜索标签
            count (int): 下载数量
            download_dir (str): 下载目录
            
        Returns:
            int: 成功下载的数量
        """
        print(f"开始爬取标签 '{tags}' 下的 {count} 张图片")
        
        # 搜索帖子
        posts = self.search_posts(tags, limit=count)
        if not posts:
            print("没有找到任何结果")
            return 0
            
        # 下载图片
        success_count = 0
        for i, post in enumerate(posts, 1):
            print(f"\n处理第 {i}/{len(posts)} 张图片")
            print(f"帖子ID: {post.get('id')}")
            print(f"标签: {', '.join(post.get('tag_string', '').split()[:10])}")  # 显示前10个标签
            
            if self.download_image(post, download_dir):
                success_count += 1
                
            # 添加延迟避免请求过于频繁
            if i < len(posts):
                time.sleep(1)
                
        print(f"\n爬取完成！成功下载 {success_count}/{len(posts)} 张图片")
        return success_count

def main():
    # 创建爬虫实例
    scraper = DanbooruScraper()
    
    # 目标标签
    target_tag = "tagphainon_(honkai:_star_rail)"
    
    # 爬取2张图片
    success_count = scraper.scrape_images(target_tag, count=2)
    
    if success_count > 0:
        print(f"\n✅ 成功下载了 {success_count} 张图片到 downloads 文件夹")
    else:
        print("\n❌ 没有成功下载任何图片")

if __name__ == "__main__":
    main()
