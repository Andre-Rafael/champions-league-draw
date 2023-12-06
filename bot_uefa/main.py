from typing import List
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

class BotUefa:

    def __init__(self, webdriver: WebDriver) -> None:
        self._driver: WebDriver = webdriver
        self.url: str = 'https://footballdatabase.com/ranking/europe'

    def navigate(self) -> None:
        self._driver.get(f'{self.url}/1')

    def get_data(self) -> List[str]:
        clubs: List[str] = []
        page_range: int = self.get_qnt_pages()
        for page_num in range(1, page_range + 1):
            clubs.extend(self.scrap_page(page_num))
        return clubs

    def scrap_page(self, page_number: int) -> List[str]:
        clubs: List[str] = []
        self._driver.get(f'{self.url}/{page_number}')
        table_team: WebElement = self._driver.find_element(
            By.TAG_NAME, 'table')

        for line in table_team.find_elements(By.TAG_NAME, 'tr')[1:]:
            try:
                club_name, country = line.find_elements(
                    By.TAG_NAME, 'td'
                )[1].text.split('\n')
                clubs.append(f'{club_name} - {country}\n')
            except IndexError:
                continue
        return clubs

    def get_qnt_pages(self) -> int:
        page_range: int = len(self._driver.find_element(
            By.CLASS_NAME, 
            'pagination-sm'
        ).find_elements(By.TAG_NAME, 'li'))
        
        return page_range

    def save_data(self, data: List[str]) -> None:
        with open('clubs.txt', 'a', encoding='utf-8') as file:
            file.writelines(data)

    def start(self) -> None:
        self.navigate()
        data = self.get_data()
        self.save_data(data)


if __name__ == '__main__':
    service = Service(ChromeDriverManager().install())
    driver = Chrome(service=service)

    bot_uefa = BotUefa(driver)
    bot_uefa.start()