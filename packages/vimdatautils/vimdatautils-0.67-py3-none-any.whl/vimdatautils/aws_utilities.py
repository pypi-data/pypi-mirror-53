import os
import re
import boto3


class AWSUtilities:

    def __init__(self) -> None:
        self.s3 = boto3.client('s3')

    # Find latest file/regex in bucket
    # Return list of file names
    def get_s3_file_key(self, key_regex, bucket):
        # Getting prefix if exists
        prefix = os.path.split(key_regex)[0]
        contents = self.list_bucket_objects(bucket, prefix)
        return self.get_latest_file(contents, key_regex)

    @staticmethod
    def get_latest_file(contents, key_regex):
        keys = []
        pattern = re.compile(key_regex)
        for content in contents:
            if re.search(pattern, content['Key']):
                keys.append({'key': content['Key'], 'date': content['LastModified']})
        keys_sorted = sorted(keys, key=lambda k: k['date'], reverse=True)
        if len(keys_sorted) == 0:
            print("File not found " + key_regex)
            return None
        return keys_sorted[0]['key']

    def list_bucket_objects(self, bucket, prefix=None):
        list_objects = self.s3.list_objects(Bucket=bucket, Prefix=prefix)
        contents = list_objects['Contents']
        while 'NextMarker' in list_objects:
            list_objects = self.s3.list_objects(Bucket=bucket, Marker=list_objects['NextMarker'])
            contents.extend(list_objects['Contents'])
        return contents

    def download_s3_file(self, key, bucket, path):
        folder = os.path.split(path)[0]
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(path, 'wb') as file:
            print(f"Downloading file from s3, file: {key}, path: {path}")
            self.s3.download_fileobj(bucket, key, file)
        file.close()

    @staticmethod
    def unzip_file(path):
        os.system("unzip -o {zip} -d {d}".format(zip=path, d=os.path.split(path)[0]))

    def download_latest_file(self, bucket, key_regex, path):
        s3_file_key = self.get_s3_file_key(key_regex, bucket)
        if s3_file_key:
            self.download_s3_file(s3_file_key, bucket, path)
            if os.path.split(path)[1].endswith('.zip'):
                self.unzip_file(path)
        else:
            print(f"No file was found in {bucket}, for regex {key_regex}")
