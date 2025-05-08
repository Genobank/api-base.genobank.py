let provider
let apiMessage = $("#apiMessage").val()
let userWallet
let currentSelectedPermittee
let web3
let root_sign
let subscriptionsTableBody = $("#subscriptions-table-body")

let isPromtpEditMode = false;
let isSystemRoleEditMode = false;
let isCsvPromptEditMode = false;

let previousPromptText = ""
let previousSystemRoleText = ""
let previousCsvPromptText = ""

const modal = $(".modal")

if (typeof window.ethereum !== 'undefined' || typeof window.web3 !== 'undefined') {
	$(async function () {
		provider = new ethers.providers.Web3Provider(window.ethereum);
		await window.ethereum.request({ method: 'eth_requestAccounts' });
		if (localStorage.getItem('user_sign') == "null" || localStorage.getItem('user_sign') == null) {
			let sign_autentication = await provider.getSigner().signMessage(apiMessage);
			localStorage.setItem('user_sign', sign_autentication);
		}
		root_sign = localStorage.getItem('user_sign');
		let valid_user = await checkRootUser(root_sign)
		if (!valid_user) {
			throw_alert_message(`Error 401: Unauthorized user: Your ${root_sign} key is not valid`);
			throw "No valid root address"
		}
		$(".panel-full-container").show()
		const prompt = await getFullPrompt(root_sign)
		const subscriptionsList = await getSubscriptions(root_sign)
		$("#promptTextArea").val(prompt?.data?.content)
		$("#systemRoleTextArea").val(prompt?.data?.system_role)
		$("#csvPromptTextArea").val(prompt?.data?.csv_prompt)
		rendersubscriptionsTable(subscriptionsList)

		// let list = await getAllPermitteeRequests(root_sign)
		// let deliveries_list = await getAllDeliveries()
		// let allBiosampleWithPendingVariants = await getAllBiosampleWithPendingVariants(root_sign)
		// renderPendingTable(list)
		// renderApprovedTable(list)
		// renderRejectedTable(list)
		// renderDeliveries(deliveries_list)
		// renderBiosamplesWithPendingVariants(allBiosampleWithPendingVariants)
		$("#loading_spinner").hide()
	})

} else {
	console.log("You not have Metamask installed")
}

window.ethereum.on('accountsChanged', function () {
	localStorage.setItem('user_sign', null);
	window.location.reload();
})

function throw_alert_message(title) {
	console.log("throwing alert message")
	$(".no-authorized-user").show();
	$(".alert-danger").html(`
	<p>${title}</p>
	`);
}

async function toggleUpdateSavePrompt(){
	if (isPromtpEditMode){
		const newPrompt = $("#promptTextArea").val()
		await savePromprHandler(newPrompt);
		$("#btn-edit-prompt").html("Edit")
	}else{
		previousPromptText = $("#promptTextArea").val()
		$("#btn-edit-prompt").html("Save")
	}
	$("#promptTextArea").attr("disabled", isPromtpEditMode)
	$("#btn-cancel-editing-prompt").attr("disabled", isPromtpEditMode)
	isPromtpEditMode = !isPromtpEditMode
}

function cancelPrompt (){
	$("#promptTextArea").attr("disabled", true)
	$("#btn-cancel-editing-prompt").attr("disabled", true)
	$("#promptTextArea").val(previousPromptText)
	isPromtpEditMode = false;
	$("#btn-edit-prompt").html("Edit")
}

async function toggleUpdateSaveSystemRole(){
	if (isSystemRoleEditMode){
		const newSystemRole = $("#systemRoleTextArea").val()
		await saveSystemRoleHandler(newSystemRole);
		$("#btn-edit-system-role").html("Edit")
	}else{
		previousSystemRoleText = $("#systemRoleTextArea").val()
		$("#btn-edit-system-role").html("Save")
	}
	$("#systemRoleTextArea").attr("disabled", isSystemRoleEditMode)
	$("#btn-cancel-editing-system-role").attr("disabled", isSystemRoleEditMode)
	isSystemRoleEditMode = !isSystemRoleEditMode
}

function cancelSystemRole(){
	$("#systemRoleTextArea").attr("disabled", true)
	$("#btn-cancel-editing-system-role").attr("disabled", true)
	$("#systemRoleTextArea").val(previousSystemRoleText)
	isSystemRoleEditMode = false;
	$("#btn-edit-system-role").html("Edit")
}

async function toggleUpdateSaveCSVPrompt(){
	if (isCsvPromptEditMode){
		const newCsvPrompt = $("#csvPromptTextArea").val()
		await saveCsvPromptHandler(newCsvPrompt);
		$("#btn-edit-csv-prompt").html("Edit")
	}else{
		previousCsvPromptText = $("#csvPromptTextArea").val()
		$("#btn-edit-csv-prompt").html("Save")
	}
	$("#csvPromptTextArea").attr("disabled", isCsvPromptEditMode)
	$("#btn-cancel-editing-csv-prompt").attr("disabled", isCsvPromptEditMode)
	isCsvPromptEditMode = !isCsvPromptEditMode
}

