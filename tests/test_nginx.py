def test_nginx_package(Package):
    pkg = Package("nginx")
    assert pkg.is_installed
    assert pkg.version.startswith('1.6.2-5')


def test_nginx_localhost_config(File):
    f = File("/etc/nginx/sites-available/localhost.conf")
    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644

    ssl_config_strings = [
      "ssl_certificate /var/lib/prosody/localhost.crt;",
      "ssl_certificate_key /var/lib/prosody/localhost.key;"
    ]
    for s in ssl_config_strings:
        assert f.contains(s)


def test_nginx_service(Service, Socket):
    service = Service("nginx")
    assert service.is_running
    assert service.is_enabled


def test_nginx_ports(Socket):
    nginx_ports = [80, 443]
    for p in nginx_ports:
        assert Socket("tcp://0.0.0.0:{}".format(p)).is_listening
        assert not Socket("tcp://127.0.0.1:{}".format(p)).is_listening


def test_nginx_worker_count(Command):
    cmd = Command('pgrep -u www-data | wc -l')
    assert cmd.stdout == "4"


def test_nginx_ports_via_netstat(Command):
    cmd = Command('sudo netstat -nlt')
    nginx_ports = [80, 443]
    for p in nginx_ports:
        assert "0.0.0.0:{}".format(p) in cmd.stdout
        assert "127.0.0.1:{}".format(p) not in cmd.stdout
