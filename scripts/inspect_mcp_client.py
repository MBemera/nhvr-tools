import mcp
import mcp.client

print(getattr(mcp, "__version__", "unknown"))

names = [name for name in dir(mcp.client) if "Client" in name or "client" in name]
print(names)
