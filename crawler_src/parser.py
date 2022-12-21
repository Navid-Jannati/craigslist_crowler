from bs4 import BeautifulSoup


class AdvertisementPageParser:
    def pars(self, html_data):
        soup = BeautifulSoup(html_data, 'html.parser')
        data = dict(
            title=None, price=None, body=None, post_id=None,
            created_time=None, modified_time=None
        )
