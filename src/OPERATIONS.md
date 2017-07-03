## Operating this app


Deployment operations are automated with Ansible.


### Terminology

* Control mahine: machine from which you manage your target environments.
  Typically it’s your working machine

* Target: where you deploy the app to

* Environment: type of your deployment target.
  Typical environments an app is deployed in are referred to as
  production (for live site),
  staging (for pre-production testing),
  development

* Inventory: definition of hosts and settings
  specific to given target environment


### Before deployment

This is a one-time sequence

1. Prepare control machine: ensure you have Ansible 2.3.0.0 installed

2. Prepare target machine(s).
   Ensure they have clean Ubuntu 16.04 installed with python-dev package:
   ```
   sudo apt-get update; sudo apt-get install -y python-dev
   ```

3. Note which SSH key you use to connect to your target machine(s),
   which user you SSH as (default is "ubuntu"),
   host and port you SSH to,
   and domain name the app should be available under.

   Provide that information as an inventory in Ansible format:
   duplicate provided "_example" inventory directory,
   name it appropriately to your environment (e.g., "staging")
   and edit hosts.ini and vars.yaml within

4. Pull Ansible role dependencies
   by running from within `ops/` directory the following:
   ```
   ansible-galaxy install -r required_roles.yaml
   ```


### Deployment

Apply Ansible playbook to your inventory
(in this example inventory named "staging"):
```
ansible-playbook -i inventories/staging/hosts.ini site.yaml
```


#### Repeat deployments

It’s safe to repeatedly run Ansible playbook if you make changes to the app.
While first deployment takes some time, subsequently it’s quicker.

You can speed them up further by preventing Ansible
from performing unnecessary checks and operations.

One way to do that is with tags. For example, if you changed
some Python code in your Django project,
you can additionally pass `--tags django` to `ansible-playbook`,
and that might be enough.


### Before development

Development process assumes you use a Vagrant-managed virtual machine
as deployment target. “Before deployment” above applies,
with following changes:

* Have Vagrant installed on your machine

* Use the provided "_example-vagrant" inventory instead of "_example"

The rest applies as described in “Before deployment” and “Deployment”.


### Troubleshooting

If the app is not loading, try connecting to target machine
and monitoring log files.

* Nginx will keep logs in `~/app/nginx-{access,error}.log`
* Django and Gunicorn logs will be found underneath `/var/log/gunicorn/`.

Services can be restarted by running e.g., `sudo service restart gunicorn`
or `sudo service restart nginx`.