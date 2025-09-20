# Add these imports to your existing script (after the current imports)
import subprocess
import tempfile
from pathlib import Path

# HCL parsing for validation
try:
    import hcl2
    HCL2_AVAILABLE = True
    print("✅ HCL2 parser loaded successfully")
except ImportError:
    HCL2_AVAILABLE = False
    print("⚠️ HCL2 parser not available")

import os
import re
import json
import sys
import time
import difflib
from typing import List, Dict, Tuple, Optional
from pathlib import Path

from pymilvus import connections, Collection
from groq import Groq

# ---------------------------
# Configuration (env-friendly)
# ---------------------------
COLLECTION_NAME = os.getenv("MILVUS_COLLECTION", "cloudstack_docs")
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

MAX_CONTEXT_CHUNKS = int(os.getenv("MAX_CONTEXT_CHUNKS", "8"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "generated"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TERRAFORM_VALIDATION_ENABLED = os.getenv("TERRAFORM_VALIDATION", "true").lower() == "true"
VALIDATION_TIMEOUT = int(os.getenv("VALIDATION_TIMEOUT", "60"))  # seconds
# Quick guard
if not GROQ_API_KEY:
    print("❌ GROQ_API_KEY is missing. Set it with: setx GROQ_API_KEY \"your_key\" and restart your shell.")
    sys.exit(1)



# Connect clients
connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
collection = Collection(COLLECTION_NAME)
client = Groq(api_key=GROQ_API_KEY, default_headers={"Content-Type": "application/json; charset=utf-8"})


# ---------------------------
# Terraform Validation Functions
# ---------------------------

def check_terraform_installed() -> bool:
    """Check if Terraform CLI is available."""
    try:
        result = subprocess.run(['terraform', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def validate_hcl_syntax(hcl_content: str) -> Tuple[bool, str]:
    """
    Validate HCL syntax using python-hcl2.
    Returns (is_valid, error_message)
    """
    if not HCL2_AVAILABLE:
        return True, "HCL2 parser not available - skipping syntax check"
    
    try:
        # Parse the HCL content
        parsed = hcl2.loads(hcl_content)
        
        # Basic structure validation
        if not isinstance(parsed, dict):
            return False, "Invalid HCL structure"
            
        # Check for required sections
        has_content = any(key in parsed for key in ['resource', 'terraform', 'provider', 'data'])
        if not has_content:
            return False, "No valid Terraform blocks found"
            
        return True, "Syntax valid"
        
    except Exception as e:
        error_msg = str(e)
        if "unexpected token" in error_msg.lower():
            return False, "Syntax error: Check for missing quotes or brackets"
        elif "unterminated" in error_msg.lower():
            return False, "Syntax error: Missing closing quotes or brackets"
        else:
            return False, f"Syntax error: {error_msg}"

def validate_terraform_cli(hcl_content: str) -> Tuple[bool, str]:
    """
    Validate using terraform validate command.
    Returns (is_valid, message)
    """
    if not check_terraform_installed():
        return True, "Terraform CLI not available"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Write main.tf
        main_tf = temp_path / "main.tf"
        with open(main_tf, 'w', encoding='utf-8') as f:
            f.write(hcl_content)
        
        # Write provider.tf
        provider_tf = temp_path / "provider.tf"
        with open(provider_tf, 'w', encoding='utf-8') as f:
            f.write('''
terraform {
  required_providers {
    cloudstack = {
      source = "cloudstack/cloudstack"
      version = "~> 0.5"
    }
  }
}

provider "cloudstack" {
  api_url    = "http://localhost:8080/client/api"
  api_key    = "dummy"
  secret_key = "dummy"
}
''')
        
        try:
            # Initialize Terraform
            init_result = subprocess.run(
                ['terraform', 'init', '-no-color'],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=VALIDATION_TIMEOUT
            )
            
            if init_result.returncode != 0:
                if "Error parsing" in init_result.stderr:
                    return False, f"Parse error: {init_result.stderr}"
                # Other init errors might be OK (network issues, etc.)
            
            # Run terraform validate
            validate_result = subprocess.run(
                ['terraform', 'validate', '-no-color'],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if validate_result.returncode == 0:
                return True, "Terraform validation passed"
            else:
                return False, f"Validation failed: {validate_result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "Validation timed out"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

def validate_required_fields(hcl_content: str, required_fields: List[str]) -> Tuple[bool, List[str]]:
    """
    Check if all required fields are present.
    Returns (all_present, missing_fields)
    """
    missing = []
    
    for field in required_fields:
        # Look for field = value pattern
        pattern = rf'\b{re.escape(field)}\s*='
        if not re.search(pattern, hcl_content):
            missing.append(field)
    
    return len(missing) == 0, missing

def comprehensive_terraform_validation(hcl_content: str, required_fields: List[str]) -> Dict[str, any]:
    """
    Run all validation checks.
    Returns comprehensive results dictionary.
    """
    if not TERRAFORM_VALIDATION_ENABLED:
        return {'overall_valid': True, 'message': 'Validation disabled'}
    
    results = {
        'overall_valid': True,
        'syntax_check': {'valid': True, 'message': ''},
        'terraform_cli': {'valid': True, 'message': ''},
        'required_fields': {'valid': True, 'missing': []},
        'suggestions': []
    }
    
    # Initialize variables to avoid UnboundLocalError
    syntax_valid = True
    cli_valid = True
    cli_msg = ""
    
    # 1. HCL Syntax Check
    try:
        syntax_valid, syntax_msg = validate_hcl_syntax(hcl_content)
        results['syntax_check'] = {'valid': syntax_valid, 'message': syntax_msg}
        if not syntax_valid:
            results['overall_valid'] = False
    except Exception as e:
        syntax_valid = False
        results['syntax_check'] = {'valid': False, 'message': f"Syntax validation error: {str(e)}"}
        results['overall_valid'] = False
    
    # 2. Required Fields Check
    try:
        fields_valid, missing_fields = validate_required_fields(hcl_content, required_fields)
        results['required_fields'] = {'valid': fields_valid, 'missing': missing_fields}
        if not fields_valid:
            results['overall_valid'] = False
    except Exception as e:
        results['required_fields'] = {'valid': False, 'missing': [f"Error checking fields: {str(e)}"]}
        results['overall_valid'] = False
    
    # 3. Terraform CLI Validation (only if syntax is OK)
    if syntax_valid:
        try:
            cli_valid, cli_msg = validate_terraform_cli(hcl_content)
            results['terraform_cli'] = {'valid': cli_valid, 'message': cli_msg}
            if not cli_valid and "not available" not in cli_msg:
                results['overall_valid'] = False
        except Exception as e:
            cli_valid = False
            cli_msg = f"CLI validation error: {str(e)}"
            results['terraform_cli'] = {'valid': False, 'message': cli_msg}
            results['overall_valid'] = False
    else:
        # Skip CLI validation if syntax is invalid
        results['terraform_cli'] = {'valid': True, 'message': 'Skipped due to syntax errors'}
    
    # 4. Generate suggestions
    suggestions = []
    if not syntax_valid:
        suggestions.append("Fix HCL syntax errors")
    if results['required_fields'].get('missing'):
        missing = results['required_fields']['missing']
        suggestions.append(f"Add missing required fields: {', '.join(missing)}")
    if not cli_valid and "not available" not in cli_msg:
        suggestions.append("Review Terraform validation errors")
    
    results['suggestions'] = suggestions
    
    return results
def print_validation_results(results: Dict[str, any]):
    """Display validation results in a user-friendly format."""
    if not TERRAFORM_VALIDATION_ENABLED:
        return
        
    print("\n📋 Validation Results:")
    print("=" * 40)
    
    # Overall status
    if results['overall_valid']:
        print("✅ Overall Status: VALID")
    else:
        print("❌ Overall Status: INVALID")
    
    # Syntax check
    syntax = results.get('syntax_check', {})
    status_icon = "✅" if syntax.get('valid') else "❌"
    print(f"{status_icon} HCL Syntax: {syntax.get('message', 'Unknown')}")
    
    # Required fields
    fields = results.get('required_fields', {})
    if fields.get('missing'):
        print(f"❌ Required Fields: Missing {fields['missing']}")
    else:
        print("✅ Required Fields: All present")
    
    # Terraform CLI
    cli = results.get('terraform_cli', {})
    status_icon = "✅" if cli.get('valid') else "❌"
    cli_msg = cli.get('message', 'Unknown')
    print(f"{status_icon} Terraform CLI: {cli_msg}")
    
    # Suggestions
    if results.get('suggestions'):
        print("\n💡 Suggestions:")
        for i, suggestion in enumerate(results['suggestions'], 1):
            print(f"   {i}. {suggestion}")
    
    print("=" * 40)


# ---------------------------
# Utility: Robust LLM JSON
# ---------------------------
def safe_groq_json(prompt: str, default=None, retries: int = 1):
    """
    Ask Groq for JSON. If parsing fails, try to extract JSON substring.
    Fallback to `default` if nothing parseable.
    """
    for attempt in range(retries + 1):
        try:
            resp = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            raw = resp.choices[0].message.content.strip()
            # Try direct JSON parse
            try:
                return json.loads(raw)
            except Exception:
                # Try to find JSON-like substring
                m = re.search(r"(\{.*\}|\[.*\])", raw, flags=re.DOTALL)
                if m:
                    try:
                        return json.loads(m.group(1))
                    except Exception:
                        pass
            # if here, parsing failed for this attempt
        except Exception as e:
            # network/LLM error, allow retry
            # small backoff
            time.sleep(0.3)
    return default

def safe_groq_text(prompt: str, default="", retries: int = 1) -> str:
    """
    Return raw LLM text with retries and safe fallback.
    """
    for attempt in range(retries + 1):
        try:
            resp = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            time.sleep(0.3)
    return default

# ---------------------------
# Resource mapping
# ---------------------------
def list_available_resources(limit: int = 10000) -> List[str]:
    """Read distinct resource names from Milvus (best-effort via query)."""
    try:
        results = collection.query(expr='resource != ""', output_fields=["resource"], limit=limit)
        return sorted({r["resource"] for r in results if r.get("resource")})
    except Exception as e:
        # fallback to empty
        return []

def best_fuzzy_match(query: str, candidates: List[str]) -> Optional[str]:
    if not candidates:
        return None
    lowered = [c.lower() for c in candidates]
    # try direct token matches
    q = query.lower()
    for c in candidates:
        if q in c.lower() or c.lower() in q:
            return c
    # difflib
    matches = difflib.get_close_matches(q, lowered, n=1, cutoff=0.6)
    if matches:
        idx = lowered.index(matches[0])
        return candidates[idx]
    # try cloudstack_ prefix
    if not q.startswith("cloudstack_"):
        matches = difflib.get_close_matches("cloudstack_" + q, candidates, n=1, cutoff=0.6)
        if matches:
            return matches[0]
    return None

def normalize_resource_query(user_input: str) -> Optional[str]:
    """
    Resolve natural user request into a canonical resource (cloudstack_xxx).
    Strategy:
      1) Ask Groq (with list of known resources) for best match.
      2) Fallback to fuzzy local heuristics.
    """
    known = list_available_resources()
    if not known:
        print("⚠ No resources found in Milvus index (cloudstack_docs). Did you ingest docs?") 
        return None

    # Ask LLM to select from list
    sys_prompt = "You map a user's natural-language request to one of the exact resource names listed below.\nReturn ONLY a single exact resource name that appears in the list. If unsure, pick the best match."
    user_prompt = f"User: \"{user_input}\"\nResources:\n" + "\n".join(known)
    try:
        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        name = resp.choices[0].message.content.strip()
        if name in known:
            return name
    except Exception:
        pass

    # Local fuzzy fallback
    fm = best_fuzzy_match(user_input, known)
    if fm:
        return fm

    # show small help
    print("⚠ Could not automatically map your query to a resource.")
    print("Available resources (sample):")
    for r in known[:40]:
        print("  -", r)
    return None

# ---------------------------
# RAG: get docs + required fields
# ---------------------------
def search_docs(resource_name: str) -> Tuple[List[str], List[str]]:
    """
    Return all doc chunks and required fields for a given resource.
    Handles Milvus query window limit by fetching in batches.
    """
    expr = f'resource == "{resource_name}"'
    batch_size = 1000
    offset = 0
    all_results = []

    while True:
        try:
            results = collection.query(
                expr=expr,
                output_fields=["text", "required_fields"],
                limit=batch_size,
                offset=offset
            )
        except Exception as e:
            break  # stop if we reach end or other query issue

        if not results:
            break

        all_results.extend(results)

        # If less than batch_size returned, no more data
        if len(results) < batch_size:
            break

        offset += batch_size

        # Hard safety stop to avoid infinite loops
        if offset >= 16000:
            break

    # Collect chunks
    chunks = [r["text"] for r in all_results if r.get("text")]
    required = []
    for r in all_results:
        rf = r.get("required_fields")
        if rf:
            try:
                parsed = json.loads(rf)
                if isinstance(parsed, list):
                    required = parsed
                    break
            except Exception:
                pass
    return chunks, required


# ---------------------------
# Optional fields extraction (robust)
# ---------------------------
def extract_optional_fields_from_docs(docs_text: str, required_fields: List[str]) -> List[str]:
    """
    Ask LLM to list optional fields, fallback to regex parsing.
    Returns a list of field names (strings).
    """
    prompt = f"""
Extract OPTIONAL argument/field names from the following Terraform CloudStack documentation.
Return ONLY a JSON array of strings, e.g. ["field1","field2"].
Exclude required fields: {required_fields}

Docs:
{docs_text}
"""
    result = safe_groq_json(prompt, default=None, retries=1)
    if isinstance(result, list):
        # ensure strings and filter duplicates
        return sorted({s for s in result if isinstance(s, str) and s not in required_fields})
    # Fallback: regex find lines with "(Optional)"
    optional = set()
    # Look only in Argument Reference sections (common pattern)
    section = docs_text
    # naive scan for "(Optional)" tokens, capture field token to left
    for m in re.finditer(r"([`]?([a-zA-Z0-9_]+)[`]?.{0,40})\((Optional)\)", section, flags=re.IGNORECASE):
        name = m.group(2)
        if name and (name not in required_fields):
            optional.add(name)
    return sorted(optional)

# ---------------------------
# Field suggestions and heuristics
# ---------------------------
def suggest_field_details(field: str, docs_text: str) -> Dict[str, Optional[object]]:
    """
    Ask LLM for type/example/default/options for a field. Safe fallback to regex heuristics.
    Returns a dict: {type, example, default, options}
    """
    prompt = f"""
You are given Terraform CloudStack documentation text. For the field name '{field}', return a JSON object:
{{"type": "...", "example": "...", "default": "...", "options": ["opt1","opt2"]}}
Use null for unknowns. Return ONLY JSON.
Docs:
{docs_text}
"""
    result = safe_groq_json(prompt, default=None, retries=1)
    if isinstance(result, dict):
        # normalize keys
        return {
            "type": result.get("type"),
            "example": result.get("example"),
            "default": result.get("default"),
            "options": result.get("options"),
        }
    # Fallback heuristics (very conservative)
    details = {"type": None, "example": None, "default": None, "options": None}
    # Try to find "Default: X" or "Defaults to X" patterns
    m = re.search(rf"{re.escape(field)}[^\n]{{0,120}}default[s]?:\s*`?([^`\n,]+)`?", docs_text, flags=re.IGNORECASE)
    if m:
        details["default"] = m.group(1).strip()
    # Try to discover options like "Valid options are X, Y, Z"
    m2 = re.search(rf"{re.escape(field)}[^\n]{{0,160}}(valid options|allowed values)[^\n]*:?\s*([^\n]+)", docs_text, flags=re.IGNORECASE)
    if m2:
        opts = re.findall(r"[A-Za-z0-9_\-]+", m2.group(2))
        if opts:
            details["options"] = opts
    # Find examples like "e.g., ubuntu-20.04" or "`ubuntu-20.04`"
    m3 = re.search(rf"{re.escape(field)}[^\n]{{0,160}}(?:e\.g\.|for example|example)[^\n:]*[:\-]?\s*`?([A-Za-z0-9_\-\.]+)`?", docs_text, flags=re.IGNORECASE)
    if m3:
        details["example"] = m3.group(1).strip()
    return details

# ---------------------------
# Field validation (LLM + heuristic fallback)
# ---------------------------
def validate_field_value(field: str, value: str, docs_text: str, details: Dict[str, Optional[object]]) -> Tuple[bool, str]:
    """
    Validate the value for the field:
    - Ask Groq to return 'valid' or 'invalid' (only).
    - If Groq fails, apply heuristics (options match, basic type checks).
    Returns (is_valid, reason_or_empty)
    """
    # quick empty check
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return False, "empty"

    # 1) Try LLM validator
    prompt = f"""
Docs:
{docs_text}

Decide whether the following value is VALID for the Terraform field '{field}'. Return ONLY the word 'valid' or 'invalid'.

Field: {field}
Value: {value}
"""
    text = safe_groq_text(prompt, default="invalid", retries=1).lower()
    if "valid" in text and "invalid" not in text:
        return True, ""
    if "invalid" in text and "valid" not in text:
        return False, text.strip()

    # 2) Fallback heuristics using 'details'
    options = details.get("options") if details else None
    if options:
        if isinstance(options, list) and str(value) in [str(o) for o in options]:
            return True, ""
        else:
            return False, f"value not in allowed options {options}"

    typ = details.get("type") if details else None
    if typ:
        t = (typ or "").lower()
        if "int" in t or "number" in t:
            if re.fullmatch(r"^-?\d+$", value):
                return True, ""
            else:
                return False, "not an integer"
        if "bool" in t:
            if value.lower() in ("true", "false", "1", "0", "yes", "no"):
                return True, ""
            else:
                return False, "not a boolean"
    # last resort: accept
    return True, ""

# ---------------------------
# User input flow with suggestions + validation
# ---------------------------
def prompt_for_fields(fields: List[str], docs_text: str, required: bool = True) -> Dict[str, str]:
    """
    For each field:
      - get details (example/default/options)
      - prompt user showing suggestions
      - validate input (repeat until valid or user chooses to skip for optional)
    Returns dict field->value for those provided (required fields must be valid)
    """
    out = {}
    for f in fields:
        details = suggest_field_details(f, docs_text)
        suggestion_parts = []
        if details.get("default"):
            suggestion_parts.append(f"default={details['default']}")
        if details.get("example"):
            suggestion_parts.append(f"example={details['example']}")
        if details.get("options"):
            suggestion_parts.append(f"options={details['options']}")
        if details.get("type"):
            suggestion_parts.append(f"type={details['type']}")

        suggestions = ", ".join(suggestion_parts) if suggestion_parts else "no suggestion"

        while True:
            prompt_txt = f"Enter value for '{f}' [{suggestions}]: "
            val = input(prompt_txt).strip()
            if val == "" and details.get("default") is not None:
                val = str(details["default"])
                print(f"➡ Using default {val}")

            if val == "" and not required:
                # optional and user skipped
                break

            ok, reason = validate_field_value(f, val, docs_text, details)
            if ok:
                out[f] = val
                break
            else:
                print(f"❌ Invalid value for '{f}': {reason}. Please try again.")
                # if not required allow skip
                if not required:
                    choice = input("Type 'retry' to try again, or Enter to skip this optional field: ").strip().lower()
                    if choice != "retry":
                        break
    return out

# ---------------------------
# Generation: final terraform HCL
# ---------------------------
def generate_terraform_hcl(resource_name: str, docs_chunks: List[str], provided_values: Dict[str,str], required_fields: List[str]) -> str:
    """
    Build a careful prompt that enforces:
      - Use only provider cloudstack/cloudstack
      - Use provided values
      - If some required field still missing, LLM must return a single-line comment:
        MISSING_REQUIRED:<field>
      - Return ONLY pure HCL code without markdown formatting
    """
    context = "\n\n---\n\n".join(docs_chunks[:MAX_CONTEXT_CHUNKS])
    sys_msg = (
        "You are an expert Terraform generator for the CloudStack provider.\n"
        "Produce ONLY valid Terraform HCL for a single resource of the requested type.\n"
        "Rules:\n"
        "- Provider must be cloudstack/cloudstack.\n"
        "- Use only the fields provided by the user for required fields.\n"
        "- If any required field is missing, output exactly one line starting with 'MISSING_REQUIRED:' and the field name and nothing else.\n"
        "- Optional fields may be included if provided by the user.\n"
        "- Output ONLY raw HCL code - NO markdown formatting, NO code fences, NO backticks.\n"
        "- Do NOT wrap the output in ```hcl or ``` or any other formatting.\n"
        "- Start directly with 'resource' keyword.\n"
    )
    user_msg = f"""
RESOURCE: {resource_name}

USER VALUES:
{json.dumps(provided_values, indent=2)}

REQUIRED FIELDS:
{required_fields}

CONTEXT (docs excerpt):
{context}

Output: ONLY raw Terraform HCL code (no prose, no markdown, no code fences). If MISSING_REQUIRED, output that single line.
"""
    
    try:
        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role":"system", "content": sys_msg}, {"role":"user", "content": user_msg}],
            temperature=0.1
        )
        raw_output = resp.choices[0].message.content.strip()
        
        # Clean up any markdown formatting that might have slipped through
        cleaned_output = clean_terraform_output(raw_output)
        
        return cleaned_output
        
    except Exception as e:
        return f"# Error generating Terraform: {str(e)}"

def clean_terraform_output(raw_output: str) -> str:
    """
    Remove markdown formatting and other unwanted content from LLM output.
    Returns clean HCL code.
    """
    # Remove markdown code fences
    cleaned = re.sub(r'```(?:hcl|terraform)?\s*\n?', '', raw_output)
    cleaned = re.sub(r'```\s*$', '', cleaned)
    
    # Remove any leading/trailing markdown or prose
    lines = cleaned.split('\n')
    hcl_lines = []
    inside_resource = False
    
    for line in lines:
        # Start collecting when we see a resource block
        if line.strip().startswith('resource '):
            inside_resource = True
            hcl_lines.append(line)
        elif inside_resource:
            hcl_lines.append(line)
            # Stop if we hit a closing brace at root level
            if line.strip() == '}' and not any(c in ''.join(hcl_lines[:-1]) for c in ['{', '}']):
                break
        # Handle MISSING_REQUIRED case
        elif line.strip().startswith('MISSING_REQUIRED:'):
            return line.strip()
    
    # If no resource block found, try to extract any HCL-looking content
    if not hcl_lines:
        for line in lines:
            # Look for any line that looks like HCL (has = or { or })
            if any(char in line for char in ['=', '{', '}']) and not line.strip().startswith('#'):
                hcl_lines.append(line)
    
    result = '\n'.join(hcl_lines).strip()
    
    # Final cleanup - ensure we have valid content
    if not result or 'resource' not in result:
        # If we still don't have good content, return the original but cleaned
        fallback = raw_output
        fallback = re.sub(r'```(?:hcl|terraform)?\s*\n?', '', fallback)
        fallback = re.sub(r'```\s*', '', fallback)
        return fallback.strip()
    
    return result
# ---------------------------
# Save files
# ---------------------------
def save_generated(resource_name: str, provided_values: Dict[str,str], terraform_code: str) -> Path:
    safe_name = provided_values.get("name") or provided_values.get("display_name") or "resource"
    safe_name = re.sub(r"[^a-zA-Z0-9_\-]+", "_", safe_name)[:64]
    fname = OUTPUT_DIR / f"terraform_{resource_name}_{safe_name}.tf"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(terraform_code)
    return fname

# ---------------------------
# Main flow
# ---------------------------
def main():
    print("Milvus RAG Terraform Agent (Step 1: validation & suggestions)\n")

    user_q = input("What do you want to provision? ").strip()
    if not user_q:
        print("Nothing provided, exiting.")
        return

    resource = normalize_resource_query(user_q)
    if not resource:
        print("Could not resolve resource. Aborting.")
        return
    print(f"[Resolved resource] {resource}")

    docs_chunks, required_fields = search_docs(resource)
    if not docs_chunks:
        print("No documentation chunks found in Milvus for resource. Aborting.")
        return

    # Compose context for suggestions
    docs_context = "\n\n".join(docs_chunks[:MAX_CONTEXT_CHUNKS])

    print(f"Required fields: {required_fields}")

    # Extract optional fields (robust)
    optional_fields = extract_optional_fields_from_docs(docs_context, required_fields)
    if optional_fields:
        print(f"Detected optional fields: {optional_fields}")

    # 1) Ask required fields (must fill & validate)
    required_vals = prompt_for_fields(required_fields, docs_context, required=True)

    # 2) Ask optional fields optionally
    opt_vals = {}
    if optional_fields:
        if input("Do you want to fill optional fields? (y/N): ").strip().lower() == "y":
            opt_vals = prompt_for_fields(optional_fields, docs_context, required=False)

    combined = {**required_vals, **opt_vals}
    # final check that all required provided
    missing = [f for f in required_fields if not combined.get(f)]
    if missing:
        print("❌ Required fields missing after prompting:", missing)
        print("Aborting to let you re-run and fill them.")
        return

    # Generate HCL
    hcl = generate_terraform_hcl(resource, docs_chunks, combined, required_fields)

    # If LLM signaled MISSING_REQUIRED, stop and show
    if isinstance(hcl, str) and hcl.strip().startswith("MISSING_REQUIRED:"):
        print("\nLLM reports missing required field:", hcl.strip())
        print("Please re-run and provide the missing value(s).")
        return
# Add this code right after: hcl = generate_terraform_hcl(...)
# and before: path = save_generated(...)

    # Check for LLM error signal
    if isinstance(hcl, str) and hcl.strip().startswith("MISSING_REQUIRED:"):
        print("\nLLM reports missing required field:", hcl.strip())
        print("Please re-run and provide the missing value(s).")
        return

    # NEW: Terraform Validation
    if TERRAFORM_VALIDATION_ENABLED:
        print("\n🔍 Validating generated Terraform configuration...")
        validation_results = comprehensive_terraform_validation(hcl, required_fields)
        print_validation_results(validation_results)
        
        # Handle validation failures
        if not validation_results['overall_valid']:
            print("\n❌ Validation failed. What would you like to do?")
            print("1. Save anyway (s)")
            print("2. Abort and fix manually (a)")
            print("3. Show the code and decide (v)")
            
            choice = input("Choose [s/a/v]: ").strip().lower()
            
            if choice == 'a':
                print("Aborting. Please fix the issues and try again.")
                return
            elif choice == 'v':
                print("\n===== GENERATED TERRAFORM (WITH ISSUES) =====")
                print(hcl)
                print("=" * 50)
                
                save_choice = input("\nSave this code anyway? [y/N]: ").strip().lower()
                if save_choice != 'y':
                    print("Aborting.")
                    return
            # If choice == 's' or user chose to save after viewing, continue
        else:
            print("✅ All validations passed!")
    
    # Continue with saving (your existing code)
    path = save_generated(resource, combined, hcl)
    
    # Update the final output message
    if TERRAFORM_VALIDATION_ENABLED and validation_results.get('overall_valid'):
        print(f"\n✅ Validated Terraform configuration saved to: {path.resolve()}")
    else:
        print(f"\n💾 Terraform configuration saved to: {path.resolve()}")
        if TERRAFORM_VALIDATION_ENABLED and not validation_results.get('overall_valid'):
            print("⚠️  Note: Contains validation warnings - review before applying")
    
    print("\n===== GENERATED TERRAFORM =====")
    print(hcl)
    
    # Add helpful next steps
    print("\n===== NEXT STEPS =====")
    print("1. Review the configuration file")
    print("2. cd to the directory containing the .tf file")
    print("3. Run: terraform init")
    print("4. Run: terraform plan")
    print("5. Run: terraform apply (if plan looks good)")
    
    if TERRAFORM_VALIDATION_ENABLED and not validation_results.get('overall_valid'):
        print("\n⚠️  Fix validation issues before running terraform apply")
    path = save_generated(resource, combined, hcl)
    print(f"\n✅ Terraform saved to: {path.resolve()}\n")
    print("===== GENERATED TERRAFORM =====\n")
    print(hcl)

if __name__ == "__main__":
    main()
