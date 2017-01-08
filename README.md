# PXE_Install
This will become a beautiful parser and generator for preseed file for debian and maybe someday for other distros using diffrent tools  

###Research:  
  * Turns out other than RedHat, Ubuntu has some support for Kickstart installation:  
  [Ubuntu Kickstart documentation](https://help.ubuntu.com/community/KickstartCompatibility Kickstart Compatibility)  
  * RedHat:  
  [RedHat Kickstart & Anaconda guide](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/5/html/Installation_Guide/ch-kickstart2.html)  
  * Some python tools for parsing kickstart files  
  [pykickstart](https://fedoraproject.org/wiki/Pykickstart)  
  * Linux docs kickstart howto:  
  [HOWTO](http://linuxdocs.org/HOWTOs/KickStart-HOWTO.html)  
  *  Setting up PXE server on debian  
  [PXE Client & Server](https://wiki.debian.org/PXEBootInstall#Installing_Debian_using_network_booting)  
  *  https://www.server-world.info/en/note?os=CentOS_7&p=pxe&f=2  
  *  Building Ubuntu's system-config-kickstart under Debian  
  [Debian system-config-kickstart](https://verahill.blogspot.com/2013/05/428-system-config-kickstart-on-debian.html)  
  *  [RHEL/CentOS PXE setup](http://www.tecmint.com/install-pxe-network-boot-server-in-centos-7/)
  *  Multi-distro PXE Server. From what I've seen this wouldn't work, but the pxelinux menu structure are valid example
     [Setting Up A PXE Install Server For Multiple Linux Distributions](https://www.howtoforge.com/ubuntu_pxe_install_server_p6)
  *  Syslinux.org, some mailing lists, dnsmasq & vsftp.conf man pages, bit of StackOverflow

###Sprawozdanie:  
1. Wstęp - żeby uruchomic sieciowo instalacje systemu potrzebne jest
  * wsparcie dla PXE,
  * serwer, który będzie udostępniał kernel i ramdisk,
  * obraz kernela pxelinux.0
  * drzewo konfiguracje pxelinux.0 w drzewie katalogów pxelinux.cfg
  * poprawne wpisy do pxelinux.cfg/default - ścieżki do plików na serwerze, parametry kernela po APPEND  

  w folderze tftproot znajdują się powyższe, z wyjątkiem plików związanych z dystrybucjami.  

2. Po pobraniu uruchomieniu kernela i załadowaniu ramdisku z serwera tftp uruchomionego przez dnsmasq system szuka drzewa katalogów związanych z dystrybucją.
  Znajduje wszystko, czego potrzebuje dzięki serwerowi vsftp (z jakiegoś powodu dnsmasqowy tftp nie udostępnia plików jako "normalny" ftp, tylko dla PXE).
  W korzeniu serwera ftp jest katalog ```/<distro>/<wypakowane-iso>/``` z którego pobiera pliki host na którym jest uruchomiona instalacja. Można też przeprowadzić instalację przez Internet i nie udostępniać całej dystrybucji na serwerze, ale ma to bardzo małe szanse powodzenia przez duże opóźnienie, które nie jest brane pod uwagę przez dracut
3. Żeby to wszystko zautomatyzować do parametrów kernela RedHatowych dystrybucji dodaję ```ks= <ścieżka-do-pliku-kickstart>```
4. Wszystko powyższe można zrobić manualnie, mój skrypt pykickxe.py dąży do zautomatyzowania tego ( z różną skutecznością ). Np. wybór pliku kickstart, kernela i parametrów
  kernela odbywa się na zasadzie złożenia pliku kickstart, znalezieniu znaczników do zastąpienia zaczynających się od ```$``` w ```/pxelinux.cfg/autoinstall.menu``` i skopiowania pliku kickstart do ```/util/``` 






###Założenia:
TEMAT INDYWIDUALNY Robert Marciniak 

1. Serwer PXE + ~~kickstart~~ -> ~~preseed~~ -> jednak kickstart  
2. Narzędzie generuje wyjściowy skrypt (preseed i post-install) z kilku "kawałków". Mogą nimi być np. zestaw pakietów, polecenie tworzenia katalogów dla usera, polecenie instalacji jakiegoś środowiska graficznego. Niektóre rzeczy mogą się wykluczać (np środowiska graficzne). 

Przykładowe scenariusze:   

1.  Użytkownik chciałby daną dystrybucję z konkretnym zestawem programów. Chciałby też mieć utworzone konto, środowisko graficzne, skonfigurowane niektóre programy  

   ```
   > użytkownik uruchamia narzędzie do generowania skryptu instalacyjnego. 
   > uruchamia narzędzie interaktywnie lub nie, wybiera dostępne opcje, zatwierdza. 
   > Skrypt jest zapisywany na serwerze, podczas instalacji PXE pobierane są z niego dane, 
   > użytkownik dostaje gotowy skonfigurowany system   
   ```  

2.  Maszyna bare metal z ustawionym bootowaniem przez sieć.   

   ```
   > podczas instalacji serwer udostępnia skrypt konfiguracji domyślnej - ustawiane są podstawowe rzeczy, np. partycje, timezone 
   > po instalacji uruchamiany jest dialog, który czeka jakiś czas na odpowiedź użytkownika - wciśnięcie dowolnego przycisku. 
   > Jeśli użytkownik odpowie, to przejście do scenariusza A, jeśli nie, to skrypt sprząta po sobie i host się wyłącza. 
   > maszyna ma zainstalowany system zgodnie z konfiguracją domyślną. 
   ```  

3. Uruchomienie instalacji aż do dostępu do powłoki.  

   ```
   > Użytkownik resztę robi sam
   ```  