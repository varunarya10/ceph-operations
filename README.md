ceph-install
============

Install ceph on multi node cluster

Preparation:
-----------
Use a formatted disk for OSD nodes.
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
