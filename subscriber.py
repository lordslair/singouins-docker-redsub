#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Reminder, Redis needs to be set with, at minimum :
# redis-cli> config set notify-keyspace-events s$xE

import os
import re

from redis              import Redis
from datetime           import datetime

# Shorted definition for actual now() with proper format
def mynow(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Log System imports
print(f'{mynow()} [DB:*][core] [✓] System imports')

# Redis variables
REDIS_HOST    = os.environ['SEP_BACKEND_REDIS_SVC_SERVICE_HOST']
REDIS_PORT    = os.environ['SEP_BACKEND_REDIS_SVC_SERVICE_PORT']
REDIS_DB      = os.environ['SEP_REDIS_DB']
# Subscriber pattern
SUB_PATH      = os.environ['SEP_REDIS_SUB_PATH']
VERBOSE       = eval(os.environ['SEP_REDIS_SUB_VERBOSE'])

# Opening Redis connection
try:
    r = Redis(host     = REDIS_HOST,
              port     = REDIS_PORT,
              db       = REDIS_DB,
              encoding = 'utf-8')
except:
    print(f'{mynow()} [DB:{REDIS_DB}][core] [✗] Connection to Redis')
else:
    print(f'{mynow()} [DB:{REDIS_DB}][core] [✓] Connection to Redis')

# Starting subscription
try:
    pubsub = r.pubsub()
    pubsub.psubscribe(SUB_PATH)
except:
    print(f'{mynow()} [DB:{REDIS_DB}][core] [✗] Subscription to Redis:"{SUB_PATH}"')
else:
    print(f'{mynow()} [DB:{REDIS_DB}][core] [✓] Subscription to Redis:"{SUB_PATH}"')

# We receive the events from Redis
for msg in pubsub.listen():
    if VERBOSE: print(f'{mynow()} [DB:{REDIS_DB}][verbose] {msg}')

    # Detect the action which triggered the event
    m = re.search(r":(?P<action>\w+)", msg['channel'].decode('utf-8'))
    if m is None:
        # If no action detected, we skip processing
        continue

    action = m.group('action')
    if action == 'expired':
        key = msg['data'].decode('utf-8')
        print(f'{mynow()} [DB:{REDIS_DB}][expired] {key}')
