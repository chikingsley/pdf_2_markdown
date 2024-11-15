# PDF to Markdown Converter

A Python-based tool for converting PDF documents to clean, formatted Markdown text. This tool processes PDF files and generates well-structured markdown output while maintaining readability and document structure.

## Features

- PDF to Markdown conversion
- Text cleaning and formatting
- Maintains document structure
- Supports readability optimization

## Requirements

- Python 3.x
- Dependencies:
  - streamlit >= 1.24.0
  - PyMuPDF >= 1.22.0
  - spacy >= 3.5.0
  - nltk >= 3.8.1
  - pyyaml >= 6.0
  - python-slugify >= 8.0.1

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pdf_2_markdown.git
cd pdf_2_markdown
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your PDF file in the project directory
2. Run the conversion script:
```bash
python main2.py
```

## Project Structure

- `main2.py`: Main conversion script
- `cleaner1.py`: Text cleaning and processing utilities
- `Readability.js`: JavaScript module for readability improvements
- `Readability Helpers.js`: Helper functions for readability processing
- `requirements.txt`: Python dependencies
- `config.toml`: Configuration settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
