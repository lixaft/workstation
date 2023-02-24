class workstation::tmux {

  file { '/Users/lixaft/.config/tmux/plugins':
    ensure  => 'directory',
    owner   => 'lixaft',
    group   => 'staff',
    mode    => '0755',
    require => File['/Users/lixaft/.config/tmux'],
  } ->
  vcsrepo { '/Users/lixaft/.config/tmux/plugins/tpm':
    ensure   => 'latest',
    provider => 'git',
    source   => 'https://github.com/tmux-plugins/tpm',
    user     => 'lixaft',
  }
}
