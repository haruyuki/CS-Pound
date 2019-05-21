class Pet:
    def __init__(self, pps=False, store_pet=False, image_url='', owner_name='', owner_link='', pet_id=0, pet_name='', pet_adoption='', pet_age=0, pet_growth='', pet_rarity='', pet_given_name=None, pet_given_url=None):
        self.pps = pps
        self.store_pet = store_pet
        self.image = image_url
        self.owner_name = owner_name
        self.owner_link = owner_link
        self.id = pet_id
        self.name = pet_name
        self.adoption_date = pet_adoption
        self.age = pet_age
        self.growth = pet_growth
        self.rarity = pet_rarity
        self.given_name = pet_given_name
        self.given_url = pet_given_url

    def __repr__(self):
        return f"<Pet id={self.id} name='{self.name}'>"

    def owner(self):
        return f'[{self.owner_name}]({self.owner_link})'

    def given_by(self):
        if self.given_name is None or self.given_url is None:
            return None
        else:
            return f'[{self.given_name}]({self.given_url})'

    def rarity_link(self):
        filename = self.rarity.replace('!', '').replace(' ', '').lower() + '.png'
        return f'rarities/{filename}'
