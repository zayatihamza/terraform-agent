import os
import re

SCRAPED_DIR = "scraped_docs2"
CLEANED_DIR = "cleaned_docs"

os.makedirs(CLEANED_DIR, exist_ok=True)

def clean_markdown(text: str) -> str:
    # Remove footer junk
    text = re.sub(r'\n?Copy\n?', '', text)
    text = re.sub(r'\n?Dismiss\n?', '', text)
    text = re.sub(r'\n?Manage Preferences\n?', '', text)
    
    # Remove cookie/privacy sections
    text = re.sub(r"We use cookies and other similar technology.*?(Privacy Policy|Cookie Policy)\.", "", text, flags=re.DOTALL)

    # Convert Markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Remove HTML entities or artifacts
    text = re.sub(r'\\_', '_', text)
    
    # Remove multiple empty lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def process_all_md_files():
    for filename in os.listdir(SCRAPED_DIR):
        if not filename.endswith(".md"):
            continue

        input_path = os.path.join(SCRAPED_DIR, filename)
        output_path = os.path.join(CLEANED_DIR, filename)

        with open(input_path, "r", encoding="utf-8") as infile:
            raw_content = infile.read()

        cleaned_content = clean_markdown(raw_content)

        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write(cleaned_content)

        print(f"[CLEANED] {filename} -> {output_path}")

if __name__ == "__main__":
    process_all_md_files()
    print("\n✅ Cleaning complete. Check the 'cleaned_docs/' folder.")
