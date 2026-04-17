#!/usr/bin/env python3
"""
批次網頁爬蟲腳本 - 抓取多個網頁的標題
功能：從 URLs 清單中批次抓取所有網頁的標題，儲存為 CSV
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time
from pathlib import Path
from urllib.parse import urlparse


def scrape_title(url, timeout=10):
    """
    抓取單個網頁的標題

    Args:
        url (str): 要抓取的網頁網址
        timeout (int): 請求超時時間（秒）

    Returns:
        dict: 包含 URL、標題和狀態的字典
    """

    # 設定 User-Agent，避免被伺服器拒絕
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    result = {
        'url': url,
        'title': '',
        'status': 'pending',
        'error_message': '',
        'timestamp': datetime.now().isoformat()
    }

    try:
        # 發送 HTTP 請求
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # 嘗試抓取頁面標題
        title = None

        # 優先嘗試 h1 標籤
        h1 = soup.find('h1')
        if h1:
            title = h1.get_text().strip()

        # 如果沒有 h1，嘗試 meta 標籤或 title 標籤
        if not title:
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                title = og_title['content'].strip()

        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()

        if title:
            result['title'] = title
            result['status'] = 'success'
        else:
            result['status'] = 'no_title'
            result['error_message'] = '找不到頁面標題'

    except requests.exceptions.Timeout:
        result['status'] = 'timeout'
        result['error_message'] = f'請求超時 (超過 {timeout} 秒)'
    except requests.exceptions.ConnectionError:
        result['status'] = 'connection_error'
        result['error_message'] = '網路連接失敗或網址不存在'
    except requests.exceptions.HTTPError as e:
        result['status'] = 'http_error'
        result['error_message'] = f'HTTP {response.status_code}'
    except Exception as e:
        result['status'] = 'error'
        result['error_message'] = str(e)

    return result


def batch_scrape_urls(urls_file, output_file=None, delay=2):
    """
    批次抓取多個網址的標題

    Args:
        urls_file (str): 包含 URLs 的檔案路徑
        output_file (str): 輸出 CSV 檔案的路徑 (預設：results/titles_TIMESTAMP.csv)
        delay (int): 每個請求之間的延遲時間（秒），預設 2 秒

    Returns:
        list: 包含所有抓取結果的列表
    """

    # 讀取 URLs
    try:
        with open(urls_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ 錯誤: 無法找到檔案 {urls_file}")
        return []
    except Exception as e:
        print(f"❌ 錯誤: 讀取檔案失敗: {str(e)}")
        return []

    if not urls:
        print(f"⚠️  警告: {urls_file} 是空的，沒有 URLs 可以抓取")
        return []

    print(f"📋 開始批次抓取", flush=True)
    print(f"📁 URLs 來源: {urls_file}")
    print(f"📊 總共 {len(urls)} 個網址要抓取")
    print(f"⏱️  延遲時間: {delay} 秒/次")
    print("-" * 80)

    results = []
    start_time = time.time()

    for idx, url in enumerate(urls, 1):
        # 驗證 URL 格式
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        print(f"\n[{idx}/{len(urls)}] 抓取中: {url}")

        # 抓取標題
        result = scrape_title(url)
        results.append(result)

        # 顯示結果
        if result['status'] == 'success':
            print(
                f"  ✅ 標題: {result['title'][:50]}{'...' if len(result['title']) > 50 else ''}")
        elif result['status'] == 'no_title':
            print(f"  ⚠️  警告: {result['error_message']}")
        else:
            print(f"  ❌ 錯誤: {result['error_message']}")

        # 延遲 (避免被封鎖)
        if idx < len(urls):
            time.sleep(delay)

    elapsed_time = time.time() - start_time

    print("\n" + "=" * 80)
    print("✨ 抓取完成！")
    print("=" * 80)
    print(f"總耗時: {elapsed_time:.2f} 秒")
    print(
        f"成功: {sum(1 for r in results if r['status'] == 'success')}/{len(urls)}")
    print(
        f"失敗: {sum(1 for r in results if r['status'] != 'success')}/{len(urls)}")
    print("-" * 80)

    # 儲存結果到 CSV
    if output_file is None:
        results_dir = Path('results')
        results_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = results_dir / f"titles_{timestamp}.csv"

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['url', 'title', 'status',
                          'error_message', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(results)

        print(f"\n💾 結果已儲存為 CSV: {output_file}")
    except Exception as e:
        print(f"\n❌ 儲存 CSV 失敗: {str(e)}")

    return results


def main():
    """主程式"""

    # 設定參數
    urls_file = "測試資料/sample_urls.txt"

    # 檢查檔案是否存在
    if not Path(urls_file).exists():
        print(f"⚠️  找不到 {urls_file}")
        print("請確保檔案存在，或修改 urls_file 變數")
        return

    # 執行批次抓取
    # delay 參數設定為 2 秒，避免過度頻繁請求
    batch_scrape_urls(
        urls_file=urls_file,
        delay=2  # 每個請求間隔 2 秒
    )


if __name__ == '__main__':
    main()
