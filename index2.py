import asyncio
from sanic import Sanic, Blueprint
from sanic.response import json

# Create a Sanic app and a blueprint
app = Sanic("MyApp")
bp = Blueprint("MyBlueprint")

# Define routes directly using the blueprint decorator
@bp.route("/health", methods=["GET"])
async def health(request):
    """Health endpoint to check service status."""
    return json({"status": "healthy"})

async def background_print(i):
    """Background printing to avoid blocking."""
    print(f"Waiting {i} seconds...")

@bp.route("/iterate", methods=["GET"])
async def iterate(request):
    """Non-blocking iteration with background printing."""
    for i in range(1, 1000000):
        asyncio.create_task(background_print(i))  # Non-blocking print
        if i % 1000 == 0:  # Yield to the event loop occasionally
            await asyncio.sleep(0)
    return json({"status": "done"})

def call_openapi_sdk():
    """Call the blocking OpenAPI SDK."""
    # Simulate the blocking SDK call
    # import time
    # time.sleep(5)  # Simulating delay from rate limiting
    
    for i in range(1, 1000000):
        print(f"{i} seconds have passed...")
    
    return {"result": "OpenAPI call successful"}

@bp.route("/api_call", methods=["GET"])
async def api_call(request):
    """Handle the OpenAPI SDK call without blocking."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, call_openapi_sdk)  # Offload to thread
    return json(result)

# Register the blueprint with the app
app.blueprint(bp)

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)