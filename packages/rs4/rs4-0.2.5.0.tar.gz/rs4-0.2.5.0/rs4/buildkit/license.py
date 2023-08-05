# Copyright (C) 2018 Semicon Networks
# Author: Hans Roh <hansroh@gmail.com>

import os
import sys
import subprocess
from getpass import getpass
from hashlib import md5
import os, struct
from ..termcolor import tc
from .. import ifaces

ENCRYPTED = None
LICENSE_FILE = None
POSITION = 0

def configure (key, name = '.license'):
    global ENCRYPTED, LICENSE_FILE, POSITION
    ENCRYPTED = md5 (key.encode ()).hexdigest ()
    POSITION = (sum ([ord (c) for c in ENCRYPTED]) * 1978524790) % 1008
    LICENSE_FILE = os.path.join (os.path.dirname (os.path.join (os.getcwd (), sys.argv [0])), name)

def hide_file (filename):
    import win32file
    import win32con
    import win32api
    flags = win32file.GetFileAttributesW(filename)
    win32file.SetFileAttributes(filename, 
        win32con.FILE_ATTRIBUTE_HIDDEN | flags)

def check_license ():
    global ENCRYPTED, LICENSE_FILE
    assert ENCRYPTED and LICENSE_FILE, 'call license.configure first'

    if not os.path.isfile (LICENSE_FILE):
        return "cannot find license"        
    try:
        hwid = ifaces.get_hwid ().lower ()
    except subprocess.CalledProcessError:
        return "cannot get hardware ID, maybe run wiht root permission"        
    key = md5 ('{}:{}'.format (ENCRYPTED, hwid).encode ()).digest ()
    with open (LICENSE_FILE, 'rb') as f:
        data = f.read ()        
    s = sum (struct.unpack ('BBB', data [:3])) + 3 + POSITION
    if data [s:s + 16] != key:
        return "invalid license"
        
def create_license (uuid = None):
    global ENCRYPTED, LICENSE_FILE
    assert ENCRYPTED and LICENSE_FILE, 'call license.configure first'

    if os.path.isfile (LICENSE_FILE):
        with open (LICENSE_FILE, 'rb') as f:
            data = f.read ()
        lns = struct.unpack ('BBB', data [:3])
        data = data [3:]
        name = data [:lns [0]].decode (); data = data [lns [0]:]
        org = data [:lns [1]].decode (); data = data [lns [1]:]
        contact = data [:lns [2]].decode (); data = data [lns [2]:]

        print (tc.ok ("\nLicense Information\n"))
        print (tc.echo ("  Organization:"), org)
        print (tc.echo ("  Point of Contact Name:"), name)
        print (tc.echo ("  Email/Phone Number:"), contact)
        print (tc.echo ("\n  License Status:"), check_license () and tc.error ('INVALID') or tc.ok ('VALID'))        

        if input ('\nDo you want to replace to new license? (n/y) ') != 'y':
            sys.exit ()

    print ()
    org, name, contact = None, None, None
    while not org:
        org = input ('Enter Organization Name: ')
        if len (org.encode ()) > 64:
            print ('  too long, should be within 64 bytes')
            org = None
    while not name:
        name = input ('Enter Point of Contact Name: ')
        if len (name.encode ()) > 64:
            print ('  too long, should be within 64 bytes')
            name = None
    while not contact:
        contact = input ('Enter Email or Phone Number: ')
        if len (contact.encode ()) > 32:
            print ('  too long, should be within 32 bytes')
            contact = None
            
    name = name.encode ()
    org = org.encode ()
    contact = contact.encode ()

    premble = struct.pack ('B', len (name)) + struct.pack ('B', len (org)) + struct.pack ('B', len (contact)) + name + org + contact
    for i in range (3):
        password = getpass('\nEnter License Permit Key: ')
        passed = False
        if md5 (password.encode ()).hexdigest () == ENCRYPTED:
            passed = True
            break
        print ("  incorrect key, try again...")
    
    if not passed:        
        return "incorrect key"

    try:
        hwid = uuid or ifaces.get_hwid ()
        hwid = hwid.lower ()
    except subprocess.CalledProcessError:
        return "cannot get hardware ID, maybe run wiht root permission"
    key = md5 ('{}:{}'.format (ENCRYPTED, hwid).encode ()).digest ()
    data = premble + os.urandom (POSITION) + key + os.urandom (1024 - 16 - POSITION)    
    with open (LICENSE_FILE, 'wb') as f:
        f.write (data)
    os.chmod (LICENSE_FILE, 0o644)
    