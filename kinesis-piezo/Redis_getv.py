import asyncio
import aioredis

async def get_values_from_redis():
    # Connect to Redis
    redis = await aioredis.create_redis('redis://localhost', encoding='utf-8')

    # Replace "rateVar" with the key you used to store values in the hash
    rate_values = await redis.hgetall("rateVar")
    accel_values = await redis.hgetall("accelVar")
    setX_values = await redis.hgetall("setXVar")
    setY_values = await redis.hgetall("setYVar")

    # Access individual values
    rate_value = float(rate_values["value"])
    accel_value = float(accel_values["value"])
    setX_value = float(setX_values["value"])
    setY_value = float(setY_values["value"])

    # Print or use the values as needed
    print("Rate Value:", rate_value)
    print("Accel Value:", accel_value)
    print("SetX Value:", setX_value)
    print("SetY Value:", setY_value)

    # Close the Redis connection
    redis.close()
    await redis.wait_closed()

# Run the asynchronous function
asyncio.run(get_values_from_redis())
