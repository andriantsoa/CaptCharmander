#!/usr/bin/python
# -*- coding: utf-8 -*-

from pgoapi import PGoApi
from pgoapi.exceptions import *
import time
import sys, getopt
import requests
import re
import sys
import csv

#####CONFIGURATION######

account_file = 'account.csv' #in username,password format
ban_file = "ban.csv" #banned accounts
captcha_file = "captcha.csv" #accounts with captcha
error_file = "error.csv" #accounts with error
ok_file = "ok.csv" #account ready to use

service = "ptc" #only support PTC for now, PR welcome
max_retry = 5 #number of retry for each account
loop = 1 #0 = loop forever
delay_between_loop = 30
lat = 0.0 #latitude
lng = 0.0 #longitude
alt = 0.0 #altitude
login_delay = 2 #delay after login
debug = False
twocaptcha_key = "YOUR_2CAPTCHA_KEY" #2captcha key. Get your here http://2captcha.com/?from=2242107 (referral link)
use_hashing_server = False #True to enable hashing server support. See https://talk.pogodev.org/d/51-api-hashing-service-by-pokefarmer for more info.
hashing_key = "YOUR_HASHING_KEY" #hashing key, you need this if you want to be on the latest API. Get it from https://talk.pogodev.org/d/51-api-hashing-service-by-pokefarmer. Depends on your usage but 150RPM should be more than enough in most cases.

usernames = []
passwords = []

def parse_csv():
  with open(account_file, 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
      if len(row) == 2:
        usernames.append(row[0])
        passwords.append(row[1])
    
def log_debug(text):
  if debug:
    print(text)

def write_to_file(filename, username, password):
  with open(filename, "a") as my_file:
    my_file.write("{},{}\n".format(username, password))

def check_account(username, password, count):
  if count < max_retry:
    try:
      print("Trying to login with {}".format(username))
      
      api = PGoApi()
      if use_hashing_server:
        api.activate_hash_server(hashing_key)
      api.set_position(lat, lng, alt)
      api.set_authentication(service, username, password)
      time.sleep(login_delay)
      api.app_simulation_login()
      req = api.create_request()
      req.check_challenge()
      response = req.call()
      log_debug(response)
      if response['status_code'] == 3:
        print("{} is banned".format(username))
        write_to_file(ban_file, username, password)
      elif 'show_challenge' in response['responses']['CHECK_CHALLENGE'] and response['responses']['CHECK_CHALLENGE']['show_challenge']:
        print("{} has captcha, solving...".format(username))
        write_to_file(captcha_file, username, password)
        
        headers = {
          'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A300 Safari/602.1'
        }
      
        url = response['responses']['CHECK_CHALLENGE']['challenge_url']
        log_debug("Captcha URL: {}".format(url))
        response = requests.get(url, headers=headers)
        m = re.search("data-sitekey=\"(.*)\"", response.content)
        site_key = m.group(1)
        m = re.search("https://(.*?)/", url)
        site_url = m.group(1)
        log_debug("Sitekey: {}".format(site_key))
        log_debug("Page URL: {}".format(site_url))

        captcha_url = 'http://2captcha.com/in.php?key=' + twocaptcha_key + '&method=userrecaptcha&googlekey='+ site_key + '&pageurl=' + site_url
        log_debug("2captcha request: {}".format(captcha_url))
        response = requests.get(captcha_url)
        response_captcha = ''
        
        if response.content[:2] == 'OK':
          captcha_id = response.content[3:]
          #loop until we got the token
          while True:
            response = requests.get('http://2captcha.com/res.php?key='+ twocaptcha_key +'&action=get&id='+captcha_id)
            if response.content[:2] == 'OK':
              response_captcha = response.content[3:]
              break
            else:
              print('Waiting waiting for a response from 2captcha...')
              time.sleep(5)
            
          req.verify_challenge(token=response_captcha)
          response = req.call()
          log_debug(response)
          if 'success' in response['responses']['VERIFY_CHALLENGE'] and response['responses']['VERIFY_CHALLENGE']['success']:
            print("Captcha is solved for {}".format(username))
            write_to_file(ok_file, username, password)
          else:
            #something is wrong, restart the process
            check_account(username, password, count + 1)
        else:
          #something is wrong with 2captcha, restart the process
          check_account(username, password, count + 1)
      else:
        print("{} is fine.".format(username))
        write_to_file(ok_file, username, password)
    except (KeyboardInterrupt, SystemExit):
      sys.exit()
    except Exception as e:
      log_debug(e)
      print("Cannot login with {}, trying again".format(username))
      check_account(username, password, count + 1)
  else:
    print("{} failed to login".format(username))
    write_to_file(error_file, username, password)

parse_csv()
loop_count = 0

while loop_count < loop or loop == 0:
  print("Loop number {} of {}".format(loop_count+1, loop))
  loop_count += 1  
  for i in range(0, len(usernames)):
    username = usernames[i]
    password = passwords[i]
    log_debug("Checking {} with password {}".format(username, password))
    check_account(username, password, 0)
    print("")
  print("Sleep for {} seconds".format(delay_between_loop))
  time.sleep(delay_between_loop)
  print("")