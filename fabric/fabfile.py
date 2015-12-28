''' fabric file to initialize environment for starcraft bots development '''
from fabric.api import env, run, put, local, cd, get

VM_NAME = ''
VS_ISO = ''

BWAPI_TAR = ''
CHAOSLAUNCHER_REG = ''
SC_TAR = ''


def w7_64():
    ''' definition of w7_64 environment '''
    env.user = 'vagrant'
    env.hosts = ['localhost:59857']


def _attach_iso(iso_path):
    attach_iso = "VBoxManage storageattach '%s' --storagectl 'IDE Controller' \
    --port 0 --device 0 --type dvddrive --medium '%s'" % (VM_NAME, iso_path)
    local(attach_iso)


def install_visual_studio():
    ''' install visual studio '''
    _attach_iso(VS_ISO)
    with cd('/cygdrive/d'):
        run('/cygdrive/d/wdexpress_full.exe /passive /noweb')


def install_bwapi():
    ''' install bwapi '''
    # takes around 70s
    # wget https://github.com/bwapi/bwapi/releases/download/v4.1.0-Beta/BWAPI_410B_2_Setup.exe
    with cd('/home/vagrant/'):
        put('', '/home/vagrant', mode=0755)
        # run('icacls %s /grant Administrator:F' % f)
        put('chaoslauncher.reg',
            '/home/vagrant/chaoslauncher.reg',
            mode=0755)
        # cf superuser 664756
        run('cmd /c "%SystemRoot%\\regedit.exe /s \
        `cygpath -w /home/vagrant/chaoslauncher.reg`"')


def install_starcraft():
    ''' run the starcraft installation '''
    # takes around 60s
    # may fail if never logged in as vagrant to the remote with cygwin console.
    put("starcraft", "/home/vagrant/", mode=0755)
    run('./SETUP.EXE ', timeout=10, quiet=True)


def build_example_bot():
    ''' build the example bot provided with BWAPI '''
    bot_project = "/home/vagrant/BWAPI/ExampleAIModule/ExampleAIModule.vcxproj"
    msbuild = "\"/cygdrive/c/Program Files\
    (x86)/MSBuild/12.0/Bin/MSBuild.exe\""
    run('%s `cygpath -aw %s` /p:Configuration=Release\
    /p:Platform=Win32' % (msbuild, bot_project))


def deploy():
    ''' function called by fabric '''
    install_visual_studio()
    install_starcraft()
    install_bwapi()
    build_example_bot()