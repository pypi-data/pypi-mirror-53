
import os
import boto3

from .miscutils import list_regfiles


def s3sync(sourcedir, S3bucket, prefix=None, update_only=True):
    """Synchronises local directory to an S3 bucket.
    if update_only is True, only copy updates,
    if prefix is set to a string, prepend key of objects with this prefix"""

    # TODO: add buffer stream, md5check, stat size/ diff
    files = list_regfiles(sourcedir, root=prefix, recursive=True)
    s3 = boto3.client('s3')

    for keyname, filepath in files.items():
        with open(filepath, 'rb') as inputfile:
            #contents = inputfile.read()
            s3.upload_fileobj(inputfile, S3bucket, keyname)
        print(keyname)
        #print(contents)
    print(files)


def s3empty(bucketname, delete_versions=False):
    """Empty contents of an S3Bucket
    NOTE: should go without saying, use function with great caution!"""
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketname)

    if delete_versions is True:
        bucket.object_versions.delete()
    else:
        bucket.objects.all().delete()
