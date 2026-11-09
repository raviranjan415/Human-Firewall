# Class: firewall
# Enforces UFW host firewall execution and basic state
class firewall {
  package { 'ufw':
    ensure => installed,
  }

  service { 'ufw':
    ensure  => running,
    enable  => true,
    require => Package['ufw'],
  }

  exec { 'ufw-default-deny-incoming':
    command => '/usr/sbin/ufw default deny incoming',
    unless  => '/usr/sbin/ufw status verbose | grep -q "Default: deny (incoming)"',
    require => Service['ufw'],
  }

  exec { 'ufw-default-allow-outgoing':
    command => '/usr/sbin/ufw default allow outgoing',
    unless  => '/usr/sbin/ufw status verbose | grep -q "Default: allow (outgoing)"',
    require => Service['ufw'],
  }
}

