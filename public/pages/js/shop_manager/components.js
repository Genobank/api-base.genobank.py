function modalAddProduct() {
	return (/*html */`
	<div class="modal-dialog modal-dialog-centered " role="document">
	  <div class="modal-content">
		<div class="modal-header">
		  <h5 class="modal-title" id="approvalModalTitle">Add New Product</h5>
		  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
		</div>
		<div class="modal-body">
			<img class="fill-width" src="/js/shop_manager/images/image-thumb-gray.png" id="id-thumbnail-new-product-viewer">
			<div class="mb-3">
				<input class="form-control" type="file" id="id-input-new-product-thumbnail" oninput="changeNewProductImage()">
			</div>
			<form>
				<div class="mb-3 row">
					<div class="col-auto">
						<label for="id-input-product-id" class="col-sm-2 col-form-label">ID</label>
					</div>
					<div class="col-sm-10">
						<input type="number" class="form-control" placeholder="Product Id" id="id-input-new-product-id" aria-describedby="emailHelp">
					</div>
				</div>
				<div class="mb-1">
					<input  type="text" class="form-control" placeholder="Product Name" id="id-input-new-product-name" aria-describedby="emailHelp" >
				</div>
				<div class="mb-1">
					<textarea placeholder="Product Description" class="form-control" id="id-textarea-new-product-description" rows="3"></textarea>
				</div>
				<div class="mb-1">
					<input  type="number" class="form-control" placeholder="Price" id="id-input-new-product-price" aria-describedby="emailHelp" >
				</div>
				<div class="mb-1">
					<select class="form-select" aria-label="Default select example" id="id-select-new-product-currency" disabled>
						<option selected>USD</option>
					</select>
				</div>
						
			</form>
			<div class="approve-message-container">
			</div>
		</div>
		<div class="modal-footer">
		  	<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
		  	<button type="button" class="btn btn-primary"  onclick="addProductHandler()">Save Product</button>
		</div>
	  </div>
	</div>
	`)
}


function modalEditProduct(product) {
	console.log("modalEditProduct", product)
	return (/*html */`
	<div class="modal-dialog modal-dialog-centered " role="document">
	  <div class="modal-content">
		<div class="modal-header">
		  <h5 class="modal-title" id="approvalModalTitle">Edit Product</h5>
		  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
		</div>
		<div class="modal-body">
			<img class="fill-width" src="${product.image_thumbnail}" id="id-thumbnail-viewer">
			<div class="mb-3">
				<input class="form-control" type="file" id="id-input-thumbnail" oninput="changeImage()">
			</div>
			<form>
				<div class="mb-3 row">
					<div class="col-auto">
						<label for="id-input-product-id" class="col-sm-2 col-form-label">ID</label>
					</div>
					<div class="col-sm-10">
						<input value="${product.id}" type="text" class="form-control" placeholder="Product Name" id="id-input-product-id" aria-describedby="emailHelp" disabled>
					</div>
				</div>
				<div class="mb-1">
					<input value="${product.name}" type="text" class="form-control" placeholder="Product Name" id="id-input-product-name" aria-describedby="emailHelp" >
				</div>
				<div class="mb-1">
					<textarea placeholder="Product Description" class="form-control" id="id-textarea-product-description" rows="3">${product.description}</textarea>
				</div>
				<div class="mb-1">
					<input value="${product.price}" type="number" class="form-control" placeholder="Product Name" id="id-input-product-price" aria-describedby="emailHelp" >
				</div>
				<div class="mb-1">
					<select class="form-select" aria-label="Default select example" id="id-select-product-currency" disabled>
						<option selected>USD</option>
					</select>
				</div>
						
			</form>
			<div class="approve-message-container">
			</div>
		</div>
		<div class="modal-footer">
		  	<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
		  	<button type="button" class="btn btn-primary"  onclick="updateProductHandler()">Update</button>
		</div>
	  </div>
	</div>
	`)
}

