from scraper import scrape_chapter
from agents import orchestrator
from chroma_store import save_to_chroma, search_chroma, list_all_documents, get_document_by_index
from rl_ranker import record_feedback, re_rank
from dotenv import load_dotenv
from human_review import human_review
import os
import hashlib
import subprocess
import asyncio

load_dotenv()


def generate_id_from_url(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def retry_logic(current_url):
    chapter_text = scrape_chapter(current_url)
    spun, reviewed = orchestrator(chapter_text)
    return chapter_text, spun, reviewed


def capture_screenshot(url: str):
    async def run():
        from playwright.async_api import async_playwright
        import hashlib
        import os

        
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        hash_id = hashlib.md5(url.encode()).hexdigest()
        filename = os.path.join(screenshots_dir, f"{hash_id}_screenshot.png")

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.screenshot(path=filename, full_page=True)
            await browser.close()

        print(f" Screenshot saved to: {filename}")

    asyncio.run(run())


def run_scrape_flow():
    url = input("Enter chapter URL: ").strip()
    if not url:
        print(" No URL provided.")
        return

    print("[1] Scraping content...")
    chapter_text = scrape_chapter(url)

    print("[2] Running agents...")
    spun, reviewed = orchestrator(chapter_text)

    print("[3] Human review in progress...")
    final_text = human_review(
        chapter_text,
        spun,
        reviewed,
        retry_callback=lambda: retry_logic(url)
    )

    print(" Capturing screenshot of the chapter...")
    capture_screenshot(url)

    print("[4] Saving to ChromaDB...")
    doc_id = generate_id_from_url(url)
    save_to_chroma(final_text, {"id": doc_id, "source": url})
    record_feedback(doc_id, reward=1)


def run_history_view():
    print("\n Listing all stored chapters...\n")
    list_all_documents()
    selection = input(
        "\n Enter any valid number to view full text (or press Enter to go back): ").strip()
    if selection.isdigit():
        index = int(selection) - 1
        content, meta = get_document_by_index(index)
        if content:
            print(f"\n Full Content of Chapter from: {meta.get('source')}\n")
            print(content)
            save_option = input(
                "\n Do you want to save the full content as a .txt file? [y/n]: ").strip().upper()
            if save_option == 'y':
                filename = f"{content.split()[0]}_{content.split()[1]}_{content.split()[-1]}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f" Saved to: ./{filename}")


def run_search():
    query = input(
        "[] Enter a search phrase (e.g., 'stormy sea'): ").strip()
    if query:
        results = search_chroma(query)
        ranked = re_rank(results)
        if ranked:
            top = ranked[0]
            print("\nTop Match Summary:",
                  top['source'], "| RL Score:", top.get('rl_score', 0))
            preview = top.get('text', '(No preview available)')[:500]
            print("Content Preview:\n", preview, "...\n")
        else:
            print("No relevant match found.")
    else:
        print(" Skipping Search no input seem to be provided")


def main():
    while True:
        print("\n Content Pipeline Menu:")
        print("1. Scrape new chapter & run AI flow")
        print("2. View rewrite history")
        print("3. Search rewritten chapters")
        print("4. Exit")
        choice = input("Choose an option [1/2/3/4]: ").strip()

        if choice == '1':
            run_scrape_flow()
        elif choice == '2':
            run_history_view()
        elif choice == '3':
            run_search()
        elif choice == '4':
            print(" Exiting")
            break
        else:
            print(" Invalid option, Please try again.")


if __name__ == "__main__":
    main()
