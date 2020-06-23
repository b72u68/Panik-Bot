import praw
import os
import configparser

class redditSubmissionScraper:

    def __init__(self, subreddit=None):
        self.subreddit = subreddit
        config = configparser.ConfigParser()
        config.read(r'./.config/reddit_conf.ini')
        self.reddit = praw.Reddit(client_id=config['REDDIT']['client_id'], client_secret=config['REDDIT']['client_secret'], user_agent='Reddit Submission Scraper by /u/b72u68')

    # check subreddit of self
    def check_sub(self):
        try:
            self.reddit.subreddits.search_by_name(self.subreddit, exact=True)
        except Exception as e:
            print(f'[-] Error Occurred: {e}')
            return False 
        return True 

    # keep track of sent item
    def get_sent(self, filename):
        sent_sub = []
        sent_file = []

        try:
            log = open(filename, 'rt')
            sent = log.readlines()

            for sent_data in sent:
                if sent_data.split()[0].strip() not in sent_sub:
                    sent_sub.append(sent_data.split()[0].strip())
                sent_file.append(sent_data.split()[1].strip())

        except Exception as e:
            print(f'[-] Error Occurred: {e}')

        return {'subreddit': sent_sub, 'files': sent_file} 

    # get image url linked to reddit submission
    def get_image(self):
        sent_images = self.get_sent('image_log.txt')['files']
        submissions = self.reddit.subreddit(self.subreddit).new(limit=None)

        try:
            for submission in submissions:
                if not submission.stickied and submission.url.endswith(('.jpg', '.png', 'jpeg')):
                    url = submission.url
                    if url and url not in sent_images: 
                        return {'url': url, 'author': submission.author}
                    
        except Exception as e:
            print(f'[-] Error Occurred: {e}')
            return None

    # get title and text from reddit submission
    def get_content(self):
        sent_text = self.get_sent('text_log.txt')['files']
        submissions = self.reddit.subreddit(self.subreddit).new(limit=None)

        try:
            for submission in submissions:
                if not submission.stickied and submission.is_self:
                    url = submission.url
                    if url and url not in sent_text:
                        author = submission.author
                        title = submission.title
                        content = submission.selftext
                        return {'url': url, 'author': author, 'title': title, 'content': content}

        except Exception as e:
            print(f'[-] Error Occurred: {e}')
            return None
    
    # get list of subreddits match with the given query
    def search_sub(self, query):
        return self.reddit.subreddits.search(query)
