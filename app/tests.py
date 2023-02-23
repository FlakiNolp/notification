from app.main import app
import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_speed():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:1002") as ac:
        response1 = await ac.post("/sign-up", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={"username": "maksimosetrov4@gmail.com", "password": "super_secret"})
        response3 = await ac.get("/registration?email_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1ha3NpbW9zZXRyb3Y0QGdtYWlsLmNvbSIsImhhc2hlZF9wYXNzd29yZCI6IjVjMGI2MmViNWZiMzA4N2FmY2U3ZTliYWM0ZTA2NjExMTliZDYyNzg1MzBmNTY4MzNmOGVlMTg5MDM0MzZjYWUiLCJleHAiOjE2NzcwMTU4NDl9.k4SBBGpSsuII-dgY_VMYQMeEJQDGEpqvf8BNuHOh2Ak")
        response2 = await ac.post("/sign-up", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={"username": "maxim.osetrov-2016@yandex.ru", "password": "secret"})
        response4 = await ac.get("/registration?email_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1heGltLm9zZXRyb3YtMjAxNkB5YW5kZXgucnUiLCJoYXNoZWRfcGFzc3dvcmQiOiIyYmI4MGQ1MzdiMWRhM2UzOGJkMzAzNjFhYTg1NTY4NmJkZTBlYWNkNzE2MmZlZjZhMjVmZTk3YmY1MjdhMjViIiwiZXhwIjoxNjc3MDE1ODUwfQ.OMSPi-mSBuFS_T3U7WtVoNEvf3osJbqnmdm8nvg-gco")
        print(response1, response2, response3, response4)
