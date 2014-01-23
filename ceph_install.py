import ConfigParser
import os
import subprocess
import sys

from os.path import expanduser

config = ConfigParser.ConfigParser()

def read_config(config_file):	
    config.read(config_file)
    
def get_config_section_map(section, sub_section):
    conf_dict = {}
    options = config.options(section)
    for option in options:
        if option == sub_section:
            conf_dict[option] = config.get(section, option)
        else:
            pass
    return conf_dict

    
def execute_shell_command(command):
    p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
    while True:
        out = p.stderr.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
	
	
if __name__ == '__main__':
    read_config('deploy_config.ini')
    '''
        create a directory on your admin node node for maintaining the 
        configuration that ceph-deploy generates for our cluster
    '''
    ceph_home = expanduser('~/test_cluster')
    
    if os.path.isdir(ceph_home):
        for file in os.listdir(ceph_home):
            file_path = os.path.join(ceph_home, file)
            os.unlink(file_path)
    else:
        execute_shell_command('mkdir ~/test_cluster')
    
    os.chdir(ceph_home)
       
    '''
        Create a cluster
    '''
    
    conf_dict = get_config_section_map('MON', 'mon_nodes')
    ceph_nodes = conf_dict.values()[0].replace(',','')
    command = 'ceph-deploy new %s' %(ceph_nodes)
    execute_shell_command(command)
       
    ######## Install ceph
    conf_dict = get_config_section_map('CEPH', 'ceph_nodes')   
    ceph_nodes = conf_dict.values()[0].replace(',','')
    command = 'ceph-deploy install %s' %(ceph_nodes)
    execute_shell_command(command) 
    
    #######Add a Ceph Monitor
    conf_dict = get_config_section_map('MON', 'mon_nodes')
    ceph_nodes = conf_dict.values()[0].replace(',','')
    command = 'ceph-deploy mon create %s' %(ceph_nodes)
    execute_shell_command(command)
    
    ####### Gather Keys
    conf_dict = get_config_section_map('MON', 'mon_nodes')
    monitor_nodes = conf_dict.values()[0].replace(',','')
    command = 'ceph-deploy gatherkeys %s' %(monitor_nodes)
    execute_shell_command(command)  
    
    ######## Add OSD
    conf_dict = get_config_section_map('OSD', 'osd_nodes')
    osd_nodes = conf_dict.values()[0].replace(',','')
    conf_dict = get_config_section_map('OSD', 'device')
    device =  conf_dict.values()[0].replace(',','')
    
    ####### Prepare OSDs
    osd_devices = []
    for node in osd_nodes.split():   
        osd_devices.append('%s:%s:/dev/%s' %(node, device, device))
    
    osds_to_install =  ' '.join(osd_devices)
    prepare_command = 'ceph-deploy osd prepare %s' %(osds_to_install)
    execute_shell_command(prepare_command)

    ###### Activate OSDs
    activate_command = 'ceph-deploy osd activate %s' %(osds_to_install)   
    execute_shell_command(activate_command)   
    
    ####### Copy Configurations
    conf_dict = get_config_section_map('CEPH', 'ceph_nodes')   
    ceph_nodes = conf_dict.values()[0].replace(',','')
    command = 'ceph-deploy admin ceph-client %s' %(ceph_nodes)
    execute_shell_command(command)    
