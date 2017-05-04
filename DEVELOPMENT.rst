==================================
Setting up development environment
==================================

Development environment assumes automated deployment as described
in Operations documentation, but with a virtual machine as the target system.
Make sure you read the Operations documentation first.

Summary of what’s different when you deploy locally under VM:
use Vagrant, use Ansible inventory adapted to Vagrant,
don’t pass the push_mode=rsync extra variable to Ansible.
(Optionally during active development:
use Django development server, set debug to yes if needed.)

Additional pre-requisite to have on the host system:

* Vagrant 1.9.4

Notes about how VM is configured with the provided Vagrantfile:

* Port 80 from development system is mirrored to 8080 on host,
  and port 8000 is mirrored to 8000.
  
  Host system should have corresponding ports available.

* Project root will be mounted in your VM under /home/vagrant/app/.

  This means you don’t have to push the code with rsync, as any changes
  in your working directory will be reflected inside the VM.

  This also means that logs and other byproducts of app operation
  will be mirrored onto host system as siblings of your repository root
  directory, so make sure your directory structure is set up as
  described in the Operations doc.

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

Typically whenever you make changes to code, static assets, templates,
Django settings, etc. you need to re-run ansible-playbook.

General syntax is as above, except to speed it up
it’s recommended to narrow down which tasks are executed
by passing ``--skip-tags`` and/or ``--tags`` options to Ansible.

Some examples:

* After the first successful run of ansible-playbook
  you would typically supply ``--skip-tags system``
  every time so that Ansible doesn’t keep upgrading system packages
  and such.

* ``--tags django-settings`` only runs tasks
  needed to apply changes to Django settings,
  all other tasks are skipped automatically.

  You need to run this if you have changed the debug flag, for example.

* ``--tags app-code`` only runs tasks necessary for the changes
  to your code, static assets or templates to take effect.

  If you’re running the `development server <Development server>`_
  under VM and did not change static assets, this is not necessary.

For details on which tags can be specified or skipped,
see task definitions in the playbook at ops/playbook.yaml.

.. note::

   Multiple tags can be combined. See `Ansible docs`_ for more info.

Debug mode
``````````
To make development easier you might want
to set the ``debug`` to ``yes`` in inventory variables.

This will cause a few adjustments, for example Django will output
full tracebacks on app-level errors.

**Don’t use the ``debug`` flag in production, it’s a security hole.**

Development server
``````````````````
You can use a SSL-enabled development server which provides automated
code reload.

This requires the debug flag to be set.
Don’t use development server in production.

#. Change into ops/ directory

#. SSH into your Vagrant VM::

       vagrant ssh

#. Change to src/ directory::

       cd app/src

#. Start development server.

   * To start the development server::

         ./manage.py runserver 0.0.0.0:8000

     The app should be accessible under https://127.0.0.1:8000/
     on your host system.

   * If you run with ``ssl`` flag set in development environment,
     you might want to start SSL-enabled development server::
     
         ./manage.py runsslserver 0.0.0.0:8000

     The app should be accessible under https://127.0.0.1:8000/
     on your host system.
     
     It should give you a warning about bad SSL certificate; that is normal
     because the certificate is self-signed for development purposes.

     (This documentation doesn’t cover running with HTTPS in develpoment.)

   Note that when you use development server, the site is accessible
   under port 8000 of the host system, as opposed to port 8080
   with normal Gunicorn + Nginx server combination.

Troubleshooting
~~~~~~~~~~~~~~~

.. note::

   You can pass ``-v`` flag to ansible-playbook to enable additional output.
   See `Ansible docs`_ for more info.

Host authenticity
`````````````````
The first time you use SSH to connect to Vagrant-based VM on your
local host, it may report something along the lines of::

    The authenticity of host '[smartfocus.local]:2222 ([127.0.0.1]:2222)' can't be established.

Ansible uses SSH, and it will propagate that message and prompt you
to input "yes" or "no" on first run.

You can freely type "yes" and hit Enter in that case.

Changed host fingerprint
````````````````````````
If Ansible fails with “WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED”,
this again is an error propagated from SSH level.

It happens because you earlier accessed a *different server*
under the same hostname.

This may happen, for example, if you have rebuilt Vagrant VM from scratch,
of if you operate more than one VM.

You might want to find the entry corresponding to your local host 
in your ~/.ssh/known_hosts, delete that line and restart Ansible playbook.
