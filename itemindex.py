class Item:
    def __init__(self, pricelist, name, cmdlist):
        self.name = name
        self.pricelist = pricelist
        self.cmdlist = cmdlist

    def getprices(self):
        return self.pricelist

    def getcmd(self):
        return self.cmdlist
