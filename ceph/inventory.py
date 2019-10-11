# Define a list of hostnames/IP addresses that will be used for running OSDs/MONs. 
# All nodes run CentOS 7. All commands will be run as root.
# Also make sure the node these playbooks run on can SSH into the Ceph nodes with a SSH keypair.

CEPH_NODES = ()

# The path to the SSH private key that will be used

SSH_KEY = ''

# Update this constant with host entries that will be populated in /etc/hosts for all nodes.
# Use the same syntax as you would in the /etc/hosts file.

HOST_ENTRIES = """



"""