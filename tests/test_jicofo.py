import re


def test_jicofo_config_file(File, Sudo):
    f = File('/etc/jitsi/jicofo/config')

    assert f.user == "root"
    assert f.is_file
    assert f.group == "root"
    assert f.mode == 0o644

    jicofo_configs = [
        r"^JICOFO_HOST=localhost$",
        r"^JICOFO_PORT=5347$",
        # The regex for the "secret" may be off. Tests have failed before
        # when matching only '\w', due to a '@', so adding that.
        r"^JICOFO_SECRET=[\w@]{8,}$",
        r"^JICOFO_AUTH_PASSWORD=\w{8,}$",
        r"^JICOFO_AUTH_USER=focus$",
    ]

    for c in jicofo_configs:
        assert re.search(c, f.content, re.MULTILINE)


def test_jicofo_logging_config_file(File, Sudo):
    f = File("/etc/jitsi/jicofo/logging.properties")
    assert f.user == "root"
    assert f.is_file
    assert f.group == "root"
    assert f.mode == 0o644

    assert re.search(r"^\.level=INFO$", f.content, re.MULTILINE)


def test_jicofo_service(Service):
    jicofo = Service("jicofo")
    assert jicofo.is_running
    assert jicofo.is_enabled


def test_jicofo_ports(Socket):
    jicofo_port = 5347
    assert Socket("tcp://127.0.0.1:{}".format(jicofo_port)).is_listening
    assert not Socket("tcp://0.0.0.0:{}".format(jicofo_port)).is_listening


def test_jicofo_ports_via_netstat(Command):
    jicofo_port = 5347
    cmd = Command("sudo netstat -nlt")
    assert "127.0.0.1:{}".format(jicofo_port) in cmd.stdout
    assert "0.0.0.0:{}".format(jicofo_port) not in cmd.stdout


def test_jicofo_service_user(Command):
    cmd = Command("pgrep -u jicofo | wc -l")
    assert cmd.stdout == "1"
