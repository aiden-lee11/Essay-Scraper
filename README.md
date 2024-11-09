# Essay Scraper and Formatter

This project is a web scraper designed to retrieve example essays from publicly available sources, specifically **essays that worked** for university admissions. The scraper uses Python with `requests` and `BeautifulSoup` to gather essay content, prompts, and reviews, then formats this data into structured JSON and plain text files. 

The resulting data is saved in a folder structure optimized for data training purposes, with text and JSON files organized in subdirectories under an `essays` folder. This setup makes it convenient for applications in machine learning and natural language processing (NLP) pipelines.

## Features
- **Web Scraping**: Extracts essays, prompts, and associated reviews from an online resource.
- **Structured Formatting**: Organizes extracted data into JSON files, suitable for data analysis or training models, and plain text files for easy readability.
- **Feedback Extraction**: Includes both positive and negative feedback on each essay, providing valuable insights into what makes an effective essay.
  
## Project Structure
- `essays/`
  - `text/` — Contains each essay formatted as a plain text file.
  - `json/` — Contains each essay formatted as a structured JSON object for easy integration into machine learning workflows.

## Getting Started
### Prerequisites
- Python 3.x
- Required libraries: `requests`, `beautifulsoup4`

Install dependencies with:
```bash
pip install -r requirements.txt
``` 

### Usage
1. Run the scraper script:
```bash
python main.py
```

2. The script will output the extracted essays in the `essays/` directory.

