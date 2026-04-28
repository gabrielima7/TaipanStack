from taipanstack.utils.rate_limit import RateLimiter

rl = RateLimiter(10, 1)

# Try giving massive tokens to consume
print(rl.consume(tokens=float('inf')))
# It should just reject
print(rl.consume(tokens=1e100))
