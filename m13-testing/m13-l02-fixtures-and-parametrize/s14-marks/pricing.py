def final_price(price, percent):
    if not 0 <= percent <= 100:
        raise ValueError("percent must be from 0 to 100")
    return price - price * percent // 100
