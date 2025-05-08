let isIdValid = false;
let isAddressValid = false;

$(document).ready(() => {
  (() => {
    var $el = $([
      '#createBiosampleUrlBase', '#batchCreateBiosampleUrlBase'
    ].join(','));
    $el.empty(); // remove old options
    for (let base of window.BIOSAMPLE_ACTIVATION_BASE) {
      $el.append($("<option></option>").attr("value", base).text(base));
    }
  })();

  (async () => {
    var $el = $([
      '#registerPermitteePermitteeId', '#uploadPermitteePublicPermitteeId', 
      '#storeProfilePermitteeId', '#createBiosamplePermitteeId',
      '#activateBiosamplePermitteeId', '#createPermissionPermitteeId', 
      '#updatePermissionPermitteeId', '#batchCreateBiosamplePermitteeId'
    ].join(','));
    $el.empty(); // remove old options
    for (let entry of await getPermitteeOptions()) {
      $el.append($("<option></option>").attr("value", entry[1]).text(entry[0]));
    }
  })();
});

async function check_id(){
  const permitteeId = $('#registerPermitteePermitteeId').val()
  const uri = `${window.API_BASE}/permittees/${permitteeId}`
  let response = await fetch(uri, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
  if (response.status == 200){
    $("#registerPermitteePermitteeId").removeClass("is-invalid");
    $("#registerPermitteePermitteeId").removeClass("is-valid");
    $("#registerPermitteePermitteeId").addClass("is-invalid");
    isIdValid = false;
  }
  if (response.status == 400){
    $("#registerPermitteePermitteeId").removeClass("is-invalid");
    $("#registerPermitteePermitteeId").removeClass("is-valid");
    $("#registerPermitteePermitteeId").addClass("is-valid");
    isIdValid = true;
  }
}

async function checkAddress(){
  $('#registerPermitteePermitteeAddress').on('blur', async function() {
    const address = $('#registerPermitteePermitteeAddress').val();
    const web3 = new Web3(window.ethereum);
    const success = web3.utils.isAddress(address);
    const cssClass = success ? 'text-success' : 'text-danger';
    const icon = success ? 'fa-check' : 'fa-times';
    const text = success ? 'This address is acceptable.' : 'This is not an Ethereum address.';
    if (success) {
      $('#registerPermitteePermitteeAddress').addClass('is-valid');
      $('#registerPermitteePermitteeAddress').removeClass('is-invalid');
      isAddressValid = true;
    } else {
      $('#registerPermitteePermitteeAddress').addClass('is-invalid');
      $('#registerPermitteePermitteeAddress').removeClass('is-valid');
      isAddressValid = false;
    }
    $('#registerPermitteePermitteeAddressValidation').html(`
      <small class="form-text ${cssClass}">
        <i class="fa ${icon}"></i> ${text}
      </small>
    `);
  });
}

async function registerPermittee(){
  if (isIdValid && isAddressValid) {
    const permitteeId = $('#registerPermitteePermitteeId').val();
    const permitteeAddress = $('#registerPermitteePermitteeAddress').val();
    const appSecret = $('#registerPermitteeApplicationSecret').val();
    const secret = await createPermitteeHMAC(permitteeId, permitteeAddress, appSecret);
    const res = await createPermittee(permitteeId, permitteeAddress, appSecret);
    console.log("res\n",res)
    console.log("Ambos son validos")
    if (res.status=="Failure"){
      $("#registerPermitteeResult").removeClass('bg-success');
      $("#registerPermitteeResult").addClass('bg-danger');
      // let inner = `<p>Error during permittee creation: ${res.status_details.description} </p>`
      // $("#registerPermitteeResult").html(inner)
    }else{
      $("#registerPermitteeResult").removeClass('bg-danger');
      $("#registerPermitteeResult").addClass('bg-success');
    }

    let inner = `<b>Permittee ID:</b> ${permitteeId}<br/>
                  <b>Permittee address:</b> ${permitteeAddress}<br/>
                  <b>Permittee secret:</b> ${secret}<br/>
                  <b>Response:</b> ${JSON.stringify(res)}`
    $("#registerPermitteeResult").html(inner)


    // $("#registerPermitteeResult").removeClass('bg-danger');
    // $("#registerPermitteeResult").addClass('bg-success');
    // $("#registerPermitteeResult").html("Correct Data")
    // $("#registerPermitteeResult").show();

  }else{
    $("#registerPermitteeResult").removeClass('bg-success');
    $("#registerPermitteeResult").addClass('bg-danger');
    $("#registerPermitteeResult").html("Invalid data")
    $("#registerPermitteeResult").show();
  }
  // $("#registerPermitteeResult").hide();
}


async function createPermittee(permitteeId, permitteeAddress, appSecret) {
  const permitteeSecret = await createPermitteeHMAC(permitteeId, permitteeAddress, appSecret);
  let bodyContent = new FormData();
  bodyContent.append("id", permitteeId);
  bodyContent.append("address", permitteeAddress);
  bodyContent.append("secret", permitteeSecret);
  bodyContent.append("env", window.ENV)
  const url = `${window.NEWAPIBASE}/create_permitee?id=${permitteeId}&address=${permitteeAddress}&secret=${permitteeSecret}`;
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  }).then((res) => {
    return res.json();
  }).catch((error) => {
    console.error(error);
    return { error: error.message };
  });

  // let data = await response.text()

  // console.log("response \n",data);
}


