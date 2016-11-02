import re


def test_expected_ufw_rules(Command, Sudo):
    ufw_expected_rules = [
      r"^.*22/tcp\s+ALLOW IN\s+Anywhere.*",
      r"^.*80/tcp\s+ALLOW IN\s+Anywhere",
      r"^.*443/tcp\s+ALLOW IN\s+Anywhere",
      r"^.*10000/udp\s+ALLOW IN\s+Anywhere",
    ]

    with Sudo():
        cmd = Command("ufw status numbered")

    assert "Status: active" in cmd.stdout

    for r in ufw_expected_rules:
        assert re.search(r, cmd.stdout, re.MULTILINE)


def test_ufw_service(Service):
    service = Service("ufw")
    assert service.is_running
    assert service.is_enabled
