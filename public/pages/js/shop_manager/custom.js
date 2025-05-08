let provider
let apiMessage = $("#apiMessage").val()
let userWallet
let currentSelectedPermittee
let web3
let root_sign

let isValidBiosampleSerial = false


RawDataDeliveryTable = $('#raw-data-delivery-table').DataTable()
TokenHoldersTable = $('#token-holders-table').DataTable()

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
    let product_list = await getAllProducts()
    let sales_list = await getAllSales()
    const deliveries_list = await getRawDataDeliveries(root_sign)
    const token_holders_list = await getTokenHolders(root_sign)

    console.log("token_holders_list", token_holders_list)

    // let deliveries_list = await getAllDeliveries()
    renderProductsTable(product_list.products)
    renderSalesTable(sales_list.sales)
    renderRawDataDeliveriesTable(deliveries_list.data)
    renderTokenHoldersTable(token_holders_list)
    
    // renderRejectedTable(product_list)


    // renderDeliveries(deliveries_list)
    $("#loading_spinner").hide()
  })
  
} else {
  console.log("You not have Metamask installed")
}

window.ethereum.on('accountsChanged', function () {
  localStorage.setItem('user_sign', null);
  window.location.reload();
})


async function renderProductsTable(products){

  let innerTableBody = ``
  for (product of products){
    let productString = JSON.stringify(product).replace(/"/g, '&quot;');
    innerTableBody+= /*html */ `
    <tr>
      <td>${product.id}</td>
      <td><img src="${product.image_thumbnail}" width="66px" height="44px"></td>
      <td>${product.name}</td>
      <td>${product.description}</td>
      <td>${product.price}</td>
      <td>${product.currency}</td>
      <td>
        <button type="button"  onclick="openEditModal('${productString}')" class="btn btn-primary">EDIT</button>
        <button type="button"  onclick="openDeleteProductModal('${product.id}')" class="btn btn-danger">DELETE</button>
      </td>
    </tr>
    `
  }
  innerTableBody += /*html */`
    <tr>
      <td colspan="7" class="text-center">
      
      <button type="button" class="btn btn-light" onclick="openAddProductModal()">
        <i class="fa-solid fa-circle-plus"></i>
        Add New Product
      </button>

      </td>
    </tr>
  ` 
  $("#product-list-body").html(innerTableBody)
}


function openAddProductModal(){
  $("#addProductModal").html(modalAddProduct())
  $("#addProductModal").modal("show")
}

function openEditModal(productString){
  let product = JSON.parse(productString);
  $("#editProductModal").html(modalEditProduct(product))
  $("#editProductModal").modal("show")
}

function openDeleteProductModal(productId){
  console.log(productId)
  $("#deleteProductModal").html(modalDeleteProduct(productId))
  $("#deleteProductModal").modal("show")
}

async function openSaleDetailsModal(saleId){
  let saleDetails = await getSaleById(saleId)
  $("#saleDetailsModal").html(modalSaleDetails(saleDetails?.sale))
  $("#saleDetailsModal").modal("show")
}

function openrawDataDeliveryModal(biosampleSerial, owner){
  $("#rawDataDeliveryModal").html(modalDeliveryRawData(biosampleSerial, owner))
  $("#rawDataDeliveryModal").modal("show")
}

async function renderSalesTable(saleList){
  // let approved_list = permittees_list.filter(perm => perm.status === 1);
  let innerTableBody = ``
  for (sale of saleList){
    const statusLabel = sale?.status_code == 0 ? 
    /*html */` ${sale?.status}`: /*html */`
      ${sale?.status}
      <i class="fa-solid fa-circle-check" style="color: #217a00;"></i>
    `
    innerTableBody+= /*html */ `
    <tr>
      <td>${sale?._id}</td>
      <td>${sale?.buyer_name}</td>
      <td>${sale?.buyer_email}</td>
      <td>${sale?.product_count}</td>
      <td>${statusLabel}</td>
      <td>${sale?.amount}</td>
      <td>
        <button class="btn btn-primary" onclick="openSaleDetailsModal('${sale?._id}')">
          Details
        </button>
      </td>
    </tr>
    `
  }
  $("#sales-list-body").html(innerTableBody)
}


async function toggleSaleStatusHandler(saleId){
  const prevousBtnContent = $("#sale-toggle-button").html()
  $("#sale-error-message").html("")
  try{
    $("#sale-toggle-button").attr("disabled",true)
    $("#sale-toggle-button").html(/*html */`
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      Loading...
    `)

    const data = new FormData();
    const saleFormData = {
      "sale_id": saleId,
      "rootSignature": root_sign
    }
    data.append("data", JSON.stringify(saleFormData));
    await postToggleSaleStatus(data);
    let sales_list = await getAllSales()
    renderSalesTable(sales_list.sales)

    if($("#sale-toggle-button").hasClass("btn-success")){
        $("#sale-toggle-button").removeClass("btn-success")
        $("#sale-toggle-button").addClass("btn-dark")
        $("#sale-toggle-button").text("Set as PENDING")

    }else{
      $("#sale-toggle-button").removeClass("btn-dark")
      $("#sale-toggle-button").addClass("btn-success")
      $("#sale-toggle-button").text("Set as SENT")

    }

    $("#sale-toggle-button").attr("disabled",false)



  }catch(e){
    console.log("error", e);
    $("#sale-toggle-button").attr("disabled",false)

    const errorMessage = e?.response?.data?.status_details?.description ? e?.response?.data?.status_details?.description : e?.message
    $("#sale-toggle-button").html(prevousBtnContent)
    $("#sale-error-message").html("Error: " + errorMessage)
  }
}


async function renderRawDataDeliveriesTable(biosampleList){
  let data = []
  for (const biosample of biosampleList){
    let actionButton = isEmpty(biosample?.raw_data_delivery) ? 
    /*html */`<button class="btn btn-primary" style="min-width: 200px !important;" onclick="openrawDataDeliveryModal('${biosample?.serial}', '${biosample?.owner}')">Deliver 23andme file</button>`
    :
    /*html */`<button class="btn btn-outline-secondary" style="min-width: 200px !important;" disabled >Delivered</button>`
    data.push([
      biosample?.serial,
      biosample?.owner,
      biosample?.status ,
      formatDate(biosample?.createdAt),
      actionButton
    ]);
  }

  RawDataDeliveryTable.clear();
  RawDataDeliveryTable.rows.add(data);
  RawDataDeliveryTable.draw();
}


function renderTokenHoldersTable(tokenHolderList){
  let data = []
  for (const tokenHolder of tokenHolderList){
    const transactionDiv = /*html */`
      <a href="https://testnet.snowtrace.io/tx/${tokenHolder?.tx_hash}" target= "_blank">
        ${shortTransactionHash(tokenHolder?.tx_hash)}
      </a>
    `
    data.push([
      shortWallet(tokenHolder?.wallet),
      tokenHolder?.token_id,
      transactionDiv,
      tokenHolder?.sex ,
      formatDate(tokenHolder?.createdAt),
    ]);
  }
  TokenHoldersTable.clear();
  TokenHoldersTable.rows.add(data);
  TokenHoldersTable.draw();
}



async function deliverRawDataFileHandler(biosampleSerial, owner) {
	const file = window.uploadedFile;
  $("#delivery-error-message").html("")
  const buttonContent = $("#deliverFileButton").html()
  try{
    $("#deliverFileButton").html(/*html */
      `<span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
      <span role="status">Uploading...</span>`
    )
    const data = new FormData();
    const registerFormData = {
      "biosampleSerial": biosampleSerial,
      "owner": owner,
      "rootSignature": root_sign
    }
    data.append("file", file);
    data.append("data", JSON.stringify(registerFormData));
    await postDeliveryRawData(data, onUploadingFile);
    const deliveries_list = await getRawDataDeliveries(root_sign)
    renderRawDataDeliveriesTable(deliveries_list.data)
    $("#rawDataDeliveryModal").modal("hide")
  }catch(e){
    console.log("error", e);
    const errorMessage = e?.response?.data?.status_details?.description ? e?.response?.data?.status_details?.description : e?.message
    $("#deliverFileButton").html(buttonContent)
    $("#id-progress-uploading-file").attr('style',`width: ${Math.round(0)}%; background-color: #ff0000;`);
    $("#delivery-error-message").html("Error: " + errorMessage)
  }
}



function onUploadingFile(progressEvent) {
  const percentCompleted = (progressEvent.loaded / progressEvent.total) * 100;
  const color = getProgressColor(percentCompleted);
  $("#id-progress-uploading-file").attr('style',`width: ${Math.round(percentCompleted)}%; background-color: ${color};`);
}


async function renderRejectedTable(permittees_list){
  let rejected_list = permittees_list.filter(perm => perm.status === 2);
  let innerTableBody = ``
  for (i in rejected_list){
    innerTableBody+= /*html */ `
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
  if (deliveries_list.length > 0){
    for (delivery of deliveries_list.data){
      let sharedFiles = ``
      for (file in delivery.files){
        sharedFiles+=file+"<br>"
      }
      innerTableBody+= /*html */ `
      <tr>
        <td>${delivery.biosample_serial}</td>
        <td style="text-align: center;">
          <a href="https://testnet.snowtrace.io/address/${delivery.owner}" target="_blank" title="${delivery.owner}">
            ${delivery.owner.substr(0,10)}...${delivery.owner.substr(delivery.owner.length-10,delivery.owner.length)}
          </a>
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

async function setCurrentOwner (button){
  let _owner = button.getAttribute("data-owner");
  currentSelectedPermittee = _owner
  $(".permittee-address").html(_owner)
  console.log(currentSelectedPermittee)
}

async function addProductHandler(){
  let messageDiv = $(".approve-message-container");
  try{
    showSpinner(messageDiv);
    const fileInput = $('#id-input-new-product-thumbnail')[0];
    const file = fileInput.files[0];
    const metadata = {
      "id": $("#id-input-new-product-id").val(),
      "name": $("#id-input-new-product-name").val(),
      "description": $("#id-textarea-new-product-description").val(),
      "price": $("#id-input-new-product-price").val(),
      "currency": $("#id-select-new-product-currency").val()
    };
    console.log("metadata: ", metadata)
    const response = await addProduct(root_sign, metadata, file);
    if (response.status === "Failure"){
      throw new Error(response.status_details.description)
    }
    console.log("response: ", response)
    $("#id-input-new-product-id").val("0")
    $("#id-input-new-product-name").val("")
    $("#id-textarea-new-product-description").val("")
    $("#id-textarea-new-product-description").val("0.00")
    showSuccessMessage(messageDiv, "Saved Product", "Saved");
    let list = await getAllProducts()
    renderProductsTable(list.products)
  }catch(e){
    showErrorMessage(messageDiv, "Error", e)
  }
  
}


async function deleteProductHandler(productId){
  let messageDiv = $(".approve-message-container");
  try{
    showSpinner(messageDiv);
    const metadata = {
      "id": productId
    };
    const response = await deleteProduct(root_sign, metadata);
    if (response.status === "Failure"){
      throw new Error(response.status_details.description)
    }
    console.log("response: ", response)
    showSuccessMessage(messageDiv, "Deleted Product", "Deleted");
    let list = await getAllProducts()
    renderProductsTable(list.products)
    $("#deleteProductModal").modal("hide")
  }catch(e){
    showErrorMessage(messageDiv, "Error", e)
  }
  
}


async function updateProductHandler(){
    let messageDiv = $(".approve-message-container");
    showSpinner(messageDiv);

    const fileInput = $('#id-input-thumbnail')[0];
    const file = fileInput.files[0];

    const metadata = {
      "id": $("#id-input-product-id").val(),
      "name": $("#id-input-product-name").val(),
      "description": $("#id-textarea-product-description").val(),
      "price": $("#id-input-product-price").val(),
      "currency": $("#id-select-product-currency").val()
    };
    await updateProduct(root_sign, metadata, file);
    showSuccessMessage(messageDiv, "Updated Successfully", "Updated");

    let list = await getAllProducts()
    renderProductsTable(list.products)
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
        getAllProducts(root_sign).then(list => {
          
          renderProductsTable(list)
          renderSalesTable(list)
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

  console.log(rejected_permittee)
}


// messages alerts








modal.on('hidden.bs.modal', function (event) {
  $(".reject-message-container").html('');
  $(".approve-message-container").html('');
});






function formatDate(dateString) {
  // Parseamos la fecha desde el string inicial
  const date = new Date(dateString);

  // Opciones para formatear la fecha
  const options = {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
  };

  // Devolvemos la fecha formateada de acuerdo a las opciones
  return date.toLocaleString('en-US', options);
}

