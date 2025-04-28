import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from page_objects.base_page import BasePage

class OrderPage(BasePage):
    NAME_FIELD = (By.XPATH, "//input[@placeholder='* Имя']")
    SURNAME_FIELD = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_FIELD = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_FIELD = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_OPTION = (By.XPATH, "//div[@class='select-search__select']/ul/li[1]")
    PHONE_FIELD = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    DATE_FIELD = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.XPATH, "//div[@class='Dropdown-root']")
    RENTAL_PERIOD_OPTION_TEMPLATE = "//div[@class='Dropdown-menu']/div[{}]"
    COLOR_BLACK_CHECKBOX = (By.ID, "black")
    COLOR_GRAY_CHECKBOX = (By.ID, "grey")
    COMMENT_FIELD = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//div[contains(@class, 'Order_Buttons')]/button[text()='Заказать']")

    YES_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_MODAL = (By.XPATH, "//div[contains(@class, 'Order_Modal__YZ-d3')]")
    SUCCESS_HEADER = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")
    SUCCESS_TEXT = "Заказ оформлен"

    @allure.step('Заполнение первой страницы формы заказа')
    def fill_order_form_first_page(self, name, surname, address, metro, phone):
        self.input_text(self.NAME_FIELD, name)
        self.input_text(self.SURNAME_FIELD, surname)
        self.input_text(self.ADDRESS_FIELD, address)

        self.click_element(self.METRO_FIELD)
        self.input_text(self.METRO_FIELD, metro)
        self.wait_for_element(self.METRO_OPTION)
        self.click_element(self.METRO_OPTION)

        self.input_text(self.PHONE_FIELD, phone)

    @allure.step('Клик по кнопке "Далее"')
    def click_next_button(self):
        self.click_element(self.NEXT_BUTTON)

    @allure.step('Заполнение второй страницы формы заказа')
    def fill_order_form_second_page(self, date, period, color, comment):
        self.input_text(self.DATE_FIELD, date)
        self.send_key_to_element(self.DATE_FIELD, Keys.ESCAPE)

        self.click_element(self.RENTAL_PERIOD_DROPDOWN)
        period_option = (By.XPATH, self.RENTAL_PERIOD_OPTION_TEMPLATE.format(period))
        self.wait_for_element(period_option)
        self.click_element(period_option)

        if color.lower() == 'black':
            self.click_element(self.COLOR_BLACK_CHECKBOX)
        elif color.lower() == 'gray':
            self.click_element(self.COLOR_GRAY_CHECKBOX)

        if comment:
            self.input_text(self.COMMENT_FIELD, comment)

    @allure.step('Клик по кнопке "Заказать"')
    def click_order_button(self):
        self.click_element(self.ORDER_BUTTON)

    @allure.step('Клик по кнопке "Да" в окне подтверждения')
    def click_yes_button(self):
        self.wait_for_element_visible(self.YES_BUTTON)
        self.click_element(self.YES_BUTTON)

    @allure.step('Проверка успешного оформления заказа')
    def check_order_success(self):
        self.wait_for_element_visible(self.SUCCESS_MODAL)
        modal_header = self.wait_for_element_visible(self.SUCCESS_HEADER)
        return self.SUCCESS_TEXT in modal_header.text