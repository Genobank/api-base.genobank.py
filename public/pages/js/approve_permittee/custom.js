let provider
let apiMessage = $("#apiMessage").val()
let userWallet
let currentSelectedPermittee
let web3
let root_sign

// const rejectModal = document.getElementById('rejectModal');
const modal = $(".modal")

if (typeof window.ethereum !== 'undefined' || typeof window.web3 !== 'undefined') {
  // Metamask is installed
  $(async function () {
    provider = new ethers.providers.Web3Provider(window.ethereum);
    await window.ethereum.request({ method: 'eth_requestAccounts' });
    if (localStorage.getItem('user_sign') == "null" || localStorage.getItem('user_sign') == null) {
      let sign_autentication = await provider.getSigner().signMessage(apiMessage);
      localStorage.setItem('user_sign', sign_autentication);
    }
    root_sign = localStorage.getItem('user_sign');

    let valid_user = await checkRootUser(root_sign)
    if (!valid_user){
      throw_alert_message(`Error 401: Unauthorized user: Your ${root_sign} key is not valid`);
      throw "No valid root address"
    }

    $(".panel-full-container").show()
    let list = await getAllPermitteeRequests(root_sign)
    let deliveries_list = await getAllDeliveries()
    let allBiosampleWithPendingVariants = await getAllBiosampleWithPendingVariants(root_sign)
    let permitteeBuckets  = await getPermitteeBuckets(root_sign)
    console.log("Buckets", permitteeBuckets)
    renderPendingTable(list)
    renderApprovedTable(list)
    renderRejectedTable(list)
    renderDeliveries(deliveries_list)
    renderBiosamplesWithPendingVariants(allBiosampleWithPendingVariants)
    renderPermitteeBuckets(permitteeBuckets)
    $("#loading_spinner").hide()
  })
  
} else {
  // Metamask is not installed
  console.log("You not have Metamask installed")
}

window.ethereum.on('accountsChanged', function () {
  localStorage.setItem('user_sign', null);
  window.location.reload();
})



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


async function getAllPermitteeRequests(_userSignature) {
  const uri = `${window.NEWAPIBASE}/get_permittee_requests`
  let requests_lab_list = await fetch(uri, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ root_signature: _userSignature })
    })
    .then(response => response.json())
    .then(data => {
      return data
    })
    .catch(error => console.error(error));
  return requests_lab_list

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

async function getAllBiosampleWithPendingVariants(_userSignature) {
	const url = new URL(`${window.NEWAPIBASE}/get_all_pending_variants`)
	url.searchParams.append('root_signature', _userSignature);
	return fetch(url, {
		method: "GET",
		header: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*'
		},
	}).then((res) => {
		return res.json();
	}).catch((error) => {
		return { error: error.message };
	});
}

async function getPermitteeBuckets(_userSignature) {
	const url = new URL(`${window.NEWAPIBASE}/get_permittee_buckets`)
	url.searchParams.append('root_signature', _userSignature);
	return fetch(url, {
		method: "GET",
		header: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*'
		},
	}).then((res) => {
		return res.json();
	}).catch((error) => {
		return { error: error.message };
	});
}


async function getvariantParticipants(_userSignature, biosampleSerial){
  const url = new URL(`${window.NEWAPIBASE}/get_participant_of_biosample`)
	url.searchParams.append('root_signature', _userSignature);
	url.searchParams.append('biosample_serial', biosampleSerial);
	return fetch(url, {
		method: "GET",
		header: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*'
		},
	}).then((res) => {
		return res.json();
	}).catch((error) => {
		return { error: error.message };
	});
}

async function getParticipantVariants(root_signature, biosampleSerial, participantSerial){
  const url = new URL(`${window.NEWAPIBASE}/get_participant_variants`)
	url.searchParams.append('root_signature', root_signature);
	url.searchParams.append('biosample_serial', biosampleSerial);
	url.searchParams.append('participant_serial', participantSerial);
	return fetch(url, {
		method: "GET",
		header: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*'
		},
	}).then((res) => {
		return res.json();
	}).catch((error) => {
		return { error: error.message };
	});
}


async function selectWinner(rootSignature, biosampleSerial, notarizerSerial) {
	const data = {
    root_signature: rootSignature,
    biosample_serial: parseInt(biosampleSerial),
    notarizer_serial: parseInt(notarizerSerial)
	};
	const url = new URL(`${window.NEWAPIBASE}/select_winning_participant`);
	const response = await fetch(url, {
			method: 'POST',
			headers: {
					'Content-Type': 'application/json',
			},
			body: JSON.stringify(data)
	});
	if (!response.ok) {
			// Intentar obtener el mensaje de error del cuerpo de la respuesta
			const errorData = await response.json();
			const errorMessage = errorData.message || 'Error desconocido';
			throw new Error(`Error ${response.status}: ${errorMessage}`);
	}

	const result = await response.json();
	return result;
}






