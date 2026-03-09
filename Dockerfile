FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY nhvr_mcp /app/nhvr_mcp

RUN pip install --no-cache-dir -e .

ENV NHVR_MCP_TRANSPORT=stdio

CMD ["python", "-m", "nhvr_mcp.server"]
