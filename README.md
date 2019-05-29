jitsi-meet
=========

Installs and configures the [Jitsi Meet] videoconferencing software.


Requirements
------------

You should have DNS pointed at the server already, and SSL keys. If you don't have SSL
keys for the domain yet, consider using the [geerlingguy.certbot] Ansible role
to obtain (free!) SSL certs from [LetsEncrypt].

You will also need to expose ports 443 TCP and 10000 UDP for the Jitsi Meet
components to work. By default the role will use `ufw` to allow these ports. If you
use another host-based firewall solution such as iptables, set
`jitsi_meet_configure_firewall: false`. If you use AWS or similar, you'll need to
expose those ports in the associated Security Group.

Role Variables
--------------

```yaml
# It allows you to specify the installation of jitsi meet creating and configuring
# self-signed HTTPS certificates, which can then be replaced by Let's Encrypt certificates
jitsi_meet_cert_choice: "Generate a new self-signed certificate (You will later get a chance to obtain a Let's encrypt certificate)"

# Without SSL, "localhost" is the correct default. If SSL info is provided,
# then we'll need a real domain name. Using Ansible's inferred FQDN, but you
# can set the variable value explicitly if you use a shorter hostname
# If automatic Nginx configuration is disabled, also use FQDN, since presumably
# another role will manage the vhost config.
jitsi_meet_server_name: "{{ inventory_hostname if (jitsi_meet_configure_nginx) else ansible_fqdn if (not jitsi_meet_configure_nginx) else 'localhost' }}"

# The default cert files are /var/lib/prosody/localhost.{crt,key}
# NOT setting them here, because empty strings for custom certs will
# cause the custom Nginx config tasks to be skipped.
jitsi_meet_ssl_cert_path: ''
jitsi_meet_ssl_key_path: ''

# List of packages that need to be installed before jitsi meet
jitsi_meet_base_packages:
  - apt-transport-https
  - default-jre-headless
  - debconf
  - debconf-utils

# Only "anonymous" auth is supported, which lets anyone use the videoconference server.
jitsi_meet_authentication: anonymous

# Whether to use nightly builds of the Jitsi Meet components.
jitsi_meet_use_nightly_apt_repo: false

jitsi_meet_apt_repos:
  stable:
    repo_url: 'deb https://download.jitsi.org/ stable/'
  unstable:
    repo_url: 'deb https://download.jitsi.org unstable/'

jitsi_meet_apt_key_url: 'https://download.jitsi.org/jitsi-key.gpg.key'
jitsi_meet_apt_key_id: '66A9CD0595D6AFA247290D3BEF8B479E2DC1389C'

# The Debian package installation of jitsi-meet will generate secrets for the components.
# The role will read the config file and preserve the secrets even while templating.
# If you wish to generate your own secrets and use those, override these vars, but make
# sure to store the secrets securely, e.g. with ansible-vault or credstash.
jitsi_meet_videobridge_secret: ''
jitsi_meet_jicofo_secret: ''
jitsi_meet_jicofo_password: ''

# Default auth information, used in multiple service templates.
jitsi_meet_jicofo_user: focus
jitsi_meet_jicofo_port: 5347

# The Jitsi components use the standard Java log levels, see:
# https://docs.oracle.com/javase/7/docs/api/java/util/logging/Level.html
# When using log aggregation for jitsi-meet components, set to "WARNING".
jitsi_meet_jicofo_loglevel: INFO
# The default config file at /etc/jitsi/videobridge/config claims the default port
# for JVB is "5275", but the manual install guide references "5347".
# https://github.com/jitsi/jitsi-meet/blob/master/doc/manual-install.md
jitsi_meet_videobridge_port: 5347

jitsi_meet_videobridge_loglevel: INFO
# A recent privacy-friendly addition, see here for details:
# https://github.com/jitsi/jitsi-meet/issues/422
# https://github.com/jitsi/jitsi-meet/pull/427
jitsi_meet_disable_third_party_requests: true

# Screensharing config for Chrome. You'll need to build and package a browser
# extension specifically for your domain; see https://github.com/jitsi/jidesha
jitsi_meet_desktop_sharing_chrome_method: 'ext'
jitsi_meet_desktop_sharing_chrome_disabled: 'false'
jitsi_meet_desktop_sharing_chrome_ext_id: 'diibjkoicjeejcmhdnailmkgecihlobk'

# Path to local extension on disk, for copying to target host. The remote filename
# will be the basename of the path provided here.
jitsi_meet_desktop_sharing_chrome_extension_filename: ''

# Screensharing config for Firefox. Set max_version to '42' and disabled to 'false'
# if you want to use screensharing under Firefox.
jitsi_meet_desktop_sharing_firefox_ext_id: 'null'
jitsi_meet_desktop_sharing_firefox_disabled: 'false'
jitsi_meet_desktop_sharing_firefox_max_version_ext_required: '-1'

# These debconf settings represent answers to interactive prompts during installation
# of the jitsi-meet deb package. If you use custom SSL certs, you may have to set more options.
jitsi_meet_debconf_settings:
  - name: jitsi-meet
    question: jitsi-meet/cert-choice
    value: "{{ jitsi_meet_cert_choice }}"
    vtype: string
  - name: jitsi-meet
    question: jitsi-meet/jvb-serve
    value: "true"
    vtype: boolean
  - name: jitsi-meet-prosody
    question: jitsi-meet-prosody/jvb-hostname
    value: "{{ jitsi_meet_server_name }}"
    vtype: string
  - name: jitsi-videobridge
    question: jitsi-videobridge/jvb-hostname
    value: "{{ jitsi_meet_server_name }}"
    vtype: string

# Role will automatically install configure ufw with jitsi-meet port holes.
# If you're managing a firewall elsewise, set this to false, and ufw will be skipped.
jitsi_meet_configure_firewall: true

# Role will automatically install nginx and configure a vhost for use with jitsi-meet.
# If you prefer to manage web vhosts via a separate role, set this to false.
jitsi_meet_configure_nginx: true


# UI customization
jitsi_meet_customize_the_ui: false

jitsi_meet_lang: 'en'
jitsi_meet_appname: 'My app name'
jitsi_meet_org_link: 'https://link-to-my-organization.com'
jitsi_meet_welcomepage_title: 'Secure, fully featured, and completely free video conferencing'
jitsi_meet_welcomepage_description: 'Go ahead, video chat with the whole team. In fact, invite everyone you know. __app__ is a fully encrypted, 100% open source video conferencing solution that you can use all day, every day, for free — with no account needed.'
jitsi_meet_welcomepage_enterRoom: 'Start a new meeting'
jitsi_meet_welcomepage_recentListEmpty: 'Your recent list is currently empty. Chat with your team and you will find all your recent meetings here.'
jitsi_meet_default_background: '#474747'
jitsi_meet_disable_video_background: 'false'
jitsi_meet_default_remote_display_name: 'Fellow Jitster'
jitsi_meet_default_local_display_name: 'me'
jitsi_meet_generate_roomnames_on_welcome_page: 'true'
jitsi_meet_lang_detection: 'false'    # Allow i18n to detect the system language
jitsi_meet_favicon_file: images/favicon.ico
jitsi_meet_logo_file: images/jitsilogo.png
jitsi_meet_watermark_file: images/watermark.png
```

