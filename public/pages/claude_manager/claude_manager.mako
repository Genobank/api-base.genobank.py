<%include file="../components/basic_scripts.mako" args="section='Permittees', env=env" />

<!DOCTYPE html>
<html>
	<head>
		<title>Claude - Claude Manager</title>
		<style>
		.nav-tabs .nav-item .nav-link { 
			color: rgba(255, 255, 255);
			border-color: rgba(255, 255, 255, 0.01);
		}
		.nav-tabs .nav-item .nav-link.active {
			margin-top:-10px;
			margin-bottom:-10px;
			height:60px;
			color: rgba(255, 255, 255);
			border-color: rgba(0, 0, 0, 0);
			background-color: rgba(0, 0, 0, 0.1);
			border-radius: 0px;
		}
		</style>
    	<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    	<link rel="stylesheet" href="/js/bootstrap/css/custom-spinner.css"/>
		<link href="/static/pages/permittees_manager/style.css" rel="stylesheet">

	</head>
	<body>
    	<input type="hidden" id="apiMessage" name="valor_oculto" value="${api_msg}">
		<div class="panel-full-container" style="display: none;">
			<ul class="navbar nav nav-tabs mb-3 navbar-expand-lg" id="pills-tab" role="tablist" style="background-image: linear-gradient(134.89deg, #49ba80 8.12%, #009abb 34.85%, #344da1 62.73%, #b03c96 86.11%);">
				<li class="nav-item" role="presentation">
					<object data="/images/GenoBank.io_white_logo.svg" width="160" height="30"> </object><br>
				</li>
				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
						Managers
					</a>
					<ul class="dropdown-menu">
						<li><a class="dropdown-item" href="/manager_dashboard"><i class="fa-solid fa-house"></i> General Manager</a></li>
						<li><a class="dropdown-item" href="/shop_manager"><i class="fa-solid fa-shop"></i> Shop Manager</a></li>
						<li><a class="dropdown-item" href="#"><i class="fa-solid fa-comment"></i> Claude Manager</a></li>
					</ul>
				</li>
				<li class="nav-item" role="presentation">
					<button class="nav-link active" id="pills-pending-tab" data-bs-toggle="pill" data-bs-target="#pills-pending" type="button" role="tab" aria-controls="pills-pending" aria-selected="true" >Prompt</button>
				</li>
				<li class="nav-item" role="presentation">
					<button class="nav-link" id="pills-approved-tab" data-bs-toggle="pill" data-bs-target="#pills-approved" type="button" role="tab" aria-controls="pills-approved" aria-selected="false" >Subscriptions</button>
				</li>
			</ul>
			<div class="tab-content" id="pills-tabContent">
				<div class="tab-pane fade show active" id="pills-pending" role="tabpanel" aria-labelledby="pills-pending-tab">
					<div class="container">
						<h1 class="h3">Prompt</h1>
						<div>Write the initial message so that Claude understands how to start a new chat, you must use the 2 variables that Claude needs <strong>{file_name}</strong> and <strong>{file_content}</strong> use them anywhere in the promtp content</div>
						Sample of valid prompt: <br><br>
						<footer class="blockquote-footer">Analyze the genetic variants of the file {file_name} and this is its content: {file_content}</footer>
						<form>
							<div class="mb-3">
								<div class="form-floating">
									<textarea class="form-control" placeholder="Write the prompt here" id="promptTextArea" style="height: 450px" spellcheck="false" disabled></textarea>
									<label for="promptTextArea">Initial Prompt</label>
								</div>
							</div>
							<div class="d-grid gap-2 d-md-flex justify-content-md-end">
								<button class="btn btn-secondary" type="button" onclick="cancelPrompt()" id="btn-cancel-editing-prompt" disabled>Cancel</button>
								<button class="btn btn-primary" type="button" onclick="toggleUpdateSavePrompt()" id="btn-edit-prompt">Edit</button>
							</div>
						</form>
						<h1  class="h3">System Role</h1>
						<div>Write a system role </div>
						Sample of valid System Role: <br><br>
						<footer class="blockquote-footer">You are the best genetic variant analyst in the world</footer>
						<form>
							<div class="mb-3">
								<div class="form-floating">
									<textarea class="form-control" placeholder="Write the prompt here" id="systemRoleTextArea" style="height: 450px" spellcheck="false" disabled></textarea>
									<label for="systemRoleTextArea">System Role</label>
								</div>
							</div>
							<div class="d-grid gap-2 d-md-flex justify-content-md-end">
								<button class="btn btn-secondary" type="button" onclick="cancelSystemRole()" id="btn-cancel-editing-system-role" disabled>Cancel</button>
								<button class="btn btn-primary" type="button" onclick="toggleUpdateSaveSystemRole()" id="btn-edit-system-role">Edit</button>
							</div>
						</form>
						<h1  class="h3">CSV conversion prompt</h1>
						<div>This is a prompt to tell claude what are the rules to follow to convert a PDF to readable CSV </div>
						<form>
							<div class="mb-3">
								<div class="form-floating">
									<textarea class="form-control" placeholder="Write the prompt here" id="csvPromptTextArea" style="height: 450px" spellcheck="false" disabled></textarea>
									<label for="csvPromptTextArea">CSV Prompt</label>
								</div>
							</div>
							<div class="d-grid gap-2 d-md-flex justify-content-md-end">
								<button class="btn btn-secondary" type="button" onclick="cancelCsvPromtp()" id="btn-cancel-editing-csv-prompt" disabled>Cancel</button>
								<button class="btn btn-primary" type="button" onclick="toggleUpdateSaveCSVPrompt()" id="btn-edit-csv-prompt">Edit</button>
							</div>
						</form>
					</div>
				</div>
				<div class="tab-pane fade" id="pills-approved" role="tabpanel" aria-labelledby="pills-approved-tab">
					<div class="container">
						<h1 class="h3">Subscriptions</h1>
						<div class="container mt-5 mb-3">
							<div class="mb-3">
								In this section you can <strong> only </strong> create and/or delete <strong>lifetime subscriptions</strong>.  If a user already has an active subscription, you will not be able to modify it
							</div>
							<div class="input-group mb-3">
								<input type="text" class="form-control" placeholder="User's Wallet" aria-label="User's Wallet" aria-describedby="btn-add-lifetime-subscription" id="input-users-wallet"  oninput="validateUsersWallet()" spellcheck="false" >
								<button class="btn btn-primary" type="button" id="btn-add-lifetime-subscription" disabled onclick="createLifetimeSubscriptionHandler()">Add Lifetime Subscription</button>
							</div>
								<div class="text-danger" id="error-subscription-message"></div>
						</div>
						<table class="table text-center">
							<thead >
								<tr>
									<th>ID</th>
									<th>Wallet</th>
									<th>Status</th>
									<th>name</th>
									<th>Create Date</th>
									<th>Options</th>
								</tr>
							</thead>
							<tbody id="subscriptions-table-body">
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>


		<div class="container no-authorized-user" style="display: None;">
			<div class="alert alert-danger" role="alert">
			Error 401: Unauthorized user
			</div>
		</div>
		<!-- Modal -->
		<div class="modal fade" id="modalContainerDeleteSubscription" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">

		</div>



    
  ## <script src="/js/metamask_validator.js"></script>
	<script src="/js/claude_manager/service.js"></script>
	<script src="/js/claude_manager/components.js"></script>
	<script src="/js/claude_manager/custom.js"></script>
	</body>

</html>
