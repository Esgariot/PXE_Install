# TODO: Write a parser and make this a .conf file or something #p3
lastCheckedDate = '03.01.17'
tftpRoot = '/svr/tftp/'
pxe_cfgPath = './pxeappend.cfg'
ks_cfgPath = './ks.cfg'
distroList = ['debian', 'fedora']
fedoraURL = (
    "http://ftp.icm.edu.pl/pub/Linux/fedora/"
    "linux/releases/25/Workstation/x86_64/os/images/pxeboot/*")  # doesnt work
debianURL = (
    "http://ftp.nl.debian.org/debian/dists/jessie/"
    "main/installer-amd64/current/images/netboot/"
    "netboot.tar.gz")
