# Define IOC types and extract IOCs from files

* Types are compatible with [Cortex-Analyzers](https://github.com/TheHive-Project/Cortex-Analyzers)
* Extract IOCs from any file
* Optionally define IOC type

## ioc_strings compared to strings

Left side is Linux `strings` command output with 112k lines and right side `ioc_strings.py` with 27 lines. Purpose is to find only the relevant IOC information.

![gimp-2.10.exe](images/strings_vs_iocstrings.png)

## Installation

```bash
sudo pip3 install ioc_strings
```

## ioc_strings.py usage as Python library

input:
```python
import ioc_strings

ioc1 = ioc_strings.IOC("8.8.8.8")
print(ioc1.is_ioc())
print(ioc1.data)

ioc2 = ioc_strings.IOC("testing")
print(ioc2.is_ioc())
print(ioc2.data)
```

output:
```python
True
{'8.8.8.8': ['ip']}
False
{'testing': []}
```

## Scanning files on CLI

`iocstrings <path/to/file> OR <path/to/directory>`

### Brain virus test (scanning directory)

Directory tree:
```
theZoo/malwares/Binaries/Brain.A
├── Brain.A
│   ├── Brain.A.img
│   ├── Brain.A.txt
│   ├── nobrains
│   │   ├── BRAIN
│   │   ├── DEBRAIN.C
│   │   ├── DEBRAIN.EXE
│   │   ├── DREAD.ASM
│   │   ├── DREAD.INC
│   │   ├── DWRITE.ASM
│   │   ├── DWRITE.INC
│   │   ├── README
│   │   ├── VACCINE.COM
│   │   ├── VACCINE.PAS
│   │   └── VACCINE.TXT
│   └── nobrains.zip
├── Brain.A.md5
├── Brain.A.pass
├── Brain.A.sha
└── Brain.A.zip
```

input:
```
iocstrings theZoo/malwares/Binaries/Brain.A/
```

output:
```
c56f135fdaff397ad207f61b4f2042fe
03f1e073761af071d373f025359da84ec39ada19
nobrains.zip
nobrains.zip
hubak@elf.stuba.sk
0123456789ABCDEF
vaccine.com
jwright@atanasoff.cs.iastate.edu
```

Get types with `-t` option:

input:
```
iocstrings theZoo/malwares/Binaries/Brain.A/ -t
```

output:
```
{'c56f135fdaff397ad207f61b4f2042fe': ['hash']}
{'03f1e073761af071d373f025359da84ec39ada19': ['hash']}
{'nobrains.zip': ['domain']}
{'nobrains.zip': ['domain']}
{'hubak@elf.stuba.sk': ['email']}
{'0123456789ABCDEF': ['hash']}
{'vaccine.com': ['domain']}
{'jwright@atanasoff.cs.iastate.edu': ['email']}
```

### WannaCry Plus test (scanning file)

input:
```bash
iocstrings theZoo/malwares/Binaries/Ransomware.WannaCry_Plus/Ransomware.Wannacry_Plus/Win32.Wannacry.exe -t
```

output:
``` 
{'http://www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com': ['url']}
{'https://accounts.google.co.id/accounts/SetSID?ssdc=1&sidt=ALWU2ctYAye7O0juMarlm532QIoi%2Bwr8tN%2BBPbrmQ/hmm96G6E8KJHUOc3MNBLmTzZF%2BexkidLilKKZhN13/fkQOCVcg%2Bbcok5xAK7sWG5Lxoux3dU/iFtv%2BYQmldSmiFoT1JcPwRTzbYSdbXZNhiYAe/%2BdXuLLI0l4Hab6NW/sHcnzFhWbbpVYVG7gunnyurnoZMEtuC57OKqYRQrySPyawX32ieY4CYXWkQ79UIjU78ZAouWsXClcqLyI1RNNry0Q%2B0rAQwB4P&continue=https://mail.google.com/mail/?auth%3DIQWcD5bS6dHIPAdUnr7YE63CdXsU6o5SpbVnn18jpNaZObI1Qi9iherHmuW9dmXac2L75A.%26authuser%3D1': ['url']}
{'http://www.search.ask.com/web?q=kontrakan+rumah+dekat+unair+kampus+c&apn_dtid=%5EBND406%5EYY%5EID&apn_ptnrs=%5EAG6&apn_uid=5945204265534554&atb=sysid%3D406%3Aappid%3D645%3Auid%3D2c832be1330c7e33%3Auc2%3D125%3Atypekbn%3Da13203%3Asrc%3Dcrb%3Ao%3DAPN10645%3Atg%3D&d=406-645&gct=ds&lang=en&o=APN10645&p2=%5EAG6%5EBND406%5EYY%5EID&shad=s_0043&tpr=2&ts=1502964506859': ['url']}
{'http://www.search.ask.com/web?l=dis&q=tele+berburu+malam&o=APN10645&apn_dtid=^BND406^YY^ID&shad=s_0043&apn_uid=5945204265534554&gct=ds&apn_ptnrs=^AG6&d=406-645&lang=en&atb=sysid%3D406%3Aappid%3D645%3Auid%3Dd87a0504773f8e21%3Auc2%3D125%3Atypekbn%3Da13203%3Asrc%3Dcrb%3Ao%3DAPN10645%3Atg%3D&p2=^AG6^BND406^YY^ID': ['url']}
{'http://www.search.ask.com/web?l=dis&q=blog+civitasakademika&o=APN10645&apn_dtid=^BND406^YY^ID&shad=s_0043&apn_uid=5945204265534554&gct=ds&apn_ptnrs=^AG6&d=406-645&lang=en&atb=sysid%3D406%3Aappid%3D645%3Auid%3Df91bde9dc992b395%3Auc2%3D125%3Atypekbn%3Da13203%3Asrc%3Dcrb%3Ao%3DAPN10645%3Atg%3D&p2=^AG6^BND406^YY^ID': ['url']}
{'http://www.search.ask.com/web?l=dis&q=ah+yusuf+unair&o=APN10645&apn_dtid=^BND406^YY^ID&shad=s_0043&apn_uid=5945204265534554&gct=ds&apn_ptnrs=^AG6&d=406-645&lang=en&atb=sysid%3D406%3Aappid%3D645%3Auid%3D17f14c8f70ebe50f%3Auc2%3D125%3Atypekbn%3Da13203%3Asrc%3Dcrb%3Ao%3DAPN10645%3Atg%3D&p2=^AG6^BND406^YY^ID': ['url']}
{'http://www.search.ask.com/web?apn_dtid=%5EBND406%5EYY%5EID&apn_ptnrs=%5EAG6&apn_uid=5945204265534554&atb=sysid%3D406%3Aappid%3D645%3Auid%3Dd87a0504773f8e21%3Auc2%3D125%3Atypekbn%3Da13203%3Asrc%3Dcrb%3Ao%3DAPN10645%3Atg%3D&d=406-645&gct=ds&lang=en&o=APN10645&p2=%5EAG6%5EBND406%5EYY%5EID&page=1&shad=s_0043&q=JUAL+TEROPONG+MALAM+NIGHT+VISION+BUSHNELL+MURAH&tpr=5&ots=1503503371536': ['url']}
{'http://www.search.ask.com/web?apn_dtid=%5EBND406%5EYY%5EID&apn_ptnrs=%5EAG6&apn_uid=5945204265534554&atb=sysid%3D406%3Aappid%3D645%3Auid%3D2c832be1330c7e33%3Auc2%3D125%3Atypekbn%3Da13203%3Asrc%3Dcrb%3Ao%3DAPN10645%3Atg%3D&d=406-645&gct=ds&lang=en&o=APN10645&p2=%5EAG6%5EBND406%5EYY%5EID&page=1&shad=s_0043&q=Kontrakan+Kost+di+Sutorejo+Surabaya&tpr=5&ots=1502965151886': ['url']}
{'http://www.sciencedirect.com/science/article/pii/S2352250X17301884/pdfft?md5=7092ee52e266c820645f45d927dd1a51&pid=1-s2.0-S2352250X17301884-main.pdf': ['url']}
{'http://wireless.unair.ac.id/login?dst=http%3A%2F%2Fdts.search.ask.com%2Fsr%3Fsrc%3Dcrb%26gct%3Dds%26appid%3D645%26systemid%3D406%26v%3Da13203-125%26apn%5Fuid%3D5945204265534554%26apn%5Fdtid%3DBND406%26o%3DAPN10645%26apn%5Fptnrs%3DAG6%26q%3Dyahoomail': ['url']}
```