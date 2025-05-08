<%include file="../components/basic_scripts.mako"  args="section='Permittees', env=env"  />
<html>
  <head>
    <title>${title}</title>
		<link href="/static/pages/minter_manager/massive_minter.css" rel="stylesheet">
  </head>
  <body class="container">
      <div class="container no-authorized-user" style="display:none;">
        <div class="alert alert-danger" role="alert">
          Error 401: Unauthorized user
        </div>
      </div>
      <div class="card minter-card-container" style="margin-top:50px; display:none;">
        <div class="card-body">
          <span>
            <object data="/images/GenoBank.io_logo.svg" width="160" height="30"> </object>
            <h1 class="display-6">Massive Minter</h1>
          </span>
          <strong><label class="col-sm-2 col-form-label">(* Required)</label></strong>

          ## form
          <div class="connect-to-bucket">
            <div class="mb-3">
              <label for="bucketSelect" class="form-label">* Permitte Serial Bucket Source</label>
              <select class="form-select bucket-select" id="bucketSelect" aria-label=""></select>
            </div>
            <div class="mb-3 row">
              <label for="inputAccessKey" class="col-sm-2 col-form-label">* Bucket Access Key</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputAccessKey" value="">
              </div>
            </div>
            <div class="mb-3 row">
              <label for="inputSecretKey" class="col-sm-2 col-form-label">* Bucket Secret Key</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputSecretKey" value="" >
              </div>
            </div>
            <div class="mb-3 row">
              <label for="inputBucketName" class="col-sm-2 col-form-label">* Bucket Name</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputBucketName" value="">
              </div>
            </div>
            <div class="mb-3 row">
              <button type="button" class="btn btn-light" onclick="connectBucket()">Connect Bucket</button>
            </div>
          </div>
          <div class="bucket-container" style="display:none">
            <div class="card">
              <div class="card-header">
                <label class=" col-form-label">Select the folder path of the files to be minted</label>
              </div>
              <div class="card-body">
                  <div class="row">
                    <div class="col-2">
                      <button onclick="goBack()" class="btn btn-light">
                          <i class="fa-solid fa-circle-arrow-left"> Go Back</i>
                      </button>
                    </div>
                  </div>
                  
                  <table class="table table-hover" id="file-datatable">
                    <tbody id="tbody-file-container">
                    </tbody>
                  </table>
              </div>
            </div>


            <div class="mb-3 row">
              <label for="inputBucketPath" class="col-sm-2 col-form-label">* File Path Selector</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputBucketPath" disabled>
                <span>
                  <span id="id-count-folders"></span>
                  <span id="id-count-files"></span>
                  <span id="id-count-total"></span>
                </span>
              </div>
            </div>

            <div class="mb-3 row">
              <label for="inputFileRange" class="col-sm-2 col-form-label">File Range</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputFileRange" placeholder="[11:20] or [:10] or [10] or [4:]">
              </div>
            </div>

            <div class="mb-3 row">
              <label for="secretApi" class="col-sm-2 col-form-label">* Secret</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="secretApi">
              </div>
            </div>

            <div class="mb-3 row">
              <button type="button" class="btn btn-primary" onclick="startingMint()">Start Mint</button>
            </div>



          </div>
        </div>
      </div>
      <section>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js" integrity="sha512-dfX5uYVXzyU8+KHqj8bjo7UkOdg18PaOtpa48djpNbZHwExddghZ+ZmzWT06R5v6NSk3ZUfsH6FNEDepLx9hPQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.2.0/crypto-js.min.js"></script>
        <script src="/js/validators/validators.js"></script>
        <script src="/js/metamaskLogin.js"></script>
        <script src="/js/massive_minter/forms.js"></script>
        <script src="/js/massive_minter/custom.js"></script>

      </section>
  </body>
</html>