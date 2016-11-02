import re

# This is actually the port for the "jicofo" service; the jitsi-meet manual
# install docs aren't explicit about default ports. FWIW, the config file
# for jvb says that the default port is "5275", but I suspect that's old info.
jvb_service_port = 5347


def test_jitsi_videobridge_config(File):
    f = File('/etc/jitsi/videobridge/config')
    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644

    assert re.search(r'^JVB_HOSTNAME=localhost$', f.content, re.MULTILINE)
    assert re.search(r'^JVB_HOST=$', f.content, re.MULTILINE)
    assert re.search(r'^JVB_PORT='+str(jvb_service_port)+r'$',
                     f.content, re.MULTILINE)
    # It may be necessary to expand the regex for matching secrets.
    # See the jicofo tests for comparison.
    assert re.search(r'^JVB_SECRET=\w{8,}$', f.content, re.MULTILINE)


def test_jitsi_videobridge_logging_config(File):
    f = File('/etc/jitsi/videobridge/logging.properties')
    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644
    assert re.search(r'^\.level=INFO$', f.content, re.MULTILINE)


def test_jitsi_videobridge_service(Service):
    videobridge = Service("jitsi-videobridge")
    assert videobridge.is_running
    assert videobridge.is_enabled


def test_jitsi_videobridge_ports(Socket):
    assert Socket("tcp://127.0.0.1:{}".format(jvb_service_port)).is_listening
    assert not Socket("tcp://0.0.0.0:{}".format(jvb_service_port)).is_listening


def test_jitsi_videobridge_ports_via_netstat(Command):
    cmd = Command("sudo netstat -nlt")
    assert "127.0.0.1:{}".format(jvb_service_port) in cmd.stdout
    assert "0.0.0.0:{}".format(jvb_service_port) not in cmd.stdout


def test_jitsi_videobridge_service_user(Command):
    cmd = Command("pgrep -u jicofo | wc -l")
    assert cmd.stdout == "1"
