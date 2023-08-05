import builtins
import unittest
from unittest import mock
from unittest.mock import call
from .aws_utilities import AWSUtilities


class TestAWS(unittest.TestCase):
    """
        Testing our usage of boto3
        1. Testing the logic of download latest
        2. Testing regex usage
        3. Testing boto3 with NextMarker logic
        4. Testing download from s3
        5. Testing unzip
    """

    @mock.patch('aws_utilities.boto3')
    def setUp(self, mock_boto3) -> None:
        self.aws = AWSUtilities()
        self.mock_boto3 = mock_boto3

    @mock.patch('os.system')
    @mock.patch("builtins.open", create=False)
    def test_download_latest_file(self, mock_open, mock_os_system):
        self.mock_boto3.client.assert_called_with('s3')
        self.mock_boto3.client().list_objects.return_value = {
            'Contents': [{
                'Key': 'test/from_testing/test_1_file_name.csv',
                'LastModified': '2019723113612',  # old file
            }]
        }
        self.aws.download_latest_file("test_bucket", "test_.*._file_name.csv", "/test")
        assert self.mock_boto3.client().list_objects.called
        assert mock_open.called
        assert self.mock_boto3.client().download_fileobj.called
        mock_os_system.assert_not_called()  # checking that unzip method wasn't called

    def test_list_bucket_objects(self):
        return_value_1 = {
            'NextMarker': 'koko',
            'Contents': [{
                'Key': 'test/from_testing/test_2_file_name.csv',
                'LastModified': '2019723113613',  # new file
            }]
        }
        return_value_2 = {
            'Contents': [{
                'Key': 'test/from_testing/test_1_file_name.csv',
                'LastModified': '2019723113612',  # old file
            }]
        }
        self.mock_boto3.client().list_objects.side_effect = [return_value_1, return_value_2]
        contents = self.aws.list_bucket_objects("test_bucket", "folder/")
        calls = [call(Bucket='test_bucket', Prefix='folder/'), call(Bucket='test_bucket', Marker='koko')]
        self.mock_boto3.client().list_objects.assert_has_calls(calls, any_order=False)
        self.assertEqual(contents, [{'Key': 'test/from_testing/test_2_file_name.csv', 'LastModified': '2019723113613'},
                                    {'Key': 'test/from_testing/test_1_file_name.csv', 'LastModified': '2019723113612'}])

    def test_get_latest_file(self):
        contents = [{
            'Key': 'test/from_testing/test_1_file_name.csv',
            'LastModified': '2019723113612',  # old file
        }, {
            'Key': 'test/from_testing/test_2_file_name.csv',
            'LastModified': '2019723113613',  # new file
        }]
        self.assertEqual(self.aws.get_latest_file(contents, "test_.*._file_name.csv"), "test/from_testing/test_2_file_name.csv")

    @mock.patch('os.makedirs')
    @mock.patch("builtins.open", create=False)
    def test_download_s3_file(self, mock_open, mock_os):
        self.aws.download_s3_file("test/from_testing/key_name", "test_bucket", "/path/to/download")
        mock_open.assert_called_with('/path/to/download', 'wb')
        mock_os.assert_called_with('/path/to')
        self.mock_boto3.client().download_fileobj.assert_called_with('test_bucket', 'test/from_testing/key_name', mock.ANY)

    def test_get_s3_file_key(self):
        self.mock_boto3.client().list_objects.return_value = {
            'Contents': [{
                'Key': 'test/from_testing/test_1_file_name.csv',
                'LastModified': '2019723113612',  # old file
            }, {
                'Key': 'test/from_testing/test_2_file_name.csv',
                'LastModified': '2019723113613',  # new file
            }]
        }
        returned_key = self.aws.get_s3_file_key("test_.*._file_name.csv", "test_bucket")
        self.assertEqual(returned_key, "test/from_testing/test_2_file_name.csv")

    @mock.patch('os.system')
    def test_unzip_file(self, mock_os_system):
        self.aws.unzip_file("test/from_testing/test_2_file_name.zip")
        mock_os_system.assert_called_with('unzip -o test/from_testing/test_2_file_name.zip -d test/from_testing')

    def tearDown(self) -> None:
        builtins.open = builtins.open


if __name__ == '__main__':
    unittest.main()
