import sys
import os
import boto
from boto.s3.key import Key

# Fix signature version problems with EU region
os.environ['S3_USE_SIGV4'] = 'True'

from config import s3_host

def upload_file(aws_access_key_id, aws_secret_access_key, file, bucket, key,
                callback=None, md5=None, reduced_redundancy=False, content_type=None):
    """
    Uploads the given file to the AWS S3
    bucket and key specified.

    callback is a function of the form:

    def callback(complete, total)

    The callback should accept two integer parameters,
    the first representing the number of bytes that
    have been successfully transmitted to S3 and the
    second representing the size of the to be transmitted
    object.

    Returns boolean indicating success/failure of upload.
    """
    try:
        size = os.fstat(file.fileno()).st_size
    except:
        # Not all file objects implement fileno(),
        # so we fall back on this
        file.seek(0, os.SEEK_END)
        size = file.tell()

    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key, host=s3_host)
    bucket = conn.get_bucket(bucket, validate=True)
    k = Key(bucket)
    k.key = key
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)

    # Rewind for later use
    file.seek(0)

    if sent == size:
        return True
    return False

try:
    from config import s3_key, s3_secret, s3_bucket
except:
    print("s3_key, s3_secret, s3_bucket not found in config.py!")

def print_help():
    print("Usage as a command line tool:\n" +
              "$ s3 [s3_key] [s3_secret] [local file] [s3_bucket]\n" +
              "If s3_key, s3_secret, s3_bucket found in config.py:\n" +
              "$ s3 [local file]") 

if __name__ == "__main__":
    # Use as a command line tool
    # argv has executable file as first arg
    if len(sys.argv) == 1:
        print_help()
        exit(1)

    if 2 <= len(sys.argv) <= 3 :
        # Read parameters from config file
        try:
            from config import s3_key, s3_secret, s3_bucket
        except:
            print("s3_key, s3_secret, s3_bucket not found in config.py!")
            print_help()
            exit(1)

        local_file = sys.argv[1]
        
    else:
        # Read parameters from command line
        s3_key = sys.argv[1]
        s3_secret = sys.argv[2]
        local_file = sys.argv[3]
        s3_bucket = sys.argv[4]

    f = open(local_file,'r+')
    upload_file(s3_key,s3_secret,f,s3_bucket,f.name)
     
    
    
