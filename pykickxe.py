import argparse
import os
import ConfigParser


def listConfig():  # TODO: Implement listConfig #p3
    return


def downloadFromURL(args, config):  # TODO: Implement download #p1
    # TODO: check if wget present #p2
    distroURL = config.get(args.distro, 'url', 1)
    os.system('wget ' + distroURL)
    filePath = os.path.split(distroURL)
    # urllib.urlretrieve(distroURL) # TODO: Decide on this or wget #p3
    # TODO: Check if file already present #p1
    # TODO: Check filesum #p2
    return filePath


def copyFiles(args, config):
    os.system('rsync --progress -av ./tftproot/* ' + args.tftp_root)


def replaceLine(filePath, srcText, destText):
    workingFile = open(filePath, 'r+')
    original = workingFile.read()
    modified = original.replace(srcText, destText)
    workingFile.seek(0)
    workingFile.write(modified)
    workingFile.close()
    return


def writeToMenu(args, config):
    menuPath = './tftproot/pxelinux.cfg/'
    # menuFile = open(menuPath + 'autoinstall.menu.source', 'r')
    # targetMenuFile = open(menuPath + 'autoinstall.menu', 'w')
    autoconfig_file = config.get(args.distro, 'auto_file', 0)
    if args.auto_cfg is not None:
        autoconfig_file = args.auto_cfg
        os.system('cp ' + autoconfig_file + ' ./tftproot/util/auto.cfg')
        autoconfig_file = '/util/auto.cfg'
    menuIn = menuPath + 'autoinstall.menu.source'
    menuOut = menuPath + 'autoinstall.menu'
    os.system('cp ' + menuIn + ' ' + menuOut)
    replaceLine(
        menuOut,
        '$DISTRO_NAME',
        config.get(args.distro, 'name', 0))
    replaceLine(
        menuOut,
        '$KERNEL',
        config.get(args.distro, 'kernel', 0))
    replaceLine(
        menuOut,
        '$APPEND',
        config.get(args.distro, 'append', 0))
    replaceLine(
        menuOut,
        '$KS',
        config.get(args.distro, 'auto_param', 0) + autoconfig_file)
    return


def parseArgs(configFIle):
    """Parser for cli arguements"""
    config = ConfigParser.SafeConfigParser()
    config.read(configFile)
    parser = argparse.ArgumentParser(
        prog='Pykickxe',
        description='a Python PXE and autoinstall tool',
        epilog=config.get('DEFAULT', 'help_text', 1))
    parser.add_argument(
        'distro',
        type=str,
        choices=config.sections(),
        help='pick a linux distro to download, unpack and append '
        'the PXE config to (Debian or Fedora for now)')
    parser.add_argument(
        '-l',
        '--list',
        help='list some default options',
        action='store_true')
    parser.add_argument(
        '-d',
        '--download',
        help='Download (not really working)',
        action='store_true')
    parser.add_argument(
        '-v',
        '--verbose (also not really working)',
        help='print some of what this is doing at any moment',
        action='store_true')
    parser.add_argument(
        '-t',
        '--tftp_root',
        type=str,
        default=config.get('DEFAULT', 'ftp_root', 0),
        help='pass an absolute path to tftp root directory')
    parser.add_argument(
        '--auto_cfg',
        type=str,
        help='pass an absolute path to Kickstart file')
    # parser.add_argument(
    #     '--pxe_cfg',
    #     type=str,
    #     default=pykickxe_conf.pxe_cfgPath,
    #     help='pass an absolute path to pxe file with entry to append')
    args = parser.parse_args()
    return args, config


# pykickxe main
if __name__ == "__main__":
    configFile = 'pykickxe.conf'
    # TODO: Add sensible options and check exclusivity #p3
    args, config = parseArgs(configFile)
    if args.list is True:
        listConfig()
    if args.download is True:
        filePath = downloadFromURL(args)
    writeToMenu(args, config)
    copyFiles(args, config)
