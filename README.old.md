# api.genobank.io

This is the API documentation for the [Genobank](https://genobank.io) API.

This API is ONLY for use by the Genobank team.
This API is ONLY to create new Permittees on the Test and Production Environment.

## Installing the dependencies
Before to download this repository, you need to install the following dependencies:
```sh
npm install
```
If this not works you can try with
```sh
sudo apt install npm
```
To start this API you need install virtual env using the following command:
```sh
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

Next to this, you need to create a virtual enviroment using the following command:
Firs create a folder, enter on it and run the following command:

```sh
virtualenv <name_of_enviroment>
```

The '<name_of_enviroment>' can be any name you want.
This will create a folder, enter it and create a folder with the name you want and enter it.
Now download the repository using the following command:

```sh
git init
git remote add origin https://github.com/Genobank/api.genobank.io.py.git
git pull origin master
```


Then you need to activate the virtual env using the following command:

```sh
. ../bin/activate
```

Install all the dependencies using the following command:
```sh
pip install -r requirements.txt
```
## Configuring the env for the file
First, create a new `.env` file with the content below. Make sure that each variable is set to the correct value.
```sh
# ENVIROMENT
# GENERAL SETTINGS
ENVIROMENT = <ENVIROMENT>
PORT = <API_PORT>
APP_SECRET = <YOUR_SECRET_APPLICATION>
BIOSAMPLE_ACTIVATION_SECRET = <YOUR_BIOSAMPLE_ACTIVATION_SECRET>
NAMESPACE = "io.genobank.test"
MESSAGE = <MESSAGE_TO_RECOVER_SIGNATURE>
NEW_MESSAGE = <SECOND_MESSAGE_TO_MULTIPLE_SIGNATURES>
ROOT_MESSAGE = <BACK_END_SIGN_MESSAGE>

#--BUCKETS
BUCKET_PATH = <BUCKET_PATH>
BUCKET_ACCESS_KEY_ID = <BUCKET_ACCESS_KEY_ID>
BUCKET_SECRET_ACCESS_KEY_ID = <BUCKET_SECRET_ACCESS_KEY_ID>
BUCKET_NAME = <BUCKET_NAME>

# API(S)
API_PERMITTEES = <YOUR_PRODUCTION_API_PERMITTEE_APPLICATION>
TEST_API_PERMITTEES = <YOUR_PRODUCTION_API_PERMITTEE_APPLICATION>

# DATABASE CONF (mongo db)
MONGO_DB_HOST = <YOUR_DATABASE_URL_CONNECTION>
DB_NAME = <DATABASE_NAME>


#--BLOCKCHAIN CONFIGURATIONS
#-PROVIDER
PROVIDER = <YOUR RINKEBY NODE WITH KEY>
CUSTOM_PROVIDER = "https://api.avax-test.network/ext/bc/C/rpc"

# SMARTCONTRACT
SMART_CONTRACT = <PRODUCTION_SMARTCONTRACT_ADDRESS>
TEST_SMART_CONTRACT = <TEST_SMARTCONTRACT_ADDRESS>
TEST_BIOSAMPLE_COTRACT = <TEST_BIOSAMPLE_SMARTCONTRACT_ADDRESS>
# ABI ROUTE
ABI_SM_PATH = <./IN/PROJECT/SMARTCONTRACT_JSONINTERFACE/FILE/PATH.json>
ABI_BIOSAMPLE_PATH = <./IN/PROJECT/BIOSAMPLE_SMARTCONTRACT_JSONINTERFACE/FILE/PATH.json>
# WALLET EXECUTOR
ROOT_KEY_EXECUTOR = <PRODUCTION_EXECUTOR_PRIVATE_KEY>
TEST_ROOT_KEY_EXECUTOR = <TEST_EXECUTOR_PRIVATE_KEY>
BIOSAMPLE_EXECUTOR = <TEST_BIOSAMPLE_EXECUTOR_PRIVATE_KEY>
ROOT_GENOBANK = <ROOT_GENOBANK_WALLET_PRIVATE_KEY>
ROOT_GENOBANK_WALLET = <ROOT_GENOBANK_WALLE_ADDRESS>

#--STORAGE
# FILE ROUTES (Static values, Do not modify)
PERMITEE_INSERTS = "./storage/permittee_prod_inserts.json"
TEST_PERMITEE_INSERTS = "./storage/permittee_test_inserts.json"

EMAIL = <GENOBANK_EMAIL_SUPPORT>
EMAIL_PASS = <EMAIL_PASSWORD>
```

## Running the API
Now you can run the API using the following command:
on the folder where you have downloaded the repository run the following command:
```sh
python3 start.py
```
to check if the API is running, open yor favourite web browser and go to http://localhost:8081/

Now you can go to 
* http://localhost:8081/adminpage  To create a permittee on PRODUCTION enviroment
* http://localhost:8081/adminpage/test  To create a permittee on TEST enviroment

## Pushing the repository
If you want to push the repository, does you will need configure the `.gitignore` file as the follow:

```sh
.env
.gitignore
```


# Endpoints
## How to connect to the DTCFILE dispatcher service
Using an http client you must call the endpoints in the following way

 
## save_genotype
Saving the DTC file
To save the DTC File You have to send
### POST
```sh
http://localhost:8081/save_genotype?data={"agreements":{"questions":"1. I have been offered the opportunity to ask questions about SOMOS ANCESTRIA, including about the benefits, risks and limitations of using SOMOS ANCESTRIA.","document":"2. I have read and understood this document in its entirety and realize I may retain a copy for my records","read":"3. I have read and understood SOMOS ANCESTRIA’s Privacy Policy and Terms of Use .","permission":"4. I confirm that I'm the owner or the lawful custodian of this Raw Dataset.","providing":"5. I consent to SOMOS ANCESTRIA analyzing my Raw Data and providing an analysis of my Traits based on SOMOS ANCESTRIA current knowledge and research.","results":"6. I will discuss the results with my healthcare provider/genetic counselor if I have any medical or health-related questions or concerns.","analysis":"7. I consent to SOMOS ANCESTRIA’ ongoing analysis and use of my Raw Data as described herein.","contacted":"8. I consent to being contacted by or on behalf of SOMOS ANCESTRIA about research studies for which I may be eligible. I understand I am under no obligation to participate in any research studies about which I am contacted."},"labAddress":"0xD85D1F5Fd5af08cdE8b99Eff4921573503921266","permittee":"0xD85D1F5Fd5af08cdE8b99Eff4921573503921266","serial":150,"signature":"0x8245b0134972f2cc6befca49a17415818f46756c5d3b7a491faa0526379b5a981048075abd662f82ba8c97d8f0dc01f10665425b1287a8d8632ddd9a2f4479ac1c","updatePermission":{},"genetic_test":"23andme","extension":"txt","userAddress":"0xC3a76b4c6A1fA08c50185B3A3dEe1f17517cc8fd","filesigned":"0x147da335a6090bcce7aadba77acd75f0e900d8a567942cd28aaf63941c24ad2f1599a2457d1d100207563b703cb5f2eb980f4af0b334d90cf657958c2a5890ea1b","filesize":44645011}
```
## find_file
### POST
```sh
http://localhost:8081/find_genotypes?owner=

```
`owner`: public address of the user's wallet