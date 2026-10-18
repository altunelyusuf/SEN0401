"""Chapter 1 deck 2.11.0: every story slide shows its licence-clear picture with the credit and the ISO date of the story; links that answer 403 or no connection from the build machine are replaced by reachable pages of the same resource or event (owner's coordinator, 2026-10-19)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sen0401_deck_story_v1_0_0 import set_pic, set_fact, move, items, slide
import importlib.util, glob, re
def stories():
    p = sorted(glob.glob(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sen0401_ch01_stories_v*.py")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
    sp = importlib.util.spec_from_file_location("st", p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return {s["id"]: s for s in m.STORIES}
def patch(plan):
    S = stories(); C = "01"
    def credit(i): return S[i]["credit"]
    # 7 genesis: the hex dump keeps its box, the credit replaces the caption
    set_pic(plan, 7, C, "genesis_hexdump.png", credit("GenesisHeadline"), 0.5, 1.42, 5.9, 2.55); set_fact(plan, 7, when=S["GenesisHeadline"]["when"])
    for n, k in ((7, "GenesisHeadline"), (8, "FirstTransaction"), (11, "StoneMoney"), (23, "PizzaDay"), (34, "MtGox"), (9, "CypherpunkLineage"), (12, "MoneyEvolution")):
        set_fact(plan, n, link=S[k]["link"], linkText=S[k]["linkLabel"])
    # 8 first payment: Hal Finney
    set_pic(plan, 8, C, "photo_hal_finney_1972.jpg", credit("FirstTransaction"), 0.5, 1.45, 2.9, 2.5, drop=("c1s32_nakamoto.jpg",)); set_fact(plan, 8, when=S["FirstTransaction"]["when"], x=0.5, y=4.42, w=9.0)
    # 9 forty years: David Chaum in a column at the right
    for it, lab in zip(items(plan, 9, "timeline")[0]["items"], ["Chaum: ecash", "Back: Hashcash", "Dai, Szabo: b-money, bit gold", "Nakamoto: the whitepaper", "The genesis block runs"]): it["label"] = lab
    move(plan, 9, "timeline", w=7.3); move(plan, 9, "bullets", w=7.3, fs=12, h=0.55)
    set_pic(plan, 9, C, "photo_david_chaum_2018.jpg", credit("CypherpunkLineage"), 7.95, 1.55, 1.55, 2.05); set_fact(plan, 9, when=S["CypherpunkLineage"]["when"])
    # 11 Yap
    set_pic(plan, 11, C, "photo_rai_stone.jpg", credit("StoneMoney"), 0.5, 1.45, 3.1, 2.55); set_fact(plan, 11, when=S["StoneMoney"]["when"], x=0.5, y=4.42, w=9.0)
    slide(plan, 11)["sub"] = "Documented in 1903; the book's free ebook edition came in 2024"
    move(plan, 11, "ledger", y=2.45); move(plan, 11, "beats", y=1.4, h=1.05)
    # 12 money through the ages: the stater gets a wider box
    set_pic(plan, 12, C, "photo_cma_stater.jpg", credit("MoneyEvolution"), 6.9, 1.5, 2.6, 1.1); move(plan, 12, "text", w=4.0); set_fact(plan, 12, when=S["MoneyEvolution"]["when"])
    # 15 online payments
    move(plan, 15, "timeline", h=1.5); move(plan, 15, "bullets", w=6.7)
    set_pic(plan, 15, C, "photo_paypal_logo.png", credit("OnlinePayments"), 7.4, 3.3, 2.1, 0.7)
    set_fact(plan, 15, when=S["OnlinePayments"]["when"], link=S["OnlinePayments"]["link"], linkText=S["OnlinePayments"]["linkLabel"])
    # 16 when money stops: cases narrower, Fedorov at the right
    c = move(plan, 16, "cases", x=0.3, w=8.05)
    c["items"][4]["link"] = S["WhenMoneyStops"]["link"]
    set_pic(plan, 16, C, "photo_fedorov_portrait.jpg", credit("WhenMoneyStops"), 8.5, 1.7, 1.15, 1.55)
    c["items"][4]["text"] = "State and NGO raised $54.7M in crypto in a week"
    set_fact(plan, 16, when=S["WhenMoneyStops"]["when"], link=S["WhenMoneyStops"]["link"], linkText=S["WhenMoneyStops"]["linkLabel"])
    # 23 pizza day: the plaque of the pizzeria instead of a stock pizza
    set_pic(plan, 23, C, "photo_papa_johns_jacksonville.jpg", credit("PizzaDay"), 0.55, 2.75, 2.95, 1.25, drop=("photo_pizza_margherita.jpg",)); set_fact(plan, 23, when=S["PizzaDay"]["when"], x=0.5, y=4.42, w=9.0); move(plan, 23, "stat", y=1.5, h=1.2)
    # 34 Mt. Gox
    move(plan, 34, "beats", w=6.2)
    set_pic(plan, 34, C, "photo_mtgox_logo.png", credit("MtGox"), 6.95, 3.0, 2.55, 1.0); set_fact(plan, 34, when=S["MtGox"]["when"])
    # 45 resources: reachable equivalents
    g = items(plan, 45, "links")[0]["groups"]
    for grp in g:
        for r in grp["rows"]:
            if "coingecko.com/en/coins/bitcoin" in r[1]:
                r[0] = "CoinGecko: Bitcoin price data (API)"; r[1] = "https://api.coingecko.com/api/v3/coins/bitcoin"; r[2] = "Price, market cap and volume of bitcoin, as CoinGecko's own data feed"
            if "web.archive.org/web/2023/http://www.hashcash.org" in r[1]:
                r[1] = "https://cdn.nakamotoinstitute.org/docs/hashcash.pdf"; r[2] = "Adam Back's proof-of-work paper; Nakamoto Institute copy"
            if "web.archive.org/web/2023/http://www.weidai.com" in r[1]:
                r[1] = "https://cdn.nakamotoinstitute.org/docs/b-money.txt"; r[2] = "The 1998 proposal Bitcoin cites; Nakamoto Institute copy"
            if "youtube.com/watch?v=bBC-nXj3Ng4" in r[1]:
                r[1] = "https://www.youtube.com/embed/bBC-nXj3Ng4"
