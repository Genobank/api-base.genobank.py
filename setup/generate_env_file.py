from settings import settings
import os

def generate_env():
    out_file = settings.OUTPUT_ENV_FILE_NAME

    lines = [
        "# TEST ENVIRONMENT",
        "#--GENERAL SETTINGS",
        "ENVIRONMENT = Local",
        "FRONT_ENV = local",
        "",
        "PORT = \"8081\"",
        f"APP_SECRET = <YOUR_SECRET_APPLICATION>",
        f"BIOSAMPLE_ACTIVATION_SECRET = <YOUR_BIOSAMPLE_ACTIVATION_SECRET>",
        f"NAMESPACE = \"{settings.BPT_NAMESPACE}\"",
        "",
        f"MESSAGE = <MESSAGE_TO_RECOVER_USER_WALLET>",
        f"NEW_MESSAGE = <MESSAGE_TO_DOWNLOAD_USER_FILE>",
        f"ROOT_MESSAGE = <YOUR_ROOT_MESSAGE_TO_SIGN>",
        "",
        "#--BUCKETS",
        f"BUCKET_PATH = <ENV>",
        f"BUCKET_ACCESS_KEY_ID = <ACCESS_KEY>",
        f"BUCKET_SECRET_ACCESS_KEY_ID = <SECRET_KEY>",
        f"BUCKET_NAME = <BUCKET_NAME>",
        "",
        "#--API(S)",
        "",
        f"API_BASE = \"https://api-test.genobank.io\"",  
        "",
        "#--DATABASE CONF (mongo db)",
        f"MONGO_DB_HOST = <MONGO_STR_CONNECTION>",
        f"DB_NAME = <DB_NAME>",
        "",
        "#--BLOCKCHAIN AND WEB3 SETTINGS",
        "# BLOCKCHAIN",
        "CHAIN_NAME = \"Avalanche\"",
        "#-PROVIDER",
        f"CUSTOM_PROVIDER = \"{settings.PROVIDER}\"",
        "",
        "#-SMCONTRACTS",
        f"BPT_CONTRACT = \"\"",
        f"xBPT_CONTRACT = \"\"",
        f"BIOSAMPLE_CONTRACT = \"\"",
        f"POSP_FACTORY_CONTRACT = \"\"",
        f"DELIVER_MANAGER_CONTRACT = \"\"",
        "",
        "#-ABI ROUTE",
        "ABI_BPT_PATH = \"./smart_contract/biosample-permission-token.json\"",
        "ABI_XBPT_PATH = \"./smart_contract/extended_biosample_permission_token/extended_biosample_permission_token.json\"",
        "ABI_BIOSAMPLE_PATH = \"./smart_contract/Biosample.json\"",
        "ABI_POSP_PATH = \"./smart_contract/posp.json\"",
        "ABI_POSP_FACTORY_PATH = \"./smart_contract/posp_factory.json\"",
        "ABI_DELIVER_MANAGER_PATH = \"./smart_contract/DeliverManager.json\"",
        "",
        "#-WALLETS",
        f"BIOSAMPLE_EXECUTOR = \"{settings.EXECUTOR_PRIVATE_KEY}\"",
        f"ROOT_GENOBANK = <YOUR_ROOT_WALLET_PRIVATE_KEY>",
        f"ROOT_GENOBANK_WALLET = <YOUR_ROOT_WALLET_PUBLIC_ADDRESS>",
        "",
        "# STORAGE AND MAILS",
        "#-PERMITTEES ROUTES",
        "UPLOAD_FILES_CHUNKS = \"./storage/file_chunks\"",
        "PERMITEE_INSERTS = \"./storage/permittee_prod_inserts.json\"",
        "",
        "# API KEYS",
        f"MAGIC_API_KEY = <MAGIC_AUTH_API_KEY>",
    ]

    with open(out_file, 'w') as f:
        f.write("\n".join(lines) + "\n")
    print(f"✔ {out_file} generated.")

if __name__ == '__main__':
    generate_env()