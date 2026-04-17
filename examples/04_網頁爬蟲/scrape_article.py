#!/usr/bin/env python3
"""
網頁爬蟲腳本 - 抓取文章標題和內容
功能：從網頁中抓取文章標題和內容，並儲存結果
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from pathlib import Path
import time


def scrape_article(url, timeout=10):
    """
    抓取網頁上的文章標題和內容
    
    Args:
        url (str): 要抓取的網頁網址
        timeout (int): 請求超時時間（秒）
    
    Returns:
        dict: 包含標題、內容和相關資訊的字典
    """
    
    # 設定 User-Agent，避免被伺服器拒絕
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f"🔄 正在抓取: {url}")
        
        # 發送 HTTP 請求
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # 若狀態碼不是 200 會拋出異常
        
        print("✅ 網頁加載成功")
        
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 嘗試抓取文章標題 (常見的選擇器)
        title = None
        title_selectors = ['h1', 'h1.title', 'h1.article-title', '.title', '.article-title']
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text().strip()
                print(f"📌 找到標題: {title}")
                break
        
        if not title:
            title = soup.title.string if soup.title else "無標題"
            print(f"📌 使用頁面標題: {title}")
        
        # 嘗試抓取文章內容 (常見的選擇器)
        content = None
        content_selectors = [
            'article',
            'main',
            '.article-content',
            '.post-content',
            '.content',
            '.entry-content',
            '#content'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                content = element.get_text().strip()
                print(f"📝 找到內容 ({len(content)} 字元)")
                break
        
        if not content:
            # 如果找不到專門的內容區域，抓取 body 中的所有文字
            content = soup.body.get_text().strip() if soup.body else ""
            print(f"📝 使用整個頁面文字 ({len(content)} 字元)")
        
        # 清理內容 (移除多餘的空白和換行)
        content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())
        
        result = {
            'url': url,
            'title': title,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'content_length': len(content)
        }
        
        return result
    
    except requests.exceptions.Timeout:
        print(f"⏱️  錯誤: 請求超時 (超過 {timeout} 秒)")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ 錯誤: 無法連接到網站 (網路連接問題或網址不存在)")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ 錯誤: HTTP {response.status_code}")
        return None
    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        return None


def save_result(result, format='txt'):
    """
    將爬蟲結果儲存到檔案
    
    Args:
        result (dict): 爬蟲結果
        format (str): 儲存格式 ('txt' 或 'json')
    
    Returns:
        str: 儲存檔案的路徑
    """
    
    # 建立結果資料夾
    results_dir = Path('results')
    results_dir.mkdir(exist_ok=True)
    
    # 生成檔名 (使用時間戳)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format == 'json':
        filename = results_dir / f"article_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 結果已儲存為 JSON: {filename}")
    
    else:  # default to txt
        filename = results_dir / f"article_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"【標題】\n{result['title']}\n\n")
            f.write(f"【網址】\n{result['url']}\n\n")
            f.write(f"【抓取時間】\n{result['timestamp']}\n\n")
            f.write(f"【內容長度】\n{result['content_length']} 字元\n\n")
            f.write(f"【內容】\n{result['content']}\n")
        print(f"💾 結果已儲存為 TXT: {filename}")
    
    return str(filename)


def main():
    """主程式"""
    
    # 抓取網頁
    url = "https://example.com/article"
    result = scrape_article(url)
    
    if result:
        print("\n" + "="*60)
        print("✨ 抓取成功！")
        print("="*60)
        print(f"標題: {result['title']}")
        print(f"內容長度: {result['content_length']} 字元")
        print(f"抓取時間: {result['timestamp']}")
        print("="*60 + "\n")
        
        # 儲存結果 (可選：改為 'json' 來儲存 JSON 格式)
        save_result(result, format='txt')
    else:
        print("\n❌ 抓取失敗，請檢查網址是否正確或網站是否可訪問")


if __name__ == '__main__':
    main()
