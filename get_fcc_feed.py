import gzip
import os
import psutil
import requests
import shutil
import threading
import time
from zipfile import ZipFile


fcc_feed_base = "http://data.fcc.gov/download/license-view/"
fcc_feed_file = "fcc-license-view-data-csv-format.zip"
fcc_url = "%s%s" % (fcc_feed_base, fcc_feed_file)
fcc_outfile = "./fcc.csv.gz"
fcc_tempfile = "%s%s" % (fcc_outfile, "tempfile")
fcc_enclosed_file = "fcc_lic_vw.csv"
chunk_size = None
global done_with_things
done_with_things = False


def travis_boohoo():
    sleep_val = 120
    sleep_total = 0
    while done_with_things is False:
        print("__________________________________________")
        print("Still running...%s seconds." % sleep_total)
        vmem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        cpu = psutil.cpu_times().user
        iowait = psutil.cpu_times().iowait
        print("Memory: %s\tDisk: %s\tUser: %s\tIO Wait: %s" % (vmem, disk,
                                                               cpu, iowait))
        print("__________________________________________")
        sleep_total += sleep_val
        time.sleep(sleep_val)
    return

placate_travis = threading.Thread(target=travis_boohoo, name="whatever_man")
placate_travis.daemon = True
placate_travis.start()
response = requests.get(fcc_url, stream=True)
print "Downloading FCC license database.  This will take a while."
written_so_far = 0
with open(fcc_tempfile, 'wb') as feed_temp_file:
    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            written_so_far += 1
            feed_temp_file.write(chunk)
            if written_so_far % 1000 == 0:
                print("%s chunks written so far...")
print "Converting FCC license from zip to gzip"
with ZipFile(fcc_tempfile, 'r') as src_file:
    src_file.extract(fcc_enclosed_file, "./")
print("Extracted contents from zip...")
os.remove(fcc_tempfile)
raw_fcc_file = "./%s" % fcc_enclosed_file
with open(raw_fcc_file, 'rb') as file_in:
    with gzip.open(fcc_outfile, 'wb') as dest_file:
        shutil.copyfileobj(file_in, dest_file)
os.remove(raw_fcc_file)
done_with_things = True
placate_travis.join()
print "FCC license database written to %s" % fcc_outfile
