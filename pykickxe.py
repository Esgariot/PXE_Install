import argparse
import pykickxe_conf
import os


def listConfig():  # TODO: Implement listConfig #p3
    return


def downloadFromURL(args):  # TODO: Implement download #p1
    distroURL = ''
    if 'debian' == args.distro:
        distroURL = pykickxe_conf.debianURL
    elif 'fedora' == args.distro:
        distroURL = pykickxe_conf.fedoraURL
    else:
        print args.distro + ' is not supported'
        return
    if args.verbose is True:
        print 'downloading ' + args.distro + ' from ' + distroURL
    # TODO: check if wget present #p2
    os.system('wget ' + distroURL)

    # urllib.urlretrieve(distroURL) # TODO: Decide on this or wget #p3
    # TODO: Check if file already present #p1
    # TODO: Check filesum #p2
    return  # fileName  # TODO: return filename from url #p1


def parseArgs():
    """Parser for cli arguements"""
    parser = argparse.ArgumentParser(
        prog='Pykickxe',
        description='A Python PXE and autoinstall tool')
    parser.add_argument(
        'distro',
        type=str,
        choices=pykickxe_conf.distroList,
        help='Pick a linux distro to download, unpack and append'
        'the PXE config to (Debian or Fedora for now)')
    parser.add_argument(
        '-l',
        '--list',
        help='List some default options',
        action='store_true')
    parser.add_argument(
        '-v',
        '--verbose',
        help='Print some of what this is doing at any moment',
        action='store_true')

    parser.add_argument(
        '-t',
        '--tftp_root',
        type=str,
        default=pykickxe_conf.tftpRoot,
        help='Pass an absolute path to tftp root directory')
    parser.add_argument(
        '--ks_cfg',
        type=str,
        default=pykickxe_conf.ks_cfgPath,
        help='Pass an absolute path to Kickstart file')
    parser.add_argument(
        '--pxe_cfg',
        type=str,
        default=pykickxe_conf.pxe_cfgPath,
        help='Pass an absolute path to pxe file with entry to append')
    args = parser.parse_args()
    return args


# pykickxe main
args = parseArgs()  # TODO: Add sensible options and check exclusivity #p3
if args.list is True:
    listConfig()
fileName = downloadFromURL(args)
# TODO: Restructure parser to make sense #p2
# parse_args() 

# assign to chosen distro
# assign to tftp-root location
# unpack() (iso or tar)


# modify using subprocess

# ISO_PATH = "your_iso_path_here"

# # Mount the ISO in your OS
# os.system("mkdir /media/tmp_iso")
# os.system("mount -o rw,loop %s /media/tmp_iso" % ISO_PATH)

# # Do your Pythonic manipulation here:
# new_file = open("/media/tmp_iso/.config", 'w')
# new_file.write(data)
# new_file.close()

# # Unmount
# os.system("umount /media/tmp_iso")
# os.system("rmdir /media/tmp_iso")
