"""
Project: Theory Discourse Analysis
Automate EBSCOhost searches for a theory-specific query and access available full-text
articles via a browser-based workflow.

Outputs:
- PDFs downloaded via the system browser (location determined by browser settings)
- Optional: HTML full texts saved to ./ebsco_articles/html/ when get_html() is enabled

Notes:
- Institution-specific workflow (UZH ezproxy / EBSCOhost UI); selectors may require adaptation
- Uses Selenium to respect publisher-controlled access and copyright constraints
"""

from dotenv import load_dotenv
load_dotenv()
import os
import re
from time import sleep
 
# set up selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# build web driver, which operates on Chrome automatically, visible
def get_driver():
  options = webdriver.ChromeOptions()
  options.add_argument('--disable-logging')
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--ignore-ssl-errors')
  options.add_experimental_option('prefs',  {
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    }
  )
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
  return driver


def driver_wait(driver, selector, timeout_s):
    return WebDriverWait(driver, timeout_s).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )


def login(driver, url, username, password):
  driver.get(url) # driver goes to URL
  # Wait max. 10 seconds for the switch edu-ID element to be visible, choose University of Zurich in dropdown menu
  driver_wait(driver, "input[id='userIdPSelection_iddtext']", 10).send_keys("University of Zurich")
  # Click submit/next
  driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
  driver.find_element(By.ID, "username").send_keys(username)
  driver.find_element(By.ID, "password").send_keys(password)
  driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


def search(driver, search_term_1, search_term_2=None):
  driver_wait(driver, "div[role='dialog']", 20)
  # sleep(1000)
  button = driver_wait(driver, "button[class=' osano-cm-dialog__close osano-cm-close ']", 10)
  print(button)
  button.click()
  # click advanced search
  try:
    driver_wait(driver, "a[id='advanced']", 10).click()
  # if already in advanced search, continue
  except:
    pass

  # select all databases for search
  choose_db_link = driver_wait(driver, "a[id='selectDBLink']", 10)
  # choose_db_link.click throws exception if not visible due to cookie banner
  driver.execute_script("arguments[0].click();", choose_db_link)
  # window with databases selection opens
  driver_wait(driver, "input[value='pxh']", 10).click()
  driver_wait(driver, "input[value='psyh']", 10).click()
  # find and click OK button
  driver.find_element(By.ID, "btnOKTop").click()

  sleep(3)
  # input search term and search, 50 elements are shown per page / standard
  driver_wait(driver, "input[id='Searchbox1']", 10).send_keys(search_term_1)
  if search_term_2:
    driver_wait(driver, "input[id='Searchbox2']", 10).send_keys(search_term_2)
  driver.find_element(By.ID, "SearchButton").click()
  sleep(5)
  driver_wait(driver, "#_doc_type_160MN", 10).click()
  driver_wait(driver, "#multiSelectCluster_LanguageTrigger", 10).click()
  driver_wait(driver, "#_cluster_Language\%24english", 10).click()
  driver_wait(driver, "#multiSelectCluster_PopulationTrigger", 10).click()
  driver_wait(driver, "#_cluster_Population\%24human", 10).click()


def get_html(driver, link, results_path, index):
  # go to html link retrieved before
  driver.get(link)
  # wait until article is loaded from beginning to end 
  driver_wait(driver,"p[class='body-paragraph']",10)
  driver_wait(driver,"p[data-auto='copyright_info']",20)

  # save the whole html page
  # main element = html content of article / whole article 
  print("HTML_LOADED")
  soup = driver.find_element(By.CSS_SELECTOR, "div[data-result-key='main']")
  # save pure HTML in variable, pass HTML to BeautifulSoup
  soup = BeautifulSoup(soup.get_attribute('innerHTML'), "html.parser")

  print("SOUP")
  # save html
  # save new file under "ebsco_articles/index_of_article.html"
  with open(f"{results_path}/{index}.html", "wb") as file:
    # standardize, save HTML
    file.write(soup.prettify("utf-8"))

  
  # go back to page with articles
  driver.execute_script("window.history.go(-1)")

def get_pdf(driver, link):
  driver.get(link)
  # find pdf url
  pdf_url = driver_wait(driver, "iframe[id='pdfIframe']", 20).get_attribute("src")
  print(pdf_url)
  # load page with pdf
  driver.get(pdf_url)
  # download file
  # driver_wait(driver, "cr-icon-button[id='download']", 10).click()
  driver.execute_script("window.history.go(-1)")


def get_links(driver, results_path):
    # wait for page to be loaded
    driver_wait(driver, "h1[class='page-title alt']", 20)
    # wait for "next" link to be available
    _next = driver_wait(driver, "a[title='Next']", 10)

    while _next:
        # wait for articles on the page
        driver_wait(driver, "li[class='result-list-li']", 50)
        links = driver.find_elements(By.CSS_SELECTOR, "li[class='result-list-li']")

        res = []
        for link in links:
            dic = {}

            # article index (e.g., "4.")
            dic['index'] = link.find_element(
                By.CSS_SELECTOR, "span[class='record-index']"
            ).text.replace('.', '').replace(',', '')

            # available formats
            try:
                formats = link.find_elements(
                    By.CSS_SELECTOR, "span[class='record-formats'] a"
                )
            except Exception:
                continue

            dic['formats'] = [
                re.sub("[^a-zA-Z]+", "", f.get_attribute('id'))
                for f in formats
            ]

            # HTML link
            dic['html_link'] = link.find_element(
                By.CSS_SELECTOR, "a[class='title-link color-p4']"
            ).get_attribute('href')

            # PDF link (optional)
            try:
                dic['pdf_link'] = link.find_element(
                    By.CSS_SELECTOR, "a[title='PDF Full Text']"
                ).get_attribute('href')
            except Exception:
                pass

            res.append(dic)

        # download PDFs
        for article in res:
            if 'pdfft' in article['formats'] and 'pdf_link' in article:
                get_pdf(driver, article['pdf_link'])

        # go to next page
        try:
            _next = driver_wait(driver, "a[title='Next']", 10)
            driver.execute_script("arguments[0].click();", _next)
        except Exception:
            _next = False

        sleep(3)
 
def fetch_articles_ebsco():
    results_path = "./ebsco_articles/html"  # used only if HTML capture is enabled
    os.makedirs(results_path, exist_ok=True)

    search_term_1 = "memory"
    search_term_2 = "decay"
    ezproxy_url = "http://ezproxy.uzh.ch/login?auth=shibboleth&url=http://search.ebscohost.com/login.aspx?authtype=ip,uid&profile=ehost&defaultdb=pdh"

    driver = get_driver()
    try:
        driver.get(ezproxy_url)
        search(driver, search_term_1, search_term_2)
        get_links(driver, results_path)
    finally:
        driver.quit()

