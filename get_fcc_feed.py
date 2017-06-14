import gzip
import os
import requests
import shutil
from zipfile import ZipFile


fcc_feed_base = "http://data.fcc.gov/download/license-view/"
fcc_feed_file = "fcc-license-view-data-csv-format.zip"
fcc_url = "%s%s" % (fcc_feed_base, fcc_feed_file)
fcc_outfile = "./fcc.csv.gz"
fcc_tempfile = "%s%s" % (fcc_outfile, "tempfile")
fcc_enclosed_file = "fcc_lic_vw.csv"
chunk_size = None

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
print "FCC license database written to %s" % fcc_outfile
