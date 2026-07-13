import asyncio
import re
import os
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
# 🟢 New Database Import
import chromadb

def get_base_domain(url: str) -> str:
    return urlparse(url).netloc

def clean_and_chunk_text(raw_text: str, chunk_size: int = 250, overlap: int = 50) -> list:
    cleaned_text = re.sub(re.compile(r'\s+'), ' ', raw_text).strip()
    words = cleaned_text.split(' ')
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i : i + chunk_size]
        if len(chunk_words) < 30 and len(chunks) > 0:
            continue
        chunks.append(" ".join(chunk_words))
    return chunks

async def crawl_site_deeply(target_url: str, status_box=None) -> str:
    base_domain = get_base_domain(target_url)
    pages_to_visit = set([target_url])
    visited_pages = set()
    all_raw_extracted_text = ""

    async with async_playwright() as p:
        if status_box:
            status_box.update(label="🚀 Initializing Stealth Firefox Core...", state="running")
            
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        try:
            msg1 = f"🕵️ Mapping website infrastructure: {target_url}"
            if status_box: status_box.write(msg1)
            
            await page.goto(target_url, wait_until="domcontentloaded", timeout=25000)
            await page.wait_for_timeout(3000) 
            
            homepage_html = await page.content()
            soup = BeautifulSoup(homepage_html, 'html.parser')
            
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']
                full_url = urljoin(target_url, href)
                
                if get_base_domain(full_url) == base_domain:
                    lower_url = full_url.lower()
                    if any(keyword in lower_url for keyword in ["about", "service", "product", "contact", "feature", "solutions"]):
                        pages_to_visit.add(full_url)

            final_queue = list(pages_to_visit)[:4]
            msg2 = f"📌 Located {len(final_queue)} valid target paths inside network boundary."
            if status_box: status_box.write(msg2)

            for current_page_url in final_queue:
                if current_page_url in visited_pages:
                    continue
                    
                msg3 = f"📖 Deep reading: {current_page_url}"
                if status_box: status_box.write(msg3)
                
                visited_pages.add(current_page_url)
                
                await page.goto(current_page_url, wait_until="domcontentloaded", timeout=25000)
                await page.wait_for_timeout(2000)
                
                page_html = await page.content()
                page_soup = BeautifulSoup(page_html, 'html.parser')
                for element in page_soup(["script", "style", "nav", "footer", "header", "noscript"]):
                    element.decompose()
                
                clean_page_text = page_soup.get_text(separator=' ', strip=True)
                all_raw_extracted_text += f" [Source: {current_page_url}] " + clean_page_text

            # Text Chunking Phase
            structured_chunks = clean_and_chunk_text(all_raw_extracted_text, chunk_size=200, overlap=40)
            
            # 🟢 WEEK 4 VECTOR DATABASE COMMIT PHASE
            msg4 = "💾 Initializing Vector Database Vectoring Engine..."
            if status_box: status_box.write(msg4)
            
            # Initialize a persistent database instance (saves data into a folder named 'chroma_db')
            chroma_client = chromadb.PersistentClient(path="./chroma_db")
            
            # Create or load a data collection table inside the database
            collection = chroma_client.get_or_create_collection(name="account_intelligence")
            
            # Prepare unique metadata lists and incremental IDs for the database entries
            documents_ids = [f"id_{base_domain}_{i}" for i in range(len(structured_chunks))]
            metadata_entries = [{"source": base_domain} for _ in structured_chunks]
            
            # Save the chunks cleanly into our vector database
            collection.upsert(
                documents=structured_chunks,
                ids=documents_ids,
                metadatas=metadata_entries
            )
            
            msg5 = f"🔒 Committed {len(structured_chunks)} structured data fragments securely to local vector memory storage."
            if status_box: status_box.write(msg5)
            
            # Stitch chunks for the layout stream output
            formatted_output = "\n\n=== CHROMA DB FRAGMENT ===\n".join(structured_chunks)
            return formatted_output

        except Exception as e:
            return f"Error crawling page: {str(e)}"
        finally:
            await browser.close()

def run_scraper(url: str, status_box=None) -> str:
    return asyncio.run(crawl_site_deeply(url, status_box))