async function getAvailableBuckets(root_signature){
	const response = await fetch(
    `${window.NEWAPIBASE}/get_buckets/${root_signature}`,{
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
  return response
}

async function getBucketRouteContent(root_signature, access_key, secret_key, bucket_name, route=""){
	params = {
		"root_signature":root_signature,
		"access_key":access_key,
		"secret_key":secret_key,
		"bucket_name":bucket_name,
		"route":route
	}
	const url = buildUrl(`${window.NEWAPIBASE}/get_protected_tree_bucket/`, params)

	const response = await fetch(url,{
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
  return response
}


function setForm(selectValues){
	var $select = $('.bucket-select');
	$select.empty();
	$select.append($('<option>', { value: '', text: 'Select Permittee Bucket Serial', selected: true }));
	var options = selectValues.map(function(item) {
			return $('<option>', {
					value: item.permittee_serial,
					text: item.permittee_serial
			});
	});
	$select.append(options);

}

function buildUrl(url, params) {
	let builtUrl = url;
	const queryParams = Object.keys(params).map(key => {
			return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
	}).join('&');
	if (queryParams.length) {
			builtUrl += '?' + queryParams;
	}
	return builtUrl;
}


function togglePassword(documentId) {
  var x = document.getElementById(documentId);
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}



async function startingMint(){
  const permitteSerial = $("#bucketSelect").val()
  const secretApi = $("#secretApi").val()
  let data = {
    permitte_serial: $("#bucketSelect").val(),
    secret_hash: createHMAC(permitteSerial, secretApi),
    files_folder_path: $("#inputBucketPath").val().slice(2),
    source_access_key: $("#inputAccessKey").val(),
    source_secret: $("#inputSecretKey").val(),
    source_name: $("#inputBucketName").val(),
    file_range: $("#inputFileRange").val()
  }
  let response = await initMint(data)
  console.log(response)
  let users = formatUserList(response["file_saved"])
  convertAndDownloadCSV(users, "datos")
  if (response["error_in_files"].length > 0){
    convertAndDownloadCSV(response["error_in_files"], "errors")
  }

}

function createHMAC(message, secret) {
  const hmac = CryptoJS.HmacSHA256(message, secret);
  return hmac.toString(CryptoJS.enc.Hex);
}

async function initMint (params){
  const uri = `${window.NEWAPIBASE}/massive_minter`
  let response = await fetch(
    urlFactory(uri, params),{
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
  }).then((res) => {
    return res.json()
  }).catch((error) => {
    console.error(error);
  })
  return response
}

function formatUserList(userList){
  let users = []
  let index = 0
  for (const user of userList){
    index ++;
    let row = {
      "id": user?.index,
      "Address": user?.userAddress,
      "Mnemonic": user?.mnemonic,
      "PrivateKey": user?.private_key,
      "Public_key": user?.public_key,
      "Biosample_serial": user?.biosample_serial,
      "Permitte_serial": user?.permitte_serial,
    }
    users.push(row)
  }
  return users
}

function convertAndDownloadCSV(jsonData, file_name) {
  let csv = Papa.unparse(jsonData, {
      header: true // Incluye el encabezado en el CSV
  });

  let csvFile = new Blob([csv], { type: "text/csv" });

  let downloadLink = document.createElement("a");
  downloadLink.download = `${file_name}.csv`;
  downloadLink.href = window.URL.createObjectURL(csvFile);
  downloadLink.style.display = "none";

  document.body.appendChild(downloadLink);
  downloadLink.click();
  document.body.removeChild(downloadLink);
}