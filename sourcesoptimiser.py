#!/usr/bin/python3

import os
import socket
import subprocess
import sys
import time
import urllib.request

# Parameters
sources_file = '/etc/pacman.d/mirrorlist.pacnew'
test_repo = 'extra'
test_arch = 'x86_64'
test_file = 'extra.files'
temp_file = '/tmp/tempfile'
min_file_size = 9300000
timeout = 30

# Get list of sources
command = "cat {} | grep \"^#\\?Server\" | sed -e \"s/^#\\?Server\\s*=\\s*//\"".format(sources_file)
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output = result.stdout.decode('utf-8').rstrip("\n")
sources = output.split("\n")

# Download timeout - seconds
socket.setdefaulttimeout(timeout)

# Each source and the time it took to download the file
results = {}

for i, source in enumerate(sources):
    # Put together the URL of the file to download from this source
    url = source.replace('$repo', test_repo).replace('$arch', test_arch) + "/" + test_file
    print("{}/{} - {}".format(i + 1, len(sources), url), file=sys.stderr)

    # Remove any existing downloaded file to ensure a clean slate
    try:
        os.remove(temp_file)
    except FileNotFoundError:
        pass

    try:
        # Download the file from this source, timing it
        start_time = time.perf_counter()
        urllib.request.urlretrieve(url, temp_file)
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        file_size = os.path.getsize(temp_file)
        print("Time taken: {} File size: {}".format(time_taken, file_size), file=sys.stderr)
        if file_size >= min_file_size:
            # File downloaded and looks like it's the correct size
            results[source] = time_taken
        else:
            # File is too small, download probably failed
            print("* TOO SMALL, IGNORING *", file=sys.stderr)
    except Exception as e:
        # In case of exception, log it and continue to next source
        print(e, file=sys.stderr)

# Output all sources that successfully downloaded the file, fastest download first
for result in sorted(results.keys(), key=lambda r: results[r]):
    print("#{}\nServer = {}".format(results[result], result))
