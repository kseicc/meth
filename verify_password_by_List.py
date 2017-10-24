#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os,sys,time
import paramiko
import csv
import logging
import logging.config

# Read host list from CVS file
def readCVS(filename):
    csv_reader = csv.reader(open(filename, 'r'))
    return csv_reader

# Login Server
def loginServer(host,username,password):
    status = 1
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect server
    try:
        ssh.connect(hostname=host[1], username=username, password=password)
    except Exception as e:
        status = 0
    return {'ssh':ssh,'status':status}

# maching host information by listed
def machingHost(targetHost,list):
    for host in list:
        if host[0] == targetHost:
            return host
    return []

# Main funcation
if __name__ == "__main__":
    ########################################################################################
    ## argv
    ########################################################################################
    username = sys.argv[1]
    password = sys.argv[2]
    ########################################################################################
    ## logger
    ########################################################################################
    # Set log file name
    token = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # OPERATION_LOG= 'log/operation_'+username+'_'+token+'.csv'
    SUCCESS_LOG= 'log/verify_password_success.log'
    FAILED_LOG= 'log/verify_password_failed.log'

    # Create system and operation logger
    success_logger = logging.getLogger('success')
    success_logger.setLevel(logging.INFO)
    failed_logger = logging.getLogger('failed')
    failed_logger.setLevel(logging.INFO)

    # Create file handler to output log in file
    file_handler_success = logging.FileHandler(SUCCESS_LOG)
    file_handler_success.setLevel(logging.INFO)
    file_handler_failed = logging.FileHandler(FAILED_LOG)
    file_handler_failed.setLevel(logging.INFO)

    # Create console handler to output log in console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # define handler format
    # formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
    formatter = logging.Formatter('%(asctime)s,%(levelname)s,%(message)s','%Y/%m/%d,%H:%M:%S')
    file_handler_success.setFormatter(formatter)
    file_handler_failed.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add handler in logger
    success_logger.addHandler(file_handler_success)
    success_logger.addHandler(console_handler)
    failed_logger.addHandler(file_handler_failed)
    failed_logger.addHandler(console_handler)

    # record log
    success_logger.info('======================  Start  ====================================')
    failed_logger.info('======================  Start  ====================================')

    ########################################################################################
    ## read server list
    ########################################################################################
    # host list
    MANAGED_HOSTS_LIST = 'list/Host_List.csv'
    TARGET_HOSTS_LIST = 'list/list.txt'

    managed_hosts_list = list(readCVS(MANAGED_HOSTS_LIST))
    target_hosts_list = readCVS(TARGET_HOSTS_LIST)

    ########################################################################################
    ## fetch server and login server to perform change password
    ########################################################################################
    resp = ''
    loginfo = ''

    # fetch server
    for row in target_hosts_list:
        host = machingHost(row[0],managed_hosts_list)
        if len(host) > 0:
            ssh = loginServer(host,username,password)
            if ssh['status'] == 0:
                ssh['ssh'].close()
                failed_logger.info(host[0]+','+host[1]+','+username+',login,failed,'+'The password is incorrect!')
            else:
                success_logger.info(host[0]+','+host[1]+','+username+',login,success,'+'The password is correct!')
        else:
            failed_logger.info(row[0]+',0.0.0.0,'+username+',scope,out,'+'The host is out of scope!')
    success_logger.info('======================   End   ====================================')
    failed_logger.info('======================   End   ====================================')
    exit(0)