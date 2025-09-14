# Auto README Generator

An automated Python tool that generates professional README.md files for any code repository using the DeepSeek AI API. It intelligently analyzes your codebase and creates documentation with minimal setup.

## Features

- **AI-Powered Documentation**: Automatically generates professional README files using DeepSeek's advanced language model
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
   pip install openai
   ```

## Setup

Before using the tool, you need to set up your DeepSeek API key:

1. Get your API key from [DeepSeek API](https://api.deepseek.com/)
2. Set the environment variable:
   ```bash
   export DEEPSEEK_API_KEY="your_api_key_here"
   ```

## Usage

Simply run the script from the root of any repository:

```bash
python generate_readme.py
```

The script will:
1. Collect all relevant files in the repository
2. Split the content into manageable chunks
3. Generate summaries for each chunk using DeepSeek AI
4. Create a complete README.md file based on these summaries

## Tech Stack

- **Python 3**: Main programming language
- **DeepSeek API**: AI model for generating documentation
- **OpenAI Python Library**: For API communication (DeepSeek is OpenAI-compatible)
- **Standard Libraries**: 
  - `os` for file system operations
  - `time` for execution timing
  - `textwrap` for content chunking

## How It Works

The script follows a three-step process:

1. **Content Collection**: Uses `os.walk` to traverse the repository, collecting code from files while ignoring common build artifacts, dependency directories, and large files
2. **Content Chunking**: Splits the collected content into appropriately sized chunks (around 8-10k tokens) for AI processing
3. **AI Processing**: 
   - Sends each chunk to DeepSeek AI for summarization
   - Combines all summaries and sends them to DeepSeek AI to generate the final README

## Limitations

- Requires a DeepSeek API key (which may have associated costs)
- Only processes files up to 50KB in size
- Limited to specific file extensions (`.py`, `.js`, `.ts`, `.dart`, `.java`, `.kt`, `.go`, `.rs`, `.swift`, `.md`, `.json`, `.yml`, `.yaml`)
- May not perfectly capture all project-specific details and nuances
- File paths in the system are hardcoded and may need adjustments for different repository structures

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.