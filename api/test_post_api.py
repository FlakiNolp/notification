from fastapi.testclient import TestClient
from api.start_server import app
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
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
        for _ in range(100):
            await ac.post('/api?api_token=62875:3cdbe814f0f2e935209b295c966717c493b2d204b433c7263f1207508825b8cc', json=request_data)