# Class: nginx
# Enforces Nginx installation, configuration compliance, and service availability
class nginx (
  Integer $worker_connections = lookup('nginx::worker_connections', Integer, 'first', 2048),
  String  $worker_processes   = lookup('nginx::worker_processes', String, 'first', 'auto')
) {
  package { 'nginx':
    ensure => installed,
  }

  file { '/etc/nginx/nginx.conf':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => template('nginx/nginx.conf.erb'),
    require => Package['nginx'],
    notify  => Service['nginx'],
  }

  service { 'nginx':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    hasstatus  => true,
    subscribe  => File['/etc/nginx/nginx.conf'],
  }
}

