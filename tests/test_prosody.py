import re


def test_prosody_config_file(File):
    f = File("/etc/prosody/conf.avail/localhost.cfg.lua")
    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644

    wanted_prosody_config_regexes = [
        r'^VirtualHost "localhost"$\s+authentication = "anonymous"',
        # Not using these vars to build regex, but documenting anyway
        # wanted_enabled_modules = ['bosh', 'pubsub', 'ping']
        r'^\s+modules_enabled = \{$\s+"bosh";\s+"pubsub";\s+"ping";\s+\}$',
        r'^VirtualHost "auth.localhost"$\s+authentication = "internal_plain"',
    ]
    for r in wanted_prosody_config_regexes:
        assert re.search(r, f.content, re.MULTILINE)

    wanted_config_line_pairs = {
        'VirtualHost "auth.localhost"': 'authentication = "internal_plain"',
        'Component "conference.localhost" "muc"':
            'admins = { "focus@auth.localhost" }',
        'Component "jitsi-videobridge.localhost"': 'component_secret = ',
        'Component "focus.localhost"': 'component_secret = ',
    }

    for setting, value in wanted_config_line_pairs.iteritems():
        assert re.search(r'^'+setting+r'$\s+'+value, f.content, re.MULTILINE)


def test_prosody_config_file_syntax(Command):
    cmd = Command('luac -p /etc/prosody/conf.avail/localhost.cfg.lua')
    assert cmd.rc == 0


def test_prosody_auth_directory(File):
    f = File("/var/lib/prosody/auth%2elocalhost")
    assert f.is_directory
    assert f.user == "prosody"
    assert f.group == "prosody"
    assert f.mode == 0o750


def test_prosody_auth_file(File):
    f = File("/var/lib/prosody/auth%2elocalhost/accounts/focus.dat")
    assert f.is_file
    assert f.user == "prosody"
    assert f.group == "prosody"
    assert f.mode == 0o640
    assert re.search(r'^\s+\["password"\] = "\w+";$', f.content, re.MULTILINE)
