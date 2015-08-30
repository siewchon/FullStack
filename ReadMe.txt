Udacity's Fulll Stack Web Developer Nanodegree
Project 2: Tournament Results

This project entails the use of PostgreSQL database to keep track of players and matches in a game tournament. The game tournament uses the Swiss Pairings system for pairing up players on each round.

Please read and follow the instructions below in order to successfully run and test out the  sql queries and python source codes implemented for this tournament project.


Requirements to execute project 2 files:
====================================================

1. Following softwares/applications are required to run files mentioned below:

            - Ubuntu VirtualBox (VM) (at least 14.04.2 up)
            - Vagrant v1.7.2
            - Python version 2.7.x
            - PostgreSQL v9.4

2. Files needed to run this project:

            - tournament.sql
            - tournament.py
            - tournament_test.py

3. Those three files above must reside in the vagrant directory where the 'Vagrantfile' and 'pg_config.sh' files are.



Instructions on how to run and test the project:
====================================================
open terminal in Mac...

1. From local prompt, cd to the directory where the project files reside.

2. Then fire up VM server by typing :

        vagrant up

3. Login to vagrant vm by typing:

        vagrant ssh

4. Now you're inside the VM. To access the vagrant shared directory in vm; at the prompt (eg: vagrant@vagrant-ubuntu-trusty-32:~$) type:

        cd /vagrant/tournament

5. Get into psql command tool inside the vagrant vm, at the ubuntu prompt type:

        psql

6. Import and run those queries prepared inside tournament.sql file;
    from the 'vagrant=>'' promp, type:

       \i tournament.sql

7. Note: New tables and view are created in the tournament database and are ready for use by the python files.

8. To test the python files, first open a new tab in the terminal then repeat step #1 above if you're not at the directory where the project files are.

9. Repeat steps #3 and #4 above to maneuver to the tournament directory where all your project 2 files are in the vm.

10. Test the functional codes inside the tournament.py file by typing:

        python tournament_test.py

11. If you wish to test the function in the tournament.py file one at a time you may comment out all the test functions inside the tournament_test.py file except the particular function that you want to test.

12. To verify and authenticate the data in the tournament at any given time, please run following sql statements at the psql command tool:

        select * from players;
        select * from matches order by winner desc;
        select * from vw_playerStandings order by wins desc;
