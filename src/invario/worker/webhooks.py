import structlog
import aiohttp
import asyncio

logger = structlog.get_logger()

async def send_webhook(url: str, payload: dict, attempt: int = 1, max_attempts: int = 3) -> None:
    """Send webhook with exponential backoff retry."""
    log = logger.bind(webhook_url=url, attempt=attempt)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=10) as response:
                if response.status >= 200 and response.status < 300:
                    log.info("webhook_sent_successfully", status=response.status)
                    return
                else:
                    log.warning("webhook_delivery_failed", status=response.status)
                    # Raise exception to trigger retry logic below
                    raise Exception(f"Webhook failed with status {response.status}")

    except Exception as e:
        log.warning("webhook_error", error=str(e))

        if attempt < max_attempts:
            wait_time = 2 ** attempt  # 2s, 4s, 8s...
            log.info("retrying_webhook", wait_time=wait_time)
            await asyncio.sleep(wait_time)
            await send_webhook(url, payload, attempt + 1, max_attempts)
        else:
            log.error("webhook_max_retries_exceeded")
