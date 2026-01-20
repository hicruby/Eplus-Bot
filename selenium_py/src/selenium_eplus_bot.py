# -*- coding: utf-8 -*-
import json, time, argparse, os
from datetime import datetime, timezone, timedelta
import yaml
from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

load_dotenv()

def wait_until(ts_iso):
    target = datetime.fromisoformat(ts_iso)
    while True:
        now = datetime.now(target.tzinfo or timezone(timedelta(hours=8)))
        dt = (target - now).total_seconds()
        if dt <= 0: return
        time.sleep(0.2 if dt < 5 else 1)

def safe_click(page, selector, timeout=4000):
    el = page.locator(selector).first
    el.wait_for(state="visible", timeout=timeout)
    el.click()

def main(args):
    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    with open(args.selectors, "r", encoding="utf-8") as f:
        sel = json.load(f)

    from utils.logger import logger  # 初始化日誌

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            cfg.get("user_data_dir", "./eplus-user-data"),
            headless=cfg["ui"].get("headless", False),
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.new_page()
        page.goto(cfg["event_url"], wait_until="domcontentloaded")
        logger.info("Loaded event page")

        # Cookie banner
        try: page.locator(sel["accept_cookies"]).first.click(timeout=1500)
        except Exception: pass

        input("若有等待室/驗證碼，請先人工通過後按 Enter 繼續...")

        wait_until(cfg["go_live"])

        tries, max_tries = 0, int(cfg["limits"]["max_refresh_tries"])
        interval = int(cfg["limits"]["refresh_interval_ms"]) / 1000.0
        while tries < max_tries:
            try:
                btn = page.locator(sel["intl_general_sales"]).first
                if btn.is_visible() and btn.is_enabled():
                    btn.click(); logger.info("Enter International general sales"); break
            except PWTimeout:
                pass
            time.sleep(interval); tries += 1
            page.reload(wait_until="domcontentloaded")
        else:
            logger.error("超過嘗試次數仍無法進場，請人工檢查。"); return

        # 票種/數量（視頁面需求）
        try: page.select_option(sel["ticket_type"], value=cfg["ticket"]["type"])
        except Exception: pass
        try:
            qty = page.locator(sel["ticket_qty"]).first
            if qty.is_visible(): qty.fill(str(cfg["ticket"]["qty"]))
        except Exception: pass

        # 加入購物車 → 前往結帳
        safe_click(page, sel["add_to_cart"], timeout=8000)
        page.wait_for_load_state("networkidle")
        safe_click(page, sel["checkout"], timeout=8000)

        input("已到結帳/付款頁，請手動完成付款；完成後按 Enter 以關閉。")
        ctx.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--selectors", required=True)
    main(ap.parse_args())