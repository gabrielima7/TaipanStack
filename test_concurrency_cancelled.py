import asyncio
from taipanstack.utils.concurrency import limit_concurrency

@limit_concurrency(max_tasks=1, timeout=5.0)
async def my_task():
    await asyncio.sleep(10)
    return "ok"

async def main():
    task = asyncio.create_task(my_task())
    await asyncio.sleep(0.1)
    task.cancel()
    try:
        res = await task
        print(f"Result: {res}")
    except asyncio.CancelledError:
        print("Cancelled properly")
    except Exception as e:
        print(f"Other exception: {e}")

asyncio.run(main())
