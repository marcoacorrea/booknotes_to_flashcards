from words_provider.words_provider import WordsProvider
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class GooglePlayBooks(WordsProvider):
    """ Extract words from notes from a Google play book """

    def __init__(self, url: str, driver: WebDriver):
        """
        :param url: Google play books URL
        :param driver: Webdriver should be configured with a profile where user is signed in their Google account
        """
        self.book_url = url
        self.driver = driver

    def retrieve_words(self):
        try:
            self.driver.get(self.book_url)

            self.wait_until_page_loads()
            self.switch_to_books_frame()
            self.click_on_contents()
            self.click_on_notes()

            notes = [note.text for note in self.capture_notes()]
            return self.sanitize(notes)
        finally:
            self.driver.quit()

    @staticmethod
    def sanitize(notes):
        words = []
        for note in notes:
            word = ''
            for char in note:
                if char.isalpha() or char in (' ', '-'):
                    word += char
            if len(word):
                words.append(word)
        return words

    def switch_to_books_frame(self):
        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[0])

    def wait_until_page_loads(self):
        WebDriverWait(self.driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")

    def click_on_contents(self):
        contents_top_bar_xpath_selector = "div.gb-topbar-controls-cell div:nth-of-type(2)"
        contents_button = self.driver.find_element_by_css_selector(contents_top_bar_xpath_selector)
        contents_button.click()

    def click_on_notes(self):
        notes_css_selector = "div.gb-tab-bar-top div:nth-of-type(3)"
        WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, notes_css_selector)))
        notes_button = self.driver.find_element_by_css_selector(notes_css_selector)
        notes_button.click()

    def capture_notes(self):
        items_css_selector = "div.gb-result span"
        WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, items_css_selector)))
        notes = self.driver.find_elements_by_css_selector(items_css_selector)
        return notes
