https://docs.openstack.org/keystone/yoga/install/

```sh
ansible-playbook site.yml inventory/localhost.yml --tags keystone-build,keystone-config
mkdir -m 750 -p /etc/capstone/keystone/fernet-keys /var/log/capstone/keystone
podman run -it --network host \
    --name capstone-keystone \
    -v /etc/capstone/keystone:/etc/keystone:ro \
    -v /var/log/capstone/keystone:/var/log/keystone:rw \
    localhost/capstone/keystone:zed
```
