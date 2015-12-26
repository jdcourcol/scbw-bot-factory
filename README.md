# scbw-bot-factory
a set of recipes to build a development environment for starcraft broodwar AI bots.

## requirements for veewee and virtualbox.

vagrant 1.4.3 virtualbox 4.3.10 ruby 1.9.1
```
sudo apt-get install vagrant virtualbox ruby-full
```
veewee 0.4.5.1
```
sudo gem install veewee --no-rdoc  --user-install


to be checked:
```
rdesktop 1.7.1 gcc 4.8.2
```
sudo apt-get install build-essential g++ rdesktop
```
knife-windows 0.8.2 winrm 0.2.2 log4r 1.1.10
```
sudo gem install em-winrm log4r knife-windows --no-rdoc
```

## vbox creation

initial box creation
```
mkdir -p ${HOME}/WORKDIR
veewee vbox define 'win7sp1ult64' 'windows-7sp1-ultimate-amd64' --workdir=${HOME}/WORKDIR
```


box instantiation
```
veewee vbox build 'win7sp1ult64'  --workdir=${HOME}/WORKDIR
```


