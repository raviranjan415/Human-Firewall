# Class: application
# Enforces Human Firewall service directory permissions and daemon lifecycle
class application (
  String $app_user  = lookup('human_firewall::app_user', String, 'first', 'appuser'),
  String $app_group = lookup('human_firewall::app_group', String, 'first', 'appgroup')
) {
  file { '/opt/human-firewall':
    ensure => directory,
    owner  => $app_user,
    group  => $app_group,
    mode   => '0750',
  }

  file { '/opt/human-firewall/instance':
    ensure  => directory,
    owner   => $app_user,
    group   => $app_group,
    mode    => '0750',
    require => File['/opt/human-firewall'],
  }

  service { 'human-firewall':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    hasstatus  => true,
  }
}

