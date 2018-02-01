#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyResetOpenVPNServiceWhenNetworkIsDown.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/1/31
Create Time:            17:29
Description:            reset OpenVPN service and network when VPN is down
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """

import os
import socket
import time


def get_remote_host_status(host, port):
    """
    :param host: str
    :param port:  int
    :return:  boolean
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    status = False
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.AF_INET)
        status = True
    except socket.error:
        pass
    finally:
        s.close()
    return status


def restart_openvpn_service():
    """
    restart service named "OpenVPNService"
    :return:
    """
    os.system('sc stop "OpenVPNService"')
    time.sleep(1)
    os.system('sc start "OpenVPNService"')


def renew_and_update_conn():
    """
    renew ipconfig of connection name
    :return:
    """
    os.system('ipconfig /renew "以太网 3"')  # "以太网 3" is OpenVPN connection name


def reset_network_interface_card():
    """
    reset NIC(Network Interface Card) adapter
    :return:
    """
    os.system('netsh interface show interface "以太网 3"')
    os.system('netsh interface set interface name="以太网 3" admin=DISABLED')
    time.sleep(1)
    os.system('netsh interface set interface name="以太网 3" admin=ENABLED')
    os.system('netsh interface show interface "以太网 3"')


if __name__ == '__main__':
    # frontend task, if there need a callable script, just remove endless loop
    while True:
        if not get_remote_host_status("192.168.88.29", 389) and not get_remote_host_status("192.168.88.30", 389):
            print "OpenVPN service is not worked, restart it."
            restart_openvpn_service()
            print "Wait 60 seconds for service up."
            time.sleep(60)
        elif not get_remote_host_status("192.168.88.29", 389) and not get_remote_host_status("192.168.88.30", 389):
            reset_network_interface_card()
            print "Wait 60 seconds for service up."
            time.sleep(60)
        elif not get_remote_host_status("192.168.88.29", 389) and not get_remote_host_status("192.168.88.30", 389):
            renew_and_update_conn()
            print "Wait 60 seconds for service up."
            time.sleep(60)
        else:
            print "Wait 30 seconds for next cycle."
            time.sleep(30)
