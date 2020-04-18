import json
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import credentials
import exceptions
import logger

log = logger.create_logger('ig_bot.bot')

IG_BASE_URL = 'https://instagram.com'
IG_TAGS_URL = f'{IG_BASE_URL}/explore/tags'

CONFIG_PATH = 'config.json'

# TODO: implement proper configuartion mechanism.
try:
    with open(CONFIG_PATH) as config:
        data = json.load(config)
except(FileNotFoundError):
    log.exception(f'Configuration file config.json was not found in root directory.')
    raise exceptions.NoConfig

try:
    HASHTAGS = data['config']['hashtags']
except(KeyError):
    log.exception(f'Specify config.hashtags fields in {CONFIG_PATH}')
    raise exceptions.BadConfig

class Instagram():
    """Class representing Instagram Bot."""

    def __init__(self, hashtag: str):
        self.hashtag = hashtag

    def __enter__(self):
        self.driver = webdriver.Chrome()
        return self

    def __exit__(self, type, value, traceback):
        self.driver.close()

    # TODO: mocking user delay should be configurable.
    def _mock_user_delay(self, value: int, range: int) -> None:
        new_range = range * 2
        time.sleep(random.randrange(new_range) - ( new_range / 2 ) + value)

    def _wait_for_browser(self, wait_time: int) -> None:
        time.sleep(wait_time)

    def close(self) -> None:
        """Closes selenium webdriver."""

        self.driver.close()

    def login(self, login: str, password: str) -> None:
        """
        Opens Instagram Home Page and logs in into given account.

        :param login: login to be used
        :param password: password to be used

        :return: None
        """

        self.driver.get(IG_BASE_URL)
        self._wait_for_browser(3)

        self.driver.find_element_by_name('username').send_keys(login)
        self.driver.find_element_by_name('password').send_keys(password + Keys.RETURN)

        self._wait_for_browser(3)

    def like_photos(self) -> None:
        """Starts process of liking photos."""

        liked_posts: list = []
        liked_posts_counter: int = 0
        hashtag_url_id = f'{IG_TAGS_URL}/{self.hashtag}'

        log.info(f'Starting liking {self.hashtag} hashtag.')

        while True:
            self.driver.get(hashtag_url_id)
            self._mock_user_delay(3, 1)

            a_tags: list = self.driver.find_elements_by_tag_name('a')
            pic_hrefs: list = [elem.get_attribute('href') for elem in a_tags]
            photo_urls: list = [href for href in pic_hrefs if '/p/' in href and href not in liked_posts]

            # Most recent photos start with 9th URL and there are 24 of them in single page.
            PHOTOS_PER_PAGE = 24
            latest_photo_urls: list = photo_urls[9:]

            if len(latest_photo_urls) == 0:
                log.info(f'Found [0] new posts. Waiting for 10 seconds.')
                self._wait_for_browser(10)
                continue

            log.info(f'Found [{len(latest_photo_urls)}] new posts.')

            for photo_url in latest_photo_urls:
                self._mock_user_delay(2, 1)
                self.driver.get(photo_url)
                self._mock_user_delay(7, 2)

                try:
                    # Alternative: self.driver.find_element_by_link_text('Like').click()
                    self.driver.find_element_by_class_name('_8-yf5').click()
                    liked_posts.append(photo_url)
                    liked_posts_counter += 1
                    print(f'Liked posts counter: {str(len(liked_posts))}')
                except(NoSuchElementException):
                    log.warning(f'Did not find \'Like\' button on loaded page. Probably browser did not load it fast enough.')

                self._mock_user_delay(2, 1)

            if len(liked_posts) > PHOTOS_PER_PAGE:
                photo_number_diff = len(liked_posts) - PHOTOS_PER_PAGE
                for _ in range(photo_number_diff):
                    liked_posts.pop(0)
            
            log.info(f'Liked {liked_posts_counter} posts so far.')
            self._wait_for_browser(30)   

# TODO: Allow for more than 1 hashtag and intruduce multitreading for that.
if __name__ == '__main__':
    credential = credentials.read_credentials()
    if len(HASHTAGS) is not 1:
        log.exception(f'Liking only one hashtag at the time is presetly implemented.')
        raise exceptions.NoImplementation

    for hashtag in HASHTAGS:
        with Instagram(hashtag) as instagram:
            try:
                instagram.login(credential.login, credential.password)
                instagram.like_photos()
            except(KeyboardInterrupt):
                instagram.close()