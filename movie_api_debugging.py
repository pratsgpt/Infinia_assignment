from abc import abstractmethod
from typing import List, Dict
import json

import requests
from requests import Response

import sys
import collections


class MovieReader:
    url: str = ""

    @abstractmethod
    def get_movies(self, title: str) -> List[Dict]:
        pass

class HackerRankMovieReader(MovieReader):
    def __init__(self):
        self.url = "https://jsonmock.hackerrank.com/api/movies/search/?Title={title}&page={page}"

    def get_movies(self, title: str) -> List[Dict]:
        """
        Returns a list of movies, as dictionaries, that contains the title and date of the movie.
        Example:
            input: title = "movie"

            returns: [{"title": "good movie", "year": 2010}, {"title": "another movie", "year": 2011}]
        """
        page_number: int = 1
        results: List[Dict] = []

        while True:
            response: Response = requests.get(self.url.format(title=title, page=page_number))
            titles = response.json()
            #changed variable name to title_i in the for loop below
            for title_i in titles['data']:
                results.append({
                    "title": title_i["Title"],
                    "year": title_i["Year"],
                })

            page_number += 1
            # updated below condition to read the last page
            #if page_number >= titles["total_pages"]:
            if page_number > titles["total_pages"]:
                break
        return results

    def match_movies(self, primary: str, secondary: str) -> Dict:
        """
        Returns a dictionary of movies along with the year(s) of release, that match both the primary
        and secondary terms (case insensitive).  The initial query is performed on the primary term.
        Example:
            input: primary = "movie", secondary = "the"

            returns:
            {
                "The Movie": [1982],
                "Movie of the Year": [1999, 2008]
            }
        """
        results = collections.defaultdict(list)
        #updated below parameter to primary 
        #movies = self.get_movies(secondary)
        movies = self.get_movies(primary)

        for movie in movies:
            #if secondary.lower() in movie["title"].upper():
            if secondary.lower() in movie["title"].lower():
                results[movie['title']].append(movie['year'])

        return results


def main():

    movie_reader = HackerRankMovieReader()

    # Validation Tests
    with open("movie_api_debugging_testcases.txt") as file:
        for data in file.read().split("\n\n"):
            data = data.split("\n")
            print(f"Running {data[0]}")

            matches = movie_reader.match_movies(data[1].split(" ")[0], data[1].split(" ")[1])
            results = json.dumps(matches, separators=(',', ':'), ensure_ascii=False)

            if (matches == json.loads(data[2])):  
                print(f"{data[0]} Passed!\n")
            else:
                print(f"{data[0]} Failed.\nExpected: {data[2]}\nActual: {results}")

if __name__ == "__main__":
    main()
