async function checkRootUser (sign){
	let validated = await fetch(
	  `${window.NEWAPIBASE}/validate_root_user/${sign}`,{
		method: 'GET',
		header: {
		  'Content-Type': 'application/json',
		  'Access-Control-Allow-Origin': '*'
		},
	}).then((res) => {
	  return res.json()
	}).catch((error) => {
	  console.error(error);
	})
	return validated
  }



  async function getAllProducts() {
	const uri = `${window.NEWAPIBASE}/get_all_products_in_shop`
	let requests_lab_list = await fetch(uri, {
		method: 'GET',
		headers: {
		  'Content-Type': 'application/json'
		}
	  })
	  .then(response => response.json())
	  .then(data => {
		return data
	  })
	  .catch(error => console.error(error));
	return requests_lab_list
  
  }


  async function getAllSales() {
	const uri = `${window.NEWAPIBASE}/get_all_sales_in_shop`
	let saleList = await fetch(uri, {
		method: 'GET',
		headers: {
		  'Content-Type': 'application/json'
		}
	  })
	  .then(response => response.json())
	  .then(data => {
		return data
	  })
	  .catch(error => console.error(error));
	return saleList
  
  }



  async function getSaleById(sale_id) {
	const uri = new URL(`${window.NEWAPIBASE}/get_sale_by_id_in_shop`);
	uri.searchParams.append('mongo_sale_id', sale_id);
	let sale = await fetch(uri, {
		method: 'GET',
		headers: {
		  'Content-Type': 'application/json'
		}
	  })
	  .then(response => response.json())
	  .then(data => {
		return data
	  })
	  .catch(error => console.error(error));
	return sale
  }

  async function updateProduct(root_signature, metadata, file) {
	const uri = new URL(`${window.NEWAPIBASE}/update_product_shop`);
	const formData = new FormData();
	formData.append('root_signature', root_signature);
	formData.append('metadata', JSON.stringify(metadata));
	if (file) {
	  formData.append('image_file', file);
	}
	console.log(uri);
	let requests_lab_list = await fetch(uri, {
	  method: 'POST',
	  body: formData
	})
	.then(response => response.json())
	.then(data => {
	  return data;
	})
	.catch(error => console.error(error));
	return requests_lab_list;
  }
  

  async function addProduct(root_signature, metadata, file) {
	const uri = new URL(`${window.NEWAPIBASE}/add_product_shop`);
	const formData = new FormData();
	formData.append('root_signature', root_signature);
	formData.append('metadata', JSON.stringify(metadata));
	if (file) {
	  formData.append('image_file', file);
	}
	console.log(uri);
	let requests_lab_list = await fetch(uri, {
	  method: 'POST',
	  body: formData
	})
	.then(response => response.json())
	.then(data => {
	  return data;
	})
	.catch(error => console.error(error));
	return requests_lab_list;
  }


  async function deleteProduct(root_signature, metadata) {
	const uri = new URL(`${window.NEWAPIBASE}/delete_product_shop`);
	const formData = new FormData();
	formData.append('root_signature', root_signature);
	formData.append('metadata', JSON.stringify(metadata));
	console.log(uri);
	let requests_lab_list = await fetch(uri, {
	  method: 'POST',
	  body: formData
	})
	.then(response => response.json())
	.then(data => {
	  return data;
	})
	.catch(error => console.error(error));
	return requests_lab_list;
  }

  async function getAllDeliveries(){
	const uri = `${window.NEWAPIBASE}/deliveries`
	let requests_lab_list = await fetch(uri, {
		method: 'GET',
		headers: {
		  'Content-Type': 'application/json'
		},
	  })
	  .then(response => response.json())
	  .then(data => {
		return data
	  })
	  .catch(error => console.error(error));
	return requests_lab_list
  }


  async function getRawDataDeliveries(rootSignature) {
	const uri = new URL(`${window.NEWAPIBASE}/raw_data_deliveries`)
	uri.searchParams.append("root_signature", rootSignature)
	let requests_lab_list = await fetch(uri, {
		method: 'GET',
		headers: {
		  'Content-Type': 'application/json'
		}
	  })
	  .then(response => response.json())
	  .then(data => {
		return data
	  })
	  .catch(error => console.error(error));
	return requests_lab_list
  
  }


  async function getTokenHolders(rootSignature) {
	const uri = new URL(`${window.NEWAPIBASE}/api_somos_dao/get_all_registrations`)
	uri.searchParams.append("root_signature", rootSignature)
	let requests_lab_list = await fetch(uri, {
		method: 'GET',
		headers: {
		  'Content-Type': 'application/json'
		}
	  })
	  .then(response => response.json())
	  .then(data => {
		return data
	  })
	  .catch(error => console.error(error));
	return requests_lab_list
  
  }




async function postDeliveryRawData(data, callBack) {
	const url = `${window.NEWAPIBASE}/deliver_raw_data_from_root`;
	const config = {
		headers: {
			"Content-Type": "multipart/form-data"
		},
		onUploadProgress: callBack,
	};
	try {
		const res = await axios.post(url, data, config);
		console.log("this is the normal response\n", res);
		return res;
	} catch (err) {
		console.log("Error completo:", err);
		throw err; // Lanzar el error para que pueda ser capturado por el llamador
	}
}



async function postToggleSaleStatus(data) {
	const url = `${window.NEWAPIBASE}/toggle_sales_status_from_root`;
	const config = {
		headers: {
			"Content-Type": "multipart/form-data"
		},
	};
	try {
		const res = await axios.post(url, data, config);
		console.log("this is the normal response\n", res);
		return res;
	} catch (err) {
		console.log("Error completo:", err);
		throw err; // Lanzar el error para que pueda ser capturado por el llamador
	}
}


async function generateNationalUSPSLabel(root_signature, sale_id) {
	const uri = new URL(`${window.NEWAPIBASE}/create_national_usps_label`);
	return await fetch(uri, {
	  method: 'POST',
	  headers: { 'Content-Type': 'application/json' },
	  body: JSON.stringify({
		root_signature: root_signature,
		sale_id: sale_id
	  }),
	})
	.then(response => response.json())
	.then(data => data)
	.catch(error => console.error(error));
}



async function generateActivationLinkAndNationalUSPSLabel(root_signature, sale_id, biosample_serial, permittee_serial, prefix) {
	const uri = new URL(`${window.NEWAPIBASE}/create_activation_link_and_national_usps_label`);
	return await fetch(uri, {
	  method: 'POST',
	  headers: { 'Content-Type': 'application/json' },
	  body: JSON.stringify({
		root_signature: root_signature,
		sale_id: sale_id,
		physical_id: prefix + biosample_serial,
		biosample_serial: parseInt(biosample_serial),
		permittee_serial: parseInt(permittee_serial),
		prefix: parseInt(prefix),
		domain: window.WWW_BASE 
	  }),
	})
	.then(response => response.json())
	.then(data => data)
	.catch(error => console.error(error));
}
  


async function getNationalLabelPresignedLinks(root_signature, sale_id) {
	const uri = new URL(`${window.NEWAPIBASE}/get_national_usps_label_presigned_links`);
	return await fetch(uri, {
	  method: 'POST',
	  headers: { 'Content-Type': 'application/json' },
	  body: JSON.stringify({
		root_signature: root_signature,
		sale_id: sale_id
	  }),
	})
	.then(response => response.json())
	.then(data => data)
	.catch(error => console.error(error));
  }