# RSS Feed Filter
# Author: Esteban Herrera

from email.message import Message
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime



#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")

        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

class NewsStory(object):
    
    def __init__(self, guid, title, description, link, pubdate):
        
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    
    def get_guid(self):
        
        return self.guid
    
    def get_title(self):
        
        return self.title
    
    def get_description(self):
        
        return self.description
    
    def get_link(self):
        
        return self.link
    
    def get_pubdate(self):
        
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS


# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    
    def __init__(self, phrase):
        
        self.phrase = phrase 
        
        
        
    def is_phrase_in(self, text):
        
        lower_phrase = self.phrase.lower()
        text1 = str(text)
        lower_text = text1.lower()
            
        current_word = ''
        words_text_list= []
                     
        for char in text1:
           
            if char in string.punctuation or char.isspace(): 
                
                if current_word:
                    word_lower = current_word.lower()
                    words_text_list.append(word_lower)
                    current_word = ''
                    
            else:        
                current_word += char
             
        if current_word:
            word_lower = current_word.lower()
            words_text_list.append(word_lower)
           
        words_phrase_list = lower_phrase.split()
        n = len(words_phrase_list)
        
        for i in range(len(words_text_list) - n + 1):
            
            if words_text_list[i:i+n] == words_phrase_list:
            
                return True
            
        return False
  
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    
    
    def __init__(self, phrase):
        
        PhraseTrigger.__init__(self, phrase)
        
    def evaluate(self, title):
        
        if self.is_phrase_in(title):
            
            return True
        
        else:
            return False
    
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    
    def __init__(self, phrase):
        
        PhraseTrigger.__init__(self, phrase)
        
    def evaluate(self, description):
        
        if self.is_phrase_in(description):
            
            return True
        
        else: 
            return False
        



# TIME TRIGGERS


# TODO: TimeTrigger



class TimeTrigger(Trigger):
    
    def __init__(self, date):
        "Please input the string date in the following format: 3 Oct 2016 17:00:10" 
        self.date = time.strptime(date)
 

# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    
    def __init__(self, date):
        
        TimeTrigger.__init__(self, date)
    
    def evaluate(self, published):
        
        if time.strptime(published) < self.date : 
            return True
    
        return False
        
    
class AfterTrigger(TimeTrigger):

    def __init__(self, date):    
        TimeTrigger.__init__(self, date)
    
    def evaluate(self, published): 
        
        if time.strptime(published) > self.date:
            return True    

        return False


# COMPOSITE TRIGGERS

# TODO: NotTrigger

class NotTrigger(Trigger):
    
    def __init__(self, trigger):
        
        self.trigger = trigger
        
    def evaluate(self, news):
        
        return not self.trigger.evaluate(news)
    

# TODO: AndTrigger

class AndTrigger(Trigger):
    
    def __init__(self, trigger1, trigger2):
        
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        
    def evaluate(self, news):
        
        if self.trigger1.evaluate(news) == True and self.trigger2.evaluate(news) == True :
            
            return True
        
        return False


# TODO: OrTrigger
class OrTrigger(Trigger):
    
    def __init__(self, trigger1, trigger2):
        
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        
    def evaluate(self, news):
        
        if self.trigger1.evaluate(news) or self.trigger2.evaluate(news):
            
            return True
        
        return False


#======================
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances and a list of triggers.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break  # Once a trigger fires for a story, no need to check other triggers
    return filtered_stories



#======================
# User-Specified Triggers
#======================


def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    trigger_file = open(filename, 'r')
    list_objects = ['Title','Description', 'AND', 'NOT', 'AFTER', 'TIME', 'BEFORE', 'OR']
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    trigger_file.close()
    
    triggers = {}
    trigger_list = []

    for line in lines:
        parts = line.split(',')
        if parts[0] == 'ADD':
            for name in parts[1:]:
                trigger_list.append(triggers[name])
        else:
            trigger_name = parts[0]
            trigger_type = parts[1]
            if trigger_type == 'TITLE':
                triggers[trigger_name] = TitleTrigger(parts[2])
            elif trigger_type == 'DESCRIPTION':
                triggers[trigger_name] = DescriptionTrigger(parts[2])
            elif trigger_type == 'AFTER':
                triggers[trigger_name] = AfterTrigger(parts[2])
            elif trigger_type == 'BEFORE':
                triggers[trigger_name] = BeforeTrigger(parts[2])
            elif trigger_type == 'NOT':
                triggers[trigger_name] = NotTrigger(triggers[parts[2]])
            elif trigger_type == 'AND':
                triggers[trigger_name] = AndTrigger(triggers[parts[2]], triggers[parts[3]])
            elif trigger_type == 'OR':
                triggers[trigger_name] = OrTrigger(triggers[parts[2]], triggers[parts[3]])

    return trigger_list   




SLEEPTIME = 20 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list 
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Kamala")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t2]

        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')

        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

