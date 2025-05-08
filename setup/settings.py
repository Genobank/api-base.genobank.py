class settings:
	# # Custom Provider and executor wallet privet key
	# PROVIDER =  <YOUR PROVIDER>
	# The private key of your executor wallet must have sufficient funds
	# EXECUTOR_PRIVATE_KEY = <YOUR EXECUTOR WALLET PRIVATE KEY>

	# Biosample Permission Token Cinstructor
	BPT_NAME = "Biosample Permission Token"
	BPT_SYMBOL = "BPT"
	BPT_NAMESPACE = "io.genobank.test"

	# Extended Biosample Permission Token Constructor
	XBPT_NAME = "Extended Biosample Permission Token"
	XBPT_SYMBOL = "XBPT"

	# Biosample Constructor
	BIOSAMPLE_URI = "https://genobank.io/"
	# Delivery Manager Constructor
	USDNA_CONTRACT = "0xB973E2B66f925bFA8206FEF61A1d89D2A664Cd23"

	OUTPUT_ENV_FILE_NAME = "generated.env"
	COPY_ENV_TO_PROJECT_ROOT  = True

	# JSON files of the JSON Interface of the necessary contracts
	ABI_BPT_PATH = "../smart_contract/biosample-permission-token.json"
	ABI_XBPT_PATH = "../smart_contract/extended_biosample_permission_token/extended_biosample_permission_token.json"
	ABI_BIOSAMPLE_PATH = "../smart_contract/Biosample.json"
	ABI_POSP_PATH = "../smart_contract/posp.json"
	ABI_POSP_FACTORY_PATH = "../smart_contract/posp_factory.json"
	ABI_DELIVER_MANAGER_PATH = "../smart_contract/DeliverManager.json"