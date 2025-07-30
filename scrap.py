from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def scrape_terraform_docs():
    url = "https://registry.terraform.io/providers/CloudAnts/cloudstack/latest/docs/data-sources/template"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        print("[INFO] Starting browser...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        print(f"[INFO] Navigating to {url}")
        driver.get(url)

        print("[INFO] Waiting for JavaScript to load...")
        time.sleep(5)

        # ✅ Exécute du JavaScript pour obtenir le texte visible dans la page
        visible_text = driver.execute_script("return document.body.innerText")

        if "affinity_group" in visible_text.lower():
            print("[SUCCESS] Page visible content retrieved.")
            print("\n[INFO] Preview:\n")
            print(visible_text[:1000])  # preview

            # 📁 Enregistrement dans un fichier
            os.makedirs("scraped_docs", exist_ok=True)
            with open("scraped_docs/affinity_group.md", "w", encoding="utf-8") as f:
                f.write(visible_text)

            print("\n[SAVED] File saved to scraped_docs/affinity_group.md")
        else:
            print("[WARNING] Keyword not found in visible text.")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        driver.quit()
        print("[INFO] Browser closed.")

if __name__ == "__main__":
    scrape_terraform_docs()
