from src.services.stats_service import send_stats_to_all_users


async def test_send_stats_to_all_users():
    data = await send_stats_to_all_users()
    assert isinstance(data, dict)
