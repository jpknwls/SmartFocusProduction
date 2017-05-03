==================
Operating this app
==================

Some commonly used tasks are automated using an Ansible playbook.

Familiarity with command line shell is assumed.

.. note::
   
   Be sure to refer to `Ansible docs <http://docs.ansible.com/ansible/index.html>`__
   for details on using Ansible for automated deployments
   and configuration management over SSH.

   See also Development documentation on this project.

Pre-requisites
~~~~~~~~~~~~~~

Target system
`````````````
Clean Ubuntu 14.04 that you have SSH access to.

System to execute deployment from
`````````````````````````````````
macOS 10.12.4 or Ubuntu Linux.
Setup under Windows is not covered.

Packages:

* Ansible 2.3.0.0

Directory structure::

    /
    Base directory referred to as “project root” or “project home”.

    On target system it would be located under /home/<user>/app/
    and should be treated as containing sensitive information.

    This layout should be observed on host system as well,
    at least during VM-based development.

    ┃
    ┡━━━src/
    │   Source code repository root
    │   ┃
    │   ┣━━━.git/
    │   ┃
    │   ┣━━━README.rst
    │   ┣━━━OPERATIONS.rst
    │   ┣━━━DEVELOPMENT.rst
    │   ┃
    │   ┣━━━manage.py
    │   ┃
    │   ┋
    │   ┃
    │   ┗━━━ops/
    │       Operations root
    │       ┃
    │       ┣━━━playbook.yaml
    │       ┃   Ansible playbook automating system setup and app deployment
    │       ┃
    │       ┣━━━requirements.txt
    │       ┃   Python package requirements
    │       ┃
    │       ┋
    │       ┃
    │       ┗━━━inventories/
    │           Definitions specific to target environments
    │           in which the app is deployed
    │           ┃
    │           ┣━━━_example/
    │           ┃   Sample inventory with placeholder contents
    │           ┃
    │           ┡━━━_example-vm/
    │           │   Sample inventory for Vagrant VM-based development workflow
    │           │
    │           │
    │           │   Your specific inventories.
    │           │   Must not be under version control (excluded by default):
    │           │
    │           ├───production/
    │           ├───staging/
    │           ┊
    │
    │
    │   Created automatically during operation on target system
    │   (mirrored onto host system in VM-based development setup):
    │
    ├───static/
    ├───db.sqlite3
    ├───nginx.smartfocus.access.log
    ├───nginx.smartfocus.error.log


Process
~~~~~~~

* Duplicate _example/ inventory directory under inventories/
  and rename it to reflect your target environment (for example, "production")

* Edit contents of inventory files to reflect specifics of your deployment,
  required items include: target host name, domain name, secret keys

* Change into ops/ directory

* Run::

      ansible-playbook -i inventories/<env>/hosts.ini playbook.yaml -e "push_mode=rsync load_initial_data=yes"

  The command will deploy current code in your working directory
  onto the server specified in <env>/hosts.ini.

* The app should be accessible under https://<your_domain_name>/.

Saving and loading data
```````````````````````
To load pre-made data fixtures into the DB, pass load_initial_data=yes
in extra_vars to Ansible.

If you want to update data fixtures with the current state of the DB,
that process is manual. You’d need to SSH into your system
and run dumpdata from inside the src/ directory, for example::

    ./manage.py dumpdata auth stores zoho -o smartfocus/fixtures/initial_data.json

Then you might want to download the smartfocus/fixtures/initial_data.json file
using something like scp and check it into your repository.

.. note::

   If your target system is VM, that file will be mirrored into your working
   directory, no need to download. Development documentation covers
   VM-based deployment in more detail.

Using Django shell
``````````````````
SSH into your target system and run ``./manage.py shell`` from under src/.
