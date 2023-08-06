import os

 

print os.environ.get("FMQL_VISTA_DATA_BASE_DIR")

 

print os.path.isdir("/data/vista1")

print os.path.islink("/data/vista1")

try:

    print os.listdir("/data/vista1")

except Exception as e:

    print e

print os.stat("/data/vista1")
