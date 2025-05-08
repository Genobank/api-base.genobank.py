const uset_auth_key = "user_sign"
const message = "I am the Chief"
let user_signature
let accessKey
let secretKey
let bucketName
let currentRoute

$(async function () {
		const user_signature = await Login(message, uset_auth_key)
		const double_signarute = await Login(user_signature, uset_auth_key)
		const valid_user = await checkRootUser(double_signarute)
    if (!valid_user){
      throw_alert_message(`Error 401: Unauthorized user: Your key "${double_signarute}" is not valid<br><strong>You need to be a Genobank.io administrator</strong>`);
      throw "No valid root address"
    }
		$(".minter-card-container").show()

		const buckets = await getAvailableBuckets(double_signarute)
		setForm(buckets)
})

window.ethereum.on('accountsChanged', function () {
	localStorage.setItem('user_sign', null);
	window.location.reload();
})


async function connectBucket(){
	user_signature = localStorage.getItem('user_sign')
	accessKey = $("#inputAccessKey").val()
	secretKey = $("#inputSecretKey").val()
	bucketName = $("#inputBucketName").val()
	await renderFiles("")
	$(".bucket-container").show()

}


async function renderFiles(route){
	const bucketContent = await getBucketRouteContent(
		user_signature,
		accessKey,
		secretKey,
		bucketName,
		route
	)
	$("#inputBucketPath").val("./"+route)
	const folders = bucketContent["folders"]
	const totalFolders = bucketContent["total_folders"]
	bucketContent["total_folders"] = bucketContent["total_folders"] == undefined ? 0 : bucketContent["total_folders"]
	bucketContent["total_files"] = bucketContent["total_files"] == undefined ? 0 : bucketContent["total_files"]
	bucketContent["total"] = bucketContent["total"] == undefined ? 0 : bucketContent["total"]
	$("#id-count-folders").html(`Folders: <a href="#${bucketContent["total_folders"]}"> ${bucketContent["total_folders"]} </a>`)
	$("#id-count-files").html(`Files: <a href="#${bucketContent["total_files"]}"> ${bucketContent["total_files"]} </a>`)
	$("#id-count-total").html(`All: <a href="#${bucketContent["total"]}"> ${bucketContent["total"]} </a>`)
	if (totalFolders > 0){
		currentRoute=route
		let htmlFilesContent = ``
		for(let folder of folders){
			isFolder = folder.slice(-1) === '/'
			if(isFolder){
				let fileIcon = isFolder ? '<i class="fa-solid fa-folder"></i>' : '<i class="fa-regular fa-file"></i>';
				let event = isFolder ? 'renderFiles(this.id)' : '';
				let location = folder
				let fileArray = folder.split("/");
				let fileName = folder.charAt(folder.length - 1) === '/' ? fileArray[fileArray.length - 2] : fileArray[fileArray.length - 1];
				let check = isFolder ? `
					${fileIcon}&nbsp;&nbsp;${fileName}
				`:
				`<input class="form-check-input" type="checkbox" value="" id="${fileName}" onclick="fileCounterManager(this.checked, this.id)">
				<label class="form-check-label" for="${fileName}">
					${fileIcon}&nbsp;&nbsp;${fileName}
				</label>`
				
				htmlFilesContent += `
					<tr>
						<td scope="row">
							<div class="form-check">
								<a href="#" id="${location}" onclick="${event}">
									${check} 
								</a>
							</div>
						</td>
					</tr>
				`
			}
		}
		$("#tbody-file-container").html(htmlFilesContent)
	}

}


async function goBack(){
	const inputBucketPath = $("#inputBucketPath").val().toString() 
	const currentLocation = inputBucketPath.slice(2)
	let segments = currentLocation.split("/")
	if(segments[segments.length - 1] == ""){
		segments.pop();
	}
	segments.pop()
	let backLocation = segments.join("/")+"/" == "/" ? "": segments.join("/")+"/"
	renderFiles(backLocation)
}





