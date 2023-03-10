Capstone is an Ansible collection for deploying Ceph and OpenStack.

# Using

```
sudo setenforce 0
sudo mkdir -m 0750 /etc/capstone /var/log/capstone
sudo chown $USER:$USER -R /etc/capstone /var/log/capstone
sudo dnf install -y ansible-core podman python3-netaddr
ansible-galaxy collection install --upgrade -r requirements.yml
ansible-playbook -i inventory/localhost.yml site.yml --list-tags
```