function cancelCsvPromtp(){
	$("#csvPromptTextArea").attr("disabled", true)
	$("#btn-cancel-editing-csv-prompt").attr("disabled", true)
	$("#csvPromptTextArea").val(previousCsvPromptText)
	isCsvPromptEditMode = false;
	$("#btn-edit-csv-prompt").html("Edit")
}


function rendersubscriptionsTable(subscriptionsList){
	subscriptionsTableBody.empty()
	if (!isEmpty(subscriptionsList?.data)){
		for (const subscription of subscriptionsList?.data){
			console.log(subscription)
			const deleteIcon = subscription?.subscription_id == "" ? 
				/*html */`
				<button class="btn btn-danger"  onclick="openDeleteSubscriptionModal('${subscription?.owner}')">
					<i class="fa-solid fa-trash" ></i>
				</button>	
				` 
				:
				""
			subscriptionsTableBody.append(/*html */`
				<tr>
					<td>${subscription?._id}</td>
					<td>${subscription?.owner}</td>
					<td>${subscription?.status}</td>
					<td>${subscription?.order_type}</td>
					<td>${subscription?.createdAt}</td>
					<td>${deleteIcon}</td>
				</tr>
			`)
		}
	}
}

async function savePromprHandler(newPrompt){
	try{
		const sanitizedPrompt = sanitizePrompt(newPrompt)
		const data = new FormData();
		const registerFormData = {
			"rootSignature": root_sign,
			"promptContent": newPrompt,
			"sanitizedPrompt": sanitizedPrompt
		}
		data.append("data", JSON.stringify(registerFormData));
		await savePrompt(data)
	}catch(e){
		throw e
	}
}


async function saveSystemRoleHandler(newSystemRole){
	try{
		const data = new FormData();
		const registerFormData = {
			"rootSignature": root_sign,
			"SystemRoleContent": newSystemRole
		}
		data.append("data", JSON.stringify(registerFormData));
		await saveSystemRole(data)
	}catch(e){
		throw e
	}
}


async function saveCsvPromptHandler(newCsvPrompt){
	try{
		const data = new FormData();
		const registerFormData = {
			"rootSignature": root_sign,
			"csvpromptContent": newCsvPrompt
		}
		data.append("data", JSON.stringify(registerFormData));
		await saveCsvPrompt(data)
	}catch(e){
		throw e
	}
}


function openDeleteSubscriptionModal(ownerWallet){
	console.log("ownerWallet", ownerWallet)
	$("#modalContainerDeleteSubscription").html(modalDeleteSubscriptionComponent(ownerWallet));
	$("#modalContainerDeleteSubscription").modal("show");
}

function validateUsersWallet(){
    const usersWallet = $("#input-users-wallet").val();
    const isValidWallet = /^0x[a-fA-F0-9]{40}$/.test(usersWallet);
    $("#btn-add-lifetime-subscription").attr("disabled", !isValidWallet);
}

async function createLifetimeSubscriptionHandler(){
	$("#error-subscription-message").html("")
	try{
		
		const owner = $("#input-users-wallet").val();
		const data = new FormData();
		const registerFormData = {
			"rootSignature": root_sign,
			"owner": owner
		}
		data.append("data", JSON.stringify(registerFormData));
		await createLifetimeSubscription(data)
		const subscriptionsList = await getSubscriptions(root_sign)
		rendersubscriptionsTable(subscriptionsList)
		$("#input-users-wallet").val("")
	}catch(e){
		$("#error-subscription-message").html(`${e?.response?.data?.status_details?.description}`)
		throw e

	}
}


async function deleteLifetimeSubscriptionHandler(owner){
	$("#delete-suscription-error-message").html("")
	const btnContent = $("#btn-delete-subscription").html()
	try{
		$("#tn-delete-subscription").attr("disabled", true)
		$("#tn-delete-subscription").html(/*html */`
				<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
				Loading...
		`)

		const data = new FormData();
		const deleteFormData = {
			"rootSignature": root_sign,
			"owner": owner
		}
		data.append("data", JSON.stringify(deleteFormData));
		await deleteLifetimeSubscription(data)
		$("#modalContainerDeleteSubscription").modal("hide");

		const subscriptionsList = await getSubscriptions(root_sign)
		rendersubscriptionsTable(subscriptionsList)
	}catch(e){
		$("#delete-suscription-error-message").attr("disabled", false)
		$("#btn-delete-subscription").html(btnContent)
		$("#delete-suscription-error-message").html(`${e?.response?.data?.status_details?.description}`)
		throw e
	}
}


function sanitizePrompt(prompt) {
    prompt = prompt.replace(/["'\s]*\{\s*csvfilename\s*\}["'\s]*/gi, `{file_name}`);
    prompt = prompt.replace(/["'\s]*\{\s*csv_content\s*\}["'\s]*/gi, `<dataset>'{file_content}'</dataset>`);
    return prompt;
}