async function renderPendingTable(permittees_list){
  let pending_list = permittees_list.filter(perm => perm.status === 0);
  let innerTableBody = ``

  for (i in pending_list){
    innerTableBody+= `
    <tr>
      <td><img src="${pending_list[i].text.logo}" width="66px" height="44px"></td>
      <td>${pending_list[i].owner}</td>
      <td>${pending_list[i].text.name}</td>
      <td>
        <button type="button" data-owner="${pending_list[i].owner}" onclick="setCurrentOwner(this)" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#approvalModal">Approve</button>
        <button type="button" data-owner="${pending_list[i].owner}" onclick="setCurrentOwner(this)" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#rejectModal">Reject</button>
        </td>
    </tr>
    `
  }

  $("#pending-lab-body").html(innerTableBody)
}

async function renderApprovedTable(permittees_list){
  let approved_list = permittees_list.filter(perm => perm.status === 1);
  let innerTableBody = ``
  for (i in approved_list){
    innerTableBody+= `
    <tr>
      <td><img src="${approved_list[i].text.logo}" width="66px" height="44px"></td>
      <td>${approved_list[i].owner}</td>
      <td>${approved_list[i].text.name}</td>
      <td>${approved_list[i].serial}</td>
      <td>
      </td>
    </tr>
    `
  }


  $("#approved-lab-body").html(innerTableBody)
}

async function renderRejectedTable(permittees_list){
  let rejected_list = permittees_list.filter(perm => perm.status === 2);
  let innerTableBody = ``
  for (i in rejected_list){
    innerTableBody+= `
    <tr>
      <td><img src="${rejected_list[i].text.logo}" width="66px" height="44px"></td>
      <td>${rejected_list[i].owner}</td>
      <td>${rejected_list[i].text.name}</td>
      <td>

      </td>
    </tr>
    `
  }
  

  $("#rejected-lab-body").html(innerTableBody)
}

function renderDeliveries(deliveries_list){
  let innerTableBody = ``
  if (deliveries_list.data.length > 0){
    for (delivery of deliveries_list.data){
      let sharedFiles = ``
      for (file in delivery.files){
        sharedFiles+=file+"<br>"
      }
      innerTableBody+= `
      <tr>
        <td>${delivery.biosample_serial}</td>
        <td style="text-align: center;">
          <a href="https://testnet.snowtrace.io/address/${delivery.owner}" target="_blank" title="${delivery.owner}">
            ${delivery.owner.substr(0,10)}...${delivery.owner.substr(delivery.owner.length-10,delivery.owner.length)}
          </a
        </td>
        <td>${delivery.permittee_id}</td>
        <td>${delivery.permittee_wallet}</td>
        <td>${sharedFiles}</td>
        <td style="text-align: center;">
          <a href="https://testnet.snowtrace.io/tx/${delivery.tx_hash}" target="_blank" title="${delivery.tx_hash}">
            ${delivery.tx_hash.substr(0,10)}...${delivery.tx_hash.substr(delivery.tx_hash.length-10,delivery.tx_hash.length)}
          </a>
        </td>
      </tr>
      `
    }
  }
  $("#deliveries-lab-body").html(innerTableBody)
}


function renderBiosamplesWithPendingVariants(biosamplesWithVariants){
  console.log("biosamples with pending variants: ", biosamplesWithVariants)
  let innerTableBody = ``
  if (biosamplesWithVariants.data.length > 0){
    for (biosample of biosamplesWithVariants.data){
      innerTableBody+= /*html */ `
      <tr>
        <td>${biosample?.serial}</td>
        <td>${biosample?.owner}</td>
        <td>${biosample?.status}</td>
        <td>${biosample?.createdAt}</td>
      </tr>
      `
    }
  }
  $("#biosample-with-pending-variants-body").html(innerTableBody)

}

