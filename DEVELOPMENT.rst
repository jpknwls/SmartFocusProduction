==================================
Setting up development environment
==================================

Development environment assumes automated deployment as described
in operations documentation, but with a virtual machine as the target system.

Additional pre-requisite to have on the host system:

* Vagrant 1.9.4

Notes about how VM is configured with the provided Vagrantfile:

* Port 80 from development system is mirrored to 8080 on host,
  and port 8000 is mirrored to 8000.

* Project root under will be mounted in your VM under /home/vagrant/app/.
  That means you don’t have to push the code with rsync, since any changes
  done in working directory will be reflected inside the VM.

Workflow stays as above with typical automated deployment, but see below.

Summary of differences: use Vagrant, use Ansible inventory adapted to Vagrant,
don’t pass push_mode=rsync to Ansible.

Optionally during active development:
use Django development server, set debug to yes if needed.

.. note::
   
   Refer to `Ansible docs <http://docs.ansible.com/ansible/index.html>`_
   for details on using Ansible for automated deployments
   and configuration management over SSH.

   Refer to `Vagrant docs <https://www.vagrantup.com/intro/index.html>`__
   for details on virtual machine operation using Vagrant.

Initial setup
~~~~~~~~~~~~~

* Duplicate _example-vm/ inventory directory under inventories/
  and rename, below assumes you’ve used "local" as environment name
  in this case

* Change into ops/ directory

* Run ``vagrant up``

* Run::

      ansible-playbook -i inventories/local/hosts.ini playbook.yaml --e "load_initial_data=yes"

* The app should be accessible under https://127.0.0.1:8080/
  on your host system

Iterating
~~~~~~~~~

To make development easier you might want
to set the ``debug`` to ``yes`` in inventory variables,

Using development server
````````````````````````
You can use a SSL-enabled development server which provides automated
code reload.

* Change into ops/ directory

* SSH into your Vagrant VM::

      vagrant ssh

* Change to src/ directory::

      cd app/src

* Stop Nginx and Gunicorn::

      sudo service nginx stop; sudo service gunicorn stop

* Start SSL-enabled development server::
  
      ./manage.py runsslserver 0.0.0.0:8000

* The app should be accessible under https://127.0.0.1:8000/
  (note changed port number) on your host system

Making Ansible skip tasks
`````````````````````````
To speed up subsequent deployments after initial setup is done
flags such as ``--skip-tags  system`` can be passed. For details
of which tags can be specified or skipped see Ansible playbook definition.

Commonly you’d pass ``--tags app-code`` to make changes in your code take
effect. Note: This is the command that’s not necessary if you’re running
a development server.

If you have changed Django settings template ``django_settings.py.j2``,
you need to pass ``--tags django-settings`` to Ansible.

Multiple tags can be supplied.

Troubleshooting running Ansible
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   You can pass -v flag to ansible-playbook to enable additional output.
   See `Ansible docs`_ for more info.

Host authenticity
`````````````````

The first time you use Ansible to connect to Vagrant-based VM on your
local host, it may report you something along the lines of::

    The authenticity of host '[smartfocus.local]:2222 ([127.0.0.1]:2222)' can't be established.

This is an error propagated from SSH.
You can freely type yes and hit Enter in that case.

Changed host fingerprint
````````````````````````

If Ansible fails with ``WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED``,
it may be because you SSHd into a _different server_ on your
local host over port 2222 earlier.

This may happen, for example, if you have rebuilt Vagrant VM from scratch.

You might want to find the entry corresponding to your local host 
in your ~/.ssh/known_hosts, delete that line and restart Ansible playbook.
