from urllib.request import urlopen
from bs4 import BeautifulSoup

# News class
class News:
    # constructor.
    # params:
    #   title - news title <string>
    #   content - news content <string>
    def __init__(self, title, content):
        self.title = title
        self.content = content

# Event class
class Event:
    # constructor.
    # params:
    #   title - event title <string>
    #   month - event month. e.g "June" <string> 
    #   day - event date. e.g "10" <string>
    #   time - event time. e.g. "7:15 PM" <string>
    def __init__(self, title, month, day, time = ""):
        self.title = title
        self.month = month
        self.day = day
        self.time = time

# Marlboro public school web page scraping class
class MPSWeb:
    HOME_URL = "https://www.mtps.org/" # home page url

    # constructor.
    # Download home page and cood soup
    def __init__(self):
        with urlopen(MPSWeb.HOME_URL) as req:
            self._soup = BeautifulSoup(req, "html.parser")

    # Return a list of news found on MPS home page.
    # Each element of the list is a News object.
    def getAllNews(self):
        #Soup already cooked in self._soup :)
        ret = []
        newsoup = self._soup.select('#index_news article')
        #ret.append(News("Hire Bus Drivers", "Apply Today!"))
        for news in newsoup:
            ret.append(News(news['aria-label'], news.select('.item-text')[0].text.strip()))
        return ret

     # Return a list of events found on MPS home page.
    # Each element of the list is an Event object
    def getAllEvents(self):
        #Soup already cooked in self._soup :)
        ret = []
        eventsoup = self._soup.select('#index_events article')
        #ret.append(Event("One session day", "June", "8"))
        for event in eventsoup:
            title = event['aria-label']
            month = event.select('.event-month')[0].text.strip()
            day = event.select('.event-day')[0].text.strip()
            time = event.select('.event-time')
            if time:
                time = time[0].text.strip()
            else:
                time = ''
            ret.append(Event(title, month, day, time))
        return ret


# Inline testing
if __name__ == "__main__":
    mps = MPSWeb()
    print("Here are the latest news for marlboro public school: ")
    print("===============================")
    for news in mps.getAllNews():
        print("Title [%s]. Content [%s]" % (news.title, news.content))

    print("\n\n")
    print("Here are the latest events for marlboro public school: ")
    print("===============================")        
    for event in mps.getAllEvents():
        print("Title [%s]. Date-Time [%s %s %s] " % (event.title, event.month, event.day, event.time))


