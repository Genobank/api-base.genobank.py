from pymongo import MongoClient
import os
import datetime
from ast import literal_eval
import re
import io
import zipfile
import gzip
import binascii








class file_dao:
	def __init__(self):
		self.client = MongoClient(os.getenv('MONGO_DB_HOST'))
		self.db = self.client[os.getenv('DB_NAME')]
		self.table = self.db.files

	def get_snips(self, file_lines):
		count = 0
		_json_snips = {
			'rs952718':"",'rs7803075':"",'rs9319336':"",'rs2397060':"",'rs1344870':"",'rs2946788':"",
			'rs6591147':"",'rs2272998':"",'rs7229946':"",'rs9951171':"",'rs525869':"",'rs530501':"",
			'rs2040962':"", 'rs2032624':"", 'rs1865680':"", 'rs17307398':"", 'rs3795366':"", 'rs2460111':"",
			'rs1675126':"", 'rs1061629':"", 'rs538847':"", 'rs76432344':"", 'rs3750390':"", 'rs1624844':"",
			'rs3803390':"", 'rs2293768':"", 'rs9358890':"", 'rs11197835':"", 'rs1806191':"", 'rs7953':"",
			'rs3736757':"", 'rs2940779':"", 'rs7522034':"", 'rs6107027':"", 'rs2275059':"", 'rs3746805':"",
			'rs4953042':"", 'rs3817098':"", 'rs6965201':"", 'rs5998':"", 'rs7259333':"", 'rs1802778':"",
			'rs907157':"",'rs8064024':"",'rs3749970':"",'rs7933089':"",'rs2292745':"",'rs1799932':"",
			'rs4078313':"",'rs2266918':"",'rs805423':"",'rs540261':"",'rs3734586':"",'rs3753886':"",
			'rs3210635':"" ,'rs2294024':"" ,'rs3812471':"" ,'rs7786497':"" ,'rs1128933':"" ,'rs4656':"" ,
			'rs238148':"", 'rs2074265':"", 'rs11274':"", 'rs10069050':"", 'rs3736510':"", 'rs2304891':"",
			'rs9482':"", 'rs1137930':"", 'rs1058486':"", 'rs27529':"", 'rs3177137':"", 'rs1043615':"", 
			'rs1054975':"", 'rs1060817':"", 'rs2232818':"",'rs2273235':"",'rs11054':"",'rs2236277':"",
			'rs2293250':"",'rs3182911':"",'rs4799':"",'rs13030':"",'rs547497':"",'rs13180':"",
			'rs957448':"",'rs3108237':"",'rs164572':"",'rs2175593':"",'rs2306641':"",'rs1594':"",
			'rs7300444':"",'rs1057908':"",'rs2152092':"",'rs2358996':"",'rs4075325':"",'rs1057925':""
		}
		array_snips = []
		for line in file_lines:
			count+=1

			decoded_line = str(line.decode('utf8'))
	

			if(self.snipid_in_line(decoded_line)):
				line_elements = decoded_line[:-1]
				line_elements = line_elements.split("\t")
				genotype = line_elements[3].replace("\n", "")
				genotype = genotype.replace("\r", "")
				_json_snips[line_elements[0]] = genotype
		for i in _json_snips:
			array_snips.append(_json_snips[i])
		return array_snips
	


	def get_optimized_snips(self, text):
		try:
			_json_snips = {
				'rs952718':"",'rs7803075':"",'rs9319336':"",'rs2397060':"",'rs1344870':"",'rs2946788':"",
				'rs6591147':"",'rs2272998':"",'rs7229946':"",'rs9951171':"",'rs525869':"",'rs530501':"",
				'rs2040962':"", 'rs2032624':"", 'rs1865680':"", 'rs17307398':"", 'rs3795366':"", 'rs2460111':"",
				'rs1675126':"", 'rs1061629':"", 'rs538847':"", 'rs76432344':"", 'rs3750390':"", 'rs1624844':"",
				'rs3803390':"", 'rs2293768':"", 'rs9358890':"", 'rs11197835':"", 'rs1806191':"", 'rs7953':"",
				'rs3736757':"", 'rs2940779':"", 'rs7522034':"", 'rs6107027':"", 'rs2275059':"", 'rs3746805':"",
				'rs4953042':"", 'rs3817098':"", 'rs6965201':"", 'rs5998':"", 'rs7259333':"", 'rs1802778':"",
				'rs907157':"",'rs8064024':"",'rs3749970':"",'rs7933089':"",'rs2292745':"",'rs1799932':"",
				'rs4078313':"",'rs2266918':"",'rs805423':"",'rs540261':"",'rs3734586':"",'rs3753886':"",
				'rs3210635':"" ,'rs2294024':"" ,'rs3812471':"" ,'rs7786497':"" ,'rs1128933':"" ,'rs4656':"" ,
				'rs238148':"", 'rs2074265':"", 'rs11274':"", 'rs10069050':"", 'rs3736510':"", 'rs2304891':"",
				'rs9482':"", 'rs1137930':"", 'rs1058486':"", 'rs27529':"", 'rs3177137':"", 'rs1043615':"", 
				'rs1054975':"", 'rs1060817':"", 'rs2232818':"",'rs2273235':"",'rs11054':"",'rs2236277':"",
				'rs2293250':"",'rs3182911':"",'rs4799':"",'rs13030':"",'rs547497':"",'rs13180':"",
				'rs957448':"",'rs3108237':"",'rs164572':"",'rs2175593':"",'rs2306641':"",'rs1594':"",
				'rs7300444':"",'rs1057908':"",'rs2152092':"",'rs2358996':"",'rs4075325':"",'rs1057925':""
			}

			lineas = text.split('\n')

			for linea in lineas:
				if linea.startswith('#'):
					continue

				# Dividir la línea en partes (asumiendo que está separada por tabuladores)
				partes = linea.strip().split('\t')
				snp = partes[0]

				# Verificar si el SNP está en la lista de interés y actualizar el diccionario
				if snp in _json_snips:
					_json_snips[snp] = partes[3]  # Asumiendo que la posición 3 contiene el genotipo

			# Retornar el diccionario actualizado
			return _json_snips
		except:
			return False



	def snipid_in_line(self, line):
		pref_list = [
			'rs952718\t', 'rs7803075\t', 'rs9319336\t', 'rs2397060\t', 'rs1344870\t', 'rs2946788\t',
			'rs6591147\t', 'rs2272998\t', 'rs7229946\t', 'rs9951171\t', 'rs525869\t', 'rs530501\t',
			'rs2040962\t', 'rs2032624\t', 'rs1865680\t', 'rs17307398\t', 'rs3795366\t', 'rs2460111\t',
			'rs1675126\t', 'rs1061629\t', 'rs538847\t', 'rs76432344\t', 'rs3750390\t', 'rs1624844\t',
			'rs3803390\t', 'rs2293768\t', 'rs9358890\t', 'rs11197835\t', 'rs1806191\t', 'rs7953\t',
			'rs3736757\t', 'rs2940779\t', 'rs7522034\t', 'rs6107027\t', 'rs2275059\t', 'rs3746805\t',
			'rs4953042\t', 'rs3817098\t', 'rs6965201\t', 'rs5998\t', 'rs7259333\t', 'rs1802778\t',
			'rs907157\t','rs8064024\t','rs3749970\t','rs7933089\t','rs2292745\t','rs1799932\t',
			'rs4078313\t','rs2266918\t','rs805423\t','rs540261\t','rs3734586\t','rs3753886\t',
			'rs3210635\t','rs2294024\t','rs3812471\t','rs7786497\t','rs1128933\t','rs4656\t',
			'rs238148\t','rs2074265\t','rs11274\t','rs10069050\t','rs3736510\t','rs2304891\t',
			'rs9482\t','rs1137930\t','rs1058486\t','rs27529\t','rs3177137\t','rs1043615\t',
			'rs1054975\t','rs1060817\t','rs2232818\t','rs2273235\t','rs11054\t','rs2236277\t',
			'rs2293250\t','rs3182911\t','rs4799\t','rs13030\t','rs547497\t','rs13180\t',
			'rs957448\t','rs3108237\t','rs164572\t','rs2175593\t','rs2306641\t','rs1594\t',
			'rs7300444\t','rs1057908\t','rs2152092\t','rs2358996\t','rs4075325\t','rs1057925\t'
		]
		res = line.startswith(tuple(pref_list))
		return res


	def exists_snips(self, snips_array):
		all_snips = self.find_all()
		if not all_snips:
			return False
		else:
			for doc in all_snips:
				docsnips = literal_eval(doc["snips"])
				matches = [i for i, j in zip(docsnips, snips_array) if i == j]
				matches = len(matches)
				prob = (100/96)*matches
				if prob > 93:
					print(f'FOUND FINGUERPRINT::: {doc["snips"]}')
					print(f'MY CURRENT FINGUERPRINT::: {snips_array}')
					raise Exception("Unique SNP Fingerprint Test Failed:  This raw data file already exists, please email support@genobank.io if you're the owner and can't login with your previous DNA Wallet (Previous 12 seed phrase lost).  A new DNA test Kit might be necessary to recover your account.")
	


	def exists_snips_optimized(self, snips_array):
		# puede_insertar = True
		for documento in self.find_all():
				similitud = self.jaccard_similarity(documento.get('snips', []), snips_array)
				if similitud > 0.90:
						raise Exception("Unique SNP Fingerprint Test Failed:  This raw data file already exists, please email support@genobank.io if you're the owner and can't login with your previous DNA Wallet (Previous 12 seed phrase lost).  A new DNA test Kit might be necessary to recover your account.")
						

	



	def jaccard_similarity(self, list1, list2):
		set1 = set(list1)
		set2 = set(list2)
		intersection = set1.intersection(set2)
		union = set1.union(set2)
		return len(intersection) / len(union)



	def Source(self, line):
		if "23andMe" in line:
			source = 0
		elif "Ancestry" in line:
			source = 1
		elif line.startswith("RSID"):
			source = 2
		elif "MyHeritage" in line:
			source = 3
		elif "Living DNA" in line:
			source = 4
		elif re.match("^#*[ \t]*rsid[, \t]*chr", line):
			source = 5
		elif "Genes for Good" in line:
			source = 6
		elif "PLINK" in line:
			source = 7
		else:
			source = -1
		return source

	def Is_zip(self, bytes_data):
		return zipfile.is_zipfile(bytes_data) 
		
	def Is_gzip(self, bytes_data):
		return binascii.hexlify(bytes_data[:2]) == b"1f8b"
		
	def Extract_source(self, a, decode=False):
		first_line = self.Read_line(a, decode)
		return self.Source(first_line)
			
	def Read_line(self, file, decode):
		if decode:
			return file.readline().decode("utf8")
		else:
			return file.readline()
	
	
	
	
	def Manejador(self, dtc):
		try:
			if self.Is_gzip(dtc):
				with gzip.open(io.BytesIO(dtc), "rb") as f1:
					source = self.Extract_source(f1,decode=True)
			elif self.Is_zip(dtc):
				with zipfile.ZipFile(io.BytesIO(dtc)) as z:
					namelist = z.namelist()[0]
					with z.open(namelist, "r") as f:
						source = self.Extract_source(f1,decode=True)
			else:
				file = io.BytesIO(dtc)
				source = self.Extract_source(file,decode=True)
			return source
		except:
			raise Exception("No valid File, upload a TXT dtc file, change your file and try again")

	def save_db_snips(self, snips, data):
		try:
			_fields = {
				"owner": str(data["userAddress"]).upper(),
				"snips": snips,
				"tag":"test",
				"created": datetime.datetime.now(),
				"updated": datetime.datetime.now()
			}
			self.table.insert_one(_fields)
			return True
		except:
			return False

	def find_all(self):
		try:
			cur = self.table.find()
			row = []
			for doc in cur:
				for key in doc:
					if (not isinstance(doc[key], str)) or (not isinstance(doc[key], int)) or (not isinstance(doc[key], float)):
						doc[key] = str(doc[key])
				row.append(doc)
			return row
		except Exception as e:
			print(e)
			return False
