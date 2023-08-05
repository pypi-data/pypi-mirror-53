import glob
import logging
import os
import platform
import sys
from collections import OrderedDict
from datetime import datetime

import django
import psutil
from django.conf import settings


def get_file_info():
    path = os.path.join(settings.BASE_DIR, "**", "*.py")
    all_files = glob.glob(path, recursive=True)
    newest = max(all_files, key=os.path.getmtime)
    return dict(file=newest, modified_time=datetime.fromtimestamp(os.path.getmtime(newest)))


START_TIME = datetime.now()
START_FILE = get_file_info()