Screen sharing
--------------
Jitsi Meet supports screen sharing functionality via browser extensions.
Only the party sharing the screen needs the extension installed—other participants
in the meeting will be able to view the shared screen without installing anything.
You'll need to build your own browser extension for Chrome and/or Firefox.
See the [Jidesha] documentation for detailed build instructions. This role
has only been tested with custom Chrome extensions.

Chrome forbids installation of extensions from unapproved websites, so you must
download the `.crx` file directly, then navigate to `chrome://extensions` and
drag-and-drop the extension to install it. If you want to grant another
participant screen-sharing support, share the URL for the extension with them
via the Jitsi Meet text chat pane.

Dependencies
------------

It's technically not a dependency, but you should check out [geerlingguy.certbot]
for astoundingly easy SSL certs.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- name: Configure jitsi-meet server.
  hosts: jitsi
  vars:
    # Change this to match the DNS entry for your host IP.
    jitsi_meet_server_name: meet.example.com
  roles:
    - role: geerlingguy.certbot
      become: yes
      certbot_create_if_missing: true
      certbot_admin_email: "webmaster@{{ jitsi_meet_server_name }}"
      certbot_certs:
        - domains:
            - "{{ jitsi_meet_server_name }}"
      certbot_create_standalone_stop_services: []

    - role: ansible-role-jitsi-meet
      jitsi_meet_ssl_cert_path: "/etc/letsencrypt/live/{{ jitsi_meet_server_name }}/fullchain.pem"
      jitsi_meet_ssl_key_path: "/etc/letsencrypt/live/{{ jitsi_meet_server_name }}/privkey.pem"
      become: yes
      tags: jitsi
```


Running the tests
-----------------

This role uses [Molecule] and [ServerSpec] for testing. To use it:

```
pip install molecule
gem install serverspec
molecule test
```

You can also run selective commands:

```
molecule idempotence
molecule verify
```

See the [Molecule] docs for more info.

License
-------

MIT

Author Information
------------------

[Freedom of the Press Foundation], [UdelaR Interior], [@santiagomr]

[Jitsi Meet]: https://github.com/jitsi/jitsi-meet
[LetsEncrypt]: https://letsencrypt.org/
[geerlingguy.certbot]: https://galaxy.ansible.com/geerlingguy/certbot
[Freedom of the Press Foundation]: https://freedom.press/
[UdelaR Interior]: https://github.com/UdelaRInterior
[@santiagomr]: https://github.com/santiagomr
[Molecule]: http://molecule.readthedocs.org/en/master/
[ServerSpec]: http://serverspec.org/
[Jidesha]: https://github.com/jitsi/jidesha
