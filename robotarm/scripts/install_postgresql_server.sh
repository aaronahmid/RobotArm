#!/usr/bin/bash
# installs a postgresql database
# installs appropiate libraries
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo service postgresql start
sudo apt install python3-dev libpq-dev -y
sudo -u postgres createuser -P --interactive