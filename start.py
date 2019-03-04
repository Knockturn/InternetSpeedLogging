# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:48:30 2019

@author: HQ104632
Req: Python 3.x, speedtest-cli min 2.0.2, geopy min 1.18.1
"""
'''
TODO:
    ADD WI-fi info (2,4 vs 6 gHz)
    add wi-fi strength
'''
import speedtest
import csv
from os.path import exists
import geopy.distance
import time
import socket
import sys
import datetime

# Check if CSV file exists, create if not
if not exists('internet_log.csv'):
    with open('internet_log.csv', mode='w', newline='') as internetLogFile:
        internetLogWriter = csv.writer(internetLogFile, delimiter=';')
        internetLogWriter.writerow(['Download - Mbps', 'Upload - Mbps', 'Ping - Ms', 'Server', 'Name',
                                    'Distance - KM', 'Timestamp', 'Client IP', 'HostName', 'Wi-Fi Frequency',
                                    'Wi-Fi Strength'])

# START LOOP
counter = 0
timeToSleep = 900 #900 = 15 minutes
for i in range(0,100):
    try:
        while True:
            try:
                counter+=1
                # START SPEED TEST
                servers = []
                
                print('Starting Test Nr.:', counter)
                
                s = speedtest.Speedtest()
                s.get_servers(servers)
                s.get_best_server()
                
                s.download()
                downloadSpeedMbps = s.results.download / 1000000
                
                s.upload()
                uploadSpeedMbps = s.results.upload / 1000000
                
                # Distance Calculation
                coords_server = (s.results.server['lat'], s.results.server['lon'])
                coords_client = (s.results.client['lat'], s.results.client['lon'])
                
                distance = round(geopy.distance.distance(coords_server, coords_client).km, 2)
                
                # WRITE TO CSV - Log the test
                with open('internet_log.csv', mode='a', newline='') as internetLogFile:
                    internetLogWriter = csv.writer(internetLogFile, delimiter=';')
                    internetLogWriter.writerow([round(downloadSpeedMbps, 2), round(uploadSpeedMbps, 2), 
                                                round(s.results.ping), s.results.server['url'], s.results.server['name'],
                                                distance, s.results.timestamp, s.results.client['ip'], socket.gethostname(),
                                                'Wifi Freq', 'Wifi Strength'])
                
                print('Test Finished. Sleeping script:', timeToSleep/60, 'minutes')
                time.sleep(timeToSleep)
            except KeyboardInterrupt:
                sys.exit()
    except:
        counter+=1
        print('\nERROR WITH RUN NR.:', counter, 'sleeping:',timeToSleep/60, 'minutes and trying again')
        #Log the error
        with open('internet_log.csv', mode='a', newline='') as internetLogFile:
                    internetLogWriter = csv.writer(internetLogFile, delimiter=';')
                    internetLogWriter.writerow(['ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR',
                                                'ERROR', datetime.datetime.now(), 'ERROR', 'ERROR',
                                                'ERROR', 'ERROR'])
        time.sleep(timeToSleep)
        continue
    