#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
替代图片爬虫方案
由于Danbooru无法访问，提供其他解决方案
"""

import requests
import json
import os
import time
from urllib.parse import urljoin
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AlternativeScraper:
    def __init__(self):
        # 使用Safebooru作为替代（Danbooru的镜像站点）
        self.base_url = "https://safebooru.org"
        self.api_url = f"{self.base_url}/index.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.session.verify = False
        self.session.proxies = {}
        
    def search_safebooru(self, tags, limit=2):
        """使用Safebooru搜索"""
        params = {
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'tags': tags,
            'limit': limit,
            'json': 1
        }
        
        try:
            print(f"正在Safebooru搜索标签: {tags}")
            response = self.session.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            posts = data.get('post', [])
            print(f"找到 {len(posts)} 个结果")
            return posts
            
        except Exception as e:
            print(f"Safebooru搜索失败: {e}")
            return []
    
    def download_image(self, post, download_dir="downloads"):
        """下载图片"""
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            
        # Safebooru的图片URL格式
        file_url = post.get('file_url')
        if not file_url:
            print(f"帖子 {post.get('id')} 没有文件URL")
            return False
            
        # 构建完整URL
        if file_url.startswith('http'):
            image_url = file_url
        else:
            image_url = urljoin(self.base_url, file_url)
            
        # 获取文件信息
        file_ext = post.get('file_ext', 'jpg')
        post_id = post.get('id')
        
        # 生成文件名
        filename = f"safebooru_{post_id}.{file_ext}"
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
            
        except Exception as e:
            print(f"下载失败 {filename}: {e}")
            return False
    
    def scrape_images(self, tags, count=2, download_dir="downloads"):
        """爬取图片"""
        print(f"开始从Safebooru爬取标签 '{tags}' 下的 {count} 张图片")
        
        # 搜索帖子
        posts = self.search_safebooru(tags, limit=count)
        if not posts:
            print("没有找到任何结果")
            return 0
            
        # 下载图片
        success_count = 0
        for i, post in enumerate(posts, 1):
            print(f"\n处理第 {i}/{len(posts)} 张图片")
            print(f"帖子ID: {post.get('id')}")
            print(f"标签: {post.get('tags', 'N/A')[:100]}...")  # 显示前100个字符
            
            if self.download_image(post, download_dir):
                success_count += 1
                
            # 添加延迟
            if i < len(posts):
                time.sleep(1)
                
        print(f"\n爬取完成！成功下载 {success_count}/{len(posts)} 张图片")
        return success_count

def manual_download_guide():
    """提供手动下载指导"""
    print("\n=== 手动下载指导 ===")
    print("由于网络连接问题，无法自动爬取图片。")
    print("请按照以下步骤手动下载：")
    print()
    print("1. 访问以下网站之一：")
    print("   - https://danbooru.donmai.us (如果可访问)")
    print("   - https://safebooru.org")
    print("   - https://gelbooru.com")
    print()
    print("2. 在搜索框中输入：tagphainon_(honkai:_star_rail)")
    print()
    print("3. 选择2张你喜欢的图片")
    print()
    print("4. 右键点击图片，选择'图片另存为'")
    print()
    print("5. 将图片保存到当前目录的 downloads 文件夹中")
    print()
    print("6. 图片文件名建议格式：")
    print("   - tagphainon_1.jpg")
    print("   - tagphainon_2.jpg")

def main():
    print("=== 替代图片爬虫方案 ===")
    
    # 创建爬虫实例
    scraper = AlternativeScraper()
    
    # 目标标签
    target_tag = "tagphainon_(honkai:_star_rail)"
    
    # 尝试爬取
    print("尝试使用Safebooru作为替代源...")
    success_count = scraper.scrape_images(target_tag, count=2)
    
    if success_count > 0:
        print(f"\n✅ 成功下载了 {success_count} 张图片到 downloads 文件夹")
    else:
        print("\n❌ 自动爬取失败")
        manual_download_guide()

if __name__ == "__main__":
    main()

