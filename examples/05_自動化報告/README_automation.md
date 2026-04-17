# 📊 自動化銷售報告使用指南

## 🎯 功能概覽

此自動化系統可以：
- ✅ 自動讀取 CSV 銷售數據
- ✅ 生成統計分析和關鍵指標
- ✅ 建立美化的 Excel 報告 (含圖表)
- ✅ 支援定時自動執行 (可選)
- ✅ 自動郵件通知 (進階版本)
- ✅ 自動備份舊報告

---

## 📁 檔案說明

| 檔案 | 說明 |
|------|------|
| `generate_sales_report.py` | ⭐ **基礎版本** - 簡單易用，推薦先用這個 |
| `generate_sales_report_advanced.py` | 🚀 **進階版本** - 支援郵件寄送和自動備份 |
| `auto_report.sh` | 🤖 **定時執行腳本** - 用於 cron 排程 |
| `reports/` | 📂 報告輸出目錄 |

---

## 🚀 快速開始

### 步驟 1: 執行基礎版本

```bash
cd /workspaces/StarPilot/examples/05_自動化報告
python3 generate_sales_report.py
```

**輸出檔案:** `週報_2026-04-17.xlsx` (依當天日期命名)

### 步驟 2: 查看生成的報告

1. 開啟終端輸出的檔案路徑
2. 用 Excel 或 Numbers 打開
3. 查看各個工作表和圖表

---

## 📊 報告包含內容

### 工作表

| 工作表 | 內容 |
|--------|------|
| **圖表_產品排行** | 前 5 名產品的銷售額長條圖 |
| **圖表_銷售佔比** | 各產品銷售金額佔比圓餅圖 |
| **圖表_銷售趨勢** | 每日銷售金額折線圖 |
| **原始數據** | 所有交易記錄 (日期、產品、數量、金額) |
| **統計摘要** | 關鍵指標 (總銷售額、平均訂單、週環比等) |
| **產品排行** | 各產品的銷售統計 (按銷售額排序) |
| **銷售趨勢** | 按日期統計的銷售金額 |

---

## 🤖 自動化設定

### 方法 1: macOS/Linux - 使用 cron

**設定指令:**
```bash
crontab -e
```

**加入以下一行** (每週一早上 9 點執行):
```
0 9 * * 1 /workspaces/StarPilot/examples/05_自動化報告/auto_report.sh
```

**Cron 表達式說明:**
```
分  時  日  月  週  指令
0   9   *   *   1   ...
│   │   │   │   └─── 週一 (0=日, 1=一, ..., 6=六)
│   │   │   └─────── 每月
│   │   └─────────── 每天
│   └─────────────── 09:00
└─────────────────── 0 分
```

**驗證設定:**
```bash
crontab -l  # 列出所有排程任務
```

### 方法 2: Windows - 使用工作排程器

1. 開啟 **工作排程器**
2. 建立基本工作
3. 設定觸發程式: 每週一 9:00
4. 動作: 執行程式
   - 程式: `python3`
   - 引數: `generate_sales_report.py`
   - 開始於: `/workspaces/StarPilot/examples/05_自動化報告`

### 方法 3: VS Code - 定時工作

安裝延伸功能 **Run on Save** 或設定 VS Code Task

---

## 🚀 進階功能

### 自動郵件通知

使用 `generate_sales_report_advanced.py` 啟用郵件功能。

**設定步驟:**

1. 編輯腳本，找到這些行:

```python
ENABLE_EMAIL = False  # ❌ 改為 True
EMAIL_SENDER = "your-email@gmail.com"  # 你的 Gmail
EMAIL_PASSWORD = "your-app-password"   # Gmail 應用密碼
EMAIL_RECIPIENTS = ["boss@company.com", "team@company.com"]  # 收件者
```

