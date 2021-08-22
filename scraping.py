
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

# Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_images": hemisphere_data(browser)
    }
    
    # Stop webdriver and return data
    browser.quit()
    print(data)
    return data

def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    # OTHER SITE IF DIFFERENCE - https://data-class-mars.s3.amazonaws.com/Mars/index.html
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # convert broswer html to a soup object 
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        #This variable holds a ton of information, so look inside of that information to find this specific data." 
        #slide_elem.find('div', class_='content_title') (THIS WAS CODE BUT NOT NEEDED AS PER 10.5.3)

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p
    
## Featured Image
    
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    # TRY https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html IF ANY ISSUES
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # add try and except block around for errors
    try: 
        # Find the relative image url   
        # An img tag is nested within this HTML, so we've included it.
        # .get('src') pulls the link to the image.
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'  # TRY THIS SIT IF ISSUES https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/
    return img_url


def mars_facts(): 
    try:
        # With this line, we're creating a new DataFrame from the HTML table. The Pandas function read_html() 
        # specifically searches for and returns a list of tables found in the HTML. By specifying an index of 0, 
        # we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, 
        # it turns the table into a DataFrame.
        df = pd.read_html('https://galaxyfacts-mars.com')[0] # use this link if any issues https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html
        # Here, we assign columns to the new DataFrame for additional clarity.
    except BaseException:
        return None
    df.columns=['Description', 'Mars', 'Earth']
    # By using the .set_index() function, we're turning the Description column into the DataFrame's index. 
    # inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
    df.set_index('Description', inplace=True)
    return df.to_html(classes="table table-striped")

def hemisphere_data(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # Parse the resulting html with soup
    html = browser.html
    img_ctr = soup(html, 'html.parser')
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    img_url_4 = img_ctr.find('div', class_='collapsible results')
    img_links = img_url_4.find_all('div', class_='item')
    for i in img_links(4):
        i.a['href']
        #print(url + i.a['href'])

        browser.visit(url + i.a['href'])
        image_html = browser.html
        page_soup = soup(image_html, 'html.parser')

        # Collect Title
        hemisphere = page_soup.find('div', class_='cover')
        title = hemisphere.h2.text
        #print(title)
        # Collect image link by browsing to hemisphere page
        image_link = page_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        image_final_url = (url + image_url)
        #print(image_final_url)
        # Create Dictionary to store title and url info
        
        hemispheres = {'image_url': image_final_url,
                    'title': title
                    }

        hemisphere_image_urls.append(hemispheres)

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


