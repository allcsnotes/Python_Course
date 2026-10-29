import asyncio


async def send(email):
    await asyncio.sleep(0.1)
    if "@" not in email:
        raise ValueError(f"bad: {email}")
    if email.endswith(".xx"):
        raise TimeoutError(f"slow: {email}")
    print("sent to", email)


emails = ["asha@x.com", "lukas.com", "priya@y.xx", "meera"]


async def main():
    try:
        async with asyncio.TaskGroup() as group:
            for email in emails:
                group.create_task(send(email))
    except* ValueError as errors:
        print("bad addresses:", len(errors.exceptions))
        for error in errors.exceptions:
            print(" ", error)
    except* TimeoutError as errors:
        print("slow servers:", len(errors.exceptions))


asyncio.run(main())
