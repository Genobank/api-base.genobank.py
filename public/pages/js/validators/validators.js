async function throw_alert_message(title){
  $(".no-authorized-user").show();
  $(".alert-danger").html(`
  <p>${title}</p>
  `);
}


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