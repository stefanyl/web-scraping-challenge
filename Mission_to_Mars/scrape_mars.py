#converting your Jupyter notebook into a Python script

#imports
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_news = {}

    url = "https://redplanetscience.com/"

    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find('div', class_='list_text')
    news_title = article.find('div', class_="content_title").get_text()
    body = article.find('div', class_="article_teaser_body").get_text()
    
    #Featured Image
    url1 = "https://spaceimages-mars.com/"
    browser.visit(url1)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    header = soup.find('div', class_='header')
    image = header.find('img', class_="headerimage fade-in")
    featured_image_url = url1 + image['src']

    #Mars Facts
    url2 = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url2)
    df = tables[0] 
    df.columns = ['Comparison', 'Mars', 'Earth']
    df = df.iloc[1:]
    df.set_index('Comparison', inplace=True)
    table_html =df.to_html() 

    #Mars Hemispheres
    url3 = "https://marshemispheres.com/"
    browser.visit(url3)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    boxes = soup.find_all('div', class_="result-list")
    res_titles = list()
    img_urls = list()
    for box in boxes:
        titles = box.find_all('h3')
        links = box.find_all('a', class_="itemLink product-item")
            
        for title,link in zip(titles,links):
            res_titles.append(title.text)
            img_click = link['href']
            browser.click_link_by_partial_text(title.text)

            html = browser.html
            soup = BeautifulSoup(html, "html.parser")
            sample = soup.find("a", text="Sample")
            sample_url = sample['href']
            img_url = url3 + sample_url
            img_urls.append(img_url)
            browser.back()
    
    mars_news = {"title": res_titles,
     "img_url": img_urls,
     "news": news_title,
     "body": body,
     "table_html":table_html,
     "feat_img": featured_image_url}
    

    # Quit the browser
    browser.quit()
    return mars_news