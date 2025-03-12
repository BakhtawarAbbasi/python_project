from fastapi import FastAPI
import random

app = FastAPI()

side_hustles = [
    "Freelancing - Start offering your skills online!",
    "Dropshipping - Sell without handling inventory!",
    "Stock Market - Invest and watch your money grow!",
    "Affiliate Marketing - Earn by promoting products!",
    "Crypto Trading - Buy and Sell digital assets!",
    "Online Courses - Share your knowledge and earn!",
    "Print-on-Demand - Sell custom-designed products!",
    "Blogging - Create content and earn through ads and sponsorships!",
    "YouTube Channel - Monetize videos through ads and sponsorships!",
    "Social Media Management - Manage accounts for brands and influencers!",
    "App Development - Create mobile or web applications for businesses!",
]

money_quotes = [
    "Money is a terrible master but an excellent servant. – P.T. Barnum",
    "Too many people spend money they haven’t earned to buy things they don’t want to impress people they don’t like. – Will Rogers",
    "An investment in knowledge pays the best interest. – Benjamin Franklin",
    "The stock market is filled with individuals who know the price of everything, but the value of nothing. – Philip Fisher",
    "Do not save what is left after spending, but spend what is left after saving. – Warren Buffett",
    "A wise person should have money in their head, but not in their heart. – Jonathan Swift",
    "It’s not about having lots of money. It’s about knowing how to manage it. – Unknown",
    "Money often costs too much. – Ralph Waldo Emerson",
    "Wealth consists not in having great possessions, but in having few wants. – Epictetus",
    "If you want to feel rich, just count the things you have that money can’t buy. – Unknown",
    "Formal education will make you a living; self-education will make you a fortune. – Jim Rohn",
    "The goal isn’t more money. The goal is living life on your terms. – Chris Brogan",
]

@app.get("/side_hustles")
def get_side_hustles():
    """Return a random side hustle idea"""
    return {"side_hustle": random.choice(side_hustles)}

@app.get("/money_quotes")
def get_money_quotes():
    """Returns a random money quote"""
    return {"money_quote": random.choice(money_quotes)}
