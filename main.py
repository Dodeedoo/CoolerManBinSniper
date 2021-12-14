import json
import re
import traceback

import requests
import itemindex
import time
import sched
import cProfile, pstats, io
from numba import jit


def profile(fnc):
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


def getInfo(call):
    r = requests.get(call)
    return r.json()


n1 = 0

s = sched.scheduler(time.time, time.sleep)

itemlists = {}

toplist = {}

nameexclude = ["✪", "Rapid", "Gentle", "Odd", "Fast", "Fair", "Epic", "Sharp", "Heroic", "Spicy", "Legendary", "Dirty",
               "Suspicious", "Gilded", "Warped", "Bulky", "Salty", "Treacherous", "Stiff", "Lucky", "Very", "Highly",
               "Extremely", "Not So", "Thicc[sic]", "Absolutely", "Even More", "Wise", "Strong", "Superior", "Heavy",
               "Light", "Perfect", "Refined", "Deadly", "Fine", "Grand", "Hasty", "Neat", "Rapid", "Unreal", "Awkward",
               "Rich", "Precise", "Spiritual", "Headstrong", "Clean", "Fierce", "Mythic", "Pure", "Smart", "Titanic",
               "Perfect", "Necrotic", "Spiked", "Cubic", "Reinforced", "Loving", "Ridiculous", "Empowered", "Giant",
               "Submerged", "Bizarre", "Itchy", "Ominous", "Pleasant", "Pretty", "Shiny", "Simple", "Strange", "Vivid",
               "Godly", "Demonic", "Forceful", "Hurtful", "Keen", "Unpleasant", "Zealous", "Silky", "Bloody", "Shaded",
               "Sweet", "Moil", "Toil", "Blessed", "Bountiful", "Magnetic", "Fruitful", "Stellar", "Mithraic",
               "Auspicious", "Fleet", "Heated", "Ambered"]

valuedenchants = ["Jaded", "Renowned", "Fabled", "Ancient", "Withered"]

auctionlink = f"https://api.hypixel.net/skyblock/auctions?page={n1}"

auctions = getInfo(auctionlink)

print("Enter Margin: (10-100%)")
margin = input()


def namerep(name):
    name = re.sub("[\[[^\]]*\]", "", name)
    name = name.replace("\u272a", "")
    for reforge in nameexclude: name = name.replace(reforge, "")
    return name.strip()


for y in range(0, auctions["totalPages"]):
    print(y)
    try:
        n1 += 1
        auctionlink = f"https://api.hypixel.net/skyblock/auctions?page={n1}"
        auctions = getInfo(auctionlink)
        try:
            for x in range(0, 1000):
                item = auctions["auctions"][x]
                if "bin" in item:
                    name = namerep(item["item_name"])
                    if name in itemlists:
                        itemlists[name] += 1
                    else:
                        itemlists[name] = 1
        except KeyError:
            print("error occurred")
            print(traceback.format_exc())
    except KeyError:
        pass
    except IndexError:
        pass

itemlists.pop("Enchanted Book")
pet = []
for x in itemlists:
    if "Lvl" in x:
        pet.append(x)
for x in pet:
    itemlists.pop(x)
print(json.dumps(itemlists, indent=2))


@profile
def update():
    print("updated")
    auctionlink = f"https://api.hypixel.net/skyblock/auctions?page=0"
    auctions = getInfo(auctionlink)
    start = time.time()
    top500 = sorted(itemlists, key=itemlists.get, reverse=True)[:500]
    #print(json.dumps(top500, indent=2))
    for y in range(0, auctions["totalPages"]):
        print(y)
        auctionlink = f"https://api.hypixel.net/skyblock/auctions?page={y}"
        auctions = getInfo(auctionlink)
        pricelist = {}
        for x in range(0, 1000):
            try:
                item = auctions["auctions"][x]
                if "bin" in item:
                    name = namerep(item["item_name"])
                    if name in top500:
                        if name in pricelist:
                            pricelist[name].append(item["starting_bid"])
                        else:
                            pricelist[name] = [item["starting_bid"]]
            except KeyError:
                print("error occurred")
                print(traceback.format_exc())
            except IndexError:
                print("error occurred")
                print(traceback.format_exc())
        print(json.dumps(pricelist, indent=3))
        for z in range(-1, len(top500)):
            toplist[top500[z]] = itemindex.Item(pricelist[top500[z]], top500[z])
    for y in toplist:
        prices = itemindex.Item.getprices(toplist[y])
        print(str(len(prices)) + str(y))
        if len(prices) > 5:
            print(y)
            prices.sort()
            prices.pop()
            prices.pop()
            prices.pop()
            average = sum(prices) / len(prices)
            average = int(average)
            reqmargin = average / float(margin)
            if min(prices) + int(reqmargin) <= average:
                print(" ")
                print(y)
                print(str(min(prices)) + " snipe")
                print(str(average) + " avg")
                print(" ")
    end = time.time()
    print(end - start)
    s.enter(3, 1, update())



s.enter(3, 1, update())
s.run()
# init method indexes auctions and adds the 500 most common items to an array

# next method will add average prices of common items and check for margins
# if "Superior" in item["item_name"]:
#   list1.insert(item["starting_bid"], int)
#  print(str(item["item_name"]) + " " + str(item["starting_bid"1]))
