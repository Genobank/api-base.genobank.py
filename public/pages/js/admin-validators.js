$(document).ready(async function(){
  $('#createBiosampleBiosampleId').on('blur', async function() {
    const biosampleId = $('#createBiosampleBiosampleId').val();
    const success = await checkCreateBiosampleBiosampleId(biosampleId) && await checkBiosampleActivations(biosampleId);
    const cssClass = success ? 'text-success' : 'text-danger';
    const icon = success ? 'fa-check' : 'fa-times';
    const text = `Biosample ID #${biosampleId} ${success ? 'has NOT been activated by a customer yet.' : 'was already activated by a customer or activation was already generated.'}`;
    if (success) {
      $('#createBiosampleBiosampleId').addClass('is-valid');
      $('#createBiosampleBiosampleId').removeClass('is-invalid');
    } else {
      $('#createBiosampleBiosampleId').addClass('is-invalid');
      $('#createBiosampleBiosampleId').removeClass('is-valid');
    }
    $('#createBiosampleBiosampleIdValidation').html(`
      <small class="form-text ${cssClass}">
        <i class="fa ${icon}"></i> ${text}
      </small>
    `);
  });
});

function validateCreateBiosampleButton() {
  if ($('#createBiosampleBiosampleId').hasClass('is-valid') &&
    $('#createBiosamplePhysicalId').val() &&
    $('#createBiosampleApplicationSecret').val()
  ) {
    return true;
  } else {
    return false;
  }
}

async function checkCreateBiosampleBiosampleId(biosampleId) {
  const url = `${window.API_BASE}/get_biosamples/?serial=${biosampleId}`;
  return fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  }).then(async (res) => {
    const result = await res.json();
    if (result.errors) {
      return true;
    }
    return false;
  }).catch((error) => {
    console.log(error);
    return true;
  });
}

async function checkBiosampleActivations(biosampleId) {
  // const url = `${window.API_BASE}/biosample-activations?filterSerials[0]=${biosampleId}`;
  const url = `${window.API_BASE}/biosample-activations?serial=${biosampleId}`;
  return fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  }).then(async (res) => {
    const result = await res.json();
    if (result.data?.length > 0) {
      return false;
    }
    return true;
  }).catch((error) => {
    console.log(error);
    return true;
  });
}