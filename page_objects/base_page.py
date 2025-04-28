from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure

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
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="element_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"Элемент с локатором {locator} не появился на странице")

    @allure.step('Ожидание видимости элемента с локатором {locator}')
    def wait_for_element_visible(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="element_not_visible",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"Элемент с локатором {locator} не стал видимым")

    @allure.step('Ожидание элемента для клика с локатором {locator}')
    def wait_for_element_clickable(self, locator):
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="element_not_clickable",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"Элемент с локатором {locator} не стал кликабельным")

    @allure.step('Ожидание исчезновения элемента с локатором {locator}')
    def wait_for_element_invisibility(self, locator):
        try:
            return self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="element_still_visible",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"Элемент с локатором {locator} все еще видим")

    @allure.step('Ожидание появления текста {text} в элементе с локатором {locator}')
    def wait_for_text_in_element(self, locator, text):
        try:
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="text_not_present",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"Текст {text} не появился в элементе с локатором {locator}")

    @allure.step('Ожидание появления новой вкладки')
    def wait_for_new_tab(self, current_handles_count):
        try:
            return self.wait.until(lambda driver: len(driver.window_handles) > current_handles_count)
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="no_new_tab",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException("Новая вкладка не была открыта")

    @allure.step('Ожидание URL, содержащего {url_part}')
    def wait_for_url_contains(self, url_part):
        try:
            return self.wait.until(EC.url_contains(url_part))
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="url_does_not_contain",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"URL не содержит {url_part}. Текущий URL: {self.driver.current_url}")

    @allure.step('Клик по элементу с локатором {locator}')
    def click_element(self, locator):
        element = self.wait_for_element_clickable(locator)
        element.click()

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

    @allure.step('Переключение на новую вкладку')
    def switch_to_new_tab(self):
        window_handles = self.driver.window_handles
        if len(window_handles) < 2:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="no_new_tab",
                attachment_type=allure.attachment_type.PNG
            )
            raise Exception("Не найдена новая вкладка")
        self.driver.switch_to.window(window_handles[-1])

    @allure.step('Переключение на вкладку по индексу')
    def switch_to_tab(self, index=0):
        window_handles = self.driver.window_handles
        if index >= len(window_handles):
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="tab_index_out_of_range",
                attachment_type=allure.attachment_type.PNG
            )
            raise IndexError(f"Индекс вкладки {index} выходит за пределы доступных вкладок ({len(window_handles)})")
        self.driver.switch_to.window(window_handles[index])

    @allure.step('Нажатие клавиши {key} в элементе {locator}')
    def send_key_to_element(self, locator, key):
        element = self.wait_for_element(locator)
        element.send_keys(key)

    @allure.step('Поиск элемента с локатором {locator}')
    def find_element(self, locator):
        return self.driver.find_element(*locator)

    @allure.step('Выполнение JavaScript: {script}')
    def execute_script(self, script, element=None):
        if element:
            return self.driver.execute_script(script, element)
        else:
            return self.driver.execute_script(script)

    @allure.step('Сделать скриншот')
    def take_screenshot(self, name="screenshot"):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )