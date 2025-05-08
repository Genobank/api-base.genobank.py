import datetime
import io
import logging
import os
import re
import traceback
import zipfile
from io import BytesIO
from typing import Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from pymongo import MongoClient

from libs import json_helper_dao, mongo_helper_dao
from libs.domain.bucket import Bucket


class bucket_dao:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_DB_HOST"))
        self.db = self.client[os.getenv("DB_NAME")]
        self.table = self.db.buckets
        self.json_helper_dao = json_helper_dao.json_helper_dao()
        self.mongo_db_helper = mongo_helper_dao.json_helper_dao()

    def create_folder(
        self,
        folder_path: str,
    ):
        access_key = os.getenv("BUCKET_ACCESS_KEY_ID")
        secret_key = os.getenv("BUCKET_SECRET_ACCESS_KEY_ID")
        bucket_name = os.getenv("BUCKET_NAME")
        if not folder_path.endswith("/"):
            folder_path += "/"

        s3_client = boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )
        try:
            s3_client.put_object(Bucket=bucket_name, Key=folder_path, Body=b"")
            print(
                f"Folder '{folder_path}' created successfully in bucket '{bucket_name}'."
            )
        except ClientError as e:
            print(f"Failed to create folder: {e}")

    def find_by_permittee_serial(self, serial):
        cur = self.db.buckets.find_one({"permittee_serial": serial})
        return cur

    def find_by_permittee_address(self, address):
        doc = self.table.find_one({"permittee": re.compile(address, re.IGNORECASE)})
        return doc

    def find_all(self):
        cur = self.db.buckets.find({})
        return self.mongo_db_helper.serialize_cur(cur)
    
    def fetch(self, _filter={}, projection={}, sort_field=None, sort_order=None):
        cur = self.table.find(_filter, projection)
        if sort_field and sort_order is not None:
            cur = cur.sort(sort_field, sort_order)
        return self.json_helper_dao.serialize_cur(cur)
        

    def get_file_name(self, f_name, access, secret, b_name, prefix="genobank/"):
        s3_client = boto3.client(
            service_name="s3", aws_access_key_id=access, aws_secret_access_key=secret
        )
        try:
            response = s3_client.list_objects_v2(Bucket=b_name, Prefix=prefix)
            for obj in response["Contents"]:
                file_name = obj["Key"]
                file_name_without_ext = file_name.split(".")[0]
                if file_name_without_ext == prefix + f_name:
                    return file_name.split("/")[-1]
            return None
        except Exception as e:
            raise e

    def get_files_routes(
        self, access_key, secret_key, bucket_name, prefix=None, delimiter="/"
    ):
        try:
            all_files = []
            s3_client = boto3.client(
                service_name="s3",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
            list_objects_kwargs = {"Bucket": bucket_name, "Delimiter": delimiter}
            if prefix:
                list_objects_kwargs["Prefix"] = prefix
            response = s3_client.list_objects_v2(**list_objects_kwargs)
            for obj in response.get("Contents", []):
                if obj["Key"] != prefix or not obj["Key"].endswith(delimiter):
                    all_files.append(obj["Key"])
            for folder in response.get("CommonPrefixes", []):
                all_files.append(folder["Prefix"])
            return all_files
        except:
            raise

    def get_all_files_routes_no_pagination(
        self, access_key, secret_key, bucket_name, prefix=None, delimiter="/"
    ):
        try:
            all_files = []
            s3_client = boto3.client(
                service_name="s3",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
            list_objects_kwargs = {"Bucket": bucket_name, "Delimiter": delimiter}
            if prefix:
                list_objects_kwargs["Prefix"] = prefix
            while True:
                response = s3_client.list_objects_v2(**list_objects_kwargs)
                for obj in response.get("Contents", []):
                    if obj["Key"] != prefix or not obj["Key"].endswith(delimiter):
                        all_files.append(obj["Key"])
                for folder in response.get("CommonPrefixes", []):
                    all_files.append(folder["Prefix"])
                if response.get("IsTruncated"):
                    list_objects_kwargs["ContinuationToken"] = response.get(
                        "NextContinuationToken"
                    )
                else:
                    break

            return all_files
        except Exception as e:
            raise e

    # def delivery_file_transfer(self, biosample_serial, src_credentials, file_routes):
    #     source_bucket_name = src_credentials["bucket_name"]
    #     destiny_key_id = os.getenv("BUCKET_ACCESS_KEY_ID")
    #     destiny_access_key = os.getenv("BUCKET_SECRET_ACCESS_KEY_ID")
    #     destiny_bucket_name = os.getenv("BUCKET_NAME")
    #     try:
    #         dest_s3_client = boto3.client(
    #             "s3",
    #             aws_access_key_id=destiny_key_id,
    #             aws_secret_access_key=destiny_access_key,
    #         )
    #         for route in file_routes:
    #             src_file = os.path.relpath(file_routes[route], ".")
    #             print("\n", src_file, "\n")
    #             copy_source = {"Bucket": source_bucket_name, "Key": src_file}
    #             dest_file_key = f"{os.getenv('BUCKET_PATH')}/deliveries/{str(biosample_serial)}/{os.path.basename(src_file)}"
    #             print("\n", dest_file_key, "\n")
    #             dest_s3_client.copy(copy_source, destiny_bucket_name, dest_file_key)
    #     except NoCredentialsError:
    #         print("Credenciales no encontradas")



    def delivery_file_transfer(self, biosample_serial, src_credentials, file_routes):
        # Source bucket (Neochromosome) credentials
        source_bucket_name = src_credentials["bucket_name"]
        source_key_id = src_credentials.get("access_key_id")  # From Neochromosome
        source_access_key = src_credentials.get("secret_access_key")  # From Neochromosome
        
        # Destination bucket (GenoBank) credentials
        destiny_key_id = os.getenv("BUCKET_ACCESS_KEY_ID")
        destiny_access_key = os.getenv("BUCKET_SECRET_ACCESS_KEY_ID")
        destiny_bucket_name = os.getenv("BUCKET_NAME")
        
        try:
            import subprocess

            # Set up environment with destination credentials
            my_env = os.environ.copy()
            my_env["AWS_ACCESS_KEY_ID"] = source_key_id       # Use source credentials
            my_env["AWS_SECRET_ACCESS_KEY"] = source_access_key  # Use source credentials
            
            for route in file_routes:
                src_file = os.path.relpath(file_routes[route], ".")
                print(f"\nStarting transfer of: {src_file}\n")
                
                dest_file_key = f"{os.getenv('BUCKET_PATH')}/deliveries/{str(biosample_serial)}/{os.path.basename(src_file)}"
                print(f"\nDestination: {dest_file_key}\n")
                
                # First download using source credentials
                download_command = [
                    "aws", "s3", "cp",
                    f"s3://{source_bucket_name}/{src_file}",
                    f"{src_file}.temp",
                    "--only-show-errors"
                ]
                
                # Then upload using destination credentials
                upload_command = [
                    "aws", "s3", "cp",
                    f"{src_file}.temp",
                    f"s3://{destiny_bucket_name}/{dest_file_key}",
                    "--only-show-errors"
                ]
                
                # Execute download with source credentials
                process = subprocess.run(
                    download_command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=my_env
                )
                
                if process.returncode != 0:
                    print(f"Download Error: {process.stderr}")
                    raise Exception("Download failed")
                    
                # Switch to destination credentials
                my_env["AWS_ACCESS_KEY_ID"] = destiny_key_id
                my_env["AWS_SECRET_ACCESS_KEY"] = destiny_access_key
                
                # Execute upload with destination credentials
                process = subprocess.run(
                    upload_command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=my_env
                )
                
                # Clean up temp file
                if os.path.exists(f"{src_file}.temp"):
                    os.remove(f"{src_file}.temp")
                
                if process.returncode == 0:
                    print(f"Successfully transferred: {src_file}")
                else:
                    print(f"Upload Error: {process.stderr}")
                    
        except Exception as e:
            print(f"Error: {str(e)}")
            # Clean up temp file in case of error
            if os.path.exists(f"{src_file}.temp"):
                os.remove(f"{src_file}.temp")
            raise
        return True

    def transfer_files_bucket_to_bucket(
        self,
        src_path_list,
        src_bucket_name,
        dest_access_key,
        dest_secret_key,
        dest_bucket_name,
        dest_path,
    ):
        try:
            dest_s3_client = boto3.client(
                "s3",
                aws_access_key_id=dest_access_key,
                aws_secret_access_key=dest_secret_key,
            )
            for path in src_path_list:
                src_path = os.path.relpath(path)
                print("\n", src_path, "\n")
                copy_source = {"Bucket": src_bucket_name, "Key": src_path}
                # dest_file_key = f"{os.getenv('BUCKET_PATH')}/deliveries/{str(biosample_serial)}/{os.path.basename(src_file_path)}"
                print("\n copy_source: ", copy_source, "\n")
                print("\n dest_path: ", dest_path, "\n")
                print("\n basename: ", os.path.basename(path), "\n")
                dest_s3_client.copy(
                    copy_source, dest_bucket_name, dest_path + os.path.basename(path)
                )
        except NoCredentialsError:
            print("Credenciales no encontradas")

    def get_biosample_zip(self, serial):
        access_key = os.getenv("BUCKET_ACCESS_KEY_ID")
        secret_key = os.getenv("BUCKET_SECRET_ACCESS_KEY_ID")
        name = os.getenv("BUCKET_NAME")
        s3_client = boto3.client(
            service_name="s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        file_key = f"{os.getenv('BUCKET_PATH')}/deliveries/{str(serial)}/"
        try:
            file_list = s3_client.list_objects_v2(Bucket=name, Prefix=file_key)[
                "Contents"
            ]
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_LZMA) as myzip:
                for file in file_list:
                    filename = file["Key"]
                    file_obj = s3_client.get_object(Bucket=name, Key=filename)
                    file_data = file_obj["Body"].read()
                    data = io.BytesIO(file_data)
                    myzip.writestr(os.path.basename(filename), data.getvalue())
            zip_buffer.seek(0)
            return zip_buffer
        except NoCredentialsError:
            print("No credentials found")

    def generate_presigned_url(
        self,
        bucket_name,
        path,
        aws_access_key,
        aws_secret_key,
        expiration=3600,
        download=False,
    ):
        url = self.create_presigned_url(
            bucket_name=bucket_name,
            object_name=path,
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            expiration=expiration,
            download=download,
        )
        return url

    def create_presigned_url(
        self,
        bucket_name: str,
        object_name: str,
        aws_access_key=None,
        aws_secret_key=None,
        expiration=3600,
        download=False,
    ) -> Optional[str]:
        """Generate a presigned URL to share an s3 object

        Arguments:
            bucket_name {str} -- Required. s3 bucket of object to share
            object_name {str} -- Required. s3 object to share

        Keyword Arguments:
            expiration {int} -- Expiration in seconds (default: {3600})

        Returns:
            Optional[str] -- Presigned url of s3 object. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name="us-west-1",
        )
        params = {"Bucket": bucket_name, "Key": object_name}

        if download:
            file_name = object_name.split("/")[-1]
            content_disposition = f'attachment; filename="{file_name}"'
            params["ResponseContentDisposition"] = content_disposition
        try:
            response = s3_client.generate_presigned_url(
                "get_object", Params=params, ExpiresIn=expiration
            )
        except ClientError as e:
            print(e)
            return None
        return response

    def find_by_permittee_serial(self, permittee_serial: int):
        try:
            doc = self.table.find_one({"permittee_serial": int(permittee_serial)})
            return self.mongo_db_helper.serialize_doc(doc)
        except Exception as e:
            print(e)
            return e

    def get_file(
        self, access_key: str, secret_key: str, bucket_name: str, file_path: str
    ):
        bucket = Bucket(
            access_key=access_key, secret_key=secret_key, name=bucket_name
        ).set_client()
        response = bucket.get_object(Bucket=bucket_name, Key=file_path)
        data = response["Body"].read()
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data
        
    def get_file_with_metadata(
        self, 
        access_key: str,
        secret_key: str,
        bucket_name: str,
        file_path: str
    ):
        s3_client = boto3.client(
            's3', 
            aws_access_key_id=access_key, 
            aws_secret_access_key=secret_key
        )
        metadata = s3_client.head_object(Bucket=bucket_name, Key=file_path)
        response = s3_client.get_object(Bucket=bucket_name, Key=file_path)
        data = response["Body"].read()
        file_obj = io.BytesIO(data)
        file_obj.name = file_path.split("/")[-1]  # Nombre del archivo
        file_obj.size = metadata.get('ContentLength', len(data))  # Tamaño del archivo
        file_obj.content_type = metadata.get('ContentType')  # Tipo de contenido, por ejemplo, "application/pdf"
        return file_obj


    def exist_file(
        self, access_key: str, secret_key: str, bucket_name: str, file_path: str
    ) -> bool:
        try:
            # Crear el cliente de S3
            s3_client = boto3.client(
                "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
            )

            # Intentar obtener el objeto
            print("\n\n filepath: ", file_path)
            s3_client.head_object(Bucket=bucket_name, Key=file_path)
            return True

        except ClientError as e:
            # Si el error es 404, el archivo no existe
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                # Re-lanzar la excepción si es otro tipo de error
                raise e

        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credenciales no válidas: {e}")
            return False

    def delete_file(
        self, bucket_name: str, access_key: str, secret_key: str, file_path: str
    ):
        access_key = access_key
        secret_key = secret_key
        bucket_name = bucket_name

        s3_client = boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )

        try:
            s3_client.delete_object(Bucket=bucket_name, Key=file_path)
            print(
                f"File '{file_path}' deleted successfully from bucket '{bucket_name}'."
            )
        except ClientError as e:
            print(f"Failed to delete file: {e}")

    def upload_file_to_bucket(
        self,
        file,
        destination_path,
        bucket_access_key,
        bucket_secret_key,
        bucket_name,
    ):
        destination_path = f"{destination_path}{file.filename}"
        print("destination_path: ", destination_path)

        s3_client = boto3.client(
            service_name="s3",
            aws_access_key_id=bucket_access_key,
            aws_secret_access_key=bucket_secret_key,
        )
        file.file.seek(0)
        content_file = file.file.read()

        try:
            s3_client.upload_fileobj(
                io.BytesIO(content_file), bucket_name, destination_path
            )
            return "sucess"
        except ClientError as e:
            print(e)
            logging.error(e)
            return str(e)

    def upload_file_part_to_bucket(
        self,
        file,
        file_name,
        destination_path,
        bucket_access_key,
        bucket_secret_key,
        bucket_name,
    ):
        destination_path = f"{destination_path}{file_name}"
        print("destination_path: ", destination_path)

        s3_client = boto3.client(
            service_name="s3",
            aws_access_key_id=bucket_access_key,
            aws_secret_access_key=bucket_secret_key,
        )
        file.seek(0)
        content_file = file.read()

        try:
            s3_client.upload_fileobj(
                io.BytesIO(content_file), bucket_name, destination_path
            )
            return "sucess"
        except ClientError as e:
            print(e)
            logging.error(e)
            return str(e)

    def upload_file_list_to_bucket(
        self,
        file_list,
        destination_path,
        bucket_access_key,
        bucket_secret_key,
        bucket_name,
    ):
        responses = []
        for file in file_list:
            response = self.upload_file_to_bucket(
                file,
                destination_path,
                bucket_access_key,
                bucket_secret_key,
                bucket_name,
            )
            responses.append(response)
        return responses

    def upload_file_part_list_to_bucket(
        self,
        file_list,
        file_name_list,
        destination_path,
        bucket_access_key,
        bucket_secret_key,
        bucket_name,
    ):
        responses = []
        index = 0
        for file in file_list:
            response = self.upload_file_part_to_bucket(
                file,
                file_name_list[index],
                destination_path,
                bucket_access_key,
                bucket_secret_key,
                bucket_name,
            )
            index += 1
            responses.append(response)
        return responses

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
        try:
            src_s3_client = boto3.client(
                "s3",
                aws_access_key_id=src_access_key,
                aws_secret_access_key=src_secret_key,
            )
            dest_s3_client = boto3.client(
                "s3",
                aws_access_key_id=dest_access_key,
                aws_secret_access_key=dest_secret_key,
            )
            for path in src_path_list:
                if path.endswith("/"):  # Trata la ruta como un prefijo de carpeta
                    files_to_copy = self.list_files_in_bucket_folder(
                        src_s3_client, src_bucket_name, path
                    )
                    for file_path in files_to_copy:
                        print(f"Copying {file_path}")
                        data = self.download_file_to_memory(
                            src_s3_client, src_bucket_name, file_path
                        )
                        dest_file_path = os.path.join(
                            dest_path, os.path.relpath(file_path, path)
                        ).replace(os.sep, "/")
                        self.upload_file_from_memory(
                            dest_s3_client, dest_bucket_name, dest_file_path, data
                        )
                        print(f"Copied {file_path} to {dest_file_path}")
                else:  # Trata la ruta como un archivo individual
                    print(f"Copying {path}")
                    data = self.download_file_to_memory(
                        src_s3_client, src_bucket_name, path
                    )
                    dest_file_path = os.path.join(
                        dest_path, os.path.basename(path)
                    ).replace(os.sep, "/")
                    self.upload_file_from_memory(
                        dest_s3_client, dest_bucket_name, dest_file_path, data
                    )
                    print(f"Copied {path} to {dest_file_path}")
        except NoCredentialsError:
            print("Credenciales no encontradas")
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            traceback.print_exc()

    def list_files_in_bucket_folder(self, s3_client, bucket_name, prefix):
        """Lista todos los archivos bajo un prefijo específico."""
        paginator = s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        file_paths = []
        for page in page_iterator:
            if "Contents" in page:
                for obj in page["Contents"]:
                    file_paths.append(obj["Key"])
        return file_paths

    def download_file_to_memory(self, s3_client, bucket_name, file_key):
        """Descarga un archivo del bucket de S3 y lo almacena en memoria."""
        data = BytesIO()
        s3_client.download_fileobj(bucket_name, file_key, data)
        data.seek(0)  # Regresa al principio del BytesIO para leer desde el inicio
        return data

    def upload_file_from_memory(self, s3_client, bucket_name, file_key, data):
        """Sube un archivo desde la memoria al bucket de S3."""
        data.seek(0)  # Asegura que la lectura se inicie desde el principio
        s3_client.upload_fileobj(data, bucket_name, file_key)
        data.close()  # Cierra el BytesIO después de subir

    def copy_files_between_buckets(
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

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        for src_key in src_files:
            # Asegurarse de que dest_folder termine con '/'
            if not dest_folder.endswith('/'):
                dest_folder += '/'

            # Construir la clave de destino usando el nombre base del archivo
            dest_key = os.path.join(dest_folder, os.path.basename(src_key)).replace("\\", "/")
            copy_source = {"Bucket": src_bucket_name, "Key": src_key}

            try:
                s3_client.copy_object(
                    CopySource=copy_source, Bucket=dest_bucket_name, Key=dest_key
                )
                print(
                    f"Archivo '{src_key}' copiado exitosamente de '{src_bucket_name}' a '{dest_key}' en '{dest_bucket_name}'."
                )
            except ClientError as e:
                print(f"Error al copiar el archivo '{src_key}': {e}")
                raise e
