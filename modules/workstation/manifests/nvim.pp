class workstation::nvim {

  file { '/Users/lixaft/.local/share/nvim/lazy':
    ensure => 'directory',
    owner  => 'lixaft',
    group  => 'staff',
    mode   => '0755',
  } ->
  vcsrepo { '/Users/lixaft/.local/share/nvim/lazy/lazy.nvim':
    ensure   => 'latest',
    provider => 'git',
    source   => 'https://github.com/wbthomason/packer.nvim',
    user     => 'lixaft',
  }
}
