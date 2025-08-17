#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek API 直接测试脚本
用于诊断网络连接问题
"""

import requests
import json
import traceback

# 使用你的密钥（和安卓端相同）
API_KEY = "sk-24f56defebb149a9a7c356d39296af07"

def test_basic_request():
    """测试基础API请求"""
    print("=== DeepSeek API 连通性测试 ===")
    print(f"API密钥前缀: {API_KEY[:10]}...")
    print(f"API密钥长度: {len(API_KEY)}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "你好，这是连通性测试"}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    try:
        print("\n1. 发送请求到 https://api.deepseek.com/v1/chat/completions")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15,
            verify=True  # 启用SSL验证
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功！")
            print(f"回复内容: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ API调用失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接错误: {e}")
        print("可能原因：网络连接问题、DNS解析失败、代理设置")
        return False
        
    except requests.exceptions.Timeout as e:
        print(f"❌ 超时错误: {e}")
        print("可能原因：网络延迟过高、服务器响应慢")
        return False
        
    except requests.exceptions.SSLError as e:
        print(f"❌ SSL证书错误: {e}")
        print("可能原因：证书验证失败、代理拦截HTTPS")
        return False
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP错误: {e}")
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        print(f"错误类型: {type(e).__name__}")
        traceback.print_exc()
        return False

def test_without_ssl_verify():
    """测试禁用SSL验证的请求（用于诊断证书问题）"""
    print("\n=== SSL验证禁用测试 ===")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat", 
        "messages": [{"role": "user", "content": "SSL测试"}],
        "max_tokens": 30
    }
    
    try:
        # 禁用SSL验证（仅用于诊断）
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15,
            verify=False  # 禁用SSL验证
        )
        
        if response.status_code == 200:
            print("✅ 禁用SSL验证后成功 -> 说明是证书问题")
            return True
        else:
            print(f"❌ 即使禁用SSL验证仍失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 禁用SSL验证后仍失败: {e}")
        return False

def test_sanitize_function():
    """测试密钥处理函数是否损坏密钥"""
    print("\n=== 密钥处理函数测试 ===")
    
    def sanitize_api_key(val):
        if not isinstance(val, str):
            return val
        s = val.strip()
        # 去除包裹引号
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        # 移除常见不可见字符
        invisible = {"\u200b", "\u200c", "\u200d", "\u2060", "\ufeff", "\xa0"}
        invisible_chars = {bytes(ch, 'utf-8').decode('unicode_escape') for ch in invisible}
        for ch in invisible_chars:
            s = s.replace(ch, '')
        return s
    
    original = API_KEY
    processed = sanitize_api_key(API_KEY)
    
    print(f"原始密钥: {original}")
    print(f"处理后密钥: {processed}")
    print(f"长度变化: {len(original)} -> {len(processed)}")
    
    if original == processed:
        print("✅ 密钥处理函数正常")
        return True
    else:
        print("❌ 密钥被处理函数修改了！这可能是问题根源")
        return False

if __name__ == "__main__":
    print("开始诊断 DeepSeek API 连接问题...\n")
    
    # 测试密钥处理函数
    sanitize_ok = test_sanitize_function()
    
    # 测试基础请求
    basic_ok = test_basic_request()
    
    # 如果基础请求失败，测试SSL问题
    if not basic_ok:
        ssl_ok = test_without_ssl_verify()
    
    print("\n=== 诊断总结 ===")
    if basic_ok:
        print("✅ API连接正常，问题可能在安卓端的其他地方")
    else:
        print("❌ API连接失败，建议检查：")
        print("  1. 网络代理设置")  
        print("  2. 防火墙配置")
        print("  3. DNS设置")
        print("  4. 系统时间是否正确（影响SSL证书验证）")