class Dragon:
    def __init__(self, html_data):
        # Lineage
        self.parents = []
        self.children = []

        # Info
        self.name = ''
        self.id = ''
        self.image = ''
        self.breeding_available = True
        self.breeding_cooldown = 0
        self.flight = ''
        self.gender = ''
        self.breed = ''

        # Genes and Colours
        self.primary_colour = ''
        self.primary_gene = ''
        self.secondary_colour = ''
        self.secondary_gene = ''
        self.tertiary_colour = ''
        self.tertiary_gene = ''
        self.eye_type = ''

        self.stats = self._Stats(html_data)
        self.growth = self._Growth(html_data)
        self._get_lineage(html_data)
        self._get_info(html_data)
        self._get_genes(html_data)

    def __repr__(self):
        return f"<Dragon id={self.id} name='{self.name}'>"

    def _get_lineage(self, data):
        parents_temp = data.xpath('//div[@id="super-container"]/div[last()]/div[5]/fieldset/div[2]/div[2]/a')
        for parent in parents_temp:
            parent_name = parent.xpath('text()')[0]
            parent_link = parent.xpath('@href')[0]
            self.parents.append((parent_name, parent_link))

        children_temp = data.xpath('//div[@id="super-container"]/div[last()]/div[5]/fieldset/div[2]/div[5]/a')
        for child in children_temp:
            child_name = child.xpath('text()')[0]
            child_link = child.xpath('@href')[0]
            self.children.append((child_name, child_link))

    def _get_info(self, data):
        name_temp = data.xpath('//div[@id="super-container"]/div/span/text()[1]')[0]
        self.name = ' '.join(name_temp.split())

        id_temp = data.xpath('//div[@id="super-container"]/div[2]/span/div/text()')[0]
        self.id = ' '.join(id_temp.split())[1:]

        try:
            breeding_temp = data.xpath('//div[@id="newname"]/fieldset/div[1]/a[@class="loginbar"]/@title')[0]
            self.breeding_available = False
            self.breeding_cooldown = int([n for n in breeding_temp.split() if n.isdigit()][0])
        except IndexError:
            self.breeding_available = True
            self.breeding_cooldown = 0

        self.image = data.xpath('//div[@id="dragbuttons"]/img/@src')[0]

        flight_temp = data.xpath('//div[@id="newname"]/fieldset/div[1]/a[@class="elemclue"]/@title')[0]
        self.flight = flight_temp.split()[0]

        gender_temp = data.xpath('//div[@id="newname"]/fieldset/div[1]/a[@class="miniclue"]/@title')[0]
        self.gender = gender_temp.split()[0]

        breed_temp = data.xpath('//div[@id="newname"]/fieldset/div[2]/span[2]/div/div[2]/text()')[0]
        self.breed = breed_temp.split()[0]

    def _get_genes(self, data):
        genes = data.xpath('//div[@id="newname"]/fieldset/div/span[last()]/div/div/text()')
        temp_primary = genes[0].split()
        self.primary_colour = temp_primary[0]
        self.primary_gene = temp_primary[1]

        temp_secondary = genes[1].split()
        self.secondary_colour = temp_secondary[0]
        self.secondary_gene = temp_secondary[1]

        temp_tertiary = genes[2].split()
        self.tertiary_colour = temp_tertiary[0]
        self.tertiary_gene = temp_tertiary[1]

        self.eye_type = genes[3]

    def primary(self):
        return f'{self.primary_colour} {self.primary_gene}'

    def secondary(self):
        return f'{self.secondary_colour} {self.secondary_gene}'

    def tertiary(self):
        return f'{self.tertiary_colour} {self.tertiary_gene}'

    class _Stats:
        def __init__(self, data):
            self.data = data
            self.STR = self._strength()
            self.INT = self._intelligence()
            self.AGI = self._agility()
            self.VIT = self._vitality()
            self.DEF = self._defense()
            self.MND = self._mind()
            self.QCK = self._quickness()

        def __call__(self):
            return {'STR': self.STR, 'INT': self.INT,
                    'AGI': self.AGI, 'VIT': self.VIT,
                    'DEF': self.DEF, 'MND': self.MND,
                    'QCK': self.QCK}

        def _strength(self):
            value = int(self.data.xpath('//a[@class="cluestat"]')[0].xpath('span[2]/text()')[0])
            return value

        def _intelligence(self):
            value = int(self.data.xpath('//a[@class="cluestat"]')[1].xpath('span[2]/text()')[0])
            return value

        def _agility(self):
            value = int(self.data.xpath('//a[@class="cluestat"]')[2].xpath('span[2]/text()')[0])
            return value

        def _vitality(self):
            value = int(self.data.xpath('//a[@class="cluestat"]')[3].xpath('span[2]/text()')[0])
            return value

        def _defense(self):
            value = int(self.data.xpath('//a[@class="cluestat"]')[4].xpath('span[2]/text()')[0])
            return value

        def _mind(self):
            value = int(self.data.xpath('//a[@class="cluestat"]')[5].xpath('span[2]/text()')[0])
            return value

        def _quickness(self):
            value = int(self.data.xpath('//a[@class="cluestat"]')[6].xpath('span[2]/text()')[0])
            return value

    class _Growth:
        def __init__(self, data):
            self.data = data
            self.raw_length = self._get_length()
            self.raw_wingspan = self._get_wingspan()
            self.raw_weight = self._get_weight()

        def __call__(self):
            return {'length': self.raw_length, 'wingspan': self.raw_wingspan, 'weight': self.raw_weight}

        def _get_length(self):
            value = self.data.xpath('//div[@id="newname"]/fieldset/div[2]/span[6]/div/span/text()')[0]
            return float(value[:-1])

        def _get_wingspan(self):
            value = self.data.xpath('//div[@id="newname"]/fieldset/div[2]/span[6]/div/span/text()')[1]
            return float(value[:-1])

        def _get_weight(self):
            value = self.data.xpath('//div[@id="newname"]/fieldset/div[2]/span[6]/div/span/text()')[2]
            return float(value[:-2])

        def length(self):
            return f'{self.raw_length}M'

        def wingspan(self):
            return f'{self.raw_wingspan}M'

        def weight(self):
            return f'{self.raw_weight}KG'
