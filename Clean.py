import os
import json
import re

# Define folders
input_folder = "scraped_docs"
output_folder = "parsed_docs"
os.makedirs(output_folder, exist_ok=True)

# Section titles
section_titles = [
    "Example Usage",
    "Argument Reference",
    "Attributes Reference",
    "Import"
]

# Helper function to parse arguments or attributes
def parse_arguments_or_attributes(text, is_attributes=False):
    items = []
    lines = text.splitlines()
    current_item = None

    # Regex to match argument/attribute lines
    # For arguments: "name - (Required) Description" or "name - (Optional) Description"
    # For attributes: "name - Description"
    if is_attributes:
        pattern = re.compile(r"^(\w+)\s*-\s*(.+)$")
    else:
        pattern = re.compile(r"^(\w+)\s*-\s*\((Required|Optional)\)\s*(.+)$")

    for line in lines:
        line = line.strip()
        if not line or line.lower() in ["the following arguments are supported:", "the following attributes are exported:"]:
            continue
        match = pattern.match(line)
        if match:
            if is_attributes:
                name, description = match.groups()
                current_item = {
                    "name": name,
                    "required": False,  # Attributes are typically not required
                    "description": description.strip()
                }
            else:
                name, requirement, description = match.groups()
                current_item = {
                    "name": name,
                    "required": requirement.lower() == "required",
                    "description": description.strip()
                }
            items.append(current_item)
        elif current_item and line:
            # Append additional lines to the description of the current item
            current_item["description"] += " " + line.strip()
    
    return items

# Helper function to clean text
def clean_text(text):
    # Remove 'Copy' and extra newlines
    text = re.sub(r"\n*Copy\n*", "", text).strip()
    return text

# Helper function to split the content
def split_sections(text):
    sections = {}
    current_section = "description"
    sections[current_section] = ""
    
    lines = text.splitlines()
    for line in lines:
        line_stripped = line.strip()
        if line_stripped in section_titles:
            current_section = line_stripped.lower().replace(" ", "_")
            sections[current_section] = ""
        else:
            sections.setdefault(current_section, "")
            sections[current_section] += line + "\n"
    
    # Clean and parse sections
    for section in sections:
        if section == "argument_reference":
            sections[section] = parse_arguments_or_attributes(sections[section], is_attributes=False)
        elif section == "attributes_reference":
            sections[section] = parse_arguments_or_attributes(sections[section], is_attributes=True)
        else:
            sections[section] = clean_text(sections[section])
    
    return sections

# Loop through .md files
for filename in os.listdir(input_folder):
    if filename.endswith(".md"):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Get the resource name (from the first non-empty line)
        match = re.search(r"^(cloudstack_[^\n]+)", content)
        resource = match.group(1).strip() if match else filename.replace(".md", "")
        
        # Clean content after ***
        if "***" in content:
            content = content.split("***", 1)[0]
        
        # Parse sections
        sections = split_sections(content)
        sections["resource"] = resource

        # Save as JSON
        output_path = os.path.join(output_folder, resource + ".json")
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(sections, out, indent=2, ensure_ascii=False)

print(f"✅ Done parsing .md files to JSON in {output_folder}/")