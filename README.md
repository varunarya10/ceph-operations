ceph-install
============

Install ceph on multi node cluster


Preparation:
-----------
1. Create a user on nodes running Ceph daemons

ssh user@ceph-server
sudo useradd -d /home/ceph -m ceph
sudo passwd ceph

2. ceph-deploy installs packages onto your nodes. This means that the user you create requires passwordless sudo privileges. Provide full previleges to ceph user.

echo "ceph ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ceph
sudo chmod 0440 /etc/sudoers.d/ceph

3. Configure password-less SSH access to each node running Ceph daemons.

ssh-keygen
Generating public/private key pair.
Enter file in which to save the key (/ceph-client/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /ceph-client/.ssh/id_rsa.
Your public key has been saved in /ceph-client/.ssh/id_rsa.pub.

4. Copy the key to each node

ssh-copy-id ceph@ceph-server

5. Modify your ~/.ssh/config file of your admin node so that it defaults to logging in as the user you created when no username is specified.


Host ceph-*
User ceph

6. Install ceph-deploy on admin node.

wget -q -O- 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc' | sudo apt-key add -
echo deb http://ceph.com/debian-emperor/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
sudo apt-get update
sudo apt-get install ceph-deploy

7. Use a formatted disk for OSD nodes.
If the disk is not formatted wipe out the GPT data on the disk on OSD nodes using z ("zap" GPT data) option in experts menu of gdisk.

Running:
--------
Execute : "python ceph_install.py" on ceph-client node.

If you want to use client node as admin node, please create a directory "/etc/ceph" to contain the conf files for ceph cluster.


Once installation is completed, run "ceph osd health", it should return "HEALTH_OK" as status.

Use "sudo ceph -w" to run ceph in watch mode.

To check the osd status, use "ceph osd tree" or "ceph osd dump"
To check the monitor status, use "ceph mon stat" or "sudo ceph mon dump".

For any issues drop an email to :
ashish.a.chandra@ril.com
