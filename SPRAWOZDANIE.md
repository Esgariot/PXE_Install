# Robert Marciniak 149500 Grupa 61 
## Projekt 109. Serwer PXE + narzędzie generujące skrypt instalacyjny dla wybranej dystrybucji Linuxa
### Sprawozdanie:
#### Opis:
Główną częścią projektu jest skrypt ```pykickxe.py``` zgodny  pythonem 2.7. Na podstawie opcji zawartych w ```pykickxe.conf``` i argumentów konsolowych
zastępuje znaczniki zaczynające się od znaku ```$``` (np. ```$KERNEL```) w pliku ```pxelinux.cfg/autoinstall.menu.source``` na określone zdefiniowane w 
```pykickxe.conf``` po czym kopiuje pliki potrzebne do uruchomienia instalacji sieciowej do folderu podanego przez użytkownika - np. korzenia serwera ftp

Drugą częścią projektu jest założenie, że istnieje poprawnie skonfigurowany serwer DHCP z którego będzie korzystać karta sieciowa komputera na którym ma
zostać zainstalowany system operacyjny oraz poprawnie skonfigurowany serwer FTP z którego instalator po załadowaniu do pamięci operacyjnej będzie pobierać
pliki pełnego systemu operacyjnego
#### Pliki:
```
├── dnsmasqappend.conf 	# przykładowa konfiguracja - dodać do /etc/dnsmasq.conf
├── interfaces   		# przykładowa konfiguracja - serwer dhcp i ftp musi mieć statyczne ip
├── ks.cfg   			# przykładowy plik kickstart
├── pykickxe.conf   	# plik konfiguracyjny dla pykickxe.conf
├── pykickxe.py   		# główny program
├── README.md   		# opis
├── SPRAWOZDANIE.md   	# ten plik
└── tftproot   			# zawartość będzie skopiowana do korzenia ftp
    ├── pxelinux.0   	# obraz bootowania
    ├── pxelinux.cfg   	# konfiguracje wpisów i wyglądu menu
    │   ├── autoinstall.menu  # docelowy wpis menu który tworzy pykickxe.py 
    │   ├── autoinstall.menu.source # kopiując ten i zastępując $<nazwa>
    │   ├── default   
    │   └── graphics.conf   
    └── util   			# pliki binarne modułów używanych przez syslinux
        ├── chain.c32   
        ├── libcom32.c32   
        ├── libutil.c32   
        ├── mboot.c32   
        ├── memdisk   
        ├── menu.c32   
        └── reboot.c32   
```

#### Przebieg:
1. Wstęp - żeby uruchomic sieciowo instalacje systemu potrzebne jest
  * wsparcie dla PXE,
  * serwer, który będzie udostępniał kernel i ramdisk,
  * obraz kernela pxelinux.0
  * drzewo konfiguracje pxelinux.0 w drzewie katalogów pxelinux.cfg
  * poprawne wpisy do pxelinux.cfg/default - ścieżki do plików na serwerze, parametry kernela po APPEND  

  w folderze tftproot znajdują się powyższe, z wyjątkiem plików związanych z dystrybucjami.  

2. Po pobraniu uruchomieniu kernela i załadowaniu ramdisku z serwera tftp uruchomionego przez dnsmasq system szuka drzewa katalogów związanych z dystrybucją.
  Znajduje wszystko, czego potrzebuje dzięki serwerowi vsftp (z jakiegoś powodu dnsmasqowy tftp nie udostępnia plików jako "normalny" ftp, tylko dla PXE).
  W korzeniu serwera ftp jest katalog ```/<distro>/<wypakowane-iso>``` z którego pobiera pliki host na którym jest uruchomiona instalacja. Można też przeprowadzić instalację przez Internet i nie udostępniać całej dystrybucji na serwerze, ale ma to bardzo małe szanse powodzenia przez duże opóźnienie, które nie jest brane pod uwagę przez dracut
3. Żeby to wszystko zautomatyzować do parametrów kernela RedHatowych dystrybucji dodaję ```ks= <ścieżka-do-pliku-kickstart>```
4. Wszystko powyższe można zrobić manualnie, mój skrypt pykickxe.py dąży do zautomatyzowania tego ( z różną skutecznością ). Np. wybór pliku kickstart, kernela i parametrów
  kernela odbywa się na zasadzie złożenia pliku kickstart, znalezieniu znaczników do zastąpienia zaczynających się od ```$``` w ```/pxelinux.cfg/autoinstall.menu``` i skopiowania pliku kickstart do ```/util/``` 