async function renderParticipantsByWallet(biosampleSerial){
  $("#biosamples-with-pending-variants-table").hide()
  $("#variants-pending-participants-section").show()
  $("#spinner-variant-container").show()
  let divContent = ``
  let participantsTableBody = $("#variants-pending-participants-body")
  participantsTableBody.empty()
  const variantParticipants = await getvariantParticipants(root_sign, biosampleSerial)
  $("#spinner-variant-container").hide()

  if (variantParticipants.length > 0) {
    for (const participants of variantParticipants) {
      const participantInfo= extractJsonFromText(participants?.text)
      console.log(participantInfo)
      participantsTableBody.append(/*html */`
        <tr onclick="showVariantsModal(${biosampleSerial}, ${participants?.serial})">
          <td class="text-start"><img src="${participantInfo?.logo}" class="img-sizer">
          <td>${participantInfo?.name}</td>
          <td>${participantInfo?.investigator}</td>
          <td>${participantInfo?.email}</td>
        </tr>
        `
      )
    }
  }
  console.log("variant participants: ",variantParticipants)
}

function renderPermitteeBuckets (bucketList){
  console.log("bucketList ", bucketList)
  let innerTableBody = ``
  if (bucketList.length > 0){
    for (bucket of bucketList){
      const profileJson = extractJsonFromText(bucket?.profile?.text)
      const bucketShortData = {
        permittee_serial: bucket?.permittee_serial,
        bucket_name: bucket?.bucket_name,
        access_key_id: bucket?.access_key_id,
        secret_access_key: bucket?.secret_access_key,
        permittee: bucket?.permittee
      }
      console.log(profileJson)
      innerTableBody+= /*html */ `
      <tr>
        <td>${bucket?.permittee_serial}</td>
        <td>${shortWallet(bucket?.permittee)}</td>
        <td>${profileJson?.name}</td>
        <td>${bucket?.bucket_name}</td>
        <td>${bucket?.access_key_id}</td>
        <td>
          <span class="secret-key">${'*'.repeat(bucket?.secret_access_key.length)}</span>
          <button type="button" class="btn btn-sm btn-light toggle-key-btn" data-key="${bucket?.secret_access_key}" onclick="toggleSecretKey(this)">
            <i class="fa-solid fa-eye"></i>
          </button>
        </td>
        <td>
          <button type="button" class="btn btn-sm btn-primary" onclick="openEditModalBucket('${encodeURIComponent(JSON.stringify(bucketShortData))}')" > Edit </button>
        </td>
      </tr>
      `
    }
  }
  $("#permittee-buckets-body").html(innerTableBody)
}

function toggleSecretKey(button) {
  const secretKeySpan = button.previousElementSibling;
  if (secretKeySpan.textContent.includes('*')) {
    secretKeySpan.textContent = button.getAttribute('data-key');
    button.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
  } else {
    secretKeySpan.textContent = '*'.repeat(secretKeySpan.textContent.length);
    button.innerHTML = '<i class="fa-solid fa-eye"></i>';
  }
}


async function showVariantsModal(biosampleSerial, notarizerSerial){
  $("#variantModal").modal("show");
  $("#variantModalContainer").html(/*html */`
    <div class="mt-5 mb-5">
      <div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>  
  `)
  const variantList = await getParticipantVariants(root_sign, biosampleSerial, notarizerSerial)
  let variantListComponent = ``;
  if (variantList.length > 0) {
    for(const variant of variantList) {
      variantListComponent+= /*html */`
        <tr>
          <td>${variant?.gene}</td>
          <td>${variant?.variant}</td>
          <td>${variant?.frequency}</td>
          <td>${variant?.pathogenecity}</td>
        </tr>
      `
    }
  }
  $("#variantModalContainer").html(/*html */`
    <div class="modal-header">
      <h5 class="modal-title">${biosampleSerial}</h5>
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body" id="variantModalBody">
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">Gene</th>
            <th scope="col">Variant</th>
            <th scope="col">Frequency</th>
            <th scope="col">Pathogenecity</th>
          </tr>
        </thead>
        <tbody>
          ${variantListComponent}
        </tbody>
      </table>
      <div class="alert alert-primary d-flex align-items-center" role="alert">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <div>
          &nbsp; Click on "Select this as winner", only when you are sure you want to choose this participant as the winner. This action is irreversible
        </div>
      </div>
    </div>
    <div id = "id-variant-winner-message"></div>
    <div class="modal-footer">
      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      <button type="button" class="btn btn-success" id="id-select-winner-button" onclick="signAndSelectAsWinner(${biosampleSerial}, ${notarizerSerial})">Select this as winner</button>
    </div>
  `)
}

function openEditModalBucket(bucketData){
  const parsedBucketData = JSON.parse(decodeURIComponent(bucketData));
  $("#editBucketModalContainer").html(editBucketModalComponent(parsedBucketData))
  $("#editBucketModal").modal("show");
}

