# Robert Marciniak 149500 Grupa 61 
## Projekt 109. Serwer PXE + narzędzie generujące skrypt instalacyjny dla wybranej dystrybucji Linuxa
## Sprawozdanie:
#### Opis:
Główną częścią projektu jest skrypt ```pykickxe.py``` zgodny pythonem 2.7. Na podstawie opcji zawartych w ```pykickxe.conf``` i argumentów wiersza poleceń
zastępuje znaczniki zaczynające się od znaku ```$``` (np. ```$KERNEL```) w pliku ```pxelinux.cfg/autoinstall.menu.source``` na określone zdefiniowane w 
```pykickxe.conf``` po czym kopiuje pliki potrzebne do uruchomienia instalacji sieciowej do folderu podanego przez użytkownika - korzenia serwera ftp.   

Drugą częścią projektu jest założenie, że istnieje poprawnie skonfigurowany serwer DHCP z którego będzie korzystać karta sieciowa komputera na którym ma
zostać zainstalowany system operacyjny oraz poprawnie skonfigurowany serwer FTP z którego instalator sieciowy po załadowaniu do pamięci operacyjnej będzie pobierać
pliki pełnego systemu operacyjnego.   

[Cały projekt jest dostępny tutaj](https://github.com/Esgariot/PXE_Install)   

#### Wymagania:
* karta sieciowa wspierająca bootowanie sieciowe
* serwer DHCP widoczny dla karty sieciowej klienta
* serwer udostępniający potrzebne pliki widoczny dla karty sieciowej klienta
* potrzebne pliki:
	* obraz pxelinux.0
	* pliki konfiguracji dla pxelinux.0 w drzewie folderu pxelinux.cfg
	* poprawny wpis menu bootowania w pliku tekstowym pxelinux.cfg/default
	* pliki binarne modułów wykorzystywanych przez konfigurację pxelinux.0
* odpowiednie dla klienta uprawnienia dostępu do zawartości udostępnianej przez serwer
* pliki związane z instalacją dystrybucji

#### Pykickxe:
```$ python pykickxe.py -h```   
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


### Przebieg:
[Posłużyłem się tym poradnikiem](http://www.tecmint.com/install-pxe-network-boot-server-in-centos-7/)   
#### konfiguracja interfejsów sieciowych:   
W ```/etc/network/interfaces``` dodałem wpis dla interfejsu sieciowego, na którym będzie udostępniany serwer dhcp i ftp
```
auto eth1
allow-hotplug eth1
iface eth1 inet static
        address 192.168.0.1 # ten sam adres co w ftp_url pliku pykickxe.conf
        netmask 255.255.255.0
        broadcast 192.168.0.255
        gateway 10.0.2.15
```
#### konfiguracja dnsmasq:   
[Źródło - Debian wiki](https://wiki.debian.org/PXEBootInstall#Another_Way_-_use_Dnsmasq)   
```
dhcp-range=192.168.0.3,192.168.0.253,255.255.255.0,1h
dhcp-boot=pxelinux.0,pxeserver,192.168.0.2 # adres z którego karta sieciowa klienta będzie pobierać obraz kernela i ramdisku, potem przełączy się na adres ftp
pxe-service=x86PC,"Install Linux",pxelinux
enable-tftp
tftp-root=/srv/tftp # ścieżka korzenia serwera ftp
``` 

#### konfiguracja vsftpd
```
local_root=/srv/tftp
anon_root=/srv/tftp
listen_address=192.168.0.1 # ten sam co w ftp_url pliku pykickxe.conf

listen_port=21
```

#### uruchomienie:
1. Uruchomiłem usługi ```dnsmasq``` i ```vsftpd``` dla systemd poprzez polecenie ```# service enable dnsmasq && service enable vsftpd``` i zrestartowałem maszynę, żeby uwzględnione zostały zmiany w ```/etc/network/interfaces```   
2. Uruchomiłem maszynę wirtualną bez zainstalowanego systemu operacyjnego, mającą za to ustawioną kartę sieciową jako urządzenie startowe (Główne okno menedżera VirtualBox->nowa maszyna->system->kolejność bootowania->Karta sieciowa zaznaczone, na pierwszej pozycji)
3. Karta sieciowa klienta odnalazła serwer dhcp, znalazła ```pxelinux.0``` i rozpoczęła instalację.
4. Przesłany został obraz kernela i ramdisk i uruchomił się system operacyjny z podanymi wcześniej parametrami kernela
5. System znalazł serwer ftp pod adresem ```192.168.0.1``` po czym zaczął pobierać pliki pełnego systemu operacyjnego. Uruchomiony został instalator graficzny CentOSa i postępował automatycznie wg. skryptu kickstart

#### problemy:
1. Nie udało mi się powtórzyć sukcesu powyżej z powodu złych uprawnień dla klienta łączącego się z serwerem ftp. Za każdym razem instalator dochodził do momentu uruchomienia systemu z kernela i ramdisku, wszystko stawało w momencie próby pobrania plików z ftp
2. Z jakiegoś powodu podczas wywołania funkcji ```writeToMenu``` w pliku ```pykickxe.py```, która nadpisuje znaczniki ```$<NAZWA>``` ich odpowiednikami z ```pykickxe.conf``` występuje błąd, i część przepisywanego tekstu jest jeszcze raz dopisywana na sam koniec pliku ```autoinstall.menu```
3. Nie wszystkie argumenty wiersza poleneń ani pliku konfiguracyjnego ```pykickxe.conf``` są zaimplementowane. Niektóre rzeczy (jeszcze) niczego nie robią



