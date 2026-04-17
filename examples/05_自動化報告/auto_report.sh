#!/bin/bash
# 🤖 定時執行銷售報告自動化腳本
# 使用 cron 設定每週一早上 9 點自動執行
# 
# 設定方式:
# 1. 執行: crontab -e
# 2. 加入這一行: 0 9 * * 1 /workspaces/StarPilot/examples/05_自動化報告/auto_report.sh
#    (週一 09:00 自動執行)
# 3. 保存離開

# 進入報告目錄
cd /workspaces/StarPilot/examples/05_自動化報告

# 執行報告生成腳本
python3 generate_sales_report.py

# 可選: 自動寄送報告 (如果有設定郵件)
# echo "新的銷售報告已生成，請查看附件" | mail -s "週報" -a "週報_*.xlsx" your-email@example.com

echo "✅ 自動化報告執行完成 $(date)"
