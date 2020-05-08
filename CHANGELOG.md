# Change Log

## [v3.0.1](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/tree/v3.0.1)

Thanks to [@tabacha](https://github.com/tabacha):
  * Fixed the settings that were static in `templates/videobridge_sip-communicator.properties.j2` ([#13](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/pull/13))

## [v3.0.0](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/tree/v3.0.0)

* **`jitsi_meet_install_recommends: no` changed to `jitsi_meet_install_recommends: yes` on *defaults/main.yml*** (See [PR #5729](https://github.com/jitsi/jitsi-meet/pull/5729))
* **`jitsi_meet_configure_firewall: true` changed to `jitsi_meet_configure_firewall: false` on *defaults/main.yml***. To avoid overlapping with the rest of your roles/playbooks and lose SSH access. (This role focuses on configuring Jitsi Meet)
* Manage videobridge stats and colibri exposure over HTTPS
* Thanks to [@tabacha](https://github.com/tabacha):
    * `jitsi_meet_disable_third_party_requests` used correctly ([#10](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/pull/10))
    * UFW ports configurable from vars ([#11](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/pull/11))
      **Note that now enabling SSH port isn't part of the default behavior**
    * Manage Prosody authentication ([#12](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/pull/12))
* Thanks to [@fabiogermann](https://github.com/fabiogermann):
    * Settings to run behind a NAT firewall ([#7](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/pull/7))
* Added Ansible tags for each component in *tasks/main.yml*
* Various improvements in code quality

## [v2.0.0](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/tree/v2.0.0)

### Second version of the role, designed for Jitsi Meet v2.X

* Default Nginx web server, custom settings are maintained from a variable (`jitsi_meet_configure_nginx`).

* Now the installation of `jitsi-meet` from apt recommends the installation of a turnserver, a feature that can cause various problems with nginx configurations. Added `jitsi_meet_install_recommends` variable to influence this behavior.

* Using `present` instead `latest` when installing packages.

* Various improvements and simplifications of tasks that are no longer necessary.

## [v1.0.0](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/tree/v1.0.0)

### First version of the role, designed for Jitsi Meet v1.X

* Jetty default web server, with option to install and configure Nginx from a variable.