function modalDeleteProduct(product_id) {
	console.log("modalEditProduct", product)
	return (/*html */`
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
		<div class="modal-header">
			<h5 class="modal-title">Remove Product</h5>
			<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
		</div>
		<div class="modal-body">
			<p>Are you sure you want to remove this product? This action is irreversible </p>
		</div>
		<div class="approve-message-container">
		<div class="modal-footer">
			<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
			<button type="button" class="btn btn-danger" onclick="deleteProductHandler('${product_id}')" >Delete</button>
		</div>
		</div>
	</div>
	`)
}

function modalSaleDetails(saleDetails) {
	const labProfilesDropdownDiv = saleDetails?.lab_profiles.map((labProfile) => {
		const labProfileInfo = extractJsonFromText(labProfile.text)
		const labProfileOption = /*html */`
			<option value="${labProfile.serial}">${labProfileInfo.name}</option>
		`
		return labProfileOption
	})
	const uspsDownloadLabelButton = isEmpty(saleDetails?.usps_label) ?  /*html */`
	<button type="button" class="btn btn-primary" id="id-generate-usps-label-button" onclick="generateUspsLabelHandler('${saleDetails?._id}', this.id)" disabled>
		Generate Nationial USPS Label
		<i class="fa-solid fa-download"></i>
	</button>
	` : /*html */`
	<button type="button" class="btn btn-secondary" id="id-download-usps-label-button" onclick="downloadUspsLabelHandler('${saleDetails?._id}', this.id)">
		Download USPS Label
		<i class="fa-solid fa-download"></i>
	</button>
	`
	let productsCardComponent = ``
	for (let product of saleDetails?.products_details) {
		hashSectionComponent = ``
		for (hash of product?.hashes) {
			hashSectionComponent += `
				${hash} <br>
			`
		}
		productsCardComponent += /*html */ `
		<div class="card mb-3">
			<div class="row">
				<div class="" style="max-height: 100px; max-width: 100px;">
					<img src="${product?.image_thumbnail}" class="img-fluid rounded-start fill-height" alt="...">
				</div>
				<div class="col-7">
					<div class="card-body">
						<h5 class="card-title">${product?.name}</h5>
						<p class="card-text">Quantity: ${product?.quantity}</p>
					</div>
				</div>
				<div class="col-3">
				<p><strong>Hash Codes</strong></p>
					${hashSectionComponent}
				</div>
			</div>
		</div>
		`
	}
	const toggleStatusButton = saleDetails?.status_code == 0 ?
	/*html */`<button type="button" class="btn btn-success" onclick="toggleSaleStatusHandler('${saleDetails?._id}')" id="sale-toggle-button">Set as SENT</button>`
		:
	/*html */`<button type="button" class="btn btn-dark" onclick="toggleSaleStatusHandler('${saleDetails?._id}')" id="sale-toggle-button">Set as PENDING</button>`
	return (/*html */`
	<div class="modal-dialog modal-dialog-centered modal-lg" role="document">
		<div class="modal-content">
		   <div class="modal-header">
			  <h5 class="modal-title" id="approvalModalTitle">Sale Details</h5>
			  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
		   </div>
		   <div class="modal-body">
			  <form>
				 <div class="mb-1">
					<label for="exampleInputEmail1" class="form-label h6">ID: </label>
					<label for="exampleInputEmail1" class="form-label">${saleDetails?._id}</label>
				 </div>
				 <div class="mb-1">
					<label for="exampleInputEmail1" class="form-label h6">Customer</label>
					<label for="exampleInputEmail1" class="form-label">${saleDetails?.buyer_name}</label>
				 </div>
				 <div class="mb-1">
					<label for="exampleInputEmail1" class="form-label h6">Customer Email</label>
					<label for="exampleInputEmail1" class="form-label">${saleDetails?.buyer_email}</label>
				 </div>
				 <div class="mb-1">
					<label for="exampleInputEmail1" class="form-label h6">Paid</label>
					<label for="exampleInputEmail1" class="form-label">${saleDetails?.amount}</label>
				 </div>
				 <hr>
				 <div class="mb-1">
					<label for="exampleInputEmail1" class="form-label h6">Counrty</label>
					<label for="exampleInputEmail1" class="form-label">${saleDetails?.buyer_country}</label>
				 </div>
				 <div class="mb-1">
					<label for="exampleInputEmail1" class="form-label h6">State</label>
					<label for="exampleInputEmail1" class="form-label">${saleDetails?.buyer_state}</label>
				 </div>
				 <div class="mb-1">
					<label for="exampleInputEmail1" class="form-label h6">City</label>
					<label for="exampleInputEmail1" class="form-label">${saleDetails?.buyer_city}</label>
				 </div>
				 <div class="mb-1">
					<label for="exampleInputEmail1" class="form-label h6">Address</label>
					<label for="exampleInputEmail1" class="form-label">${saleDetails?.buyer_address}</label>
				 </div>
				 <hr>
				 <small>*Note: <strong>Hash codes</strong> are used to link an activation link with your respective purchase, copy and paste a hash code when generating a new biosample activation link</small> 
				 ${productsCardComponent}
				 <hr>
			  <form>
				<div class="mb-1">
					<label for="id-prefix-id-input" class="form-label">Prefix</label>
					<input type="number" class="form-control" id="id-prefix-id-input" oninput="validatePrefix()">
				</div>
				 <div class="mb-1">
					<label for="id-biosample-serial-input" class="form-label">Biosample Serial</label>
					<input type="number" class="form-control" id="id-biosample-serial-input" onchange="validateBiosampleSerial()" oninput="disableButtonWhenWriting()">
					<div class="text-secondary" id="id-verifying-biosample-serial" style="display: none;">
						<div class="spinner-border spinner-border-sm" role="status">
							<span class="visually-hidden">Loading...</span>
						</div>
						Verifying Biosample Serial, please wait...
					</div>
				</div>
				<div class="mb-1">
				 <label for="id-permittee-serial-select" class="form-label">Permittee</label>
				 <select class="form-select" aria-label="Default select example" id="id-permittee-serial-select">
					${labProfilesDropdownDiv}
				  </select>
				</div>
				 <!-- create the -->
				 <div id="printReturnStickerResult" class="rounded p-3 text-wrap text-break"></div>
				 <div style="display: none;" id="returnStickerQrCode"></div>
			  </form>
			  </form>
			  <div class="approve-message-container">
			  </div>
			  <div class="text-danger" id="sale-error-message"></div>
		   </div>
		   <div class="modal-footer">
			  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
			  ${toggleStatusButton}
			  ${uspsDownloadLabelButton}
		   </div>
		</div>
	 </div>
	`)
}


