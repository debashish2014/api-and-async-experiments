import asyncio
from sanic import Blueprint, Sanic, json, response
from aiologger import Logger

app = Sanic("MyApp")
bp = Blueprint("MyBlueprint")
logger = Logger.with_default_handlers(name="MyLogger")

# Define routes directly using the blueprint decorator
@bp.route("/health", methods=["GET"])
async def health(request):
    """Health endpoint to check service status."""
    return json({"status": "healthy"})

async def background_task():
    """Simulate a non-blocking background task."""
    # await asyncio.sleep(5)  # Non-blocking sleep

    for i in range(1, 1000000):
        await logger.info(f"Waiting {i} seconds...")
    
    return "Blocking function completed"

@bp.route("/api_call")
async def api_call(request):
    """Create a background task and get its result."""
    # task = asyncio.create_task(background_task())  # Non-blocking
    # result = await task  # Wait for the task to complete and get the result
    result = await background_task()
    return response.json({"status": "Task completed", "result": result})

app.blueprint(bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)