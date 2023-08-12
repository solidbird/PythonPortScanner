# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:39:35 2023

@author: Ich
"""

import os
#import concurrent.futures

import threading
import click
import socket

port_list = []

def open_sock(timeout: int) -> socket:
    s = socket.socket()
    s.settimeout(timeout)
    
    return s

def scan_ports(host, portrange, timeout):
        
    for p in range(portrange[0],portrange[1]+1):
        s = open_sock(timeout)
        
        try:
            #print(f"{host}:{p}")
            s.connect((host, p))
        except:
            #print(f"closed!")
            continue
        
        port_list.append(p)

@click.command()
@click.option('--host', '-h', prompt='Host', help="Host the port Scanner should connect to.")
@click.option('--ports', '-p', default="1-6000", help=f"'{os.path.basename(__file__)} -p 1-200' Port range for the port Scanner.")
@click.option('--timeout', '-t', default=1, help="Timeout of each port connection.")
def main(host, ports, timeout):
    
    port_start_end = ports.split('-')
    port_start_end = (int(port_start_end[0]), int(port_start_end[1]))
    
    x=port_start_end[0]
    y=port_start_end[1]
    
    thread_count = int((y-x)/2)
    thread_list = []
    
    step = int((y-x)/thread_count)

    for a in range(x,y+1,step):
        end_bound = a+step-1
        
        if end_bound <= y:
            #executor.map(scan_ports, host, (a,end_bound), timeout)
            
            #print(f"{thread_count} Thread Started!")
            thr = threading.Thread(target=scan_ports, args=(host, (a,end_bound), timeout))
            thread_list.append(thr)
            thr.start()
             
    for x in thread_list:
        x.join()
    
    print("\tOpen ports:")
    for x in port_list:
        try:
            serv_name = socket.getservbyport(x)
        except:
            serv_name = "<unknown>"
            
        print(f"\t\t{serv_name}:{x}")

if __name__ == "__main__":
    main()