// add an input for permittee address
function editBucketModalComponent(bucketData){
  return /*html */`
    <div class="modal-header">
      <h5 class="modal-title">Edit Bucket</h5>
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body" id="editBucketModalBody">
      <div class="mb-3">
        <label for="bucket-name" class="form-label">Bucket Name</label>
        <input type="text" class="form-control" id="bucket-name" value="${bucketData?.bucket_name}" oninput="checkForChanges('${bucketData?.bucket_name}', '${bucketData?.access_key_id}', '${bucketData?.secret_access_key}', '${bucketData?.permittee_serial}', '${bucketData?.permittee_wallet}')">
      </div>
      <div class="mb-3">
        <label for="access-key-id" class="form-label">Access Key ID</label>
        <input type="text" class="form-control" id="access-key-id" value="${bucketData?.access_key_id}" oninput="checkForChanges('${bucketData?.bucket_name}', '${bucketData?.access_key_id}', '${bucketData?.secret_access_key}', '${bucketData?.permittee_serial}', '${bucketData?.permittee_wallet}')">
      </div>
      <div class="mb-3">
        <label for="secret-access-key" class="form-label">Secret Access Key</label>
        <input type="text" class="form-control" id="secret-access-key" value="${bucketData?.secret_access_key}" oninput="checkForChanges('${bucketData?.bucket_name}', '${bucketData?.access_key_id}', '${bucketData?.secret_access_key}', '${bucketData?.permittee_serial}', '${bucketData?.permittee_wallet}')">
      </div>
      <div class="mb-3">
        <label for="permittee-serial" class="form-label">Permittee Serial</label>
        <input type="number" class="form-control" id="permittee-serial" value="${bucketData?.permittee_serial}" oninput="checkForChanges('${bucketData?.bucket_name}', '${bucketData?.access_key_id}', '${bucketData?.secret_access_key}', '${bucketData?.permittee_serial}', '${bucketData?.permittee_wallet}')">
      </div>
      <div class="mb-3">
        <label for="permittee-wallet" class="form-label">Permittee Wallet</label>
        <input type="text" class="form-control" id="permittee-wallet" value="${bucketData?.permittee}" oninput="checkForChanges('${bucketData?.bucket_name}', '${bucketData?.access_key_id}', '${bucketData?.secret_access_key}', '${bucketData?.permittee_serial}', '${bucketData?.permittee_wallet}')">
      </div>
    </div>
    <div class="modal-footer">
      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      <button type="button" class="btn btn-primary" id="save-changes-button" disabled>Save changes</button>
    </div>
  `
}

function checkForChanges(originalBucketName, originalAccessKeyId, originalSecretAccessKey, originalPermitteeSerial, originalPermitteeWallet) {
  const bucketName = document.getElementById('bucket-name').value;
  const accessKeyId = document.getElementById('access-key-id').value;
  const secretAccessKey = document.getElementById('secret-access-key').value;
  const permitteeSerial = document.getElementById('permittee-serial').value;
  const permitteeWallet = document.getElementById('permittee-wallet').value;

  const saveButton = document.getElementById('save-changes-button');

  if (bucketName !== originalBucketName || accessKeyId !== originalAccessKeyId || secretAccessKey !== originalSecretAccessKey || permitteeSerial !== originalPermitteeSerial || permitteeWallet !== originalPermitteeWallet) {
    saveButton.disabled = false;
  } else {
    saveButton.disabled = true;
  }
}

async function signAndSelectAsWinner(biosampleSerial, notarizerSerial){
  const tempTextButton = $("#id-select-winner-button").text()
  $("#id-select-winner-button").html(/*html */`
    <div class="d-flex justify-content-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  `)
  try{
    let sign_autentication = await provider.getSigner().signMessage(apiMessage);
    console.log("sign_autentication: ", sign_autentication)
    console.log("biosampleSerial: ", biosampleSerial)
    console.log("notarizerSerial: ", notarizerSerial)
    const selectedWinner = await selectWinner(sign_autentication, biosampleSerial, notarizerSerial)
    console.log("selectedWinner: ", selectedWinner)
    showSuccessMessage($("#id-variant-winner-message"), "Selected Winner", "Winner selected successfully")
  }catch(e){
    showErrorMessage($("#id-variant-winner-message"), e?.code, e?.message)
    console.error(e)
  }finally{
    $("#id-select-winner-button").text(tempTextButton)
  }
}


function backToPendigBiosamplesWithVariants(){
  $("#variants-pending-participants-section").hide()
  $("#biosamples-with-pending-variants-table").show()
}

async function setCurrentOwner (button){
  let _owner = button.getAttribute("data-owner");
  currentSelectedPermittee = _owner
  $(".permittee-address").html(_owner)
}

