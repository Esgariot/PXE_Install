# TODO: Write a parser and make this a .conf file or something #p3
lastCheckedDate = '03.01.17'
tftpRoot = '/svr/tftp/'
pxe_cfgPath = './pxeappend.cfg'
ks_cfgPath = './ks.cfg'
distroList = ['debian', 'fedora']
fedoraURL = (
    "https://download.fedoraproject.org/pub/fedora/linux/"
    "releases/25/Workstation/x86_64/iso/"
    "Fedora-Workstation-netinst-x86_64-25-1.3.iso")
debianURL = (
    "http://ftp.nl.debian.org/debian/dists/jessie/"
    "main/installer-amd64/current/images/netboot/"
    "netboot.tar.gz")
