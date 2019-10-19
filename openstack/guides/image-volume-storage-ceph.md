# Image & Volume Storage with Ceph

As has been noted before, Ceph is an amazing storage system. Luckily for us, it's also very easy to configure OpenStack with a view to storing VM images and volumes in Ceph.

## Prerequisites

1. A working Ceph cluster.
2. A working OpenStack cluster with Nova and Cinder installed.

## Integrating Ceph with OpenStack Glance

1. On any Ceph node, create a new pool for storing images:
```
ceph osd pool create images 64
```

2. Now create a new Ceph user for Glance, and grab its keyring:
```
ceph auth get-or-create client.images mon 'allow r' osd 'allow class-read object_prefix rdb_children, allow rwx pool=images' -o /etc/ceph/ceph.client.images.keyring
```

3. Next, copy the keyring generated as well as the `ceph.conf` configuration file on the Ceph node to the OpenStack node where `glance-api` is deployed. Typically this would be the controller node. Ensure you copy the keyring to `/etc/ceph/ceph.client.images.keyring`.

4. On the controller node, edit `/etc/ceph/ceph.conf` and add the new keyring:
```
[client.images]
keyring = /etc/ceph/ceph.client.images.keyring
```

5. Next, edit `/etc/glance/glance-api.conf`:
```
[glance_store]

stores = glance.store.rbd.Store
default_store = rbd
rbd_store_pool = images
rbd_store_user = images
rbd_store_ceph_conf = /etc/ceph/ceph.conf
```

6. Restart `glance-api`: `service glance-api restart`.

And that's it! Let's download a test image on the OpenStack controller node and add it to Glance:
```
wget http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img

openstack image create "Cirros 0.4.0" --file cirros-0.4.0-x86_64-disk.img --disk-format qcow2 --container-format bare --public
```

The new Cirros image will be available for you to use to spin up VMs. Executing `rbd ls images` on a Ceph node will show you the UUID of the image stored on the `images` Ceph pool.

