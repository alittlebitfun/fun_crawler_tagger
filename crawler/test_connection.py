#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络连接测试脚本
用于测试Danbooru API的连接性
"""

import requests
import urllib3
import os

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_connection():
    """测试网络连接"""
    print("正在测试网络连接...")
    
    # 设置代理
    proxy_url = "http://127.0.0.1:7890"
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    # 测试基本连接
    try:
        response = requests.get("https://www.baidu.com", timeout=5, verify=False, proxies=proxies)
        print("✅ 基本网络连接正常")
    except Exception as e:
        print(f"❌ 基本网络连接失败: {e}")
        return False
    
    # 测试Danbooru连接
    try:
        response = requests.get("https://danbooru.donmai.us", timeout=10, verify=False, proxies=proxies)
        print("✅ Danbooru网站连接正常")
    except Exception as e:
        print(f"❌ Danbooru网站连接失败: {e}")
        return False
    
    # 测试API连接
    try:
        api_url = "https://danbooru.donmai.us/posts.json"
        params = {'tags': 'rating:safe', 'limit': 1}
        response = requests.get(api_url, params=params, timeout=10, verify=False, proxies=proxies)
        if response.status_code == 200:
            print("✅ Danbooru API连接正常")
            return True
        else:
            print(f"❌ Danbooru API返回错误状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Danbooru API连接失败: {e}")
        return False

def main():
    print("=== 网络连接测试 ===")
    
    # 设置Clash代理（默认端口7890）
    proxy_url = "http://127.0.0.1:7890"
    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url
    os.environ['http_proxy'] = proxy_url
    os.environ['https_proxy'] = proxy_url
    
    print(f"使用代理: {proxy_url}")
    
    if test_connection():
        print("\n🎉 网络连接正常，可以尝试运行爬虫脚本")
    else:
        print("\n⚠️  网络连接有问题，建议检查：")
        print("1. 检查网络连接")
        print("2. 检查防火墙设置")
        print("3. 检查代理设置")
        print("4. 尝试使用VPN")

if __name__ == "__main__":
    main()
