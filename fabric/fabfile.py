''' fabric file to initialize environment for starcraft bots development '''
import tarfile
import os
from fabric.api import env, run, put, local, cd, get, settings, sudo, path, lcd


def vm1():
    ''' definition of vm1 environment '''
    env.user = 'vagrant'
    env.hosts = ['localhost:59857']
    env.vm_name = 'vm1'


def vm2():
    ''' definition of vm2 environment '''
    env.user = 'vagrant'
    env.hosts = ['localhost:59858']
    env.vm_name = 'vm2'


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
        run('/cygdrive/d/wdexpress_full.exe /passive /noweb /ForceRestart')


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
    with settings(warn_only=True):
        run('/home/vagrant/starcraft/SETUP.EXE', timeout=10, quiet=True)


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


def clone_tournament_manager():
    ''' clone tournament manger '''
    default = 'https://github.com/davechurchill/StarcraftAITournamentManager'
    repo = env.TM_git
    if not repo:
        repo = default
    run('git clone %s' % repo)


def build_tournament_manager():
    ''' build tournament manager '''
    with cd('/home/vagrant/StarcraftAITournamentManager/src/'):
        with path("/cygdrive/c/Program\ Files/Java/jdk" + env.jdk_version + "/bin",
                  behavior='append'):
            run('chmod +x make.bat')
            run('cmd /c make.bat')
            get('/home/vagrant/StarcraftAITournamentManager/server/server.jar',
                env.server_jar)
            get('/home/vagrant/StarcraftAITournamentManager/client/client.jar',
                env.client_jar)


def _local_clone_TM():
    with lcd(env.clone_TM):
        if not os.path.exists(os.path.join(env.clone_TM, 'StarcraftAITournamentManager')):
            local('git clone https://github.com/davechurchill/StarcraftAITournamentManager')


def _add_to_archive(file_path, base_path, tar_file):
    archive_name = os.path.relpath(file_path, base_path)
    tar_file.add(file_path, archive_name)


def create_server_bundle():
    ''' create TM bundle for server '''
    _local_clone_TM()
    tf_server = tarfile.open(env.server_bundle, mode='w')
    path_server = os.path.join(env.clone_TM,
                               'StarcraftAITournamentManager',
                               'server')
    for f in['html', 'run_server.bat']:
        _add_to_archive(os.path.join(path_server, f), path_server, tf_server)

    tf_server.add(env.server_jar, 'server.jar')


def create_client_bundle():
    ''' create TM bundle for client '''
    _local_clone_TM()
    tf_client = tarfile.open(env.client_bundle, mode='w')
    path_client = os.path.join(env.clone_TM,
                               'StarcraftAITournamentManager',
                               'client')

    for f in ['BWAPI.ini', 'run_client.bat']:
        _add_to_archive(os.path.join(path_client, f), path_client, tf_client)

    tf_client.add(env.client_jar, 'client.jar')


def deploy():
    ''' function called by fabric '''
    install_visual_studio()
    install_starcraft()
    install_bwapi()
    build_example_bot()
