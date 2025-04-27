import allure
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage

class MainPage(BasePage):
    YANDEX_LOGO = (By.CSS_SELECTOR, ".Header_LogoYandex__3TSOI")
    SCOOTER_LOGO = (By.CSS_SELECTOR, ".Header_LogoScooter__3lsAR")
    ORDER_BUTTON_TOP = (By.CSS_SELECTOR, ".Button_Button__ra12g")
    ORDER_BUTTON_BOTTOM = (By.CSS_SELECTOR, ".Home_FinishButton__1_cWm button")

    FAQ_SECTION = (By.CSS_SELECTOR, ".Home_FAQ__3uVm4")
    FAQ_ITEM_TEMPLATE = ".accordion__item:nth-child({}) .accordion__button"
    FAQ_ANSWER_TEMPLATE = ".accordion__item:nth-child({}) .accordion__panel"

    @allure.step('Клик по логотипу Яндекс')
    def click_yandex_logo(self):
        self.click_element(self.YANDEX_LOGO)

    @allure.step('Клик по логотипу Самокат')
    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    @allure.step('Клик по кнопке "Заказать" ({position})')
    def click_order_button(self, position):
        if position.lower() == 'top':
            self.click_element(self.ORDER_BUTTON_TOP)
        elif position.lower() == 'bottom':
            self.scroll_to_element(self.ORDER_BUTTON_BOTTOM)
            self.click_element(self.ORDER_BUTTON_BOTTOM)
        else:
            raise ValueError(f"Неверная позиция кнопки: {position}. Допустимые значения: 'top', 'bottom'")

    @allure.step('Прокрутка к блоку FAQ')
    def scroll_to_faq(self):
        self.scroll_to_element(self.FAQ_SECTION)

    @allure.step('Клик по вопросу FAQ № {index}')
    def click_faq_item(self, index):
        locator = (By.CSS_SELECTOR, self.FAQ_ITEM_TEMPLATE.format(index + 1))
        self.click_element(locator)

    @allure.step('Получение текста ответа FAQ № {index}')
    def get_faq_item_answer_text(self, index):
        locator = (By.CSS_SELECTOR, self.FAQ_ANSWER_TEMPLATE.format(index + 1))
        element = self.wait_for_element(locator)
        return element.text

    @allure.step('Переключение на новую вкладку')
    def switch_to_new_tab(self):
        window_handles = self.driver.window_handles

        if len(window_handles) < 2:
            raise Exception("Не найдена новая вкладка")

        self.driver.switch_to.window(window_handles[-1])