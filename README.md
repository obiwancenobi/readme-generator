# Auto README Generator

An automated Python tool that generates professional README.md files for any code repository using various AI APIs. It intelligently analyzes your codebase and creates documentation with minimal setup, supporting multiple AI providers.

## Features

- **Multi-Provider AI Support**: Works with DeepSeek, OpenAI, Ollama, Cerebras, Gemini, and OpenRouter AI models
- **AI-Powered Documentation**: Automatically generates professional README files using advanced language models
- **Smart Content Collection**: Walks through your repository and collects relevant files while ignoring unnecessary directories and files
- **Large File Handling**: Skips files larger than 50KB to prevent API overload
- **Content Chunking**: Splits large repositories into manageable chunks for optimal AI processing
- **Multi-Language Support**: Works with Python, JavaScript, TypeScript, Dart, Java, Kotlin, Go, Rust, Swift, and more
- **Selective File Processing**: Only processes files with common development extensions
- **Performance Tracking**: Shows execution time for README generation
- **Error Handling**: Gracefully skips files that cannot be processed

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install openai google-generativeai
   ```

## Setup

Before using the tool, you need to set up your API key for the selected provider:

### For DeepSeek (default):
1. Get your API key from [DeepSeek API](https://api.deepseek.com/)
2. Set the environment variable:
   ```bash
   export DEEPSEEK_API_KEY="your_api_key_here"
   ```

### For OpenAI:
1. Get your API key from [OpenAI API](https://platform.openai.com/)
2. Set the environment variable:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

### For Ollama:
1. Install and run [Ollama](https://ollama.com/)
2. Pull a model (e.g., llama3):
   ```bash
   ollama pull llama3
   ```

### For Cerebras:
1. Get your API key from [Cerebras API](https://www.cerebras.ai/)
2. Set the environment variable:
   ```bash
   export CEREBRAS_API_KEY="your_api_key_here"
   ```
### For Gemini:
1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the environment variable:
    ```bash
    export GEMINI_API_KEY="your_api_key_here"
    ```

### For OpenRouter:
1. Get your API key from [OpenRouter](https://openrouter.ai/)
2. Set the environment variable:
    ```bash
    export OPENROUTER_API_KEY="your_api_key_here"
    ```

## Usage

Run the script from the root of any repository with optional arguments:

```bash
python generate_readme.py [--provider PROVIDER] [--model MODEL] [--api-key API_KEY] [--base-url BASE_URL]
```

### Options:
- `--provider`: AI provider to use (choices: "deepseek", "openai", "ollama", "cerebras", "gemini", "openrouter", default: "deepseek")
- `--model`: Model to use for AI generation (default: "deepseek-chat")
- `--api-key`: API key for the selected provider (optional, can use environment variables)
- `--base-url`: Base URL for the selected provider (optional, uses defaults if not provided)

### Examples:
```bash
# Using DeepSeek (default)
python generate_readme.py

# Using OpenAI with GPT-4
python generate_readme.py --provider openai --model gpt-4

# Using Ollama with Llama3
python generate_readme.py --provider ollama --model llama3
# Using Gemini
python generate_readme.py --provider gemini

# Using a specific model with DeepSeek
python generate_readme.py --provider deepseek --model deepseek-coder

# Using Cerebras with llama3.1
python generate_readme.py --provider cerebras --model llama3.1

# Using OpenRouter with GPT-4o
python generate_readme.py --provider openrouter --model openai/gpt-4o
```

The script will:
1. Collect all relevant files in the repository
2. Split the content into manageable chunks
3. Generate summaries for each chunk using the selected AI provider
4. Create a complete README.md file based on these summaries

## Tech Stack

- **Python 3**: Main programming language
- **Multiple AI Providers**:
  - DeepSeek API (default)
  - OpenAI API
  - Ollama (local AI models)
  - Cerebras API
  - Google Gemini API
  - OpenRouter API
- **OpenAI Python Library**: For API communication (all providers use OpenAI-compatible APIs)
- **Standard Libraries**: 
  - `os` for file system operations
  - `time` for execution timing
  - `textwrap` for content chunking
  - `argparse` for command-line argument parsing

## How It Works

The script follows a three-step process:

1. **Content Collection**: Uses `os.walk` to traverse the repository, collecting code from files while ignoring common build artifacts, dependency directories, and large files
2. **Content Chunking**: Splits the collected content into appropriately sized chunks (around 8-10k tokens) for AI processing
3. **AI Processing**: 
   - Sends each chunk to the selected AI provider for summarization
   - Combines all summaries and sends them to the AI provider to generate the final README

## Limitations

- Requires an API key for DeepSeek, OpenAI, Cerebras, Gemini, or OpenRouter (which may have associated costs)
- For Ollama, requires local installation and model downloads
- For Cerebras, requires an API key from Cerebras
- For Gemini, requires an API key from Google AI Studio
- For OpenRouter, requires an API key from OpenRouter
- Only processes files up to 50KB in size
- Limited to specific file extensions (`.py`, `.js`, `.ts`, `.dart`, `.java`, `.kt`, `.go`, `.rs`, `.swift`, `.md`, `.json`, `.yml`, `.yaml`)
- May not perfectly capture all project-specific details and nuances

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.