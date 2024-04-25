import requests
from bs4 import BeautifulSoup

# Change API key from newsapi.org
NEWS_API_KEY = 'API KEY HERE'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'
SOURCES_API_URL = 'https://newsapi.org/v2/top-headlines/sources'


COUNTRY_CODES = {
    'United States': 'us',
    'United Kingdom': 'gb',
    'China': 'zh',
}


def fetch_news(source):
    params = {
        'apiKey': NEWS_API_KEY,
        'sources': source,
        'pageSize': 8
    }
    response = requests.get(NEWS_API_URL, params=params)
    news_data = response.json()
    articles = news_data.get('articles', [])
    if not articles:
        print("No articles found.")

    return articles


def choose_country():
    print("Available countries: ")
    for idx, country in enumerate(COUNTRY_CODES.keys()):
        print(f"{idx + 1}. {country}")
    choice = int(input("Select a country or enter 0 to stop: "))
    if choice != 0:
        country = list(COUNTRY_CODES.values())[choice - 1]
    else:
        country = 0
    return country


def fetch_news_sources(country):
    params = {
        'apiKey': NEWS_API_KEY,
        'country': country
    }
    response = requests.get(NEWS_API_URL + "/sources", params=params)
    news_data = response.json()

    if news_data['status'] == 'ok':
        sources = news_data.get('sources', [])
        return sources
    else:
        print("Error fetching news sources:", news_data['message'])
        return []


def display_full_article(articles, article_number):
    article = articles[article_number - 1]
    url = article['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_content = soup.find('article')
    if article_content:
        for section in article_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            print(section.get_text().strip())
            print()

        while True:
            choice = input(
                "Press enter to view other articles.").strip().upper()
            if choice == '':
                return
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Full article content not available.")


def main():
    while True:
        country = choose_country()
        if country == 0:
            break
        else:
            while True:
                sources = fetch_news_sources(country)
                if sources:
                    print("Available news sources in " + country + ": ")
                    for idx, source in enumerate(sources):
                        print(f"{idx + 1}. {source['name']}")

                    choice = input("Select a source or enter 0 to return: ")
                    if choice == '0':
                        break
                    elif choice.isdigit() and 0 < int(choice) <= len(sources):
                        articles = fetch_news(sources[int(choice) - 1]['id'])
                        while True:
                            print("Articles:")
                            for idx, article in enumerate(articles):
                                print(f"{idx + 1}. {article['title']}")
                            article_choice = input(
                                "Select the article you'd like to read in full or enter 0 to return: ")
                            if article_choice == '0':
                                break
                            elif article_choice.isdigit() and 0 < int(article_choice) <= len(articles):
                                display_full_article(
                                    articles, int(article_choice))
                            else:
                                print("Invalid article number.")
                    else:
                        print("Invalid source number.")
                else:
                    break


if __name__ == "__main__":
    main()
