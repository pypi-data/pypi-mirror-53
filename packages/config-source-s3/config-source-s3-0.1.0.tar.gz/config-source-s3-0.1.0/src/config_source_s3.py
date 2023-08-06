# Copyright 2019 Luddite Labs Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import os.path as op
import logging
import boto3
from io import BytesIO
from boto3.exceptions import Boto3Error
from config_source import config_source, load_to

__version__ = '0.1.0'

logger = logging.getLogger(__name__)


def split_s3_path(path):
    """Split S3 path into bucket name and object path.

    For example::

        s3://my-bucket -> ('my-bucket', '')
        s3://my-bucket/filename -> ('my-bucket', 'filename')
        s3://my-bucket/dir/ -> ('my-bucket', 'dir')
        s3://my-bucket/dir/filename -> ('my-bucket', 'dir/filename')

    Args:
        path: S3 path ``s3://<bucket_name>[/path/to/object]``

    Returns:
        Tuple ``(<bucket_name>, <path>)``.
    """
    if not path.startswith('s3://'):
        raise ValueError('Invalid S3 path')

    path = path[5:]  # remove 's3://'
    parts = path.strip('/').strip().split('/')
    name = parts.pop(0)
    path = '/'.join(parts)

    if not name:
        raise ValueError('Invalid S3 path')

    return name, path


def get_bucket(bucket_name, profile=None, access_key=None, secret_key=None):
    """Get S3 bucket.

    Args:
        bucket_name: S3 sucket name.
        profile: AWS profile.
        access_key: AWS access key.
        secret_key: AWS secret key.

    Returns:
        Bucket object.
    """
    logger.info('Connecting to S3...')
    session = boto3.Session(
        profile_name=profile,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key)
    s3 = session.resource('s3')
    return s3.Bucket(bucket_name)


@config_source('s3')
def load_from_s3(config, filename, profile=None, access_key=None,
                 secret_key=None, cache_filename=None, update_cache=False,
                 silent=False):
    """Load configs from S3 bucket file.

    If ``cache_filename`` is not set then it downloads to memory,
    otherwise content is saved in ``cache_filename`` and reused on next calls
    unless ``update_cache`` is set.

    If ``update_cache`` is set then it downloads remote file and updates
    ``cache_filename``.

    Args:
        config: :class:`~configsource.Config` instance.
        filename: S3 file path ``s3://<bucket>/path/to/file``.
        profile: AWS credentials profile.
        access_key: AWS access key id.
        secret_key: AWS secret access key.
        cache_filename: Filename to store downloaded content.
        update_cache: Use cached file or force download.
        silent: Don't raise an error on missing remote files or file loading
            errors.

    Returns:
        ``True`` if config is loaded and ``False`` otherwise.

    See Also:
        https://docs.aws.amazon.com/cli/latest/userguide/cli-multiple-profiles.html
    """
    bucket, filename = split_s3_path(filename)

    if not filename:
        raise ValueError('Empty filename')

    try:
        if cache_filename is None:
            src = BytesIO()
            bucket = get_bucket(bucket, profile, access_key, secret_key)
            bucket.download_fileobj(filename, src)
            src.flush()
            src.seek(0)
        else:
            # If cache file is not set or doesn't exist then force download.
            src = cache_filename
            if not op.exists(cache_filename) or update_cache:
                bucket = get_bucket(bucket, profile, access_key, secret_key)
                bucket.download_file(filename, src)
    except Boto3Error:
        if silent:
            return False
        raise

    # If cache update is not required then just load configs from existing
    # cached file.
    return load_to(config, 'pyfile', 'dict', src, silent=silent)
