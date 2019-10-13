# K3s + Ceph

K3s works really, really well with Ceph to provide reliable and high-performant persistent volumes for Kubernetes pods. It's a fucking win.

## Prerequisites

1. A working Ceph cluster. Use [this playbook](https://github.com/rudimk/eurus-fabric-playbooks/tree/master/ceph/centos7) to deploy a nice little Ceph cluster for yourself.

2. A working K3s cluster. Since you're reading this, we're going to assume you know where the [instructions](https://github.com/rudimk/eurus-fabric-playbooks/tree/master/k3s/ubuntu18) are for deploying one.

3. Access to the K3s cluster via `kubectl`.

## Getting started

1. Create a Ceph pool for storing your K3s volumes. For simplicity, we're going to create a pool here called `kube` with a placement group size of 64 - in production, you really should think this one through and tweak it. Run this on any Ceph node.

```
ceph osd pool create kube 64 replicated
```

2. Next, create a new set of credentials for accessing this pool:
```
ceph auth get-or-create client.kube mon 'allow r' osd 'allow rwx pool=kube'
```
Make sure you copy the key returned by this command - if you are unable to, run `ceph --cluster ceph auth get-key client.kube` to grab it.

3. Grab the Ceph admin key for provisioning storage:
```
ceph auth get-key client.admin
```

4. Next, on your deployment machine/whatever machine you're running `kubectl` on, make sure this repository ic cloned there and navigate to the `manifests/ceph` directory:
```
cd k3s/ubuntu18/manifests/ceph
```

4. Create the RBD provisioner:
```
kubectl create -f CephRBDProvisioner.yaml
```
Verify that worked:
```
kubectl get pods -l app=rbd-provisioner -n kube-system
```

5. Now you need to create Kubernetes secrets for storing the Ceph admin and client.kube keys:
```
kubectl create secret generic ceph-secret --type="kubernetes.io/rbd" --from-literal=key="<CEPH_ADMIN_KEY>" --namespace=kube-system

kubectl create secret generic ceph-secret-kube --type="kubernetes.io/rbd" --from-literal=key="<CEPH_CLIENT_KUBE_KEY>" --namespace=kube-system
```

6. Let's create the storage class for Ceph, through `StorageClass.yaml`. In this manifest, ensure you provide the correct IP addresses for the Ceph MON nodes in the `parameters.monitors` section. Also, they should be accessible from the K3s cluster.
```
kubectl create -f StorageClass.yaml
```

7. Booyeah! Now all we need to do is test this whole shit out. Let's create a PersistentVolumeClaim:
```
kubectl create -f PersistentVolumeClaim.yaml
```

Running `kubectl get pvc` should show you the PVC you just created. If all went well, its status will be set to `Bound`; this can also be verified by running `kubectl get pv` which will show you the new persistent volume, provided by Ceph.