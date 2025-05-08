// function validatePrintReturnSticker() {
// 	if ($('#returnStickerLaboratoryUrl').hasClass('is-valid') &&
// 	  $('#returnStickerTrackingCode').hasClass('is-valid')
// 	) {
// 	  return true;
// 	} else {
// 	  return false;
// 	}
//   }



$(document).ready(async function () {

	/**
	 * Validates Register a permittee, permittee ID field.
	 */
	$('#registerPermitteePermitteeId').on('blur', async function () {
		const permitteeId = $('#registerPermitteePermitteeId').val();
		const success = await checkRegisterPermitteePermitteeId(permitteeId);
		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = `Permittee ID #${permitteeId} ${success ? 'has NOT been registered yet.' : 'was already registered.'}`;
		if (success) {
			$('#registerPermitteePermitteeId').addClass('is-valid');
			$('#registerPermitteePermitteeId').removeClass('is-invalid');
		} else {
			$('#registerPermitteePermitteeId').addClass('is-invalid');
			$('#registerPermitteePermitteeId').removeClass('is-valid');
		}
		$('#registerPermitteePermitteeIdValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});

	/**
	 * Validates Register a permittee, permittee address field.
	 */
	$('#registerPermitteePermitteeAddress').on('blur', async function () {
		const address = $('#registerPermitteePermitteeAddress').val();
		const web3 = new Web3(window.ethereum);
		const success = web3.utils.isAddress(address);
		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = success ? 'This address is acceptable.' : 'This is not an Ethereum address.';
		if (success) {
			$('#registerPermitteePermitteeAddress').addClass('is-valid');
			$('#registerPermitteePermitteeAddress').removeClass('is-invalid');
		} else {
			$('#registerPermitteePermitteeAddress').addClass('is-invalid');
			$('#registerPermitteePermitteeAddress').removeClass('is-valid');
		}
		$('#registerPermitteePermitteeAddressValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});

	/**
	 * Validates Create a biosample, biosample ID field.
	 */
	$('#createBiosampleBiosampleId').on('blur', async function () {
		const biosampleId = $('#createBiosampleBiosampleId').val();
		const success = await checkCreateBiosampleBiosampleId(biosampleId) && await checkBiosampleActivations(biosampleId);
		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = `Biosample ID #${biosampleId} ${success ? 'has NOT been activated by a customer yet.' : 'was already activated by a customer or activation was already generated.'}`;
		if (success) {
			$('#createBiosampleBiosampleId').addClass('is-valid');
			$('#createBiosampleBiosampleId').removeClass('is-invalid');
		} else {
			$('#createBiosampleBiosampleId').addClass('is-invalid');
			$('#createBiosampleBiosampleId').removeClass('is-valid');
		}
		$('#createBiosampleBiosampleIdValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});

	/**
	 * Validates batch create a biosample, biosample ID field.
	 */
	$('#batchCreateBiosampleBiosampleId').on('blur', async function () {
		let success = true;
		const input = $('#batchCreateBiosampleBiosampleId').val();
		let text = '';

		const data = parseBiosamplesInput(input);
		if (!data) {
			success = false;
			text = 'Error parsing input.';
		}

		if (success) {
			for (const biosampleId of data.biosampleIds) {
				success = await checkCreateBiosampleBiosampleId(biosampleId) && await checkBiosampleActivations(biosampleId);
				if (!success) {
					text = `Biosample ID #${biosampleId} was already activated by a customer or activation was already generated.`;
					break;
				}
			}
		}

		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		if (success) {
			$('#batchCreateBiosampleBiosampleId').addClass('is-valid');
			$('#batchCreateBiosampleBiosampleId').removeClass('is-invalid');
		} else {
			$('#batchCreateBiosampleBiosampleId').addClass('is-invalid');
			$('#batchCreateBiosampleBiosampleId').removeClass('is-valid');
		}
		if (text != '') {
			$('#batchCreateBiosampleBiosampleIdValidation').html(`
		  <small class="form-text ${cssClass}">
			<i class="fa ${icon}"></i> ${text}
		  </small>
		`);
		} else {
			$('#batchCreateBiosampleBiosampleIdValidation').html('');
		}
	});

	/**
	 * Validates Activate a biosample, biosample ID field.
	 */
	$('#activateBiosampleBiosampleId').on('blur', async function () {
		const biosampleId = $('#activateBiosampleBiosampleId').val();
		const success = await checkCreateBiosampleBiosampleId(biosampleId);
		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = `Biosample ID #${biosampleId} ${success ? 'has NOT been activated by a customer yet.' : 'was already activated by a customer.'}`;
		if (success) {
			$('#activateBiosampleBiosampleId').addClass('is-valid');
			$('#activateBiosampleBiosampleId').removeClass('is-invalid');
		} else {
			$('#activateBiosampleBiosampleId').addClass('is-invalid');
			$('#activateBiosampleBiosampleId').removeClass('is-valid');
		}
		$('#activateBiosampleBiosampleIdValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});

	/**
	 * Validates create permission biosample ID field.
	 */
	$('#createPermissionBiosampleId').on('blur', async function () {
		const biosampleId = $('#createPermissionBiosampleId').val();
		const success = !await checkCreateBiosampleBiosampleId(biosampleId);
		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = `Biosample ID #${biosampleId} ${success ? 'is an active biosample.' : 'has not been activated yet.'}`;
		if (success) {
			$('#createPermissionBiosampleId').addClass('is-valid');
			$('#createPermissionBiosampleId').removeClass('is-invalid');
		} else {
			$('#createPermissionBiosampleId').addClass('is-invalid');
			$('#createPermissionBiosampleId').removeClass('is-valid');
		}
		$('#createPermissionBiosampleIdValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});


	/**
	 * Validates update permission biosample ID field.
	 */
	$('#updatePermissionBiosampleId').on('blur', async function () {
		const biosampleId = $('#updatePermissionBiosampleId').val();
		const success = !await checkCreateBiosampleBiosampleId(biosampleId);
		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = `Biosample ID #${biosampleId} ${success ? 'is an active biosample.' : 'has not been activated yet.'}`;
		if (success) {
			$('#updatePermissionBiosampleId').addClass('is-valid');
			$('#updatePermissionBiosampleId').removeClass('is-invalid');
		} else {
			$('#updatePermissionBiosampleId').addClass('is-invalid');
			$('#updatePermissionBiosampleId').removeClass('is-valid');
		}
		$('#updatePermissionBiosampleIdValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});

	/**
	 * Validates Download file document ID field.
	 */
	$('#downloadFileDocumentId').on('blur', async function () {
		const documentId = $('#downloadFileDocumentId').val();
		const success = await checkFileDownload(documentId);
		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = `Document ID #${documentId} ${success ? 'is a valid document.' : 'is not a valid document.'}`;
		if (success) {
			$('#downloadFileDocumentId').addClass('is-valid');
			$('#downloadFileDocumentId').removeClass('is-invalid');
		} else {
			$('#downloadFileDocumentId').addClass('is-invalid');
			$('#downloadFileDocumentId').removeClass('is-valid');
		}
		$('#downloadFileDocumentIdValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});

	/**
	 * Validates Biosample activation URL field.
	 */
	$('#biosampleStickerUrl').on('blur', async function () {
		const biosampleUrl = $('#biosampleStickerUrl').val();
		let success = true;
		try {
			const url = new URL(biosampleUrl);
			const biosampleId = url.searchParams.get('biosampleId');
			if (!biosampleId || biosampleId == '') {
				success = false;
			}
		} catch (e) {
			console.log(e);
			success = false;
		}

		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = `${success ? 'Is a valid url.' : 'Is not a valid url.'}`;
		if (success) {
			$('#biosampleStickerUrl').addClass('is-valid');
			$('#biosampleStickerUrl').removeClass('is-invalid');
		} else {
			$('#biosampleStickerUrl').addClass('is-invalid');
			$('#biosampleStickerUrl').removeClass('is-valid');
		}
		$('#biosampleStickerUrlValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});

	$('#returnStickerLaboratoryUrl').on('blur', async function () {
		const biosampleUrl = $('#returnStickerLaboratoryUrl').val();
		let success = true;
		try {
			const url = new URL(biosampleUrl);
			const biosampleId = url.searchParams.get('biosampleId');
			if (!biosampleId || biosampleId == '') {
				success = false;
			}
		} catch (e) {
			console.log(e);
			success = false;
		}

		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = `${success ? 'Is a valid url.' : 'Is not a valid url.'}`;
		if (success) {
			$('#returnStickerLaboratoryUrl').addClass('is-valid');
			$('#returnStickerLaboratoryUrl').removeClass('is-invalid');
		} else {
			$('#returnStickerLaboratoryUrl').addClass('is-invalid');
			$('#returnStickerLaboratoryUrl').removeClass('is-valid');
		}
		$('#returnStickerLaboratoryUrlValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});

	$('#returnStickerTrackingCode').on('blur', async function () {
		const trackingCode = $('#returnStickerTrackingCode').val();
		let success = true;
		let unsuccessfulText = '';

		const regex = /^[0-9]*$/g; // 0–9
		const trackingCodeRes = regex.exec(trackingCode);

		if (trackingCode.length != 22) {
			success = false;
			unsuccessfulText = "Tracking number length is not 22."
		} else if ((!trackingCodeRes || trackingCodeRes.length != 1)) {
			success = false;
			unsuccessfulText = "Tracking number format invalid. Only numbers allowed."
		}

		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = `${success ? 'Is a valid tracking number.' : unsuccessfulText}`;
		if (success) {
			$('#returnStickerTrackingCode').addClass('is-valid');
			$('#returnStickerTrackingCode').removeClass('is-invalid');
		} else {
			$('#returnStickerTrackingCode').addClass('is-invalid');
			$('#returnStickerTrackingCode').removeClass('is-valid');
		}
		$('#returnStickerTrackingCodeValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});

	$('#permissionMnemonic').change(function () {
		if (this.checked) {
			$('#permissionMnemonicInputs').show();
		} else {
			$('#permissionMnemonicInputs').hide();
		}
	});
});


/**
 * Checks if permittee exists on servers and returns true if he does NOT and false otherwise.
 * @param permitteeId 
 */
async function checkRegisterPermitteePermitteeId(permitteeId) {
	const url = `${window.API_BASE}/permittees/${permitteeId}`;
	return fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		},
	}).then(async (res) => {
		const result = await res.json();
		if (result.errors) {
			return true;
		}
		return false;
	}).catch((error) => {
		console.log(error);
		return true;
	});
}

/**
 * Checks if biosample exists on servers and returns true if he does NOT and false otherwise.
 * @param biosampleId 
 */
async function checkCreateBiosampleBiosampleId(biosampleId) {
	const url = `${window.API_BASE}/biosamples/${biosampleId}`;
	return fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		},
	}).then(async (res) => {
		const result = await res.json();
		if (result.errors) {
			return true;
		}
		return false;
	}).catch((error) => {
		console.log(error);
		return true;
	});
}

async function checkBiosampleActivations(biosampleId) {
	const url = `${window.API_BASE}/biosample-activations?filterSerials[0]=${biosampleId}`;
	return fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		},
	}).then(async (res) => {
		const result = await res.json();
		if (result.data?.length > 0) {
			return false;
		}
		return true;
	}).catch((error) => {
		console.log(error);
		return true;
	});
}

/**
 * Checks if document exists on servers and returns true if it does and false otherwise.
 * @param documentId 
 */
async function checkFileDownload(documentId) {
	const url = `${window.API_BASE}/documents/${documentId}`;
	return fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		},
	}).then(async (res) => {
		const result = await res.json();
		if (result.errors) {
			return false;
		}
		return true;
	}).catch((error) => {
		console.log(error);
		return false;
	});
}

/**
 * Validates if register permittee can be performed.
 */
function validateRegisterPermitteeButton() {
	if ($('#registerPermitteePermitteeAddress').hasClass('is-valid') &&
		$('#registerPermitteePermitteeId').hasClass('is-valid') &&
		$('#registerPermitteeApplicationSecret').val()
	) {
		return true;
	} else {
		return false;
	}
}

/**
 * Validates if store permittee profile can be performed.
 */
function validateStoreProfileButton() {
	if ($('#storeProfilePermitteeId').val() &&
		$('#storeProfileName').val() &&
		$('#storeProfileApplicationSecret').val()
	) {
		return true;
	} else {
		return false;
	}
}


/**
 * Validates if create biosample can be performed.
 */
function validateCreateBiosampleButton() {
	if ($('#createBiosampleBiosampleId').hasClass('is-valid') &&
		$('#createBiosamplePhysicalId').val() &&
		$('#createBiosampleApplicationSecret').val()
	) {
		return true;
	} else {
		return false;
	}
}

/**
 * Validates if batch create biosample can be performed.
 */
function validateBatchCreateBiosampleButton() {
	if ($('#batchCreateBiosampleBiosampleId').hasClass('is-valid') &&
		$('#batchCreateBiosampleApplicationSecret').val()
	) {
		return true;
	} else {
		return false;
	}
}

/**
 * Validates if activate biosample can be performed.
 */
function validateActivateBiosampleButton() {
	if ($('#activateBiosampleBiosampleId').hasClass('is-valid') &&
		$('#activateBiosampleApplicationSecret').val()
	) {
		return true;
	} else {
		return false;
	}
}

/**
 * Validates if create a permission can be performed.
 */
function validateCreatePermissionButton() {
	if ($('#createPermissionBiosampleId').hasClass('is-valid')) {
		return true;
	} else {
		return false;
	}
}


/**
 * Validates if create a permission can be performed.
 */
function validateUpdatePermissionButton() {
	if ($('#updatePermissionBiosampleId').hasClass('is-valid')) {
		return true;
	} else {
		return false;
	}
}

/**
 * Validates if Download file can be performed.
 */
function validateDownloadFileButton() {
	if ($('#downloadFileDocumentId').hasClass('is-valid') &&
		$('#downloadFilePrivateKey').val()
	) {
		return true;
	} else {
		return false;
	}
}

/**
 * Validates if print biosample activation sticker can be performed.
 */
function validatePrintBiosampleActivationSticker() {
	if ($('#biosampleStickerUrl').hasClass('is-valid')) {
		return true;
	} else {
		return false;
	}
}

/**
 * Validates if print biosample activation sticker can be performed.
 */
function validatePrintReturnSticker() {
	if ($('#returnStickerLaboratoryUrl').hasClass('is-valid') &&
		$('#returnStickerTrackingCode').hasClass('is-valid')
	) {
		return true;
	} else {
		return false;
	}
}

function parseBiosamplesInput(input) {
	const data = {
		biosampleIds: [],
		physicalIds: [],
	}

	try {
		const inputs = input.split('\n');

		for (const inp of inputs) {
			let splitData = inp.split('\t');
			const biosampleId = splitData[0].trim();
			const physicalId = splitData[1].trim();
			if (biosampleId == '') {
				return null;
			} else {
				data.biosampleIds.push(biosampleId);
			}

			if (physicalId == '') {
				return null;
			} else {
				data.physicalIds.push(physicalId);
			}
		}

	} catch (e) {
		return null;
	}

	return data;
}


	$('#returnStickerLaboratoryUrl').on('blur', async function () {
		const biosampleUrl = $('#returnStickerLaboratoryUrl').val();
		let success = true;
		try {
			const url = new URL(biosampleUrl);
			const biosampleId = url.searchParams.get('biosampleId');
			if (!biosampleId || biosampleId == '') {
				success = false;
			}
		} catch (e) {
			console.log(e);
			success = false;
		}

		const cssClass = success ? 'text-success' : 'text-danger';
		const icon = success ? 'fa-check' : 'fa-times';
		const text = `${success ? 'Is a valid url.' : 'Is not a valid url.'}`;
		if (success) {
			$('#returnStickerLaboratoryUrl').addClass('is-valid');
			$('#returnStickerLaboratoryUrl').removeClass('is-invalid');
		} else {
			$('#returnStickerLaboratoryUrl').addClass('is-invalid');
			$('#returnStickerLaboratoryUrl').removeClass('is-valid');
		}
		$('#returnStickerLaboratoryUrlValidation').html(`
		<small class="form-text ${cssClass}">
		  <i class="fa ${icon}"></i> ${text}
		</small>
	  `);
	});