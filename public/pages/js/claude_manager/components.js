function modalDeleteSubscriptionComponent(ownerWallet){
	return /*html */`
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				¿Delete subscription?
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			</div>
			<div class="modal-body">
				Are you sure you want to unsubscribe for user <strong>${ownerWallet}</strong>? This action cannot be undone
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
				<button type="button" id="btn-delete-subscription" class="btn btn-danger" onclick="deleteLifetimeSubscriptionHandler('${ownerWallet}')" >
					<i class="fa-solid fa-trash"></i>
					Delete
				</button>
			</div>
			<div class="text-danger" id="delete-suscription-error-message"></div>
		</div>
	</div>
`
}