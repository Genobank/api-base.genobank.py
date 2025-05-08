
async function Login(message, storageKey){
  if (typeof window.ethereum !== 'undefined' || typeof window.web3 !== 'undefined') {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    await window.ethereum.request({ method: 'eth_requestAccounts' });
    const sign_autentication = await provider.getSigner().signMessage(message);
    localStorage.setItem(storageKey, sign_autentication);
    return sign_autentication
  } else {
    console.log("You not have Metamask installed")
  }
}

function getValidations(value){
  return value == "null" || value == null || value == ""
}

