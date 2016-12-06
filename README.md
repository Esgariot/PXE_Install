# PXE_Install
Slice of config files and install scripts for automated PXE linux install.
Not a functional repo, just collection of useful stuff to make it work.

##Research:  
  * Turns out other than RedHat, Ubuntu has some support for Kickstart installation:  
  [Ubuntu Kickstart documentation](https://help.ubuntu.com/community/KickstartCompatibility Kickstart Compatibility)  
  * RedHat:  
  [RedHat Kickstart & Anaconda guide](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/5/html/Installation_Guide/ch-kickstart2.html)  
  * Some python tools for parsing kickstart files  
  [pykickstart](https://fedoraproject.org/wiki/Pykickstart)  
  * Linux docs kickstart howto:  
  [HOWTO](http://linuxdocs.org/HOWTOs/KickStart-HOWTO.html Redhat Kickstart Howto)  
  *  Setting up PXE server on debian  
  [PXE Client & Server](https://wiki.debian.org/PXEBootInstall#Installing_Debian_using_network_booting)  

  *  https://www.server-world.info/en/note?os=CentOS_7&p=pxe&f=2  



Założenia:
TEMAT INDYWIDUALNY Robert Marciniak 

1. Serwer PXE + kickstart 
2. Narzędzie generuje wyjściowy skrypt (kickstart i post-install) z kilku "kawałków". Mogą nimi być np. zestaw pakietów, polecenie tworzenia katalogów dla usera, polecenie instalacji jakiegoś środowiska graficznego. Niektóre rzeczy mogą się wykluczać (np środowiska graficzne). 

Przykładowe scenariusze:  
1.  Użytkownik chciałby daną dystrybucję z konkretnym zestawem programów. Chciałby też mieć utworzone konto, środowisko graficzne, skonfigurowane niektóre programy - np. sudo
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