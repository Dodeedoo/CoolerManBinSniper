class Item:
    def __init__(self, pricelist, name):
        self.name = name
        self.pricelist = pricelist

    def getprices(self):
        return self.pricelist
