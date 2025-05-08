async function throw_alert_message(title){
	$(".no-authorized-user").show();
	$(".alert-danger").html(`
	<p>${title}</p>
	`);
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


  function shortString(str, startChars, endChars) {
	if (startChars + endChars >= str.length) {
	  return str;
	}
	return str.substring(0, startChars) + "..." + str.substring(str.length - endChars);
  }
  
  function shortWallet(wallet) {
	return shortString(wallet, 7, 5);
  }
  
  function shortTransactionHash(transactionHash) {
	return shortString(transactionHash, 14, 12);
  }