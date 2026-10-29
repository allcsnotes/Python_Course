import asyncio


async def worker():
    for step in range(1, 6):
        try:
            await asyncio.sleep(0.4)
            print("step", step)
        except:
            print("ignored the cancel")


async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(0.5)
    task.cancel()
    await task
    print("cancelled?", task.cancelled())


asyncio.run(main())
