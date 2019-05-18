from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


def scrape_all():

 
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_p = mars_news(browser)
    
   
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": feature_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }


    browser.quit()
    return data


def mars_news(browser):
    url_news = 'https://mars.nasa.gov/news/'
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    browser.visit(url_news)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    result = BeautifulSoup.find_all('li', class_='slide')[0]
    news_date = result.find('div',class_='list_date').text


    try:
        news_title= result.find('div',class_="content_title" ).text
        news_p=result.find('div', class_="article_teaser_body").text
        #slide_elem = news_soup.select_one("ul.item_list li.slide")
        #news_title = slide_elem.find("div", class_="content_title").get_text()
        #news_p = slide_elem.find(
         #   "div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def feature_image(browser):
    
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.is_element_present_by_text("more info", wait_time=0.5)
    browser.click_link_by_partial_text('more info')
    image_html = browser.html
    img_soup = BeautifulSoup(image_html, 'html.parser')
    
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None
    
    img_url = f"https://www.jpl.nasa.gov{img_url_rel}"

    return img_url


def hemispheres(browser):
    url_hemi='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)

    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}
    
        browser.find_by_css("a.product-item h3")[i].click()
    
        original = browser.find_link_by_text('Original')
        hemisphere['img_url'] =  original['href']
    
        hemisphere['title'] = browser.find_by_css("h2.title").text

        hemisphere_image_urls.append(hemisphere)

        browser.back()
    return hemisphere_image_urls

def twitter_weather(browser):
    url_weather="https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    html_weather = browser.html
    weather_soup = BeautifulSoup(html_weather, 'html.parser')

    mars_weather_tweet = weather_soup.find('div', {"class": "tweet", "data-name": "Mars Weather"})
    mars_weather=mars_weather_tweet.find('p',class_="TweetTextSize").get_text()

    return mars_weather

def hemisphere(browser):
    url_hemi='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)

    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")


    for i in range(len(links)):
        hemisphere = {}
    
        browser.find_by_css("a.product-item h3")[i].click()
    
        original = browser.find_link_by_text('Original')
        hemisphere['img_url'] =  original['href']
    
        hemisphere['title'] = browser.find_by_css("h2.title").text

        hemisphere_image_urls.append(hemisphere)

        browser.back()
    
    return hemisphere

def mars_facts():
    try:
        df = pd.read_html("http://space-facts.com/mars/")[0]
    except BaseException:
        return None

    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)


    return df.to_html(classes="table table-striped")
