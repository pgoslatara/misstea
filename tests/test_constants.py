from misstea.constants import MY_EMAIL_ADDRESS


def test_my_email_address():
    assert MY_EMAIL_ADDRESS is not None
    assert "@" in MY_EMAIL_ADDRESS