async function createPermitteeHMAC(permitteeId, permitteeAddress, appSecret) {
  const hmacClaim = `${permitteeId}${permitteeAddress}`;
  const enc = new TextEncoder();
  const key = await window.crypto.subtle.importKey(
      "raw", // raw format of the key - should be Uint8Array
      enc.encode(appSecret),
      { // algorithm details
          name: "HMAC",
          hash: {name: "SHA-256"}
      },
      false, // export = false
      ["sign", "verify"] // what this key can do
  );
  const hmac = await window.crypto.subtle.sign(
    "HMAC",
    key,
    enc.encode(hmacClaim)
  );
  var b = new Uint8Array(hmac);
  return Array.prototype.map.call(b, x => ('00'+x.toString(16)).slice(-2)).join("");
}

async function createBiosample() {
  if(validateCreateBiosampleButton()) {
    const domainId = $('#createBiosampleUrlBase').val();
    const biosampleId = $('#createBiosampleBiosampleId').val();
    const permitteeId = $('#createBiosamplePermitteeId').val();
    const physicalId = $('#createBiosamplePhysicalId').val();
    const appSecret = $('#createBiosampleApplicationSecret').val();
    const permittee = await getPermittee(permitteeId);
    const publicKey = await getPublicKey(permittee.data.owner);
    let html = '';
    if (!publicKey || !publicKey.data) {
      html = `<small class="form-text text-warning"><i class="fa fa-warning"></i> Selected permittee does not have public key set. Activations will not be possible until public key is set!</small><br/>`
    }
    const biosampleActivation = await createBiosampleActivation(biosampleId, permitteeId, physicalId, appSecret);
    if (biosampleActivation.errors) {
      $('#createBiosampleResult').removeClass('bg-success');
      $('#createBiosampleResult').addClass('bg-danger');
      $('#createBiosampleResult').html(JSON.stringify(biosampleActivation.errors));
    } else {
      const url = await createActivationURL(domainId, biosampleId, permitteeId, physicalId, biosampleActivation.data.secret);
      html = `${html}
        <b>Activation URL:</b> ${url}<br/>
      `;
      createQRURL(url)
      $('#createBiosampleResult').addClass('bg-success');
      $('#createBiosampleResult').removeClass('bg-danger');   
      $('#createBiosampleResult').html(html);
    }
  } else {
    $('#createBiosampleResult').removeClass('bg-success');
    $('#createBiosampleResult').addClass('bg-danger');
    $('#createBiosampleResult').html('Inputs invalid');
  }
}