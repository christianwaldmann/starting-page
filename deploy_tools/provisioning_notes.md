Provisioning a new site
=======================

## Required packages:

- nginx
- Python 3.7
- virutalenv + pip
- Git

e.g., on Ubuntu:

	sudo add-apt-repository ppa:fkrull/deadsnakes
	sudo apt-get install nginx git python37 python3.7-venv

## Nginx Virtual Host config

- see nginx.template.conf
- replace SITENAME with, e.g., staging.my-domain.com

## Systemd service

- see gunicorn-systemd.template.service
- replace SITENAME with, e.g., staging.my-domain.com

## Folder structure
Assume we have a user accout at /home/username

/home/username
	sites
		SITENAME
			database
			source
			static
			virtualenv

