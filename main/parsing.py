from bs4 import BeautifulSoup
import requests
import json
import re
def main():
    url = 'http://www.imdb.com/chart/top'
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    movies = content.select('td.titleColumn')
    links = [a.attrs.get('href') for a in content.select('td.titleColumn a')]
    crew = [a.attrs.get('title') for a in content.select('td.titleColumn a')]
    ratings = [b.attrs.get('data-value') for b in content.select('td.posterColumn span[name=ir]')]
    votes = [b.attrs.get('data-value') for b in content.select('td.ratingColumn strong')]

    movArr = []

    for index in range(0, len(movies)):
        movie_string = movies[index].get_text()
        movie = (' '.join(movie_string.split()).replace('.', ''))
        movie_title = movie[len(str(index)) + 1:-7]
        year = re.search('\((.*?)\)', movie_string).group(1)
        place = movie[:len(str(index)) - (len(movie))]
        data = {"movie_title": movie_title,
                "year": year,
                "place": place,
                "star_cast": crew[index],
                "rating": ratings[index],
                "vote": votes[index],
                "link": links[index]}
        movArr.append(data)

    return movArr