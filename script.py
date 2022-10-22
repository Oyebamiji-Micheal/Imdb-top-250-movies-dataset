from bs4 import BeautifulSoup
import requests
import csv


def main():
    url = 'https://www.imdb.com/chart/top'
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'lxml')
    extract_write(soup)


def helper(movie_url):
    """
    Extract and return additional information such as
    runtime, popularity, reviews and so on.
    """
    response = requests.get(movie_url).content
    soup = BeautifulSoup(response, 'lxml')

    runtime = soup.find('div', class_='sc-80d4314-2 iJtmbR').text[-6:]
    summary = soup.find('span', class_='sc-16ede01-0 fMPjMP').text
    try:
        popularity = soup.find('div', class_='sc-edc76a2-1 gopMqI').text
    except AttributeError:
        popularity = None
    total_reviewers = soup.find('div', class_='sc-7ab21ed2-3 dPVcnq').text
    user_reviews = soup.find_all('span', class_='score')[0].text
    critic_reviews = soup.find_all('span', class_='score')[1].text

    return (
        runtime, summary, popularity, total_reviewers, user_reviews,
        critic_reviews
    )


def extract_write(soup):
    """Extract movie attributes and write them to a csv file."""
    csv_file = open('imdb_movies.csv', 'w', newline='')

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        [
            'title', 'release_year', 'rating',
            'runtime', 'summary', 'popularity',
            'total_reviewers', 'user_reviews',
            'critic_reviews'
        ]
    )

    movie_info = soup.find_all('td', class_='titleColumn')
    ratings = soup.find_all('td', class_='ratingColumn imdbRating')

    for info, rating in zip(movie_info, ratings):
        title = info.find('a').text
        year = info.find('span').text[1:-1]
        rating = rating.text.strip()

        movie_url = info.find('a')['href']
        movie_url = f'https://www.imdb.com/{movie_url}'
        additional_info = helper(movie_url)

        csv_writer.writerow(
            [
                title, year, rating,
                additional_info[0], additional_info[1],
                additional_info[2], additional_info[3],
                additional_info[4], additional_info[5]
            ]
        )

        print('I\'m still running')

    print('Done!')


if __name__ == '__main__':
    main()