async function validateBiosampleSerial(){
    isValidBiosampleSerial = false;
    $("#id-verifying-biosample-serial").show();
    const biosampleSerialInput = $('#id-biosample-serial-input');
    biosampleSerialInput.removeClass('is-invalid is-valid');
    const biosampleSerial = biosampleSerialInput.val().trim();
    if (!biosampleSerial) {
        biosampleSerialInput.addClass('is-invalid');
        $("#id-verifying-biosample-serial").hide();
        return;
    }
    const biosampleId = parseInt(biosampleSerial, 10);
    if (isNaN(biosampleId) || biosampleId < 1 || biosampleId > 281474976710655) {
        biosampleSerialInput.addClass('is-invalid');
        $("#id-verifying-biosample-serial").hide();
        return;
    }
    const found_biosample = await fetch(`${window.API_BASE}/biosample_activations/?serial=${biosampleSerial}`)
      .then(res => res.json())
      .catch(err => { console.error(err); return null; });
    console.log("found_biosample", found_biosample);
    if (found_biosample && found_biosample.length > 0 ){
      biosampleSerialInput.addClass('is-invalid');
      isValidBiosampleSerial = false;
      $("#id-generate-usps-label-button").attr('disabled', true);
    } else {
      biosampleSerialInput.addClass('is-valid');
      isValidBiosampleSerial = true;
      if (isValidPrefix()){
          $("#id-generate-usps-label-button").attr('disabled', false);
      }
    }
    $("#id-verifying-biosample-serial").hide();
}


