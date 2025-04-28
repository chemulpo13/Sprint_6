import pytest
import allure
from page_objects.main_page import MainPage
from page_objects.order_page import OrderPage
from data.order_data import order_test_data

class TestOrder:
    @allure.feature('Заказ самоката')
    @allure.story('Заказ через верхнюю кнопку')
    @allure.severity('critical')
    @pytest.mark.parametrize('order_data', order_test_data)
    def test_order_from_top_button(self, driver, order_data):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        main_page.go_to_site()
        main_page.click_order_button('top')

        order_page.wait_for_element_visible(order_page.NAME_FIELD)

        order_page.fill_order_form_first_page(
            order_data['name'],
            order_data['surname'],
            order_data['address'],
            order_data['metro'],
            order_data['phone']
        )

        order_page.click_next_button()

        order_page.wait_for_element_visible(order_page.DATE_FIELD)

        order_page.fill_order_form_second_page(
            order_data['date'],
            order_data['rental_period'],
            order_data['color'],
            order_data['comment']
        )

        order_page.click_order_button()
        order_page.click_yes_button()

        assert order_page.check_order_success(), "Заказ не был успешно оформлен"

    @allure.feature('Заказ самоката')
    @allure.story('Заказ через нижнюю кнопку')
    @allure.severity('critical')
    @pytest.mark.parametrize('order_data', order_test_data)
    def test_order_from_bottom_button(self, driver, order_data):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        main_page.go_to_site()
        main_page.click_order_button('bottom')

        order_page.wait_for_element_visible(order_page.NAME_FIELD)

        order_page.fill_order_form_first_page(
            order_data['name'],
            order_data['surname'],
            order_data['address'],
            order_data['metro'],
            order_data['phone']
        )

        order_page.click_next_button()

        order_page.wait_for_element_visible(order_page.DATE_FIELD)

        order_page.fill_order_form_second_page(
            order_data['date'],
            order_data['rental_period'],
            order_data['color'],
            order_data['comment']
        )

        order_page.click_order_button()
        order_page.click_yes_button()

        assert order_page.check_order_success(), "Заказ не был успешно оформлен"