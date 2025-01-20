import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from concurrent.futures import ThreadPoolExecutor
import uvicorn

# Create a FastAPI app
app = FastAPI()

# Define routes directly using the FastAPI decorators
@app.get("/health")
async def health():
    """Health endpoint to check service status."""
    return JSONResponse(content={"status": "healthy"})

async def background_print(i):
    """Background printing to avoid blocking."""
    print(f"Waiting {i} seconds...")


@app.get("/iterate")
async def iterate():
    """Non-blocking iteration with background printing."""
    for i in range(1, 1000000):
        asyncio.create_task(background_print(i))  # Non-blocking print
        if i % 1000 == 0:  # Yield to the event loop occasionally
            await asyncio.sleep(0)
    return JSONResponse(content={"status": "done"})


def call_openapi_sdk():
    """Call the blocking OpenAPI SDK."""
    # Simulate the blocking SDK call
    for i in range(1, 1050000):
        print(f"{i} seconds have passed...")
    return {"result": "OpenAPI call successful"}


@app.get("/api_call")
async def api_call():
    """Handle the OpenAPI SDK call without blocking."""
    loop = asyncio.get_event_loop()
    # Use ThreadPoolExecutor to offload blocking tasks
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, call_openapi_sdk)
    return JSONResponse(content=result)


if __name__ == "__main__":
    # Use uvicorn.run() to start the FastAPI app programmatically
    uvicorn.run(app, host="0.0.0.0", port=8000)