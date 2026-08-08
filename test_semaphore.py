import asyncio

async def main():
    sem = asyncio.Semaphore(1)
    await sem.acquire()
    print("value:", getattr(sem, "_value", None))
    print("locked:", sem.locked())
    sem.release()
    print("value:", getattr(sem, "_value", None))
    print("locked:", sem.locked())

asyncio.run(main())
