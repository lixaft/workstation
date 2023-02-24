class workstation::dotfiles {

  $links = [
    '.config/bat',
    '.config/fish',
    '.config/nvim',
    '.config/starship.toml',
    '.config/tmux',
    '.gitconfig',
    '.pdbrc',
    '.pythonrc',
  ]

  $links.each |$link| {
    file { "/Users/lixaft/${link}":
      ensure  => 'link',
      owner   => 'lixaft',
      group   => 'staff',
      target  => "/Users/lixaft/workspace/dotfiles/src/${link}",
      require => Vcsrepo['/Users/lixaft/workspace/dotfiles'],
    }
  }
}