async function approvePermittee(){
  let messageDiv = $(".approve-message-container")
  showSpinner(messageDiv)

  const uri = `${window.NEWAPIBASE}/approve_permittee?owner=${currentSelectedPermittee}`
  let approved_permittee = await fetch(uri, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ root_signature: root_sign })
    })
    .then(response => response.json())
    .then(data => {
      if (data.status == 'Failure'){
        showErrorMessage(messageDiv, "Error", data.status_details.description)
      }else{
        showSuccessMessage(messageDiv, "Permittee Approved", data.text)
        getAllPermitteeRequests(root_sign).then(list => {
          renderPendingTable(list)
          renderApprovedTable(list)
          renderRejectedTable(list)
        })
      }
      return data
    })
    .catch(error => {
      showErrorMessage(messageDiv, "Error", error.status_details.description)
    });


  // aqui debe aparecer un modal de exito o de fallo

  console.log(approved_permittee)
}

async function rejectPermittee(){
  let messageDiv = $(".reject-message-container")
  showSpinner(messageDiv)
  const uri = `${window.NEWAPIBASE}/reject_permittee?owner=${currentSelectedPermittee}`
  
  const inicioTiempo = performance.now();
  
  let rejected_permittee = await fetch(uri, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ root_signature: root_sign })
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'Failure'){
        showErrorMessage(messageDiv, "Error", data.status_details.description)
      }else{
        showSuccessMessage(messageDiv, "Permittee rejected", data.text)
        getAllPermitteeRequests(root_sign).then(list => {
          
          renderPendingTable(list)
          renderApprovedTable(list)
          renderRejectedTable(list)
        })
      }
      return data
    })
    .catch(error => {
      showErrorMessage(messageDiv, "Error", error.status_details.description)
    });

    const finTiempo = performance.now();

    const tiempoTotal = finTiempo - inicioTiempo;
    console.log(`La función tardó ${tiempoTotal} milisegundos en ejecutarse.`);


  // aqui debe aparecer un modal de exito o de fallo
}





// messages alerts

async function showSpinner(divElement){
  divElement.html(`
  <div class="d-flex justify-content-center" >
  <div class="custom-spinner">
    <div class="erlenmeyer">
      <div class="liquid">
        <div class="bubble"></div>
      </div>
    </div>
    &nbsp;&nbsp;Loading ...
  </div>
</div>
  `)
}

async function showSuccessMessage(divElement, title, successMessage){
  divElement.html(`
  <div class="container mt-3">
    <div class="alert alert-success" role="alert">
      <h4 class="alert-heading">${title}</h4>
      <p>${successMessage}</p>
    </div>
  </div>
  `)
}

async function showErrorMessage(divElement, title, errorMessage){
  divElement.html(`
    <div class="container mt-3">
      <div class="alert alert-danger" role="alert">
        <h4 class="alert-heading">${title}</h4>
        <p>${errorMessage}.</p>
      </div>
    </div>`
  )
}


// rejectModal.addEventListener('hidden.bs.modal', function (event) {
//   console.log('Modal cerrado');
//   window.location.reload()

//   // Agrega aquí el código que quieras ejecutar cuando el modal se cierre
// });

modal.on('hidden.bs.modal', function (event) {
  $(".reject-message-container").html('');
  $(".approve-message-container").html('');
  // Agrega aquí el código que quieras ejecutar cuando el modal se cierre
});



async function throw_alert_message(title){
  $(".no-authorized-user").show();
  $(".alert-danger").html(`
  <p>${title}</p>
  `);
}

async function fetchWithRetry(url, options, retries) {
  for(let i = 0; i <= retries; i++){
      try {
          let response = await fetch(url, options);
          if (!response.ok) throw new Error(response.status);
          return response.json(); 
      } catch(error) {
          if (i < retries){
              console.log(`Retrying... Attempt number: ${i + 2}`);
          } else {
              return { error: error.message };
          }
      }
  }
}


function extractJsonFromText(text) {
  try {
    if (text != null) {
      let normalizedText = text.trim();
      normalizedText = normalizedText.replace(/^'{|}'$/g, function (match) {
        return match === "'{" ? '{"' : '"}';
      });
      normalizedText = normalizedText.replace(/([^\\])'([^']|$)/g, '$1"$2').replace(/([^\\])'([^'])/g, '$1"$2');
      const json = JSON.parse(normalizedText);
      return json;
    }
    return {};
  } catch (e) {
    console.error("Error parsing JSON:", e);
    return false;
  }
}