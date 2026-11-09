# Class: users
# Enforces existence and attributes of unprivileged system service accounts
class users (
  String  $app_user  = lookup('human_firewall::app_user', String, 'first', 'appuser'),
  String  $app_group = lookup('human_firewall::app_group', String, 'first', 'appgroup'),
  Integer $app_uid   = lookup('human_firewall::app_uid', Integer, 'first', 10001),
  Integer $app_gid   = lookup('human_firewall::app_gid', Integer, 'first', 10001)
) {
  group { $app_group:
    ensure => present,
    gid    => $app_gid,
  }

  user { $app_user:
    ensure     => present,
    uid        => $app_uid,
    gid        => $app_gid,
    shell      => '/sbin/nologin',
    home       => '/opt/human-firewall',
    managehome => false,
    require    => Group[$app_group],
  }
}

