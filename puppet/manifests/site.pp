# ==============================================================================
# Human Firewall — Puppet Master Manifest (site.pp)
# INT333 DevOps Advanced Configuration Management
# ==============================================================================

# Global Default Node Definition
node default {
  include packages
  include users
  include ssh
  include firewall
  include security_baseline
  include monitoring
}

# Edge Load Balancer Nodes
node /^.*lb.*$/ inherits default {
  include nginx
}

# Flask Application Replica Nodes
node /^.*replica.*$/ inherits default {
  include application
}

# Database & Cache Persistence Nodes
node /^.*db.*$/ inherits default {
  # Database specific configuration baseline
  file { '/var/lib/postgresql/data':
    ensure => directory,
    owner  => 'postgres',
    group  => 'postgres',
    mode   => '0700',
  }
}

