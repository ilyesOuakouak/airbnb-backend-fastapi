import asyncio
import httpx
import time

TARGET_URL = "http://127.0.0.1:8000/reservations/create"

PAYLOAD = {
    "listing_id": 1,
    "user_id": 1,
    "start_date": "2024-06-01",
    "end_date": "2024-06-05",
    "total_price": 500
}

CONCURRENT_REQUESTS = 20


async def send_booking_request(session, request_id):
    try:
        start_time = time.time()
        # Ensure we follow redirects if any
        response = await session.post(TARGET_URL, json=PAYLOAD, follow_redirects=True)
        duration = time.time() - start_time

        status = response.status_code
        # Print success or specific error codes
        print(f"User {request_id:02d} | Status: {status} | Time: {duration:.2f}s")
        return status
    except Exception as e:
        # FIX: Print the ACTUAL error representation
        print(f"User {request_id:02d} | Error: {repr(e)}")
        return 500


async def run_attack():
    print(f" STARTING ATTACK: {CONCURRENT_REQUESTS} users targeting Listing #{PAYLOAD['listing_id']}...")

    # Increase timeout just in case
    async with httpx.AsyncClient(timeout=30.0) as session:  # Give it 30 seconds
        tasks = [send_booking_request(session, i) for i in range(CONCURRENT_REQUESTS)]
        results = await asyncio.gather(*tasks)

    success_count = results.count(201)
    fail_count = CONCURRENT_REQUESTS - success_count

    print("\n" + "=" * 30)
    print("      ATTACK REPORT      ")
    print("=" * 30)
    print(f"Total Requests: {CONCURRENT_REQUESTS}")
    print(f"✅ Successful Bookings: {success_count}")
    print(f"❌ Failed/Rejected:     {fail_count}")
    print("-" * 30)

    if success_count > 1:
        print("🚨 FAIL: CRITICAL BUG DETECTED!")
        print(f"   Race Condition confirmed. You sold the room {success_count} times.")
    else:
        print("🛡️ PASS: System seems safe (or attack failed).")


if __name__ == "__main__":
    asyncio.run(run_attack())