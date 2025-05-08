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
    <link rel="stylesheet" href="/js/shop_manager/css/shop_manager.css"/>
    <link rel="stylesheet" href="https://cdn.datatables.net/2.1.8/css/dataTables.dataTables.css" />
    <script src="https://cdn.datatables.net/2.1.8/js/dataTables.js"></script>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>

    
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
            <li><a class="dropdown-item" href="#"><i class="fa-solid fa-shop"></i> Shop Manager</a></li>
            <li><a class="dropdown-item" href="/claude_manager"><i class="fa-solid fa-comment"></i> Claude Manager</a></li>
          </ul>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link active" id="pills-pending-tab" data-bs-toggle="pill" data-bs-target="#pills-pending" type="button" role="tab" aria-controls="pills-pending" aria-selected="true" >
            <i class="fa-solid fa-store"></i>
            Products
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="pills-sales-tab" data-bs-toggle="pill" data-bs-target="#pills-sales" type="button" role="tab" aria-controls="pills-sales" aria-selected="false" >
            <i class="fa-solid fa-cart-shopping"></i>
            Sales
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="pills-raw-data-delivery-tab" data-bs-toggle="pill" data-bs-target="#pills-raw-data-delivery" type="button" role="tab" aria-controls="pills-raw-data-delivery" aria-selected="false" >
            <i class="fa-solid fa-truck-ramp-box"></i>
            Raw Data File Delivery
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="pills-token-holders-tab" data-bs-toggle="pill" data-bs-target="#pills-token-holders" type="button" role="tab" aria-controls="pills-token-holders" aria-selected="false" >
            <i class="fa-solid fa-user"></i>
            Token Holders
          </button>
        </li>
      </ul>
      <div class="tab-content" id="pills-tabContent">
        <div class="tab-pane fade show active" id="pills-pending" role="tabpanel" aria-labelledby="pills-pending-tab">
          <div class="container">
            <h1>Products</h1>
            <table class="table">
              <thead >
                <tr>
                  <th>id</th>
                  <th>Thumbnail</th>
                  <th>Name</th>
                  <th>Description</th>
                  <th>Price</th>
                  <th>Currency</th>
                  <th style="width: 200px;">Options</th>
                </tr>
              </thead>
              <tbody id="product-list-body">
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

        <div class="tab-pane fade" id="pills-sales" role="tabpanel" aria-labelledby="pills-sales-tab">
          <div class="container">
            <h1>Sales</h1>
            <table class="table text-center">
              <thead >
                <tr>
                  <th>id</th>
                  <th>Customer</th>
                  <th>Email</th>
                  <th>Products</th>
                  <th>Status</th>
                  <th>Amount</th>
                  <th>Options</th>
                </tr>
              </thead>
              <tbody id="sales-list-body">
              </tbody>
            </table>
          </div>
        </div>



        <div class="tab-pane fade" id="pills-raw-data-delivery" role="tabpanel" aria-labelledby="pills-raw-data-delivery-tab">
          <div class="container">
            <h1>Raw Data Delivery</h1>
            <h1 class="h4">(Ancestry Service Included) </h1>
            <table class="table text-center" id="raw-data-delivery-table">
              <thead >
                <tr>
                  <th>Serial</th>
                  <th>Owner</th>
                  <th>Status</th>
                  <th>Created</th>
                  <th>Options</th>
                </tr>
              </thead>
              <tbody id="raw-data-delivery-list-body">
              </tbody>
            </table>
          </div>
        </div>
        <div class="tab-pane fade" id="pills-token-holders" role="tabpanel" aria-labelledby="pills-token-holders-tab">
          <div class="container">
            <h1>Token Holders</h1>
            <h1 class="h4">Somos Registered Users</h1>
            <table class="table text-center" id="token-holders-table">
              <thead >
                <tr>
                  <th>Wallet</th>
                  <th>Token ID</th>
                  <th>Transaction</th>
                  <th>Sex</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody id="token-holders-list-body">
              </tbody>
            </table>
          </div>
        </div>






  <div class="container no-authorized-user" style="display:none;">
    <div class="alert alert-danger" role="alert">
      Error 401: Unauthorized user
    </div>
  </div>


    <!-- Update Product Modal -->
  <div class="modal fade" id="addProductModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">

  </div>


  <div class="modal fade" id="editProductModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">

  </div>

  <div class="modal fade" id="deleteProductModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">

  </div>


  <div class="modal fade" id="saleDetailsModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">

  </div>


  <div class="modal fade" id="rawDataDeliveryModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">

  </div>

    
  ## <script src="/js/metamask_validator.js"></script>
  <script src="/js/qrcode.min.js"></script>
  <script src="/js/bwip-js-min.js"></script>
  <script src="/js/blob-stream.min.js"></script>
  <script src="/js/pdfkit.standalone.js"></script>
  <script src="/js/shop_manager/shopService.js"></script>
  <script src="/js/shop_manager/scripts/forms.js"></script>
  <script src="/js/shop_manager/scripts/libs.js"></script>
  <script src="/js/shop_manager/scripts/validators.js"></script>
  <script src="/js/shop_manager/utils.js"></script>
  <script src="/js/shop_manager/components.js"></script>
  <script src="/js/shop_manager/custom.js"></script>
	</body>

</html>
