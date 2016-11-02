def test_base_packages(Package):
    pkgs = ['jitsi-meet', 'default-jre-headless']
    for p in pkgs:
        assert Package(p).is_installed


def test_debconf_settings(Command):
    expected_settings = {
        "jitsi-meet/jvb-hostname": "0 localhost",
        "jitsi-meet/jvb-serve": "0 false",
        "jitsi-meet-prosody/jvb-hostname": "0 localhost",
    }
    for debconf_setting, debconf_value in expected_settings.iteritems():
        cmd_fmt = "echo 'get {}' | debconf-communicate".format(debconf_setting)
        cmd = Command(cmd_fmt)
        assert debconf_value in cmd.stdout


def test_jitsi_meet_config_file(File):

    f = File('/etc/jitsi/meet/localhost-config.js')
    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644

    wanted_configs = [
       "domain: 'localhost',",
       "muc: 'conference.localhost',",
       "bridge: 'jitsi-videobridge.localhost',",
       "bosh: '//localhost/http-bind',",
       "disableThirdPartyRequests: true,",
    ]
    for c in wanted_configs:
        assert f.contains(c)
