import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

def scrape_page(driver, url):
    print(f"[INFO] Navigating to {url}")
    driver.get(url)
    time.sleep(5)  # wait for JS to render page

    visible_text = driver.execute_script("return document.body.innerText")

    if visible_text.strip():
        print(f"[SUCCESS] Content retrieved from {url[:50]}...")
        return visible_text
    else:
        print(f"[WARNING] No visible content found at {url}")
        return None

def url_to_filename(url):
    parsed = urlparse(url)
    # get last path segment, or fallback to 'index'
    filename = parsed.path.rstrip('/').split('/')[-1] or "index"
    # sanitize filename if needed
    filename = filename.replace('.', '_').replace(' ', '_')
    return filename + ".md"

def main():
    with open("Links.json", "r", encoding="utf-8") as f:
        links = json.load(f)

    os.makedirs("scraped_docs", exist_ok=True)

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        for url in links:
            try:
                content = scrape_page(driver, url)
                if content:
                    filename = url_to_filename(url)
                    filepath = os.path.join("scraped_docs", filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"[SAVED] {filepath}\n")
                else:
                    print(f"[SKIP] No content to save for {url}\n")

            except Exception as e:
                print(f"[ERROR] Failed to scrape {url}: {e}\n")

    finally:
        driver.quit()
        print("[INFO] Browser closed.")

if __name__ == "__main__":
    main()
