#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Reminder, Redis needs to be set with, at minimum :
# redis-cli> config set notify-keyspace-events s$xE

import os
import time

from redis              import Redis
from datetime           import datetime

# Shorted definition for actual now() with proper format
def mynow(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Log System imports
print(f'{mynow()} [core] System imports [✓]')

# Redis variables
REDIS_HOST    = os.environ['SEP_BACKEND_REDIS_SVC_SERVICE_HOST']
REDIS_PORT    = os.environ['SEP_BACKEND_REDIS_SVC_SERVICE_PORT']
REDIS_DB_NAME = os.environ['SEP_REDIS_DB']
# Subscriber pattern
SUB_PATH      = os.environ['SEP_REDIS_SUB_PATH']
VERBOSE       = os.environ['SEP_REDIS_SUB_VERBOSE']

# Opening Redis connection
try:
    r = Redis(host     = REDIS_HOST,
              port     = REDIS_PORT,
              db       = REDIS_DB_NAME,
              encoding = 'utf-8')
except:
    print(f'{mynow()} [core] Connection to redis:{REDIS_DB_NAME} [✗]')
else:
    print(f'{mynow()} [core] Connection to redis:{REDIS_DB_NAME} [✓]')

# Starting subscription
try:
    pubsub = r.pubsub()
    pubsub.psubscribe(SUB_PATH)
except:
    print(f'{mynow()} [core] Subscription to redis:"{SUB_PATH}" [✗]')
else:
    print(f'{mynow()} [core] Subscription to redis:"{SUB_PATH}" [✓]')

# We receive the events from Redis
for msg in pubsub.listen():
    if VERBOSE: print(f'{mynow()} [verbose] {msg}')
