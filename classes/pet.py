from library import multi_replace


class Pet:
    def __init__(self, html_data):
        self.pps = self._get_pps(html_data)
        self.store_pet = self._get_store_pet(html_data)
        self.image_url = self._get_image_url(html_data)
        self.owner_name = ''
        self.owner_link = ''
        self.id = self._get_id(html_data)
        self.name = self._get_name(html_data)
        self.adoption_date = self._get_adoption_date(html_data)
        self.age = self._get_age(html_data)
        self.growth = self._get_growth(html_data)
        self.rarity = self._get_rarity(html_data)
        self.given_name = ''
        self.given_url = ''

        self._get_owner(html_data)
        self._get_given(html_data)

    def __repr__(self):
        return f"<Pet id={self.id} name='{self.name}'>"

    @staticmethod
    def _get_pps(data):
        pps = data.xpath('//table[@class="spine"]/tr[td/text() = "PPS"]')
        if pps:
            return True
        else:
            return False

    @staticmethod
    def _get_store_pet(data):
        store_pet = data.xpath('//table[@class="spine"]/tr[td/text() = "Store"]')
        if store_pet:
            return True
        else:
            return False

    @staticmethod
    def _get_image_url(data):
        image_url = data.xpath('//table[@class="spine"]/tr[1]//img/@src')[0]
        return image_url

    def _get_owner(self, data):
        owner_data = data.xpath('//table[@class="spine"]/tr[td/text() = "Owner"]')[0]
        self.owner_name = owner_data.xpath('.//a/text()')[0]
        self.owner_link = owner_data.xpath('.//a/@href')[0]

    @staticmethod
    def _get_id(data):
        pet_id = data.xpath('//table[@class="spine"]/tr[td/text() = "Pet ID"]/td[last()]/text()')[0]
        return int(pet_id)

    @staticmethod
    def _get_name(data):
        name = data.xpath('//table[@class="spine"]/tr[td/text() = "Pet\'s name"]/td[last()]/text()')
        if name:
            return name[0]
        else:
            return None

    @staticmethod
    def _get_adoption_date(data):
        adoption_date = data.xpath('//table[@class="spine"]/tr[td/text() = "Adopted"]/td[last()]/text()')[0]
        return adoption_date

    @staticmethod
    def _get_age(data):
        age_string = data.xpath('//table[@class="spine"]/tr[td/text() = "Age"]/td[last()]/text()')[0]
        try:
            age = age_string.split()[0]
        except IndexError:  # If no number found (i.e Pet is less than a day old)
            age = 0
        return int(age)

    @staticmethod
    def _get_growth(data):
        growth = data.xpath('//table[@class="spine"]/tr[td/text() = "Growth"]/td[last()]/text()')[0]
        return growth

    @staticmethod
    def _get_rarity(data):
        rarity = data.xpath('//table[@class="spine"]/tr[td/text() = "Rarity"]//img/@alt')[0]
        return rarity

    def _get_given(self, data):
        rarity_xpath = data.xpath('//table[@class="spine"]/tr[td/text() = "Rarity"]')[0]
        given_xpath = data.xpath('//table[@class="spine"]/tr[last()]')[0]
        if rarity_xpath == given_xpath:
            self.given_name = None
            self.given_url = None
        else:
            self.given_name = given_xpath.xpath('.//a/text()')[0]
            self.given_url = given_xpath.xpath('.//a/@href')[0]

    def owner(self):
        return f'[{self.owner_name}]({self.owner_link})'

    def given_by(self):
        if self.given_name is None or self.given_url is None:
            return None
        else:
            return f'[{self.given_name}]({self.given_url})'

    def rarity_link(self):
        filename = multi_replace(self.rarity.lower(), {'!': '', ' ': ''}) + '.png'
        return f'rarities/{filename}'
