urls_to_scrape # list containing urls I want to perform the code below for 
               # each url


results = []

articles = driver.find_elements_by_css_selector('#MainW article')

counter = 1

for article in articles:
    result = {}
    try:
        title = article.find_element_by_css_selector('a').text
    except: 
        continue

    counter = counter + 1

    excerpt = article.find_element_by_css_selector('div > div > p').text

    author = 
    article.find_element_by_css_selector('div > footer > address > a').text

    date = article.find_element_by_css_selector('div > footer > time').text

    link=
    article.find_element_by_css_selector('div>h2>a').get_attribute('href')

    result['title'] = title
    result['excerpt'] = excerpt
    result['author'] = author
    result['date'] = date
    result['link'] = link

