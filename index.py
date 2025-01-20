import asyncio
from sanic import Sanic, Blueprint
from sanic.response import json
from functools import wraps

# Create a Sanic app and blueprint
app = Sanic("MyApp")
bp = Blueprint("MyBlueprint")

# Custom decorator for GET routes
def get_route(path):
    def decorator(func):
        func._route_path = path  # Store the route path
        func._http_method = "GET"  # Store the HTTP method
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Define a class with methods annotated for routes
class CustomRoutes:
    @get_route("/health")
    async def health(self, request):
        return json({"status": "healthy"})

    @get_route("/iterate")
    async def iterate(self, request):
        # Perform a dummy iteration in a separate thread
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.print_items)
        return json({"result": result})

    def print_items(self):  # Change to a regular function
        for i in range(1, 1000000):
            print(f"Processing item {i}...")
        return "Processing completed"

# Instantiate the custom routes class
routes = CustomRoutes()

# Programmatically register routes using add_route
for attr_name in dir(routes):
    attr = getattr(routes, attr_name)
    if callable(attr) and hasattr(attr, "_route_path") and attr._http_method == "GET":
        bp.add_route(attr, attr._route_path, methods=["GET"], name=f"{attr_name}_route")

# Register the blueprint to the app
app.blueprint(bp)

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)