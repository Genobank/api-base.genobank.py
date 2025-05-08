async function checkRootUser (sign){
	let validated = await fetch(
	  `${window.NEWAPIBASE}/validate_root_user/${sign}`,{
		method: 'GET',
		header: {
		  'Content-Type': 'application/json',
		  'Access-Control-Allow-Origin': '*'
		},
	}).then((res) => {
	  return res.json()
	}).catch((error) => {
	  console.error(error);
	})
	return validated
}


async function getFullPrompt(rootSignature) {
	const url = new URL(`${window.NEWAPIBASE}/api_claude_ia/get_full_prompt`)
	url.searchParams.append('root_signature', rootSignature);
	return await fetch(url)
		.then(response => {
			if (!response.ok) {
				const errorResponse = response.json(); 
				throw errorResponse
			}
			return response.json();
		})
		.catch(error => {
			console.error('Fetch error:', error);
			throw error
		});
}

async function getSubscriptions(rootSignature) {
	const url = new URL(`${window.NEWAPIBASE}/api_claude_ia/get_all_subscriptions`)
	url.searchParams.append('root_signature', rootSignature);
	return await fetch(url)
		.then(response => {
			if (!response.ok) {
				const errorResponse = response.json(); 
				throw errorResponse
			}
			return response.json();
		})
		.catch(error => {
			console.error('Fetch error:', error);
			throw error
		});
}
  



async function savePrompt(data) {
	const url = `${window.NEWAPIBASE}/api_claude_ia/save_prompt`;
	const config = {
		headers: {
			"Content-Type": "multipart/form-data"
		}
	};
	try {
		const res = await axios.post(url, data, config);
		console.log("this is the normal response\n", res);
		return res;
	} catch (err) {
		console.log("Error completo:", err);
		throw err; // Lanzar el error para que pueda ser capturado por el llamador
	}
}


async function saveSystemRole(data) {
	const url = `${window.NEWAPIBASE}/api_claude_ia/save_system_role`;
	const config = {
		headers: {
			"Content-Type": "multipart/form-data"
		}
	};
	try {
		const res = await axios.post(url, data, config);
		console.log("this is the normal response\n", res);
		return res;
	} catch (err) {
		console.log("Error completo:", err);
		throw err; // Lanzar el error para que pueda ser capturado por el llamador
	}
}


async function saveCsvPrompt(data) {
	const url = `${window.NEWAPIBASE}/api_claude_ia/save_csv_prompt`;
	const config = {
		headers: {
			"Content-Type": "multipart/form-data"
		}
	};
	try {
		const res = await axios.post(url, data, config);
		console.log("this is the normal response\n", res);
		return res;
	} catch (err) {
		console.log("Error completo:", err);
		throw err; // Lanzar el error para que pueda ser capturado por el llamador
	}
}


async function createLifetimeSubscription(data) {
	const url = `${window.NEWAPIBASE}/api_claude_ia/create_lifetime_subscription_from_root`;
	const config = {
		headers: {
			"Content-Type": "multipart/form-data"
		}
	};
	try {
		const res = await axios.post(url, data, config);
		console.log("this is the normal response\n", res);
		return res;
	} catch (err) {
		throw err; // Lanzar el error para que pueda ser capturado por el llamador
	}
}


async function deleteLifetimeSubscription(data) {
	const url = `${window.NEWAPIBASE}/api_claude_ia/delete_lifetime_subscription_from_root`;
	const config = {
		headers: {
			"Content-Type": "multipart/form-data"
		}
	};
	try {
		const res = await axios.post(url, data, config);
		console.log("this is the normal response\n", res);
		return res;
	} catch (err) {
		throw err; // Lanzar el error para que pueda ser capturado por el llamador
	}
}