2. **Gmail 應用密碼設定**:
   - 進入 [Google 帳號安全設定](https://myaccount.google.com/security)
   - 啟用雙步驟驗證
   - 建立應用專用密碼
   - 複製 16 位密碼到 `EMAIL_PASSWORD`

3. 執行:
```bash
python3 generate_sales_report_advanced.py
```

**郵件範例:**
```
收件人: boss@company.com, team@company.com
主旨: [自動化] 週報 2026-04-17

本週銷售報告已自動生成。

📊 本週重點摘要:
- 總銷售額: NT$113,900
- 總銷售量: 234 件
- 平均訂單額: NT$3,797
- 週環比: +12.5%
...

[附件: 週報_2026-04-17.xlsx]
```

---

## 🔧 自訂報告

### 修改資料來源

编辑檔案頂部的設定:

```python
# 改為你的資料檔案位置
DATA_FILE = "../../data/sales.csv"
```

### 修改圖表類型

在腳本中找到圖表部分，修改圖表類型:

```python
# 長條圖改為折線圖
bar_chart = BarChart()  # 改為 LineChart()

# 圓餅圖改為長條圖
pie_chart = PieChart()  # 改為 BarChart()
```

### 新增計算欄位

在統計分析段落新增:

```python
# 計算平均銷售額
avg_per_product = df['金額'].sum() / len(product_stats)

# 年度目標對比
annual_target = 1000000
progress = (df['金額'].sum() / annual_target) * 100
```

---

## 📈 進階統計分析

### 同期比較

```python
# 上個月同期
last_month = df[df['日期'].dt.month == (df['日期'].max().month - 1)]
month_on_month = (df['金額'].sum() - last_month['金額'].sum()) / last_month['金額'].sum() * 100
```

### 銷售排名變化

```python
# 按周統計產品排名變化
weekly_stats = df.groupby([df['日期'].dt.isocalendar().week, '產品'])['金額'].sum().reset_index()
```

### 異常偵測

```python
# 偵測銷售異常
mean_sale = df['金額'].mean()
std_dev = df['金額'].std()
anomalies = df[df['金額'] > mean_sale + 2*std_dev]  # 異常值 (超過平均 + 2個標準差)
```

---

## 🐛 常見問題

### Q: 報告沒有生成怎麼辦？

**檢查清單:**
- [ ] 確認 `data/sales.csv` 存在
- [ ] 確認 Python 3.7+ 已安裝
- [ ] 確認 pandas 和 openpyxl 已安裝:
  ```bash
  pip3 install pandas openpyxl
  ```
- [ ] 查看完整錯誤信息:
  ```bash
  python3 generate_sales_report.py 2>&1 | head -50
  ```

### Q: 圖表為什麼沒有顯示？

**常見原因:**
- 資料不足 (少於 2 筆)
- 資料格式不正確
- Excel 版本過舊

**解決方案:**
```bash
# 檢查資料量
python3 -c "import pandas as pd; df = pd.read_csv('../../data/sales.csv'); print(f'記錄數: {len(df)}')"

# 檢查資料格式
python3 -c "import pandas as pd; df = pd.read_csv('../../data/sales.csv'); print(df.head())"
```

### Q: 怎樣修改報告名稱？

編輯這一行:
```python
OUTPUT_FILE = f"週報_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
# 改為:
OUTPUT_FILE = f"銷售分析_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
```

### Q: cron 任務未執行怎麼辦？

**除錯步驟:**

```bash
# 1. 檢查 cron 日誌
log stream --predicate 'process == "cron"' --level debug

# 2. 手動測試腳本
bash auto_report.sh

# 3. 檢查執行權限
chmod +x auto_report.sh

# 4. 檢查路徑是否正確
which python3
```

---

## 🎓 學習資源

### 相關知識
- [Python pandas 線上教程](https://pandas.pydata.org/docs/)
- [Excel 圖表自動化](https://openpyxl.readthedocs.io/en/stable/charts/)
- [Linux cron 排程](https://linux.die.net/man/5/crontab)

### 進階應用
- 整合多個資料來源 (數據庫、API)
- 實時儀表板 (用 Streamlit 或 Dash)
- 自動異常警報
- 機器學習預測

---

## 💡 提示和最佳實踐

### ✅ 推薦做法
- 定期備份報告檔案
- 監控資料品質和一致性
- 設定每週固定時間生成報告
- 保留至少 3 個月的報告歷史

### ❌ 避免
- 手動修改自動生成的報告結構
- 在資料還未驗證時就分享報告
- 遺忘備份舊報告
- 定時任務設定在高峰時段

---

## 📞 支援和反饋

如有任何問題或建議，請：
1. 查看上述 FAQ
2. 檢查腳本輸出的錯誤訊息
3. 驗證資料檔案和環境設定

---

**祝你使用愉快！🚀**
