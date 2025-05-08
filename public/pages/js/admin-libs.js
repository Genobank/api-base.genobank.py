async function createActivationURL(urlBase, biosampleId, permitteeId, physicalId, activationSecret) {
  return `${urlBase}/?biosampleId=${biosampleId}&laboratoryId=${permitteeId}&physicalId=${physicalId}#${activationSecret}`;
}

async function createBiosampleHMAC(biosampleId, appSecret) {
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
  )
  const hmac = await window.crypto.subtle.sign(
    "HMAC",
    key,
    enc.encode(biosampleId)
  );
  var b = new Uint8Array(hmac);
  return Array.prototype.map.call(b, x => ('00'+x.toString(16)).slice(-2)).join("");
}

async function createBiosampleActivation(biosampleId, permitteeId, physicalId, appSecret) {
  const hmac = await createBiosampleHMAC(biosampleId, appSecret);
  const url = `${window.API_BASE}/biosample-activation`;
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      serial: biosampleId,
      biosampleSecret: hmac,
      physicalId,
      permitteeSerial: permitteeId
    })
  }).then((res) => {
    return res.json();
  }).catch((error) => {
    console.error(error);
    return { error: error.message };
  });
}

async function createQRURL(magicUrl){
// change this 
// magicUrl = "https://genobank.io/test/activate/?biosampleId=1001234567893&laboratoryId=150&physicalId=1234567893#a3070c061dbfa79e6c97918e0cc4427e53d63aa97fee65d448ad3704084b826c"

$("#qrCode").html("")
$("#imageDownloader").html("")
  const qrcode = await new QRCode(document.getElementById("qrCode"), {
    text: magicUrl,
    width: 400,
    height: 400,
    colorDark: "#000000",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.M
  });

  // qr_image = $("#qrCode").find('img').get(0).src

  const qr_source = qrcode._oDrawing._elCanvas.toDataURL("image/png")

  $("#qrCode").html(`
    <a href="${qr_source}" download="filename.png"><img src="${qr_source}"/></a>
  `)
}

// async function downloadQRCode(){
//   console.log($("#qrCode").find('img'))
//   const blob = stream.toBlob('image/png');
//   const fileName="QRCode"




// }

async function getPermittee(serial) {
  return fetch(`${window.API_BASE}/permittees/${serial}`, {
    method: 'GET',
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    },
  }).then((res) => {
    return res.json();
  }).catch((e) => {
    return { errors: [{message: e }]};
  });
}

/**
 * Gets public key based on address.
 * @param address Address for which we want a public key.
 */
async function getPublicKey(address) {
  return fetch(`${window.API_BASE}/public-key/${address}`, {
		method: 'GET',
		headers: {
			"Content-type": "application/json; charset=UTF-8"
		},
	}).then((res) => {
		return res.json();
	}).catch((e) => {
		return { errors: [{message: e }]};
	});
}

async function getPermittees() {
  const url = `${window.API_BASE}/permittees`;
  return fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  }).then((res) => {
    return res.json();
  }).then((res) => {
    return res.data;
  }).catch((error) => {
    console.error(error);
    return { error: error.message };
  });
}

async function getProfiles(serials) {
  let url = `${window.API_BASE}/profiles`;
  // if (Array.isArray(serials) && serials.length > 0) {
  //   url += '?' + serials.map((s) => `filterSerials[]=${s}`).join('&');
  // }


  return fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  }).then((res) => {
    return res.json();
  }).then((res) => {
    return res.data;
  }).catch((error) => {
    console.error(error);
    return { error: error.message };
  });
}

async function getPermitteeOptions() {
  let permittees = await getPermittees();
  console.log("debug permittees:  ", permittees )

  // get all profiles
  // let permitteeSerials = permittees.map((p) => p.serial);
  let profiles = await getProfiles([]); // [permitteeSerials]
  console.log("debug profiles:  ", profiles )
  return permittees.map((pe) => {
    let item = [`${pe.serial} - Anonymous`, pe.serial];
    let profile = profiles.find((pr) => pe.serial == pr.serial);
    if (profile) {
      try {
        let data = profile.text
        data = data.replace(/'/g, '"');
        data = JSON.parse(data);
        console.log(data)
        if (data.name) {
          item[0] = `${pe.serial} - ${data.name}`;
        }
      } catch(e) {}
    }
    return item;
  });
}