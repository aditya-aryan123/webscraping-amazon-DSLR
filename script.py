import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs


def get_product_name(_soup):
    try:
        title = _soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.string
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string


def get_price(_soup):
    try:
        price = _soup.find("span", attrs={'class': 'a-offscreen'}).string.strip()
    except AttributeError:
        price = ""
    return price


def get_score(_soup):
    try:
        rating = _soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = _soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating


def get_total_reviews_and_ratings(_soup):
    try:
        review_count = _soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""
    return review_count


def getnextpage(_soup):
    pages = _soup.find('span', attrs={'class': 's-pagination-strip'})
    if not pages.find('span', attrs={'class': 's-pagination-item s-pagination-next s-pagination-disabled'}):
        _url = 'https://www.amazon.in' + pages.find('a', attrs={'class': 's-pagination-item s-pagination-next '
                                                                         's-pagination-button '
                                                                         's-pagination-separator'}).get('href')
        return _url
    else:
        return


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path='C:/browserdriver/chromedriver.exe')

    link = 'https://www.amazon.in/s?k=dslr&crid=1EJJMI7DCNZUX&sprefix=ds%2Caps%2C644&ref=nb_sb_noss_2'

    driver.get(link)
    content = driver.page_source
    soup = bs(content, "lxml")

    product_name = []
    price = []
    score = []
    review_and_rating = []

    while True:
        url = getnextpage(soup)
        if not url:
            break
        else:
            links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
            links_list = []

            for link in links:
                links_list.append(link['href'])

            for link in links_list:
                new_link = "https://www.amazon.in" + link
                driver.get(new_link)
                new_content = driver.page_source
                new_soup = bs(new_content, "lxml")

                product_name.append(get_product_name(new_soup))
                price.append(get_price(new_soup))
                score.append(get_score(new_soup))
                review_and_rating.append(get_total_reviews_and_ratings(new_soup))

                print("Product Title =", get_product_name(new_soup))
                print("Product Price =", get_price(new_soup))
                print("Product Rating =", get_score(new_soup))
                print("Product Rating =", get_total_reviews_and_ratings(new_soup))

    df = pd.DataFrame({'Product Name': product_name, 'Price': price, 'Score': score, 'Ratings': review_and_rating})
    df.to_csv('dslr.csv', index=False)
