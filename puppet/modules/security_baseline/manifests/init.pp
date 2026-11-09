# Class: security_baseline
# Enforces system hardening parameters, file permissions, and limits
# Central target for Configuration Drift Demonstration and Remediation
class security_baseline (
  Integer $tcp_syncookies = lookup('security_baseline::sysctl_tcp_syncookies', Integer, 'first', 1),
  Integer $ip_forward     = lookup('security_baseline::sysctl_ip_forward', Integer, 'first', 1),
  Integer $file_limits    = lookup('security_baseline::file_limits_nofile', Integer, 'first', 65535)
) {
  # 1. Enforce Kernel Security Parameters File
  file { '/etc/sysctl.d/99-human-firewall-security.conf':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => "# Managed by Puppet - Security Baseline\nnet.ipv4.tcp_syncookies = ${tcp_syncookies}\nnet.ipv4.ip_forward = ${ip_forward}\nnet.ipv4.conf.all.rp_filter = 1\nnet.ipv4.conf.default.rp_filter = 1\nnet.ipv4.conf.all.accept_redirects = 0\nfs.file-max = 2097152\n",
  }

  # 2. Enforce File Descriptor Limits
  file { '/etc/security/limits.d/99-human-firewall-limits.conf':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => "# Managed by Puppet - Baseline Resource Limits\n* soft nofile ${file_limits}\n* hard nofile ${file_limits}\nroot soft nofile ${file_limits}\nroot hard nofile ${file_limits}\n",
  }

  # 3. Enforce Permissions on System Identity Tables
  file { '/etc/shadow':
    ensure => file,
    owner  => 'root',
    group  => 'shadow',
    mode   => '0640',
  }

  file { '/etc/passwd':
    ensure => file,
    owner  => 'root',
    group  => 'root',
    mode   => '0644',
  }
}

