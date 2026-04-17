#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
銷售數據分析工具
= Sales Data Analysis Tool =

這個腳本分析 sales_data.csv，生成詳細的銷售報告
"""

import csv
from collections import defaultdict
from datetime import datetime

def load_data(csv_file):
    """讀取 CSV 檔案"""
    data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                '日期': row['日期'],
                '產品': row['產品'],
                '數量': int(row['數量']),
                '金額': int(row['金額']),
                '地區': row['地區'],
                '業務': row['業務']
            })
    return data

def print_summary(data):
    """打印基本統計信息"""
    total_records = len(data)
    total_amount = sum(d['金額'] for d in data)
    total_quantity = sum(d['數量'] for d in data)
    avg_amount = total_amount / total_records if total_records > 0 else 0
    
    dates = [d['日期'] for d in data]
    min_date = min(dates)
    max_date = max(dates)
    
    print("=" * 70)
    print("📊 銷售數據分析報告".center(70))
    print("=" * 70)
    print(f"\n📈 基本信息：")
    print(f"  • 總筆數：{total_records:,} 筆")
    print(f"  • 時間范圍：{min_date} 至 {max_date}")
    print(f"  • 總銷售額：${total_amount:,.0f}")
    print(f"  • 平均訂單金額：${avg_amount:,.0f}")
    print(f"  • 總銷售量：{total_quantity:,} 件")

def print_product_analysis(data):
    """產品銷售分析"""
    product_stats = defaultdict(lambda: {'金額': 0, '數量': 0, '筆數': 0})
    for d in data:
        product_stats[d['產品']]['金額'] += d['金額']
        product_stats[d['產品']]['數量'] += d['數量']
        product_stats[d['產品']]['筆數'] += 1
    
    products_sorted = sorted(product_stats.items(), key=lambda x: x[1]['金額'], reverse=True)
    
    print(f"\n🏆 產品銷售排排看：")
    print(f"{'產品':<10} {'銷售額':>15} {'銷售量':>10} {'筆數':>8} {'平均單價':>15}")
    print("-" * 70)
    for product, stats in products_sorted:
        avg_price = stats['金額'] / stats['數量'] if stats['數量'] > 0 else 0
        print(f"{product:<10} ${stats['金額']:>14,.0f} {stats['數量']:>10} {stats['筆數']:>8} ${avg_price:>14,.0f}")
    
    return products_sorted

def print_region_analysis(data):
    """地區銷售分析"""
    region_stats = defaultdict(lambda: {'金額': 0, '數量': 0, '筆數': 0})
    for d in data:
        region_stats[d['地區']]['金額'] += d['金額']
        region_stats[d['地區']]['數量'] += d['數量']
        region_stats[d['地區']]['筆數'] += 1
    
    regions_sorted = sorted(region_stats.items(), key=lambda x: x[1]['金額'], reverse=True)
    
    print(f"\n🗺️  地區銷售分布：")
    print(f"{'地區':<10} {'銷售額':>15} {'銷售量':>10} {'筆數':>8} {'佔比':>8}")
    print("-" * 70)
    
    total_amount = sum(d['金額'] for d in data)
    for region, stats in regions_sorted:
        percentage = (stats['金額'] / total_amount * 100) if total_amount > 0 else 0
        print(f"{region:<10} ${stats['金額']:>14,.0f} {stats['數量']:>10} {stats['筆數']:>8} {percentage:>7.1f}%")
    
    return regions_sorted

def print_salesman_analysis(data):
    """業務員銷售分析"""
    salesman_stats = defaultdict(lambda: {'金額': 0, '數量': 0, '筆數': 0})
    for d in data:
        salesman_stats[d['業務']]['金額'] += d['金額']
        salesman_stats[d['業務']]['數量'] += d['數量']
        salesman_stats[d['業務']]['筆數'] += 1
    
    salesman_sorted = sorted(salesman_stats.items(), key=lambda x: x[1]['金額'], reverse=True)
    
    print(f"\n👔 業務員銷售績效：")
    print(f"{'業務':<10} {'銷售額':>15} {'銷售量':>10} {'筆數':>8} {'佔比':>8}")
    print("-" * 70)
    
    total_amount = sum(d['金額'] for d in data)
    for salesman, stats in salesman_sorted:
        percentage = (stats['金額'] / total_amount * 100) if total_amount > 0 else 0
        print(f"{salesman:<10} ${stats['金額']:>14,.0f} {stats['數量']:>10} {stats['筆數']:>8} {percentage:>7.1f}%")
    
    return salesman_sorted

def print_monthly_analysis(data):
    """月度銷售趨勢"""
    monthly_stats = defaultdict(lambda: {'金額': 0, '數量': 0})
    for d in data:
        month = d['日期'][:7]
        monthly_stats[month]['金額'] += d['金額']
        monthly_stats[month]['數量'] += d['數量']
    
    print(f"\n📅 月度銷售趨勢：")
    print(f"{'月份':<10} {'銷售額':>15} {'銷售量':>10} {'月度增長':>12}")
    print("-" * 70)
    
    prev_amount = 0
    for month in sorted(monthly_stats.keys()):
        stats = monthly_stats[month]
        growth = ((stats['金額'] - prev_amount) / prev_amount * 100) if prev_amount > 0 else 0
        growth_str = f"({growth:+.1f}%)" if prev_amount > 0 else "（基準月）"
        print(f"{month:<10} ${stats['金額']:>14,.0f} {stats['數量']:>10} {growth_str:>12}")
        prev_amount = stats['金額']

def print_insights(data):
    """關鍵洞察"""
    # 產品分析
    product_stats = defaultdict(lambda: {'金額': 0, '數量': 0})
    for d in data:
        product_stats[d['產品']]['金額'] += d['金額']
        product_stats[d['產品']]['數量'] += d['數量']
    
    # 地區分析
    region_stats = defaultdict(lambda: {'金額': 0})
    for d in data:
        region_stats[d['地區']]['金額'] += d['金額']
    
    # 業務分析
    salesman_stats = defaultdict(lambda: {'金額': 0})
    for d in data:
        salesman_stats[d['業務']]['金額'] += d['金額']
    
    top_product = max(product_stats.items(), key=lambda x: x[1]['金額'])
    top_region = max(region_stats.items(), key=lambda x: x[1]['金額'])
    top_salesman = max(salesman_stats.items(), key=lambda x: x[1]['金額'])
    
    # 計算變化
    monthly_stats = defaultdict(lambda: {'金額': 0})
    for d in data:
        month = d['日期'][:7]
        monthly_stats[month]['金額'] += d['金額']
    
    months = sorted(monthly_stats.keys())
    if len(months) >= 2:
        growth = (monthly_stats[months[-1]]['金額'] - monthly_stats[months[-2]]['金額']) / monthly_stats[months[-2]]['金額'] * 100
        growth_str = f"（月增長 {growth:+.1f}%）"
    else:
        growth_str = ""
    
    print(f"\n💡 關鍵洞察：")
    print(f"  ✓ 最暢銷產品：{top_product[0]}（${top_product[1]['金額']:,.0f}）")
    print(f"  ✓ 最強地區：{top_region[0]}（${top_region[1]['金額']:,.0f}）")
    print(f"  ✓ 銷售冠軍：{top_salesman[0]}（${top_salesman[1]['金額']:,.0f}）")
    print(f"  ✓ 銷售趨勢：持續成長 {growth_str}")

def main():
    """主程式"""
    csv_file = 'examples/02_數據分析/測試資料/sales_data.csv'
    
    try:
        data = load_data(csv_file)
        print_summary(data)
        print_product_analysis(data)
        print_region_analysis(data)
        print_salesman_analysis(data)
        print_monthly_analysis(data)
        print_insights(data)
        print("\n" + "=" * 70)
        print("✅ 分析完成！".center(70))
        print("=" * 70 + "\n")
    except FileNotFoundError:
        print(f"❌ 錯誤：找不到檔案 {csv_file}")
    except Exception as e:
        print(f"❌ 錯誤：{e}")

if __name__ == '__main__':
    main()
