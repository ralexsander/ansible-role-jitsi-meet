jitsi-meet
=========

[![Galaxy](https://img.shields.io/badge/galaxy-ralexsander.jitsi__meet-blue.svg)](https://galaxy.ansible.com/ralexsander/jitsi_meet) ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/ralexsander/ansible-role-jitsi-meet?label=release&logo=github&style=social) ![GitHub stars](https://img.shields.io/github/stars/ralexsander/ansible-role-jitsi-meet?style=social) ![GitHub forks](https://img.shields.io/github/forks/ralexsander/ansible-role-jitsi-meet?style=social)

Installs and configures the [Jitsi Meet] videoconferencing software.


Requirements
------------

You should have DNS pointed at the server already, and SSL keys. If you don't have SSL keys for the domain yet, consider using the [geerlingguy.certbot] Ansible role to obtain (free!) SSL certs from [LetsEncrypt].

You will also need to expose ports 443 TCP and 10000 UDP for the Jitsi Meet components to work. This role can use `ufw` to allow these ports setting `jitsi_meet_configure_firewall: true`. If you use another host-based firewall solution such as iptables, keep `jitsi_meet_configure_firewall: false`. If you use AWS or similar, you'll need to expose those ports in the associated Security Group.

Role Variables
--------------

```yaml
########################################
###### most important variables ########
# and that you must adapt to your case #
########################################

# Without SSL, "localhost" is the correct default. If SSL info is provided,
# then we'll need a real domain name. Using Ansible's inferred FQDN, but you
# can set the variable value explicitly if you use a shorter hostname
# If automatic Nginx configuration is disabled, also use FQDN, since presumably
# another role will manage the vhost config.
jitsi_meet_server_name: "{{ ansible_fqdn | default('localhost') }}"

# Note from official documentation:
# The installer will check if Nginx or Apache is present (in that order) and configure
# a virtualhost within the web server it finds to serve Jitsi Meet. If none of the above
# is found it then defaults to Nginx. If you are already running Nginx on port 443 on
# the same machine you better skip the turnserver configuration as it will conflict with
# your current port 443, so use the command apt install --no-install-recommends jitsi-meet
jitsi_meet_install_recommends: yes

# If (jitsi_meet_install_recommends == no), there won't be turnserver installed and available
jitsi_meet_use_stun_turn: false

# The STUN servers that will be used in the peer to peer connections
jitsi_meet_stun_servers:
  - 'meet-jit-si-turnrelay.jitsi.net:443'
  # - '{{ jitsi_meet_server_name }}:443'

# Enable the p2p mode
jitsi_meet_enable_p2p_mode: true

# Configure nginx and jitsi-meet to listening also IPv6
jitsi_meet_ipv6_enable: true

# It allows you to specify the installation of jitsi meet creating and configuring
# self-signed HTTPS certificates, which can then be replaced by Let's Encrypt certificates
jitsi_meet_cert_choice: "Generate a new self-signed certificate (You will later get a chance to obtain a Let's encrypt certificate)"
# Due to the behavior of the Jitsi installer scripts, it is recommended to keep this value, even if you
# plan to use your own generated certificates (for example). with certbot. You can do it from this role

# NOT setting them here, because empty strings for custom certs will
# cause the custom Nginx config tasks to be skipped.
jitsi_meet_ssl_cert_path: ''
jitsi_meet_ssl_key_path: ''

# Enables calendar on Jitsi homepage, when its enabled you should
# configure the Google API Key or Microsoft API Key or both.
jitsi_meet_calendar_integration: false

# Google API for Calendar Integration
# If you dont know how to adquire the API Key follow the link below:
# https://github.com/jitsi/jitsi-meet/blob/master/doc/integrations.md#creating-the-google-api-client-for-google-calendar-and-youtube-integration
jitsi_meet_google_api_client_id: ''

# Microsoft API for Calendar Integration
# If you dont know how to adquire the API Key follow the link below:
# https://github.com/jitsi/jitsi-meet/blob/master/doc/integrations.md#creating-the-microsoft-app-for-microsoft-outlook-integration
jitsi_meet_ms_api_client_id: ''

#############
### NGINX ###
# This role will automatically configure a nginx vhost for use with jitsi-meet.
# If you prefer to manage web vhosts via a separate role, set this to false.
jitsi_meet_configure_nginx: true

# If you wish, you can use your own jitsi_meet_nginx.conf.j2 template indicating another path
jitsi_meet_nginx_config_template:  "jitsi_meet_nginx.conf.j2"


###########################################
# other useful variables to customize the #
# installation, but less frequently used  #
###########################################

# The Debian package installation of jitsi-meet will generate secrets for the components.
# The role will read the config file and preserve the secrets even while templating.
# If you wish to generate your own secrets and use those, override these vars, but make
# sure to store the secrets securely, e.g. with ansible-vault or credstash.
jitsi_meet_videobridge_secret: ''
jitsi_meet_jicofo_secret: ''
jitsi_meet_jicofo_password: ''

##################
### APT things ###
# List of packages that need to be installed before jitsi meet
jitsi_meet_base_packages:
  - apt-transport-https
  - debconf
  - debconf-utils

# Whether to use nightly builds of the Jitsi Meet components.
jitsi_meet_use_nightly_apt_repo: false

jitsi_meet_apt_repos:
  stable:
    repo_url: 'deb https://download.jitsi.org/ stable/'
  unstable:
    repo_url: 'deb https://download.jitsi.org unstable/'

jitsi_meet_apt_key_url: 'https://download.jitsi.org/jitsi-key.gpg.key'
jitsi_meet_apt_key_id: '66A9CD0595D6AFA247290D3BEF8B479E2DC1389C'

# These debconf settings represent answers to interactive prompts during installation
# of the jitsi-meet deb package. If you use custom SSL certs, you may have to set more options.
jitsi_meet_debconf_settings:
  - name: jitsi-meet
    question: jitsi-meet/jvb-serve
    value: "false"
    vtype: boolean
  - name: jitsi-meet-prosody
    question: jitsi-meet-prosody/jvb-hostname
    value: "{{ jitsi_meet_server_name }}"
    vtype: string
  - name: jitsi-videobridge
    question: jitsi-videobridge/jvb-hostname
    value: "{{ jitsi_meet_server_name }}"
    vtype: string
  - name: jitsi-meet-web-config
    question: jitsi-meet/cert-choice
    value: "{{ jitsi_meet_cert_choice }}"
    vtype: select
  - name: jitsi-meet-web-config
    question: jitsi-meet/cert-path-key
    value: "{{ jitsi_meet_ssl_key_path }}"
    vtype: string
  - name: jitsi-meet-web-config
    question: jitsi-meet/cert-path-crt
    value: "{{ jitsi_meet_ssl_cert_path }}"
    vtype: string


#######################
### Server firewall ###
# This role can automatically install and configure ufw with jitsi-meet port holes setting this variable in true.
# If you're managing a firewall elsewise, keep in false, and ufw tasks will be skipped.
jitsi_meet_configure_firewall: false

# WARNING: until v2.0.0 of this role, also SSH port (22/tcp) was enabled.
# This role focuses on configuring Jitsi Meet, so to avoid overlapping with the rest of
# your roles/playbooks, the default values will be only the necessary ports for Jitsi
jitsi_meet_firewall_ports_allow:
  tcp:
    # - "22" # SSH
    - "80"   # HTTP / Lets Encrypt
    - "443"  # HTTPS
  udp:
    - "10000" # Videobridge

### Other firewall
# This will configure NATed connection to Jitsi Meet
jitsi_meet_behind_nat_firewall: false
jitsi_meet_nat_private_ip: 127.0.0.1
jitsi_meet_nat_public_ip: 255.255.255.255


##############
### Jicofo ###
# Default auth information, used in multiple service templates.
jitsi_meet_jicofo_user: focus
jitsi_meet_jicofo_port: 5347
# The Jitsi components use the standard Java log levels, see:
# https://docs.oracle.com/javase/7/docs/api/java/util/logging/Level.html
# When using log aggregation for jitsi-meet components, set to "WARNING".
jitsi_meet_jicofo_loglevel: INFO

# If you wish, you can use your own jinja config template indicating another path
jitsi_meet_jicofo_config_template: jicofo_config.j2
jitsi_meet_jicofo_sip_template: jicofo_sip-communicator.properties.j2


###################
### Videobridge ###
# The default config file at /etc/jitsi/videobridge/config claims the default port
# for JVB is "5275", but the manual install guide references "5347".
# https://github.com/jitsi/jitsi-meet/blob/master/doc/manual-install.md
jitsi_meet_videobridge_port: 5347
jitsi_meet_videobridge_loglevel: INFO
jitsi_meet_videobridge_opts: '--apis=,'            # comma separated list '--apis=rest,'

jitsi_meet_videobridge_statistics_enable: true
jitsi_meet_videobridge_statistics_interval: 1000
jitsi_meet_videobridge_statistics_transport: 'muc' # comma separated list: 'muc,colibri,xmpp'

# Configure reverse proxy to publish colibri/stats over HTTPS
# https://{{ jitsi_meet_server_name }}/colibri/stats
# YOU SHOULD ALSO ENABLE 'rest' in jitsi_meet_videobridge_opts and
# 'colibri,xmpp' in jitsi_meet_videobridge_statistics_transport
jitsi_meet_expose_colibri_stats: false

# (Dictionary type) Other servers credentials to enable the MUC (Multi User Chat) mode.
# https://github.com/jitsi/jitsi-videobridge/blob/master/doc/muc.md#legacy-videobridge-configuration
jitsi_meet_videobridge_other_xmpp_servers: {}
  # xmppserver1:
  #   hostname: example.net
  #   domain: auth.example.net
  #   username: jvb
  #   password: $PASSWORD
  #   muc_jids: JvbBrewery@internal.auth.example.net
  #   muc: JvbBrewery@internal.auth.boris2.jitsi.net
  #   muc_nickname: unique-instance-id
  #   # disable_certificate_verification: true

# If you wish, you can use your own jinja config template indicating another path
jitsi_meet_videobridge_config_template:  videobridge_config.j2
jitsi_meet_videobridge_sip_template: videobridge_sip-communicator.properties.j2

############
### Meet ###
# "anonymous" lets anyone use the videoconference server.
jitsi_meet_authentication: anonymous

# Privacy-friendly addition, see here for details:
# https://github.com/jitsi/jitsi-meet/issues/422
# https://github.com/jitsi/jitsi-meet/pull/427
jitsi_meet_enable_third_party_requests: true

# Screensharing config for Chrome. You'll need to build and package a browser
# extension specifically for your domain; see https://github.com/jitsi/jidesha
jitsi_meet_desktop_sharing_chrome_method: 'ext'
jitsi_meet_enable_desktop_sharing_chrome: true
jitsi_meet_desktop_sharing_chrome_ext_id: 'diibjkoicjeejcmhdnailmkgecihlobk'

# Path to local extension on disk, for copying to target host. The remote filename
# will be the basename of the path provided here.
jitsi_meet_desktop_sharing_chrome_extension_filename: ''

# Screensharing config for Firefox. Set max_version to '42' and disabled to 'false'
# if you want to use screensharing under Firefox.
jitsi_meet_desktop_sharing_firefox_ext_id: 'null'
jitsi_meet_enable_desktop_sharing_firefox: true
jitsi_meet_desktop_sharing_firefox_max_version_ext_required: '-1'

jitsi_meet_channel_last_n: -1
jitsi_meet_enable_layer_suspension: false
jitsi_meet_start_audio_only: false
jitsi_meet_show_audio_levels: false
jitsi_meet_audio_levels_interval: 200

jitsi_meet_resolution: 480
jitsi_meet_constraints_video_aspect_ratio: "16 / 9"
jitsi_meet_constraints_video_height_ideal: "{{ jitsi_meet_resolution }}"
jitsi_meet_constraints_video_height_max: 720
jitsi_meet_constraints_video_height_min: 240

# If you wish, you can use your own jinja config template indicating another path
jitsi_meet_config_js_template: jitsi_meet_config.js.j2
jitsi_meet_interface_config_js_template: interface_config.js.j2

###################
### SIP gateway ###
jitsi_meet_configure_sip_gateway: false
jitsi_meet_jigasi_account: sipnumber@sip-provider.name
jitsi_meet_jigasi_password: fdi49fndKjhe3

########################
### UI customization ###
jitsi_meet_customize_the_ui: false

jitsi_meet_lang: 'en'
jitsi_meet_appname: 'My app name'
jitsi_meet_org_link: 'https://link-to-my-organization.com'
jitsi_meet_welcomepage_title: 'Secure, fully featured, and completely free video conferencing'
jitsi_meet_welcomepage_description: 'Go ahead, video chat with the whole team. In fact, invite everyone you know. __app__ is a fully encrypted, 100% open source video conferencing solution that you can use all day, every day, for free — with no account needed.'

# By default it is an empty string because the CSS file is a bundled file for
# the entire site, and it change very frequently with each release. It will be
# replaced only if you have a custom CSS file and indicate its path in this variable
jitsi_meet_css_file: ''
jitsi_meet_welcome_page_additions_file: welcomePageAdditionalContent.html.j2
jitsi_meet_title_template: title.html.j2

jitsi_meet_favicon_file: images/favicon.ico
jitsi_meet_logo_file: images/jitsilogo.png
jitsi_meet_watermark_file: images/watermark.png

jitsi_meet_default_background: '#474747'
jitsi_meet_show_video_background: true
jitsi_meet_default_remote_display_name: 'Fellow Jitster'
jitsi_meet_default_local_display_name: 'me'
jitsi_meet_generate_roomnames_on_welcome_page: true
jitsi_meet_lang_detection: false    # Allow i18n to detect the system language

jitsi_meet_download_link_android: 'https://play.google.com/store/apps/details?id=org.jitsi.meet'
jitsi_meet_download_link_ios: 'https://itunes.apple.com/us/app/jitsi-meet/id1165103905'
jitsi_meet_android_app_scheme: 'org.jitsi.meet'
jitsi_meet_android_app_package: 'org.jitsi.meet'
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

    - role: ralexsander.jitsi_meet
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
