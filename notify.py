from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import get_expiring_products

scheduler = AsyncIOScheduler()

async def notify_expiring_products(bot):
    expiring = get_expiring_products()
    for user_id, items in expiring.items():
        lines = ["⏰ Продукты скоро испортятся:"]
        for name, date in items:
            lines.append(f"— {name}, до {date}")
        try:
            await bot.send_message(user_id, "\n".join(lines))
        except:
            continue