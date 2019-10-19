# Setting up OpenStack networks

OpenStack provides powerful SDN capabilities with minimal installation and configuration. 

## Architecture

Note - while this approach follows the self-service networking model, current tests indicate that private networks within OpenStack don't work with the external provider network.

This setup can be deployed over a series of bare metal nodes connected to a switch, or a set of VMware ESXi virtual machines connected to a bunch of ESXi networks powered by vSwitch. For simplicity's sake, let's assume we have one controller node and one compute node; each node has two network interfaces:

1. A management network interface, used by OpenStack components to talk to each other. This will also be the primary IP you'd use to access these nodes. 

2. A provider network that's attached to both nodes, with no IP address assigned. This network is typically provided by your bare metal switch/vSwitch, and is responsible for providing a public network for OpenStack VMs to access the Internet - and be accessed by you.

Here's an example:

```
Hostname: controller
Management NIC: ens192
Management IP: 172.29.0.30
Provider NIC: ens224
Provider IP: <unassigned>
```

```
Hostname: compute01
Management NIC: ens160
Management IP: 172.29.0.29
Provider NIC: ens224
Provider IP: <unassigned>
```

Ensure that the names of the provider NICs on all nodes are the same, and that the `/etc/hosts` file contains entries to allow hostname resolution.

## Configuration

### Neutron ml2

We're going to use `ml2`, a neutron plugin which uses the Linux bridge mechanism to build layer-2 (bridging and switching) virtual networking infrastructure for instances.. This guide assumes you've installed the neutron database.

1. [Configure](https://docs.openstack.org/neutron/stein/install/controller-install-ubuntu.html#configure-networking-options) networking on the controller node. For a self-service network like the one we're trying to set up, follow this [guide](https://docs.openstack.org/neutron/stein/install/controller-install-option2-ubuntu.html). Then, continue with the first guide to set up the metadata agent, configuring nova to use neutron and populate the database.

2. Next, [configure](https://docs.openstack.org/neutron/stein/install/compute-install-ubuntu.html) the compute node. For a self-service network, follow [this guide](https://docs.openstack.org/neutron/stein/install/compute-install-option2-ubuntu.html).

Additional instructions for actually getting OpenStack virtual networks to work with our provider network will be added soon.