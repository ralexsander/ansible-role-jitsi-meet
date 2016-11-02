

def test_base_packages(Package):
    packages = ['apt-transport-https', 'default-jre-headless']
    for package in packages:
        p = Package(package)
        assert p.is_installed


def test_apt_cache_policy_for_repo(Command):
    cmd = Command('apt-cache policy')
    jitsi_apt_repo_policy = "\n".join([
        " 500 https://download.jitsi.org/ stable/ Packages",
        "     release o=jitsi.org,a=stable,n=stable," +
        "l=Jitsi Debian packages repository,c=",
        "     origin download.jitsi.org"])
    assert jitsi_apt_repo_policy in cmd.stdout


def test_apt_repo_file(File):
    passwd = File("/etc/apt/sources.list.d/jitsi_meet.list")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644


def test_apt_fingerprint(Command, TestinfraBackend):
    cmd = Command("apt-key finger")
    jitsi_apt_key_stable = """pub   4096R/2DC1389C 2016-06-23
      Key fingerprint = 66A9 CD05 95D6 AFA2 4729  0D3B EF8B 479E 2DC1 389C
uid                  Jitsi <dev@jitsi.org>
sub   4096R/88D3172B 2016-06-23
"""

    jitsi_apt_key_unstable = """pub   1024D/EB0AB654 2008-06-20
      Key fingerprint = 040F 5760 8F84 BAF1 BF84  \
4A62 C697 D823 EB0A B654
uid                  SIP Communicator (Debian package) \
<deb-pkg@sip-communicator.org>
sub   2048g/F6EFCE13 2008-06-20"""
    hostname = TestinfraBackend.get_hostname()
    if hostname.endswith('unstable'):
        assert jitsi_apt_key_unstable in cmd.stdout
        assert jitsi_apt_key_stable not in cmd.stdout
    else:
        assert jitsi_apt_key_stable in cmd.stdout
        assert jitsi_apt_key_unstable not in cmd.stdout
