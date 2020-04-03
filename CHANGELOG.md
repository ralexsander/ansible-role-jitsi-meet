# Change Log

## [v2.0.0](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/tree/v2.0.0)

### Second version of the role, designed for Jitsi Meet v2.X

* Default Nginx web server, custom settings are maintained from a variable (`jitsi_meet_configure_nginx`).

* Now the installation of `jitsi-meet` from apt recommends the installation of a turnserver, a feature that can cause various problems with nginx configurations. Added `jitsi_meet_install_recommends` variable to influence this behavior.

* Using `present` instead `latest` when installing packages.

* Various improvements and simplifications of tasks that are no longer necessary.

## [v1.0.0](https://github.com/UdelaRInterior/ansible-role-jitsi-meet/tree/v1.0.0)

### First version of the role, designed for Jitsi Meet v1.X

* Jetty default web server, with option to install and configure Nginx from a variable.
