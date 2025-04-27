import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://qa-scooter.praktikum-services.ru/"
        self.wait = WebDriverWait(driver, 10)

    @allure.step('Переход на сайт')
    def go_to_site(self):
        self.driver.get(self.base_url)

    @allure.step('Получение текущего URL')
    def get_current_url(self):
        return self.driver.current_url

    @allure.step('Ожидание элемента с локатором {locator}')
    def wait_for_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="element_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"Элемент с локатором {locator} не найден")

    def wait_for_element_visibility(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.driver.save_screenshot("debug_screenshot.png")
            raise TimeoutException(f"Элемент с локатором {locator} не найден или не стал видимым за {timeout} секунд")

    @allure.step('Клик по элементу с локатором {locator}')
    def click_element(self, locator):
        element = self.wait_for_element(locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step('Ввод текста {text} в поле с локатором {locator}')
    def input_text(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step('Прокрутка к элементу с локатором {locator}')
    def scroll_to_element(self, locator):
        try:
            element = self.wait_for_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        except TimeoutException:
            print(f"Не удалось прокрутить к элементу с локатором {locator}")