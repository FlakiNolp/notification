from fastapi.testclient import TestClient
from api.main import app
import pytest
from httpx import AsyncClient

client = TestClient(app)


@pytest.mark.anyio
async def test_api_logs():
    request_data = {
        "code": "123",
        "message": "asdfjsd",
        "additional": "kajsdfkasdj"
    }
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        for _ in range(100):
            await ac.post('/api?token=secret', json=request_data)