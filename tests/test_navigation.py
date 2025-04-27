import pytest
import allure
import time
from page_objects.main_page import MainPage
from constants import DZEN_URL

class TestNavigation:
    @allure.feature('Навигация')
    @allure.story('Редирект на главную страницу Самоката')
    @allure.severity('critical')
    def test_scooter_logo_redirects_to_main_page(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_site()

        main_page.click_order_button('top')

        main_page.click_scooter_logo()

        current_url = main_page.get_current_url()
        assert current_url == main_page.base_url, f"Неверный URL после нажатия на логотип Самоката: {current_url}"

    @allure.feature('Навигация')
    @allure.story('Редирект на Дзен')
    @allure.severity('critical')
    def test_yandex_logo_redirects_to_dzen(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_site()

        main_page.click_yandex_logo()

        time.sleep(3)

        main_page.switch_to_new_tab()

        current_url = main_page.get_current_url()
        assert DZEN_URL in current_url, f"Неверный URL после нажатия на логотип Яндекса: {current_url}"