#### pykickxe.conf:
Plik konfiguracji ```pykickxe.py``` zgodny z formatem .INI i dzięki temu parsowalny przez bibliotekę ConfigParser pythona 2.7.
Format .INI pozwala na wykorzystanie makr w postaci ```%(<nazwa_zmiennej_z_jakiejś_sekcji>)<typ_zmiennej>``` co jest przydatne np. używając
```method=%(ftp_url)s/%(dir)s```, bo ConfigParser sam rozszerzy to do ```method=ftp://192.168.0.1/centos```
Podzielony jest na sekcje postaci ```[DEFAULT]``` i ```[<nazwa_dystrybucji>]```.
w ```[DEFAULT]``` znajdują się opcje główne, niezależne od dystrybucji:

* ```last_updated = DD.MM.YYYY``` - data ostatniego sprawdzenia urla z którego można pobrać dystrybucję (nie zaimplementowane)
* ```ftp_root = /sciezka/do/roota/ftp``` - bezwzględna ścieżka do folderu korzenia serwera ftp
* ```ftp_url = ftp://192.168.0.1``` - lokacja sieciowa pod którą można dostać pliki udostępniane przez serwer ftp
* ```default_distro = centos``` - domyślna dystrybucja która zostanie użyta gdy użytkownik nie poda dystrybucji jako opcji przy wywołaniu
* ```default_autocfg = %(default_distro)s/ks.cfg``` - domyślny plik autokonfiguracji użyty przy instalacji systemu
* ```default_kernel = %(default_distro)s/images/vmlinuz``` - domyślny plik kernela do uruchomienia
* ```default_append = ``` - domyślne parametry kernela 
* ```pxe_cfgPath = ./pxeappend.cfg``` - ścieżka do własnego pliku wpisu menu podana przez użytkownika (nie zaimplementowane)


w ```[<nazwa_dystrybucji>]``` znajdują się opcje zależne od konkretnej dystrybucji:

* ```[debian]``` - nazwa sekcji
* ```name = Debian``` - nazwa dystrybucji
* ```dir = debian``` - ścieżka względna do ```ftp_root``` pod którą program spodziewa się znaleźć pliki instalacji dystrybucji
* ```auto_file = ``` - ścieżka do pliku autokonfiguracji (kickstart lub preseed) względna do ```ftp_root```
* ```auto_param = <ks lub preseed>\=``` - zależnie od dystrybucji parametr kernela potrzebny do dołączenia pliku autokonfiguracji jest inny - np. dla Debiana jest to ```preseed=ścieżka/do/pliku.preseed``` a dla RHEL ```ks=ścieżka/do/ks.cfg```. Ta opcja pozwala wybrać parametr kernela bez jego argumentu, czyli np. ```ks=``` lub ```preseed=```
* ```kernel = %(dir)s/linux``` - plik kernela do uruchomienia danej dystrybucji
* ```append = initrd\=%(dir)/initrd.gz``` - parametry kernela potrzebne do uruchomienia danej dystrybucji
* ```url = ``` - adres pod którym można znaleźć aktualne co do ```last_updated``` pliki instalacji sieciowej danej dystrybucji  (nie zaimplementowane)

#### parametry wywołania:
python pykickxe.py -h:
```
usage: Pykickxe [-h] [-l] [-d] [-v] [-t TFTP_ROOT] [--auto_cfg AUTO_CFG]
                {debian,fedora,centos}

a Python PXE and autoinstall tool

positional arguments:
  {debian,fedora,centos}
                        pick a linux distro to download, unpack and append the
                        PXE config to (Debian or Fedora for now)

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            list some default options
  -d, --download        Download (not really working)
  -v, --verbose (also not really working)
                        print some of what this is doing at any moment
  -t TFTP_ROOT, --tftp_root TFTP_ROOT
                        pass an absolute path to tftp root directory
  --auto_cfg AUTO_CFG   pass an absolute path to Kickstart file

This program requires that the root from where pxe gets files has following
structure: <distro>/<~copied content of iso image~> for everything, especially
<distro>/images/pxeboot for kernel and ramdisk, kickstart file in
<distro>/ks.cfg or passed manually, (will get copied to util/ks.cfg)
```
