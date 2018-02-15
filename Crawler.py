import requests
from bs4 import BeautifulSoup


class Crawler:

    count = 0
    visited = {}

    def __init__(self,link):
        count = 0
        self.crawl(link,self.count)

    def prepend(self,link):
        return "http://www.imdb.com"+link

    def crawl(self,link,count):

        if count > 200:
            return

        # Requests the server for webpage
        r = requests.get(link)

        # Create a DOM for the response
        soup = BeautifulSoup(r.text,"html.parser")

        # Create a list of all in page links
        related = soup.select('a[href$="tt_rec_tti"]')

        # Check for the current movie
        if self.check(soup) == True:
            self.printValue(soup)
            count += 1


        # Get the href values for the links found in related
        for relatedLink in related:
            if self.visited.__contains__(relatedLink['href']) == False:
                self.visited.__setitem__(relatedLink['href'],False)

        for relatedLink in related:
            if self.visited.get(relatedLink['href']) == False:
                self.visited.__setitem__(relatedLink['href'],True)
                self.crawl(self.prepend(relatedLink['href']),count)

    def check(self,soup):

        el = soup.find("span",attrs={"itemprop":"ratingValue"})

        if el.string < '8.5' and el.string > '6.5':
            return True
        else:
            return False

    def printValue(self,soup):

        el = soup.find("span",attrs={"itemprop":"ratingValue"})
        print(el.string,end=" ")

        el = soup.find("h1",attrs={"itemprop":"name"})
        print(el.contents[0],end=" ")

        el = soup.find("span",attrs={"itemprop":"name"})
        print(el.string)

obj = Crawler('http://www.imdb.com/title/tt0108052/?ref_=fn_al_tt_1')
