# Class: packages
# Enforces installation and state of foundational system utilities
class packages (
  Array[String] $base_list = lookup('packages::base_list', Array[String], 'first', ['curl', 'wget', 'git', 'htop', 'jq', 'ca-certificates', 'ufw'])
) {
  package { $base_list:
    ensure => installed,
  }
}

