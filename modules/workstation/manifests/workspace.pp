class workstation::workspace {

  file { '/Users/lixaft/workspace':
    ensure => 'directory',
    owner  => 'lixaft',
    group  => 'staff',
    mode   => '0755',
  }

  $repositories = [
    'lixaft/dotfiles',
    'lixaft/workstation',
  ]

  $repositories.each |$repository| {
    $name = basename($repository)
    vcsrepo { "/Users/lixaft/workspace/${name}":
      ensure   => 'present',
      provider => 'git',
      user     => 'lixaft',
      source   => "git@github.com:${repository}",
      require  => File['/Users/lixaft/workspace'],
    }
  }

  vcsrepo { '/Users/lixaft/workspace/cpython':
    ensure   => 'present',
    provider => 'git',
    user     => 'lixaft',
    source   => {
      origin => 'git@github.com:python/cpython',
      lixaft => 'git@github.com:lixaft/cpython',
    },
    require  => File['/Users/lixaft/workspace'],
  }
}
