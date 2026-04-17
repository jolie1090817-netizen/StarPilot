#!/usr/bin/env python3
"""
抓取 i23.uk 網頁的文章標題和內容
只提取前三篇文章，存成 TXT 檔
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def scrape_articles(url, num_articles=3):
    """
    抓取網頁文章
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f"🕷️  正在連接到 {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 尋找文章容器 - 嘗試常見的選擇器
        articles = []
        
        # 嘗試多種可能的選擇器
        article_selectors = [
            'article',
            '.post',
            '.entry',
            '[class*="article"]',
            '[class*="post"]',
            '.content article',
            'div.post',
        ]
        
        for selector in article_selectors:
            articles = soup.select(selector)
            if articles:
                print(f"✅ 找到文章容器（使用選擇器: {selector}）")
                break
        
        if not articles:
            print("⚠️  未找到標準文章容器，嘗試手動解析")
            # 如果找不到，嘗試其他方法
            articles = soup.find_all(['h1', 'h2', 'h3'])[:num_articles*2]
        
        # 提取前 N 篇文章的標題和內容
        extracted_articles = []
        
        for i, article in enumerate(articles[:num_articles*2]):
            try:
                # 提取標題
                title_elem = article.find(['h1', 'h2', 'h3', 'a'])
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                if not title or len(title) < 5:
                    continue
                
                # 提取內容
                content_elem = article.find(['p', 'div'])
                content = ""
                
                if content_elem:
                    # 獲取文章內所有段落
                    paragraphs = article.find_all('p')
                    if paragraphs:
                        content = "\n".join([p.get_text(strip=True) for p in paragraphs[:5]])
                    else:
                        content = content_elem.get_text(strip=True)
                
                if title and content:
                    extracted_articles.append({
                        'title': title,
                        'content': content
                    })
                
                if len(extracted_articles) >= num_articles:
                    break
                    
            except Exception as e:
                print(f"⚠️  處理文章時出錯: {e}")
                continue
        
        return extracted_articles
        
    except requests.exceptions.Timeout:
        print("❌ 連接超時（超過 10 秒）")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ 無法連接到網站: {e}")
        return []
    except Exception as e:
        print(f"❌ 出錯: {e}")
        return []


def save_to_txt(articles, output_file):
    """
    將文章保存到 TXT 檔
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"網頁爬蟲結果 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"來源: https://www.i23.uk/\n")
            f.write(f"共提取: {len(articles)} 篇文章\n")
            f.write("=" * 70 + "\n\n")
            
            for idx, article in enumerate(articles, 1):
                f.write(f"📰 第 {idx} 篇\n")
                f.write(f"標題: {article['title']}\n")
                f.write("-" * 70 + "\n")
                f.write(f"內容:\n{article['content']}\n")
                f.write("=" * 70 + "\n\n")
        
        print(f"✅ 已保存到: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 保存失敗: {e}")
        return False


if __name__ == '__main__':
    url = "https://www.i23.uk/"
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "i23_articles.txt")
    
    print("🕷️  開始爬蟲...\n")
    
    # 抓取文章
    articles = scrape_articles(url, num_articles=3)
    
    if articles:
        print(f"\n✅ 成功提取 {len(articles)} 篇文章\n")
        
        # 顯示預覽
        for idx, article in enumerate(articles, 1):
            print(f"第 {idx} 篇: {article['title'][:50]}...")
        
        print()
        
        # 保存到檔案
        save_to_txt(articles, output_file)
    else:
        print("\n❌ 未能提取任何文章")
        print("\n💡 可能原因:")
        print("  1. 網站結構與預期不同")
        print("  2. 網站需要 JavaScript 渲染（建議改用 Selenium）")
        print("  3. 網站禁止爬蟲訪問")
