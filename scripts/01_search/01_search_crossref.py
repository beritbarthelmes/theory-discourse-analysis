"""
Project: Theory Discourse Analysis
Retrieve available PDF links from Crossref for a list of DOIs and download them
via a browser-based workflow.

Outputs:
- PDFs downloaded via the system browser (location determined by browser settings)

Notes:
- Uses Selenium to respect publisher-controlled download mechanisms
- Requires local Chrome installation and compatible ChromeDriver
- Intended for manual or semi-automated use due to copyright restrictions
"""

from crossref.restful import Works
from selenium import webdriver
from time import sleep


def get_driver():
    """Initialize a visible Chrome browser for PDF downloading."""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-logging')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option(
        'prefs',
        {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        }
    )
    driver = webdriver.Chrome(options=options)
    return driver


def fetch_articles_crossref(dois, wait_time=3):
    """
    For each DOI, query Crossref for available PDF links and open them
    in a browser to trigger downloads.
    """
    driver = get_driver()
    works = Works()

    for doi in dois:
        try:
            article = works.doi(doi)
        except Exception:
            continue

        if not article or "link" not in article:
            continue

        try:
            pdf_link = next(
                link for link in article["link"]
                if link.get("content-type") == "application/pdf"
            )
        except StopIteration:
            pdf_link = None

        if pdf_link:
            driver.get(pdf_link["URL"])
            sleep(wait_time)

    driver.quit()
