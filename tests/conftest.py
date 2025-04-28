import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.set_page_load_timeout(15)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()