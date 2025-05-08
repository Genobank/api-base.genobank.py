const toDataURL = url => fetch(url)
	.then(response => response.blob())
	.then(blob => new Promise((resolve, reject) => {
		const reader = new FileReader()
		reader.onloadend = () => resolve(reader.result)
		reader.onerror = reject
		reader.readAsDataURL(blob)
	}))



async function printReturnSticker() {
	if (validatePrintReturnSticker()) {
		const url = $('#returnStickerLaboratoryUrl').val();
		console.log("url: " + url)
		const element = document.getElementById("returnStickerQrCode");
		console.log("element: " + element)


		new QRCode(element, {
			text: url,
			width: 200,
			height: 200,
			colorDark: "#000000",
			colorLight: "#ffffff",
			correctLevel: QRCode.CorrectLevel.M
		});

		setTimeout(generateReturnSticker, 1000);
	}
}


async function generateReturnSticker() {
	const laboratoryUrl = $('#returnStickerLaboratoryUrl').val();
	const trackingCode = $('#returnStickerTrackingCode').val();
	const url = new URL(laboratoryUrl);
	let biosampleId = url.searchParams.get('biosampleId');
	biosampleId = formatBiosampleId(biosampleId);
	const barcode = `(42)0921231111(${trackingCode.substr(0, 2)})${trackingCode.substr(2)}`;

	const doc = new PDFDocument({
		size: [288, 432],
		margins: {
			top: 0,
			bottom: 0,
			left: 0,
			right: 0,
		}
	});

	const formattedTrackingCode = [
		trackingCode.substr(0, 4),
		trackingCode.substr(4, 4),
		trackingCode.substr(8, 4),
		trackingCode.substr(12, 4),
		trackingCode.substr(16, 4),
		trackingCode.substr(20),
	].join(' ');

	// pipe the document to a blob
	const stream = doc.pipe(blobStream());

	const template = await toDataURL('/js/shop_manager/scripts/ups-tracking-clean.png');
	doc.image(template, 0, 0, { width: 288 });

	const element = document.getElementById("returnStickerQrCode");
	const img = element.getElementsByTagName('img');
	doc.image(img[0].src, 18, 296, { width: 36 });

	let canvas = document.createElement('canvas');
	try {
		bwipjs.toCanvas(canvas, {
			bcid: 'gs1-128',       // Barcode type
			text: barcode,    // Text to encode
			scale: 2,               // 3x scaling factor
			height: 17,              // Bar height, in millimeters
			includetext: false,            // Show human-readable text
			//padding: 5,
			//textxalign:  'center',        // Always good to set this
		});
		doc.image(canvas.toDataURL('image/png'), 18, 218, { width: 252 });
	} catch (e) {
		console.log(e);
	}


	// add your content to the document here, as usual
	doc.fontSize(8);
	doc.font('Helvetica-Bold');
	doc.text(`${formattedTrackingCode}`, 18, 278, { width: 252, height: 9, align: 'center' });
	doc.fontSize(10);
	doc.text(`Laboratory activation URL`, 65, 302);
	doc.text(`Biosample ID ${biosampleId}`, 65, 313);

	// get a blob when you're done
	doc.end();
	stream.on('finish', function () {
		// get a blob you can do whatever you like with
		const blob = stream.toBlob('application/pdf');
		const fileName = `tracking-sticker-${trackingCode}.pdf`;
		if (navigator.msSaveBlob) {
			// IE 10+
			navigator.msSaveBlob(blob, fileName);
		} else {
			const link = document.createElement('a');
			// Browsers that support HTML5 download attribute
			if (link.download !== undefined) {
				const url = URL.createObjectURL(blob);
				link.setAttribute('href', url);
				link.setAttribute('download', fileName);
				link.style.visibility = 'hidden';
				document.body.appendChild(link);
				link.click();
				document.body.removeChild(link);
			}
		}
	});
}


async function generateUspsLabelHandler(productId, buttonId){
	console.log("buttonId", buttonId)
	const button = $("#"+buttonId)
	const prevHtmlButton = button.html();
	const biosampleSerial = $("#id-biosample-serial-input").val();
	const permitteeSerial = $("#id-permittee-serial-select").val()
	const prefix = $("#id-prefix-id-input").val()
	try{
		button.html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...`)
		const userSignature = root_sign;
		// const pdf_links = await generateNationalUSPSLabel(userSignature, productId);
		const pdf_links = await generateActivationLinkAndNationalUSPSLabel(userSignature, productId, biosampleSerial, permitteeSerial, prefix);
		
		if ("download_links" in pdf_links){
			if (pdf_links.download_links.length > 0){
				window.open(pdf_links.download_links[0], '_blank');
			}
		}
	}catch(e){
		console.log(e)
	}finally{
		button.html(prevHtmlButton)
	}
}


async function downloadUspsLabelHandler(productId, buttonId){
	console.log("buttonId", buttonId)
	const button = $("#"+buttonId)
	const prevHtmlButton = button.html();
	try{
		button.html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Downloading...`)
		const userSignature = root_sign;
		const pdf_links = await getNationalLabelPresignedLinks(userSignature, productId);
		if ("download_links" in pdf_links){
			if (pdf_links.download_links.length > 0){
				window.open(pdf_links.download_links[0], '_blank');
			}
		}
	}catch(e){
		console.log(e)
	}finally{
		button.html(prevHtmlButton)
	}
}


function formatBiosampleId(biosampleId) {
	const remainder = biosampleId.length % 4;
	if (remainder > 0) {
		biosampleId = `${Array(5 - remainder).join("0")}${biosampleId}`;
	}
	const biosampleArray = split(biosampleId, 4);
	biosampleId = biosampleArray.join('-');
	return biosampleId;
}

function split(input, len) {
	return input.match(new RegExp('.{1,' + len + '}(?=(.{' + len + '})+(?!.))|.{1,' + len + '}$', 'g'))
}