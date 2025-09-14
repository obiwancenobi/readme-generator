import os
import time
import re
import argparse
from openai import OpenAI
import google.generativeai as genai
import textwrap

# If using OpenAI
# Make sure you set your API key before running:
# export OPENAI_API_KEY="your_api_key_here"
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# If using Cerebras
# Make sure you set your API key before running:
# export CEREBRAS_API_KEY="your_api_key_here"


IGNORED_DIRS = {".git", ".github", "__pycache__", "node_modules", "build", "dist", ".idea", ".vscode", "venv", ".venv", "__snapshots__"}
ALLOWED_EXTS = (".py", ".js", ".ts", ".dart", ".java", ".kt", ".go", ".rs", ".swift", ".md", ".json", ".yml", ".yaml")
IGNORED_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "Cargo.lock", "poetry.lock", "pubspec.lock",
    "requirements.txt", "Pipfile.lock"
}

MAX_FILE_SIZE = 50_000   # skip files bigger than 50KB
MAX_CHARS = 12_000       # safe chunk size (~8-10k tokens)

def initialize_ai_client(provider, api_key=None, base_url=None):
    """Initialize AI client based on provider"""
    if provider == "deepseek":
        api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        base_url = base_url or "https://api.deepseek.com/v1"
        return OpenAI(api_key=api_key, base_url=base_url)
    elif provider == "openai":
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        return OpenAI(api_key=api_key)
    elif provider == "ollama":
        api_key = "ollama"  # Ollama doesn't require an API key
        base_url = base_url or "http://localhost:11434/v1"
        return OpenAI(api_key=api_key, base_url=base_url)
    elif provider == "cerebras":
        api_key = api_key or os.getenv("CEREBRAS_API_KEY")
        base_url = base_url or "https://api.cerebras.ai/v1"
        return OpenAI(api_key=api_key, base_url=base_url)
    elif provider == "gemini":
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    elif provider == "openrouter":
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        base_url = base_url or "https://openrouter.ai/api/v1"
        return OpenAI(api_key=api_key, base_url=base_url)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def collect_repo_content(path="."):
    repo_texts = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for filename in files:
            if filename in IGNORED_FILES:
                continue
            if not filename.lower().endswith(ALLOWED_EXTS):
                continue

            file_path = os.path.join(root, filename)
            try:
                if os.path.getsize(file_path) > MAX_FILE_SIZE:
                    print(f"⚠️ Skipped large file: {file_path}")
                    continue

                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    repo_texts.append(f"# File: {file_path}\n{content}")

            except Exception as e:
                print(f"⚠️ Skipped {file_path}: {e}")
    return "\n\n".join(repo_texts)

def chunk_text(text, max_chars=MAX_CHARS):
    """Split long text into chunks within safe size."""
    return textwrap.wrap(text, max_chars)

def summarize_chunk(chunk, idx, model):
    global provider
    prompt = f"""
    You are an expert software documenter.
    Summarize this part of the repository (chunk {idx}).
    Focus on describing purpose, features, and usage.

    Content:
    {chunk}
    """

    if provider == "gemini":
        response = client.generate_content(prompt)
        return response.text
    else:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()

def extract_preserved_sections(readme_content):
    """Extract sections that should be preserved from existing README"""
    preserved = {}
    
    # Extract license section (everything from ## License to end of file)
    license_pattern = r"(## License\s*\n(?:.|\n)*)"
    license_match = re.search(license_pattern, readme_content)
    if license_match:
        preserved['license'] = license_match.group(1)
    
    # Extract contributing section
    contributing_pattern = r"(## Contributing\s*\n(?:.|\n)*?)(?=\n## \w+|\Z)"
    contributing_match = re.search(contributing_pattern, readme_content)
    if contributing_match:
        preserved['contributing'] = contributing_match.group(1)
    
    # Extract installation/setup section
    installation_pattern = r"(## Installation\s*\n(?:.|\n)*?)(?=\n## \w+|\Z)"
    installation_match = re.search(installation_pattern, readme_content)
    if installation_match:
        preserved['installation'] = installation_match.group(1)
    
    setup_pattern = r"(## Setup\s*\n(?:.|\n)*?)(?=\n## \w+|\Z)"
    setup_match = re.search(setup_pattern, readme_content)
    if setup_match:
        preserved['setup'] = setup_match.group(1)
    
    return preserved

def generate_readme(chunks, model):
    global provider
    summaries = []
    for i, chunk in enumerate(chunks, 1):
        print(f"📝 Summarizing chunk {i}/{len(chunks)}...")
        summaries.append(summarize_chunk(chunk, i, model))

    combined_summary = "\n\n".join(summaries)

    # Check if README.md exists and extract preserved sections
    preserved_sections = {}
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            existing_content = f.read()
            preserved_sections = extract_preserved_sections(existing_content)

    # Format preserved sections for the prompt
    preserved_info = ""
    if preserved_sections:
        preserved_info = "\n\nIMPORTANT: The following sections from the existing README.md should be preserved in the final output:\n"
        for section_name, content in preserved_sections.items():
            preserved_info += f"{section_name.capitalize()} section:\n```\n{content}\n```\n\n"

    final_prompt = f"""
    Based on the provided summaries of repository chunks, generate a complete and professional README.md file if one does not already exist. If a README.md is present, update and improve it accordingly.
    Include:
    - Project Title
    - Description
    - Features
    - Installation / Setup instructions
    - Usage examples
    - Tech stack
    - Screenshots
    - Contributing (if applicable)
    - License (leave placeholder if unknown)

    Summaries:
    {combined_summary}

    {preserved_info}
    """

    if provider == "gemini":
        response = client.generate_content(final_prompt)
        return response.text
    else:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": final_prompt}],
        )
        return response.choices[0].message.content.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate or update README.md using AI")
    parser.add_argument("--provider", choices=["deepseek", "openai", "ollama", "cerebras", "gemini", "openrouter"], default="deepseek",
                        help="AI provider to use (default: deepseek)")
    parser.add_argument("--model", default="deepseek-chat",
                         help="Model to use for AI generation (default: deepseek-chat for DeepSeek, gpt-4 for OpenAI, llama3 for Ollama, llama3.1 for Cerebras, gemini-1.5-flash for Gemini, openai/gpt-4o for OpenRouter)")
    parser.add_argument("--api-key", help="API key for the selected provider")
    parser.add_argument("--base-url", help="Base URL for the selected provider")
    
    args = parser.parse_args()
    
    provider = args.provider
    start_time = time.time()
    print("📦 Collecting repository content...")
    repo_content = collect_repo_content()

    print("🔧 Initializing AI client...")
    client = initialize_ai_client(args.provider, args.api_key, args.base_url)

    print("🔪 Splitting into chunks...")
    chunks = chunk_text(repo_content)

    print(f"🤖 Summarizing {len(chunks)} chunks...")
    readme_content = generate_readme(chunks, args.model)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    end_time = time.time()
    duration = end_time - start_time
    print(f"✅ README.md has been generated/updated successfully!")
    if duration < 60:
        print(f"⏱️ Total execution time: {duration:.2f} seconds")
    else:
        minutes = int(duration // 60)
        seconds = duration % 60
        print(f"⏱️ Total execution time: {minutes} minutes {seconds:.2f} seconds")