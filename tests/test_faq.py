import pytest
import allure
from data.faq_data import EXPECTED_FAQ_TEXTS
from page_objects.main_page import MainPage

class TestFaq:
    @pytest.mark.parametrize('index, expected_text', enumerate(EXPECTED_FAQ_TEXTS))
    @allure.title('Проверка текста ответа в разделе FAQ')
    def test_faq_item_opens_correct_text(self, driver, index, expected_text):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.scroll_to_faq()

        main_page.click_faq_item(index)
        answer_text = main_page.get_faq_item_answer_text(index)

        assert expected_text in answer_text, f"Текст ответа не содержит ожидаемый текст. Ожидалось: '{expected_text}', получено: '{answer_text}'"