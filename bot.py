import json
import time
import random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import logger
import credentials
import exceptions

log = logger.create_logger('ig_bot.bot')

IG_BASE_URL = 'https://instagram.com'
IG_TAGS_URL = f'{IG_BASE_URL}/explore/tags'

CONFIG_PATH = 'config.json'

try:
    with open(CONFIG_PATH) as config:
        data = json.load(config)
except(FileNotFoundError):
    log.exception(f'Configuration file config.json was not found in root directory.')
    raise exceptions.BadConfig
try:
    HASHTAGS = data['config']['hashtags']
except(KeyError):
    log.exception(f'Specify config.hashtags fields in {CONFIG_PATH}')
    raise exceptions.BadConfig

class Instagram():
    """Class representing Instagram Bot."""

    def __init__(self, hashtag):
        self.hashtag = hashtag

    def __enter__(self):
        self.driver = webdriver.Chrome()
        return self

    def __exit__(self, type, value, traceback):
        self.driver.close()

    def _mock_user_delay(self, value: int, range: int) -> None:
        new_range = range * 2
        time.sleep(random.randrange(new_range) - ( new_range / 2 ) + value)

    def close(self):
        self.driver.close()

    def login(self, login: str, password: str):
        self.driver.get(IG_BASE_URL)
        time.sleep(2)

        self.driver.find_element_by_name('username').send_keys(login)
        self.driver.find_element_by_name('password').send_keys(password + Keys.RETURN)

        time.sleep(2)

    def like_photos(self):
        liked_posts: list = []
        liked_posts_counter: int = 0
        id_hashtag_url = f'{IG_TAGS_URL}/{self.hashtag}'

        log.info(f'Starting liking {self.hashtag} hashtag.')

        while True:
            self.driver.get(id_hashtag_url)
            self._mock_user_delay(3, 1)

            a_tag = self.driver.find_elements_by_tag_name('a')
            pic_hrefs: list = [elem.get_attribute('href') for elem in a_tag]
            photo_urls: list = [href for href in pic_hrefs if '/p/' in href and href not in liked_posts]

            # Most recent photos start with 9th URL and there are 24 of them in single page.
            latest_photo_urls = photo_urls[9:]

            if len(latest_photo_urls) == 0:
                log.info(f'Found [{str(len(latest_photo_urls))}] new posts. Waiting for 10 seconds.')
                self._mock_user_delay(10, 3) # should be config
                continue

            log.info(f'Found [{len(latest_photo_urls)}] new posts.')
            liked_posts_counter += len(latest_photo_urls)

            for photo_url in latest_photo_urls:
                self.driver.get(photo_url)
                liked_posts.append(photo_url)

                self._mock_user_delay(7, 2)

                try:
                    # Alternative: self.driver.find_element_by_link_text('Like').click()
                    self.driver.find_element_by_class_name('_8-yf5').click()
                    print(f'Liked posts counter: {str(len(liked_posts))}')
                except(NoSuchElementException):
                    log.warning(f'Did not find \'Like\' button on loaded page. Probably browser did not load it fast enough.')

                self._mock_user_delay(3, 1)

            PHOTOS_PER_PAGE = 24

            if len(liked_posts) > PHOTOS_PER_PAGE:
                photo_number_diff = len(liked_posts) - PHOTOS_PER_PAGE
                for _ in range(photo_number_diff):
                    liked_posts.pop(0)
            
            log.info(f'Liked {liked_posts_counter} posts.')
            time.sleep(30)    

if __name__ == '__main__':
    credential = credentials.read_credentials()
    if len(HASHTAGS) is not 1:
        raise exceptions.NoImplementation

    for hashtag in HASHTAGS:
        with Instagram(hashtag) as instagram:
            try:
                instagram.login(credential.login, credential.password)
                instagram.like_photos()
            except(KeyboardInterrupt):
                instagram.close()