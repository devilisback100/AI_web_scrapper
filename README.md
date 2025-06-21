#  AI Chapter Rewriter & Reviewer

An AI-powered content pipeline that scrapes literature chapters from Wikisource, rewrites them using Large Language Models (LLMs), facilitates human-in-the-loop edits, captures webpage screenshots, and stores all final versions with RL-enhanced search capabilities using ChromaDB.

---

##  Features

| Module                  | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
|  Scraping             | Fetches chapter content from Wikisource using `requests`.                  |
|  AI Writing & Review  | Rewrites chapters with an AI writer and reviewer (LLM-powered).            |
|  Human-in-the-loop    | Allows manual review and iterative improvements before finalizing.         |
|  Screenshot Capture   | Uses `Playwright` to capture full-page screenshots of the source.          |
|  Agentic Flow         | Structured AI agents (writer, reviewer, editor) in a modular pipeline.     |
|  ChromaDB Storage     | Saves rewritten chapters with metadata for versioning and retrieval.       |
|  RL-based Search      | Retrieves chapters based on semantic similarity and RL score re-ranking.   |

---

##  Tech Stack

- **Python** – Core programming language  
- **Playwright** – Full-page screenshot automation  
- **Requests** – HTML content fetching  
- **ChromaDB** – Vector DB for document storage and search  
- **TQDM** – Progress tracking  
- **Dotenv** – Environment variable management  

---

##  Installation

```bash
# 1. Clone the repository
git clone https://github.com/devilisback100/AI_web_scrapper.git
cd AI_web_scrapper

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright's browser binaries
playwright install
