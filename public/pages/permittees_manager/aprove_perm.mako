<%include file="../components/basic_scripts.mako" args="section='Permittees', env=env" />
<!DOCTYPE html>
<html>
   <head>
      <title>Dashboard - Laboratorios Pendientes</title>
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
               <li><a class="dropdown-item" href="#"><i class="fa-solid fa-house"></i> General Manager</a></li>
               <li><a class="dropdown-item" href="/shop_manager"><i class="fa-solid fa-shop"></i> Shop Manager</a></li>
               <li><a class="dropdown-item" href="/claude_manager"><i class="fa-solid fa-comment"></i> Claude Manager</a></li>
            </ul>
         </li>
         <li class="nav-item" role="presentation">
            <button class="nav-link active" id="pills-pending-tab" data-bs-toggle="pill" data-bs-target="#pills-pending" type="button" role="tab" aria-controls="pills-pending" aria-selected="true" >Pending Permittees</button>
         </li>
         <li class="nav-item" role="presentation">
            <button class="nav-link" id="pills-approved-tab" data-bs-toggle="pill" data-bs-target="#pills-approved" type="button" role="tab" aria-controls="pills-approved" aria-selected="false" >Approved Permittes</button>
         </li>
         <li class="nav-item" role="presentation">
            <button class="nav-link" id="pills-rejected-tab" data-bs-toggle="pill" data-bs-target="#pills-rejected" type="button" role="tab" aria-controls="pills-rejected" aria-selected="false" >Rejected Permittes</button>
         </li>
         <li class="nav-item" role="presentation">
            <button class="nav-link" id="pills-deliveries-tab" data-bs-toggle="pill" data-bs-target="#pills-deliveries" type="button" role="tab" aria-controls="pills-deliveries" aria-selected="false" >All Deliveries</button>
         </li>
         <li class="nav-item" role="presentation">
            <button class="nav-link" id="pills-variants-tab" data-bs-toggle="pill" data-bs-target="#pills-variants" type="button" role="tab" aria-controls="pills-variants" aria-selected="false" >Pending Variants</button>
         </li>
         <!-- New Tab -->
         <li class="nav-item" role="presentation">
            <button class="nav-link" id="pills-permittee-buckets-tab" data-bs-toggle="pill" data-bs-target="#pills-permittee-buckets" type="button" role="tab" aria-controls="pills-permittee-buckets" aria-selected="false">Permittee Buckets</button>
         </li>
      </ul>
      <div class="tab-content" id="pills-tabContent">
      <div class="tab-pane fade show active" id="pills-pending" role="tabpanel" aria-labelledby="pills-pending-tab">
         <div class="container">
            <h1>Pending Laboratories</h1>
            <table class="table text-center">
               <thead >
                  <tr>
                     <th>Logo</th>
                     <th>Address</th>
                     <th>Name</th>
                     <th style="width: 200px;">Options</th>
                  </tr>
               </thead>
               <tbody id="pending-lab-body">
               </tbody>
            </table>
            <div class="d-flex justify-content-center" >
               <div class="custom-spinner" id="loading_spinner">
                  <div class="erlenmeyer">
                     <div class="liquid">
                        <div class="bubble"></div>
                     </div>
                  </div>
                  &nbsp;&nbsp;Loading ...
               </div>
            </div>
         </div>
      </div>
      <div class="tab-pane fade" id="pills-approved" role="tabpanel" aria-labelledby="pills-approved-tab">
         <div class="container">
            <h1>Approved Laboratories</h1>
            <table class="table text-center">
               <thead >
                  <tr>
                     <th>Logo</th>
                     <th>Address</th>
                     <th>Name</th>
                     <th style="width: 150px;">serial</th>
                  </tr>
               </thead>
               <tbody id="approved-lab-body">
               </tbody>
            </table>
         </div>
      </div>
      <div class="tab-pane fade" id="pills-rejected" role="tabpanel" aria-labelledby="pills-rejected-tab">
         <div class="container">
            <h1>Rejected Laboratories</h1>
            <table class="table text-center">
               <thead >
                  <tr>
                     <th>Logo</th>
                     <th>Address</th>
                     <th>Name</th>
                     <th style="width: 200px;">Options</th>
                  </tr>
               </thead>
               <tbody id="rejected-lab-body">
               </tbody>
            </table>
         </div>
      </div>
      <div class="tab-pane fade" id="pills-deliveries" role="tabpanel" aria-labelledby="pills-deliveries-tab">
         <div class="container">
            <h1>All Deliveries</h1>
            <table class="table text-center">
               <thead >
                  <tr>
                     <th>Biosample Serial</th>
                     <th>Owner</th>
                     <th>Permittee Id</th>
                     <th>Permittee Wallet</th>
                     <th>Shared Files</th>
                     <th>Transaction</th>
                  </tr>
               </thead>
               <tbody id="deliveries-lab-body">
               </tbody>
            </table>
         </div>
      </div>
      <div class="tab-pane fade" id="pills-variants" role="tabpanel" aria-labelledby="pills-variants-tab">
         <div class="container">
            <h1>Biosamples With Pending Variants</h1>
            <table class="table text-center" id="biosamples-with-pending-variants-table">
               <thead >
                  <tr>
                     <th>Biosample Serial</th>
                     <th>Owner</th>
                     <th>Status</th>
                     <th>Created</th>
                  </tr>
               </thead>
               <tbody id="biosample-with-pending-variants-body">
               </tbody>
            </table>
            <div id="variants-pending-participants-section" style="display: none;">
               <button class="btn btn-secondary" onclick="backToPendigBiosamplesWithVariants()">
               <i class="fa-solid fa-arrow-left"></i>
               Back
               </button>
               <table class="table text-center">
                  <thead >
                     <tr>
                        <th>Logo</th>
                        <th>Wallet Name</th>
                        <th>Wallet Investigator</th>
                        <th>Wallet Email</th>
                     </tr>
                  </thead>
                  <tbody id="variants-pending-participants-body">
                  </tbody>
               </table>
               <div class="d-flex justify-content-center" >
                  <div class="spinner-border" role="status" id="spinner-variant-container">
                     <span class="visually-hidden">Loading...</span>
                  </div>
               </div>
               <div>
               </div>
            </div>
         </div>
      </div>
      <div class="tab-pane fade" id="pills-permittee-buckets" role="tabpanel" aria-labelledby="pills-permittee-buckets-tab">
         <div class="container">
            <div class="d-flex justify-content-between align-items-center">
               <h1>Permittee Buckets</h1>
               <button class="btn btn-light" data-bs-toggle="modal" data-bs-target="#newBucketModal"><i class="fa-solid fa-plus"></i> New Bucket </button>
            </div>
            <table class="table text-center">
               <thead>
                  <tr>
                     <th>Permittee</th>
                     <th>Permittee Serial</th>
                     <th>Permittee Address</th>
                     <th>Bucket Name</th>
                     <th>Access Key ID</th>
                     <th>Secret Key ID</th>
                     <th>Options</th>
                  </tr>
               </thead>
               <tbody id="permittee-buckets-body">
               </tbody>
            </table>
         </div>
      </div>
      <div class="container no-authorized-user" style="display:none;">
         <div class="alert alert-danger" role="alert">
            Error 401: Unauthorized user
         </div>
      </div>
      <!-- Approve Modal -->
      <div class="modal fade" id="approvalModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
         <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
               <div class="modal-header">
                  <h5 class="modal-title" id="approvalModalTitle">Approve Permittee</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
               </div>
               <div class="modal-body">
                  Are you sure you want to approve this Permittee Laboratory?
                  <strong>
                     <p class="permittee-address"></p>
                  </strong>
                  <div class="approve-message-container">
                  </div>
               </div>
               <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                  <button type="button" class="btn btn-primary"  onclick="approvePermittee()">Approve</button>
               </div>
            </div>
         </div>
      </div>
      <!-- Reject Modal -->
      <div class="modal fade" id="rejectModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
         <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
               <div class="modal-header">
                  <h5 class="modal-title" id="rejectModalTitle">Reject Permittee</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
               </div>
               <div class="modal-body">
                  Are you sure you want to reject:
                  <strong>
                     <p class="permittee-address"></p>
                  </strong>
                  <div class="reject-message-container">
                  </div>
               </div>
               <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                  <button type="button" class="btn btn-danger"  onclick="rejectPermittee()">Reject</button>
               </div>
            </div>
         </div>
      </div>
      <!-- Check Variants Modal -->
      <div class="modal fade" id="variantModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
         <div class="modal-dialog modal-xl modal-dialog-centered">
            <div class="modal-content" id="variantModalContainer">
            </div>
         </div>
      </div>

      ## create a modal container similar to the variantModal container this modal will be used to show the edit bucket form
      <div class="modal fade" id="editBucketModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
         <div class="modal-dialog modal-xl modal-dialog-centered">
            <div class="modal-content" id="editBucketModalContainer">
            </div>
         </div>
      </div>

      <!-- New Bucket Modal -->
      <div class="modal fade" id="newBucketModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
         <div class="modal-dialog modal-xl modal-dialog-centered" role="document">
            <div class="modal-content">
               <div class="modal-header">
                  <h5 class="modal-title" id="newBucketModalTitle">New Bucket</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
               </div>
               <div class="modal-body">
                  <div class="form-group">
                     <label for="bucketName">Bucket Name</label>
                     <input type="text" class="form-control" id="bucketName" placeholder="Enter Bucket Name">
                  </div>
                  <div class="form-group
                     ">
                     <label for="accessKeyId">Access Key ID</label>
                     <input type="text" class="form-control" id="accessKeyId" placeholder="Enter Access Key ID">
                  </div>
                  <div class="form-group
                     ">
                     <label for="secretKeyId">Secret Key ID</label>
                     <input type="text" class="form-control" id="secretKeyId" placeholder="Enter Secret Key ID">
                  </div>
                  <!-- Permittee serial must be an integer number higher than 0 -->
                  <div class="form-group">
                     <label for="permitteeSerial">Permittee Serial </label>
                     <input type="number" class="form-control" id="permitteeSerial" placeholder="Enter Permittee Serial" min="1" required>
                  </div>
                  ## add an input for permittee address
                  <div class="form-group">
                     <label for="permitteeAddress">Permittee Address</label>
                     <input type="text" class="form-control" id="permitteeAddress" placeholder="Enter Permittee Address" required>
                  </div>

               </div>
               <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                  <button type="button" class="btn btn-primary"  onclick="createBucket()">Create</button>
               </div>
            </div>
         </div>
      </div>
      



      ## <script src="/js/metamask_validator.js"></script>
      <script src="/js/approve_permittee/custom.js"></script>
      <script src="/js/approve_permittee/utils.js"></script>
   </body>
</html>