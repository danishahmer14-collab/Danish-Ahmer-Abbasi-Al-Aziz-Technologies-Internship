import sqlite3
import httpx

def get_weather(city: str) -> dict:
    try:
        geo = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=10,
        ).json()
        if not geo.get("results"):
            return {"error": f"City '{city}' not found"}
        place = geo["results"][0]

        wx = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
            },
            timeout=10,
        ).json()["current"]

        return {
            "city": place["name"],
            "country": place.get("country"),
            "temperature_c": wx["temperature_2m"],
            "wind_speed_kmh": wx["wind_speed_10m"],
            "humidity_percent": wx["relative_humidity_2m"],
        }
    except Exception as e:
        return {"error": f"Weather lookup failed: {e}"}

_db = sqlite3.connect(":memory:", check_same_thread=False)
_db.execute("CREATE TABLE products (name TEXT, category TEXT, price REAL, stock INTEGER)")
_db.executemany(
    "INSERT INTO products VALUES (?, ?, ?, ?)",
    [
        ("Laptop Pro", "electronics", 1200.0, 5),
        ("Wireless Mouse", "electronics", 25.0, 40),
        ("Desk Lamp", "home", 35.0, 12),
        ("Office Chair", "home", 150.0, 0),
        ("Notebook Pack", "stationery", 8.0, 100),
    ],
)

def search_products(category: str | None = None, max_price: float | None = None) -> dict:
    query = "SELECT name, category, price, stock FROM products WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category.lower())
    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)
    rows = _db.execute(query, params).fetchall()
    return {"products": [dict(zip(["name", "category", "price", "stock"], r)) for r in rows]}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current real-time weather for a city. Use for any question about current weather or temperature.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City name, e.g. 'Islamabad'"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search the store's product database. Can filter by category (electronics, home, stationery) and maximum price.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Product category"},
                    "max_price": {"type": "number", "description": "Maximum price"},
                },
            },
        },
    },
]

TOOL_FUNCTIONS = {"get_weather": get_weather, "search_products": search_products}

def run_tool(name: str, args: dict) -> dict:
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return {"error": f"Unknown tool: {name}"}
    try:
        return func(**args)
    except TypeError as e:
        return {"error": f"Bad arguments: {e}"}