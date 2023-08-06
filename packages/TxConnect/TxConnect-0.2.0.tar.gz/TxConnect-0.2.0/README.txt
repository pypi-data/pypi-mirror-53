==============================
TxConnect SCUC Scraper v0.2.0
==============================

This is a Python library for web scrapping TxConnect, a grade viewing service. It is oriented towards SCUCISD with future plans to be able to extend it to other school districts.

Installation
---------------

Use the package manager pip to install TxConnect.::
pip install TxConnect

Usage
---------------

::
from txconnect.txconnect import TxConnect

tx = TxConnect()
tx.login(username, password) # returns if login successful
tx.get_student_list() # returns student names and ids associated with account in json format
tx.get_classes(student_id) # returns all classes associated with student id