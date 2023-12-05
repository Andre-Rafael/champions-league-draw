from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


service = Service(ChromeDriverManager().install())
driver = Chrome(service=service)
driver.get('https://footballdatabase.com/ranking/europe/1')

page_range: int = len(driver.find_element(
    By.CLASS_NAME, 
    'pagination-sm'
).find_elements(By.TAG_NAME, 'li'))


for page_num in range(2, page_range + 1):
    table_team: WebElement = driver.find_element(By.TAG_NAME, 'table')

    for line in table_team.find_elements(By.TAG_NAME, 'tr')[1:]:
        try:
            club_name, country = line.find_elements(By.TAG_NAME, 'td')[1].text.split('\n')
        except IndexError:
            continue


        with open('clubs.txt', 'a', encoding='utf-8') as write:
            write.write(f'{club_name} - {country}\n')
            
    driver.get(f'https://footballdatabase.com/ranking/europe/{page_num}')


    