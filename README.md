# Mupadie
Mupadie stands for **mu**sical **pa**ttern **di**scovery **e**valuation.

A web application to run different musical pattern discovery algorithms to MIDI files and evaluate the results.

A running version of Mupadie can be found in <https://mupadie.herokuapp.com/>.


## Installation
To run Mupadie on your own computer, you need to first clone the repository to the location of your choice and move to the directory. These commands should work for a Linux machine:

    git clone git@github.com:MWargelin/mupadie.git
    cd mupadie/

Then, in the root directory of the repository, run:

    python3 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt
    python3 app.py

and the application should start.