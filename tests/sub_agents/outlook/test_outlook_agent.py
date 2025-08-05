from misstea.sub_agents.outlook import agent


def test_get_outlook_account_authenticated():
    agent.get_outlook_account.cache_clear()
    agent.get_outlook_account()
