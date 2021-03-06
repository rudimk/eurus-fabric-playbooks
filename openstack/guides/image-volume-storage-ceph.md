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

The new Cirros image will be available for you to use to spin up VMs. Executing `rbd ls images` on a Ceph node will show you the UUID of the image stored on the `images` Ceph pool. Note that any VM/volume snapshots will also be stored on this pool.


## Integrating Ceph with Cinder

This section will deal with configuring OpenStack Cinder for deploying addon volumes on Ceph.

1. On any Ceph node, create a new pool for storing volumes:
```
ceph osd pool create volumes 128
```

2. Create and authorise a Ceph user for Cinder:
```
ceph auth get-or-create client.volumes mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=volumes, allow rx pool=images' -o /etc/ceph/ceph.client.volumes.keyring
```

3. On both the controller node running Cinder and the compute node, copy the keyring generated above to `/etc/ceph/ceph.client.volumes.keyring`. Ensure that the Ceph configuration file on your controller node(`/etc/ceph/ceph.conf`) is also copied over to the compute node at the same path.

4. On the controller node, add the keyring to `/etc/ceph/ceph.conf`:
```
[client.volumes]
keyring = /etc/ceph/ceph.client.volumes.keyring
```

5. Generate a UUID which will be used by `libvirt` to integrate with Ceph. Copy the UUID generated by running this command on the controller node:
```
uuidgen
```

6. Edit `/etc/cinder/cinder.conf`:
```
[DEFAULT]

enabled_backends = rbd

[rbd]
volume_driver = cinder.volume.drivers.rbd.RBDDriver
rbd_pool = volumes
rbd_ceph_conf = /etc/ceph/ceph.conf
rbd_flatten_volume_from_snapshot = false
rbd_max_clone_depth = 5
rbd_store_chunk_size = 4
rados_connect_timeout = -1
glance_api_version = 2
rbd_user = volumes
rbd_secret_uuid = <GENERATED_UUID>
```

7. Restart Cinder: `service cinder-api restart && service cinder-volume restart`

8. On the compute node, add the following XML to `/etc/ceph/ceph-volumes.xml`, ensuring the UUID here matches what you generated previously:
```
<secret ephemeral="no" private="no"> <uuid>ADD UUID HERE</uuid> <usage type="ceph"> <name>client.volumes secret</name> </usage> </secret>
```

9. Now add this to `virsh`:
```
virsh secret-define --file ceph-volumes.xml
virsh secret-set-value  --secret <ADD UUID HERE>  --base64 $(cat /etc/ceph/ceph.client.volumes.keyring)
```

Let's verify volume creation:
```
openstack volume create --size 1 testVolume1
```

This should create a Cinder volume backed by Ceph; this can be also be verified by running `rbd ls volumes` on a Ceph node, which will throw up the UUID of the Ceph object containing the volume.


## Integrating Cinder+Ceph with Nova

Let's configure OpenStack Cinder and Nova to use Ceph for provisioning root disks for Nova VMs.

This section will deal with configuring OpenStack Cinder for deploying addon volumes on Ceph.

1. On any Ceph node, create a new pool for storing VM root disks:
```
ceph osd pool create vms 128
```

2. Create and authorise a Ceph user for Cinder:
```
ceph auth get-or-create client.vms mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=vms, allow rx pool=images' -o /etc/ceph/ceph.client.vms.keyring
```

3. On both the controller node running Cinder and the compute node, copy the keyring generated above to `/etc/ceph/ceph.client.vms.keyring`. Ensure that the Ceph configuration file on your controller node(`/etc/ceph/ceph.conf`) is also copied over to the compute node at the same path.

4. On the controller and compute nodes, add the keyring to `/etc/ceph/ceph.conf`:
```
[client.vms]
keyring = /etc/ceph/ceph.client.vms.keyring
```

5. Create a new UUID for integrating `libvirt` with Ceph. Copy the UUID generated by running the `uuidgen` command on the compute node:
```
uuidgen
```

6. Add the following parameters to `/etc/nova/nova.conf` on the compute node:
```
[libvirt]

images_type = rbd
images_rbd_pool = vms
images_rbd_ceph_conf = /etc/ceph/ceph.conf
rbd_user = vms
rbd_secret_uuid = <GENERATED_UUID>
```

7. Restart `nova-compute`: `service nova-compute restart`

8. On the compute node, add the following XML to `/etc/ceph/ceph-vms.xml`, ensuring the UUID here matches what you generated previously:
```
<secret ephemeral="no" private="no"> <uuid>5b67401f-dc5e-496a-8456-9a5dc40e7d3c</uuid> <usage type="ceph"> <name>client.vms secret</name> </usage> </secret>
```

9. Now add this to `virsh`:
```
virsh secret-define --file ceph-vms.xml
virsh secret-set-value  --secret <ADD UUID HERE>  --base64 $(cat /etc/ceph/ceph.client.vms.keyring)
```

Now you're all set. Verify this by spinning up a VM on OpenStack with a root disk.
