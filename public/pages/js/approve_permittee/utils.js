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