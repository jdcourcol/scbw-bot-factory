# -*- coding: utf-8 -*-
#video memory size should be at least 32meg for windows 7 to do full screen on my desktop
# I'm not sure how to set that with veewee::session yet
Veewee::Session.declare({
    :os_type_id => 'Windows7_64',
    :iso_file => "",
    :iso_md5 => "",
    :iso_download_timeout => "100000",

    :cpu_count => '2',
    :memory_size=> '2048',
    #disk size is required because of VS express installation.
    :disk_size => '70560', :disk_format => 'VDI', :hostiocache => 'off',

    :floppy_files => [
      "Autounattend.xml",
      "install-winrm.bat",
      "oracle-cert.cer",
      "install-cygwin-sshd.bat"
    ],

    :ssh_login_timeout => "10000",
    # Actively attempt to winrm (no ssh on base windows) in for 10000 seconds
    :ssh_user => "vagrant", :ssh_password => "vagrant", :ssh_key => "",
    :ssh_host_port => "59857", :ssh_guest_port => "22",
    # And run postinstall.sh for up to 10000 seconds
    :postinstall_timeout => "10000",
    :postinstall_files => ["postinstall.sh"],
    # No sudo on windows
    :sudo_cmd => "sh '%f'",
    # Shutdown is different as well
    :shutdown_cmd => "shutdown /s /t 0 /c \"Vagrant Shutdown\" /f /d p:4:1",
  })
