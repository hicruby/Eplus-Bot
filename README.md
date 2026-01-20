
# eplus-bot (International General Sales – 半自動化)
> 自動化到「加入購物車/進入結帳」為止；等待室/驗證碼與付款保留人工，並採限流輪詢避免風控。

## 特色
- **Playwright / Selenium** 兩種實作
- **人工確認點**：等待室/驗證碼、付款
- **限流輪詢**：避免過度刷新/被封
- **設定外置**：`config/config.yaml` 與 `config/selectors.json`

## 1. 需求
- Python 3.10+（公司電腦可依《Python Automation Tool Guideline》安裝）
- （Playwright）首次需要 `playwright install`
- 建議 NTP 同步系統時間

## 2. 安裝
```bash
# 推薦使用虛擬環境
python -m venv .venv
# Windows
.\\.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

# Playwright 版
pip install -r playwright_py/requirements.txt
python -m playwright install

# 或 Selenium 版
pip install -r selenium_py/requirements.txt
```

## 3. 快速開始
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Playwright 版
pip install -r playwright_py/requirements.txt
python -m playwright install

# 複製設定
cp config/config.example.yaml config/config.yaml
cp config/selectors.example.json config/selectors.json

# 依 README 內說明更新 config 與 selectors
bash playwright_py/scripts/run.sh   # 或在 Windows 執行 run.bat
```

## 設定說明
- `config/config.yaml`：活動網址、開賣時間、票種/數量、輪詢間隔
- `config/selectors.json`：請用 `playwright codegen` 錄到穩定 selector 後貼入

## 合規
請見 `COMPLIANCE.md`。
