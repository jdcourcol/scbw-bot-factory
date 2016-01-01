''' fabric file to initialize environment for starcraft bots development '''
from fabric.api import env, run, put, local, cd, get


def vm1():
    ''' definition of vm1 environment '''
    env.user = 'vagrant'
    env.hosts = ['localhost:59857']


def vm2():
    ''' definition of vm2 environment '''
    env.user = 'vagrant'
    env.hosts = ['localhost:59858']


def _detach_drive():
    detach_drive = "vboxmanage storageattach '%s' --storagectl 'IDE Controller'\
    --port 0 --device 0 --type dvddrive --medium 'emptydrive'" %(env.vm_name)
    local(detach_drive)


def _attach_iso(path_iso):
    _detach_drive()
    attach_iso = "VBoxManage storageattach '%s' --storagectl 'IDE Controller' \
    --port 0 --device 0 --type dvddrive \
    --medium '%s'" % (env.vm_name, path_iso)
    local(attach_iso)


def install_visual_studio():
    ''' install visual studio '''
    _attach_iso(env.visual_studio_iso)
    with cd('/cygdrive/d'):
        run('/cygdrive/d/wdexpress_full.exe /passive /noweb')


def install_bwapi():
    ''' install bwapi '''
    # takes around 70s
    # wget https://github.com/bwapi/bwapi/releases/download/v4.1.0-Beta/BWAPI_410B_2_Setup.exe
    with cd('/home/vagrant/'):
        put(env.bwapi_tar, '/home/vagrant/bwapi.tar.gz')
        run('tar xzvf /home/vagrant/bwapi.tar.gz')
        put(env.chaoslauncher_reg,
            '/home/vagrant/chaoslauncher.reg',
            mode=0755)
        # run('icacls %s /grant Administrator:F' % f)
        put(env.chaoslauncher_reg,
            '/home/vagrant/chaoslauncher.reg',
            mode=0755)
        # cf superuser 664756
        run('cmd /c "%SystemRoot%\\regedit.exe /s \
        `cygpath -w /home/vagrant/chaoslauncher.reg`"')


def install_starcraft():
    ''' run the starcraft installation '''
    # takes around 60s
    # may fail if never logged in as vagrant to the remote with cygwin console.
    put(env.starcraft_tar, "/home/vagrant/starcraft.tar.gz", mode=0755)
    run('tar xzvf /home/vagrant/starcraft.tar.gz')
    run('/home/vagrant/starcraft/SETUP.EXE ', timeout=10, quiet=True)


def build_example_bot():
    ''' build the example bot provided with BWAPI '''
    bot_project = "/home/vagrant/BWAPI/ExampleAIModule/ExampleAIModule.vcxproj"
    msbuild = "\"/cygdrive/c/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe\""
    run('%s `cygpath -aw %s` /p:Configuration=Release\
    /p:Platform=Win32' % (msbuild, bot_project))


def install_jdk():
    ''' silent install java jdk '''
    put(env.jdk_exe, "/home/vagrant/jdk.exe", mode=0755)
    run('/home/vagrant/jdk.exe /s')


def deploy():
    ''' function called by fabric '''
    install_visual_studio()
    install_starcraft()
    install_bwapi()
    build_example_bot()
