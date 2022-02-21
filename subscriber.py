#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Reminder, Redis needs to be set with, at minimum :
# redis-cli> config set notify-keyspace-events s$xE

import os
import re

from loguru             import logger
from redis              import Redis

# Log System imports
logger.info('[DB:*][core] [✓] System imports')

# Redis variables
REDIS_HOST    = os.environ['SEP_BACKEND_REDIS_SVC_SERVICE_HOST']
REDIS_PORT    = os.environ['SEP_BACKEND_REDIS_SVC_SERVICE_PORT']
REDIS_DB      = os.environ['SEP_REDIS_DB']
# Subscriber pattern
SUB_PATH      = os.environ['SEP_REDIS_SUB_PATH']

# Opening Redis connection
try:
    r = Redis(host     = REDIS_HOST,
              port     = REDIS_PORT,
              db       = REDIS_DB,
              encoding = 'utf-8')
except (exceptions.ConnectionError,
        exceptions.BusyLoadingError):
    logger.error(f'[DB:{REDIS_DB}][core] [✗] Connection to Redis')
else:
    logger.info(f'[DB:{REDIS_DB}][core] [✓] Connection to Redis')

# Starting subscription
try:
    pubsub = r.pubsub()
    pubsub.psubscribe(SUB_PATH)
except:
    logger.error(f'[DB:{REDIS_DB}][core] [✗] Subscription to Redis:"{SUB_PATH}"')
else:
    logger.info(f'[DB:{REDIS_DB}][core] [✓] Subscription to Redis:"{SUB_PATH}"')

# We receive the events from Redis
for msg in pubsub.listen():
    logger.debug(f'[DB:{REDIS_DB}] {msg}')

    # Detect the action which triggered the event
    m = re.search(r":(?P<action>\w+)", msg['channel'])
    if m is None:
        # If no action detected, we skip processing
        continue

    action = m.group('action')
    if action == 'expired':
        key = msg['data']
        logger.notice(f'[DB:{REDIS_DB}][expired] {key}')
