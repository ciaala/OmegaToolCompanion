#!/usr/bin/env python3
import urllib.request
from time import sleep
from xml.etree.ElementTree import XMLParser

import datetime
from bs4 import BeautifulSoup
import json
import requests
import threading

votingUrl = "https://59hev72m1l.execute-api.eu-central-1.amazonaws.com/prod/"
url = 'http://blogger.grazia.it/talent/darphin'
champion = 2228


def extract_data(url, extractor):
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    extractor(soup)


class RatingsExtractor:

    def __init__(self, champion):
        self.champion = champion
        self.bestAdversary = None
        self.ratings = dict()
        self.competitors = dict()
        self.bestAdversaryRating = 0

    def __call__(self, soup):
        self.extract_ratings(soup)

    def extract_ratings(self, soup):
        elements = soup.find_all("div", class_="blogger-info-bar")

        for element in elements:
            # ratingSquare = element.find_all("rate-square")
            ratingElement = element.find_all("span")[2]
            rating = int(ratingElement.text.strip())
            competitor = element.find_all("a")[0].text.strip()
            key = int(ratingElement.get('id')[8:])
            self.ratings[key] = rating
            self.competitors[key] = competitor
            if (key != self.champion) and (rating > self.bestAdversaryRating):
                self.bestAdversary = key
                self.bestAdversaryRating = rating

    def buildVoteString(self, label, key):
        return label + ": " + self.competitors[key] + ", vote: " + str(self.ratings[key])

    def should_vote(self):
        if datetime.date.today().day < 30:
            margin = (datetime.date.today().day % 6) - 3
        else:
            margin = 5
        margin = (100 + margin) / 100.0
        if self.ratings[self.champion] < (self.bestAdversaryRating * margin):
            return True
        else:
            return False

    def can_vote(self):
        hour = datetime.datetime.now().hour
        if hour > 7 and hour < 23:
            return True
        else:
            return True

    def run(self):
        if self.can_vote() and self.should_vote():
            self.do_vote()
        else:
            print(".")

    def print_status(self):
        print(self.buildVoteString("champion", self.champion))
        print(self.buildVoteString("bestAdversary", self.bestAdversary))
        self.do_vote()

    def do_vote(self):
        response = requests.get(votingUrl)
        json_response = json.loads(response.text)
        print(json_response)

def execute():
    while True:
        extractor = RatingsExtractor(champion)
        extract_data(url, extractor)
        extractor.run()
        sleep(1)

if __name__ == "__main__":
    for i in range(1,100):
        threading.Thread(target = execute).start()

    sleep(6000)

"""
def stuff() :
    with urllib.request.urlopen() as response:
        html = response.read(url)
        xmlParser = XMLParser()
        xmlParser.parser
        UseForeignDTD(True)
        dom = ET.fromstring(html)
        rating = dom.getElementById("ratings_2228")
        print(rating)
        """
