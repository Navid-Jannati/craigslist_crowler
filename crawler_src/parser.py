from bs4 import BeautifulSoup


class AdvertisementPageParser:

    def __init__(self):
        self.soup = None

    @property
    def title(self):
        title_tag = self.soup.find('span', attrs={'id': 'titletextonly'})
        if title_tag:
            return title_tag.text

    @property
    def price(self):
        price_tag = self.soup.find('span', attrs={'class': 'price'})
        if price_tag:
            return price_tag.text

    @property
    def body(self):
        body_tag = self.soup.select_one('#postingbody')
        if body_tag:
            return body_tag.text

    @property
    def post_id(self):
        selector = 'body > section > section > section > div.postinginfos > p:nth-child(1)'
        post_id_tag = self.soup.select_one(selector)
        if post_id_tag:
            # return post_id_tag.text[9:]
            return post_id_tag.text.replace('post id: ', '')

    @property
    def created_time(self):
        selector = 'body > section > section > section > div.postinginfos > p.postinginfo.reveal > time'
        time_tag = self.soup.select_one(selector)
        if time_tag:
            return time_tag.attrs['datetime']

    @property
    def modified_time(self):
        selector = 'body > section > section > section > div.postinginfos > p:nth-child(3) > time'
        time_tag = self.soup.select_one(selector)
        if time_tag:
            return time_tag.attrs['datetime']

    @property
    def images(self):
        images_list = self.soup.find_all('img')
        images_sources = set([img.attrs['src'].replace('50x50c', '600x450') for img in images_list])
        return [{'url': src, 'flag': False} for src in images_sources]

    def pars(self, html_data):
        self.soup = BeautifulSoup(html_data, 'html.parser')
        data = dict(
            title=self.title, price=self.price, body=self.body, post_id=self.post_id,
            created_time=self.created_time, modified_time=self.modified_time, images=self.images
        )
        return data
