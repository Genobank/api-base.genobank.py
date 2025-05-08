import os
from typing import Optional

from libs.dao import bucket_dao
from libs.exceptions import DomainInjectionError


class bucket_service:
    def __init__(self, _bucket):
        if not isinstance(_bucket, bucket_dao.bucket_dao):
            raise DomainInjectionError.DomainInjectionError("bucket_service", "bucket")
        self.bucket_dao = _bucket

    def create_folder(self, folder_path):
        return self.bucket_dao.create_folder(folder_path)
    
    def fetch(self, _filter={}, projection={}, sort_field=None, sort_order=None):
        result = self.bucket_dao.fetch(_filter, projection, sort_field, sort_order)
        if not result:
            return []
        return result

    def fetch_one(self, _filter={}, projection={}, sort_field=None, sort_order=None):
        result = self.bucket_dao.fetch(_filter, projection, sort_field, sort_order)
        if not result:
            return {}
        return result[0]


    def has_bucket_with_permittee_serial(self, serial):
        print(serial)
        bucket_found = self.bucket_dao.find_by_permittee_serial(serial)
        return bool(bucket_found)

    def has_bucket_with_permittee_address(self, address):
        bucket_found = self.bucket_dao.find_by_permittee_address(address)
        return bucket_found is not None

    def get_file_name(self, biosample_id, permittee_serial):
        permittee_serial = int(permittee_serial)
        bucket_db = self.bucket.find_by_permittee_serial(permittee_serial)

        # WARNING!!!!!! HARCODED PERMITTTEE SERIAL THIS SERIAL MUST CHANGE
        # bucket_db = self.bucket_dao.find_by_permittee_serial(39)

        if not bucket_db:
            raise Exception("This bucket does not exist")
        b_access_key = bucket_db["access_key_id"]
        b_secret_key = bucket_db["secret_access_key"]
        b_name = bucket_db["bucket_name"]
        aux_name = biosample_id + "_" + str(permittee_serial)
        filename = self.bucket_dao.get_file_name(
            aux_name, b_access_key, b_secret_key, b_name
        )
        return filename

    def get_file_routes(self, address, prefix=None):
        bucket_db = self.bucket_dao.find_by_permittee_address(address)
        if not bucket_db:
            raise Exception(
                "Bucket NOT Found: This Permittee does not have an existing bucket"
            )
        else:
            print("\n\nprefix", prefix)
            access_key = bucket_db["access_key_id"]
            secret_key = bucket_db["secret_access_key"]
            bucket_name = bucket_db["bucket_name"]
            return self.bucket_dao.get_files_routes(
                access_key, secret_key, bucket_name, prefix
            )

    def get_bucket_routes(self, bucket_access_key, bucket_secret_key, bucket_name, prefix):
        return self.bucket_dao.get_files_routes(
            bucket_access_key, bucket_secret_key, bucket_name, prefix
        )

    def get_user_file_rutes(self, user_wallet, prefix=None):
        access_key = os.getenv("BUCKET_ACCESS_KEY_ID")
        secret_key = os.getenv("BUCKET_SECRET_ACCESS_KEY_ID")
        bucket_name = os.getenv("BUCKET_NAME")
        main_path = user_wallet.upper()
        prefix = os.getenv("BUCKET_PATH") + "/users/" + main_path + "/" + prefix
        return self.bucket_dao.get_files_routes(
            access_key, secret_key, bucket_name, prefix
        )

    def get_bucket_tree(self, access_key, secret_key, bucket_name, prefix):
        return self.bucket_dao.get_all_files_routes_no_pagination(
            access_key, secret_key, bucket_name, prefix
        )

    def get_file_routes_by_permittee_serial(self, serial, prefix=None):
        bucket_db = self.bucket_dao.find_by_permittee_serial(serial)
        if not bucket_db:
            raise Exception(
                "Bucket NOT Found: This Permittee does not have an existing bucket"
            )
        else:
            print("\n\nprefix", prefix)
            access_key = bucket_db["access_key_id"]
            secret_key = bucket_db["secret_access_key"]
            bucket_name = bucket_db["bucket_name"]
            return self.bucket_dao.get_files_routes(
                access_key, secret_key, bucket_name, prefix
            )

    def delivery_file_transfer(self, biosample_serial, permittee_address, file_routes):
        bucket_source_credentials = self.bucket_dao.find_by_permittee_address(
            permittee_address
        )
        if not bucket_source_credentials:
            raise Exception(
                "Bucket NOT Found: This Permittee does not have an existing bucket"
            )
        else:
            self.bucket_dao.delivery_file_transfer(
                biosample_serial, bucket_source_credentials, file_routes
            )

    def transfer_bucket_to_bucket(
        self,
        src_paths,
        src_bucket_name,
        dest_acc_key,
        dest_sec_key,
        dest_bucket_name,
        dest_path,
    ):
        transfer = self.bucket_dao.transfer_files_bucket_to_bucket(
            src_paths,
            src_bucket_name,
            dest_acc_key,
            dest_sec_key,
            dest_bucket_name,
            dest_path,
        )
        return transfer

    def transfer_permittee_bucket_to_bucket(
        self,
        src_paths,
        permitte_serial,
        dest_acc_key,
        dest_sec_key,
        dest_bucket_name,
        dest_path,
    ):
        permittee_bucket = self.bucket_dao.find_by_permittee_serial(permitte_serial)
        transfer = self.bucket_dao.transfer_files_bucket_to_bucket(
            src_paths,
            permittee_bucket["bucket_name"],
            dest_acc_key,
            dest_sec_key,
            dest_bucket_name,
            dest_path,
        )
        return transfer

    def get_biosample_zip(self, serial):
        biosample_zip = self.bucket_dao.get_biosample_zip(serial)
        return biosample_zip

    def get_presigned_bucket_file(
        self, biosample_serial, files_list, downloadable=True, expiration=3600
    ):
        link_list = []
        for filename in files_list:
            link = self.bucket_dao.generate_presigned_url(
                os.getenv("BUCKET_NAME"),
                f'{os.getenv("BUCKET_PATH")}/deliveries/{biosample_serial}/{filename}',
                os.getenv("BUCKET_ACCESS_KEY_ID"),
                os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
                download=downloadable,
                expiration=expiration,
            )
            link_list.append(link)
        return link_list

    def get_presigned_link(
        self,
        path_list,
        bucket_name=os.getenv("BUCKET_NAME"),
        aws_access_key=os.getenv("BUCKET_ACCESS_KEY_ID"),
        aws_secret_key=os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
        expiration=3600,
        downloadable=True,
    ):
        link_list = []
        bucket_name = bucket_name or os.getenv("BUCKET_NAME")
        aws_access_key = aws_access_key or os.getenv("BUCKET_ACCESS_KEY_ID")
        aws_secret_key = aws_secret_key or os.getenv("BUCKET_SECRET_ACCESS_KEY_ID")
        if not bucket_name or not aws_access_key or not aws_secret_key:
            raise ValueError(
                "bucket_name, aws_access_key y aws_secret_key deben tener valores válidos."
            )
        for path in path_list:
            link = self.bucket_dao.generate_presigned_url(
                bucket_name=bucket_name,
                path=path,
                aws_access_key=aws_access_key,
                aws_secret_key=aws_secret_key,
                expiration=expiration,
                download=downloadable,
            )
            link_list.append(link)
        return link_list

    def get_user_bucket_file_link(
        self, user, path_list, downloadable=True, expiration=3600
    ):
        link_list = []
        for path in path_list:
            print("\n\n\n path: ", path)
            link = self.bucket_dao.generate_presigned_url(
                os.getenv("BUCKET_NAME"),
                f'{os.getenv("BUCKET_PATH")}/users/{user.upper()}/{path}',
                os.getenv("BUCKET_ACCESS_KEY_ID"),
                os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
                download=downloadable,
                expiration=expiration,
            )
            link_list.append(link)
        return link_list

    def delete_user_file_path(self, user, path_list):
        for path in path_list:
            self.bucket_dao.delete_file(
                bucket_name=os.getenv("BUCKET_NAME"),
                access_key=os.getenv("BUCKET_ACCESS_KEY_ID"),
                secret_key=os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
                file_path=f'{os.getenv("BUCKET_PATH")}/users/{user.upper()}/{path}',
            )
        return True
    
    def delete_file_from_bucket(self, bucket_name, access_key, secret_key, file_path):
        return self.bucket_dao.delete_file(bucket_name, access_key, secret_key, file_path)

    def find_by_permitte_serial(self, permittee_serial: int):
        permittee_serial = self.bucket_dao.find_by_permittee_serial(permittee_serial)
        return permittee_serial

    def get_file_from_bucket(
        self, access_key: str, secret_key: str, bucket_name: str, file_path: str
    ):
        return self.bucket_dao.get_file(access_key, secret_key, bucket_name, file_path)
    
    def get_file_obje_with_metadata(
        self, access_key: str, secret_key: str, bucket_name: str, file_path: str
    ):
        return self.bucket_dao.get_file_with_metadata(access_key, secret_key, bucket_name, file_path)

    def list_files_in_path(
        self, access_key: str, secret_key: str, bucket_name: str, file_path: str
    ):
        return self.bucket_dao.get_all_files_routes_no_pagination(
            access_key, secret_key, bucket_name, file_path
        )

    def find_all(self):
        bucket_list = self.bucket_dao.find_all()
        if not bucket_list:
            return []
        return bucket_list

    def format_bucket_list(self, bucket_list):
        formatted_bukets = []
        for bucket in bucket_list:
            formatted_bukets.append(self.format_bucket(bucket))
        return formatted_bukets

    def format_bucket(self, bucket):
        del bucket["user_name"]
        del bucket["bucket_name"]
        del bucket["access_key_id"]
        del bucket["secret_access_key"]

        return bucket

    def classify_files_and_folders(self, content_list):
        files = []
        folders = []
        for content in content_list:
            if content.endswith("/"):
                folders.append(content)
            else:
                files.append(content)
        return files, folders

    def upload_file_to_bucket(
        self,
        _file,
        destination_path,
        bucket_access_key,
        bucket_secret_key,
        bucket_name,
    ):
        print("type of file", type(_file))
        if isinstance(_file, list):
            return self.bucket_dao.upload_file_list_to_bucket(
                _file,
                destination_path,
                bucket_access_key,
                bucket_secret_key,
                bucket_name,
            )
        else:
            return self.bucket_dao.upload_file_to_bucket(
                _file,
                destination_path,
                bucket_access_key,
                bucket_secret_key,
                bucket_name,
            )

    def upload_file_part_to_bucket(
        self,
        _file,
        file_name,
        destination_path,
        bucket_access_key,
        bucket_secret_key,
        bucket_name,
    ):
        print("type of file", type(_file))
        if isinstance(_file, list) and isinstance(file_name, list):
            return self.bucket_dao.upload_file_part_list_to_bucket(
                _file,
                file_name,
                destination_path,
                bucket_access_key,
                bucket_secret_key,
                bucket_name,
            )
        else:
            return self.bucket_dao.upload_file_part_to_bucket(
                _file,
                file_name,
                destination_path,
                bucket_access_key,
                bucket_secret_key,
                bucket_name,
            )

    # def get_presigned_bucket_file(self, downloadable=True, expiration=3600):
    #     return self.bucket_dao.generate_presigned_url(
    #         os.getenv("BUCKET_NAME"),
    #         "localstaging/deliveries/9961079397/123456789_39.txt",
    #         os.getenv("BUCKET_ACCESS_KEY_ID"),
    #         os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
    #         download=downloadable,
    #         expiration=expiration
    #     )

    def download_and_upload_files(
        self,
        src_path_list,
        src_bucket_name,
        src_access_key,
        src_secret_key,
        dest_access_key,
        dest_secret_key,
        dest_bucket_name,
        dest_path,
    ):
        self.bucket_dao.download_and_upload_files(
            src_path_list,
            src_bucket_name,
            src_access_key,
            src_secret_key,
            dest_access_key,
            dest_secret_key,
            dest_bucket_name,
            dest_path,
        )

    def copy_files_between_buckets_service(
        self,
        src_bucket_name: str,
        dest_bucket_name: str,
        src_files: list,
        dest_folder: str,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        # Si no se proporcionan credenciales, se obtienen de las variables de entorno
        if aws_access_key_id is None:
            aws_access_key_id = os.getenv("BUCKET_ACCESS_KEY_ID")
        if aws_secret_access_key is None:
            aws_secret_access_key = os.getenv("BUCKET_SECRET_ACCESS_KEY_ID")

        # Llamar al método del DAO
        self.bucket_dao.copy_files_between_buckets(
            src_bucket_name=src_bucket_name,
            dest_bucket_name=dest_bucket_name,
            src_files=src_files,
            dest_folder=dest_folder,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
