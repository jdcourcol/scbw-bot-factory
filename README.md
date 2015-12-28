# scbw-bot-factory
a set of recipes to build a development environment for starcraft broodwar AI bots.

## requirements for veewee and virtualbox.

vagrant 1.4.3 virtualbox 4.3.10 ruby 1.9.1
```
sudo apt-get install vagrant virtualbox ruby-full
```
veewee 0.4.5.1
```
sudo gem install --user-install veewee --no-rdoc
```

winrm 0.2.2 (to launch windows boxes)
```
sudo gem install --user-install em-winrm  --no-rdoc
```
note when installing with user-install, you need to add ~/.gem/..... /bin to your path.

veewee requires java to be installed to run the floppy files




the items below need to be checked:
rdesktop 1.7.1 gcc 4.8.2
```
sudo apt-get install build-essential g++ rdesktop
```

```
log4r knife-windows
```

## vbox creation

set WORKDIR to a path.
set VMNAME to a particular VM name

### VM vdi storage

```
mkdir -p ${WORKDIR}/vm
vboxmanage setproperty machinefolder ${WORKDIR}/vm
```
### iso storage
```
mkdir -p ${WORKDIR}/iso
```
copy win7, visual studio, and vbox guest additions in iso/

### definitions storage
```
mkdir -p ${WORKDIR}/definitions
ln -s path_to_win7sp1ult64_definition_dir ${WORKDIR}/${VMNAME}
```

### box instantiation
```
veewee vbox build ${VMNAME}  --workdir=${WORKDIR}
```

### login
```
ssh -p 59857 vagrant@localhost
```

## bot development environment installation

this requires to have python-virtualenv, python-dev (Fabric requires it)
```
sudo apt-get install python-virtualenv python-dev
```