function validatePrefix(){
	const prefixInput = $('#id-prefix-id-input');
	prefixInput.removeClass('is-invalid is-valid');
	if (isValidPrefix()){
		prefixInput.addClass('is-valid');
		if (isValidBiosampleSerial){
			$("#id-generate-usps-label-button").attr('disabled', false);
		}
	} else {
		prefixInput.addClass('is-invalid');
		$("#id-generate-usps-label-button").attr('disabled', true);
	}
}


function isValidPrefix(){
	const prefixInput = $('#id-prefix-id-input');
	const prefix = parseInt(prefixInput.val());
	return !isNaN(prefix) && prefix != "" && prefix > 0;
}

function disableButtonWhenWriting(){
	$("#id-generate-usps-label-button").attr('disabled', !(isValidPrefix() && isValidBiosampleSerial));

}
  


function modalDeliveryRawData(biosampleSerial, owner) {
	return /*html */ `
	<div class="modal-dialog modal-dialog-centered modal-lg" role="document">
		<div class="modal-content">
			<div class="modal-header">
				<p class="modal-title" id="selectedBiosample">
					Selected Bio Sample: <strong>${biosampleSerial}</strong> <br>
					Deliver to: <strong>${owner}</strong>	
				</p>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			</div>
			<div class="modal-body">
				<form id="fileUploadForm" class="file-upload-form" ondragover="event.preventDefault()" ondrop="handleFileDrop(event)">
					<div class="file-drop-area text-center border border-dashed rounded py-5">
						<p>Drag & drop your file here or click to upload</p>
						<input type="file" class="file-input" id="fileInput" accept=".csv,.txt,.xlsx" onchange="handleFileUpload(event)" style="display: none;"/>
						<button type="button" class="btn btn-outline-primary mt-3" onclick="document.getElementById('fileInput').click()">Choose File</button>
					</div>
					<div id="fileDetails" class="mt-3"></div>
				</form>
				<div id="delivery-error-message" class="text-danger"></div>
			</div>

			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
				<button type="button" class="btn btn-primary" id="deliverFileButton" onclick="deliverRawDataFileHandler('${biosampleSerial}', '${owner}')" disabled>
					Deliver This File
					<i class="fa-solid fa-arrow-up-from-bracket"></i>
				</button>
			</div>


			<div class="progress" style="height: 8px;">
				<div class="progress-bar" id="id-progress-uploading-file" role="progressbar" style="width: 0%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
			</div>
		</div>
	</div>
	`
}

// JavaScript functions for handling file uploads
function handleFileDrop(event) {
	event.preventDefault();
	const file = event.dataTransfer.files[0];
	if (file) {
		displayFileDetails(file);
		window.uploadedFile = file; // Store the file globally
	}
}

function handleFileUpload(event) {
	const file = event.target.files[0];
	if (file) {
		displayFileDetails(file);
		window.uploadedFile = file; // Store the file globally
	}
}

function displayFileDetails(file) {
	const fileDetails = document.getElementById('fileDetails');
	fileDetails.innerHTML = `<p>File name: <strong>${file.name}</strong></p>`;
	$("#deliverFileButton").attr('disabled', false);
}





function changeImage() {
	const fileInput = $('#id-input-thumbnail')[0];
	const imageViewer = $('#id-thumbnail-viewer');

	if (fileInput.files && fileInput.files[0]) {
		const reader = new FileReader();

		reader.onload = function (e) {
			imageViewer.attr('src', e.target.result);
		}

		reader.readAsDataURL(fileInput.files[0]);
	}
}



function changeNewProductImage() {
	const fileInput = $('#id-input-new-product-thumbnail')[0];
	const imageViewer = $('#id-thumbnail-new-product-viewer');

	if (fileInput.files && fileInput.files[0]) {
		const reader = new FileReader();

		reader.onload = function (e) {
			imageViewer.attr('src', e.target.result);
		}

		reader.readAsDataURL(fileInput.files[0]);
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