"""
Cloudflare R2 Storage Service
Handles file uploads and downloads using Cloudflare R2 (S3-compatible)
"""

import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from typing import Optional, BinaryIO
from dotenv import load_dotenv

load_dotenv()


class R2StorageService:
    """Service for Cloudflare R2 object storage"""

    def __init__(self):
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
        self.access_key_id = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID", "")
        self.secret_access_key = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY", "")
        self.bucket_name = os.getenv("CLOUDFLARE_R2_BUCKET_NAME", "graphmind-uploads")
        self.public_url = os.getenv("CLOUDFLARE_R2_PUBLIC_URL", "")

        self._client = None
        self._available = False

        if self.account_id and self.access_key_id and self.secret_access_key:
            self._init_client()

    def _init_client(self):
        """Initialize the S3-compatible R2 client"""
        try:
            endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"
            self._client = boto3.client(
                "s3",
                endpoint_url=endpoint_url,
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                config=Config(signature_version="s3v4"),
                region_name="auto",
            )
            # Verify bucket access
            self._client.head_bucket(Bucket=self.bucket_name)
            self._available = True
            print(f"[OK] Connected to Cloudflare R2 bucket: {self.bucket_name}")
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                # Bucket doesn't exist, try to create it
                try:
                    self._client.create_bucket(Bucket=self.bucket_name)
                    self._available = True
                    print(f"[OK] Created Cloudflare R2 bucket: {self.bucket_name}")
                except Exception as create_err:
                    print(f"[WARNING] Could not create R2 bucket: {create_err}")
            else:
                print(f"[WARNING] R2 connection failed: {e}")
        except Exception as e:
            print(f"[WARNING] R2 not available: {e}")
            print("[INFO] Falling back to local file storage")

    @property
    def is_available(self) -> bool:
        return self._available

    def upload_file(self, file_obj: BinaryIO, object_key: str, content_type: str = "application/octet-stream") -> Optional[str]:
        """
        Upload a file to R2.

        Args:
            file_obj: File-like object to upload
            object_key: Key (path) in the bucket
            content_type: MIME type of the file

        Returns:
            Public URL of the uploaded file, or None on failure
        """
        if not self._available:
            return None

        try:
            self._client.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_key,
                ExtraArgs={"ContentType": content_type},
            )

            if self.public_url:
                return f"{self.public_url.rstrip('/')}/{object_key}"

            return f"r2://{self.bucket_name}/{object_key}"

        except Exception as e:
            print(f"[ERROR] R2 upload failed: {e}")
            return None

    def download_file(self, object_key: str, destination_path: str) -> bool:
        """
        Download a file from R2 to a local path.

        Args:
            object_key: Key (path) in the bucket
            destination_path: Local path to save the file

        Returns:
            True on success, False on failure
        """
        if not self._available:
            return False

        try:
            self._client.download_file(self.bucket_name, object_key, destination_path)
            return True
        except Exception as e:
            print(f"[ERROR] R2 download failed: {e}")
            return False

    def delete_file(self, object_key: str) -> bool:
        """
        Delete a file from R2.

        Args:
            object_key: Key (path) in the bucket

        Returns:
            True on success, False on failure
        """
        if not self._available:
            return False

        try:
            self._client.delete_object(Bucket=self.bucket_name, Key=object_key)
            return True
        except Exception as e:
            print(f"[ERROR] R2 delete failed: {e}")
            return False

    def get_presigned_url(self, object_key: str, expiry_seconds: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for temporary access to a private file.

        Args:
            object_key: Key (path) in the bucket
            expiry_seconds: URL expiry time in seconds (default 1 hour)

        Returns:
            Presigned URL string, or None on failure
        """
        if not self._available:
            return None

        try:
            url = self._client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": object_key},
                ExpiresIn=expiry_seconds,
            )
            return url
        except Exception as e:
            print(f"[ERROR] R2 presigned URL generation failed: {e}")
            return None


# Global singleton
r2_storage = R2StorageService()
