# Class: ssh
# Enforces SSH hardening configuration and daemon execution state
class ssh (
  Integer $port                   = lookup('ssh::port', Integer, 'first', 22),
  String  $permit_root_login      = lookup('ssh::permit_root_login', String, 'first', 'no'),
  String  $password_authentication = lookup('ssh::password_authentication', String, 'first', 'no'),
  Integer $client_alive_interval  = lookup('ssh::client_alive_interval', Integer, 'first', 300),
  Integer $client_alive_count_max = lookup('ssh::client_alive_count_max', Integer, 'first', 2)
) {
  package { 'openssh-server':
    ensure => installed,
  }

  file { '/etc/ssh/sshd_config':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0600',
    content => template('ssh/sshd_config.erb'),
    require => Package['openssh-server'],
    notify  => Service['ssh'],
  }

  service { 'ssh':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    hasstatus  => true,
    subscribe  => File['/etc/ssh/sshd_config'],
  }
}

