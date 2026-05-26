FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml requirements.txt ./
COPY src ./src
COPY data ./data
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -e .

EXPOSE 8088
CMD ["python", "-m", "wear_edge_opea.gateway"]

