<%include file="components/detail.mako" args="section='Permittees', other='abcde', env=env" />
<html>
  <head>
    <meta charset="utf-8">
    <title>${plc}</title>
    <script src="/js/qrcode.min.js"></script>
    <script src="/js/admin-libs.js"></script>
    <script src="/js/admin-forms.js"></script>
    <script src="/js/admin-validators.js"></script>
  </head>
  <body>
    <div class="container">

      <div class="header">
      </div>
      ## form
      <div class="row">
        <div class="col-7" style="min-width: 370px;">
          <div class="card">
            <div class="card-header">
              <h3>Permittees</h3>
            </div>
            <div class="card-body">
              <h3>Register a permittee</h3>
              <p>A donor allows permission on their biosample when they activate it. Recipients of all permissions must first register with GenoBank.io.</p>
              <h4>Instructions</h4>
              <ol>
                <li>A laboratory that wants to solve consent management and donor privacy signs up with GenoBank.io</li>
                <li>The laboratory creates a public/private key pair</li>
                <li>Choose an available Permittee ID number in the Fulfillment/Biosamples fil</li>
                <li>Submit the form</li>
                <li>Record to the file</li>
                <li>-> The laboratory registers their public key below</li>
              </ol>
            </div>
          </div>
        </div>
        <div class="col-5" style="min-width: 370px;">
          <div class="card">
            <div class="card-header">
              <h3>Create Permittee</h3>
            </div>
            <div class="card-body">
              <form>
                <div class="form-group">
                  <label>Permittee ID</label>
                  <input type="number" min="0" max="281474976710655" class="form-control" id="registerPermitteePermitteeId" onchange="check_id()">
                </div>
                <div class="form-group">
                  <label>Permittee address</label>
                  <input type="text" class="form-control" id="registerPermitteePermitteeAddress" onchange="checkAddress()">
                </div>
                <div class="form-group">
                  <label>Application Secret</label>
                  <input type="password" class="form-control" id="registerPermitteeApplicationSecret">
                  <small class="form-text text-muted">This same secret is installed on the API server. If you enter the wrong secret here then the operation will fail.</small>
                </div>
                <div class="form-group row">
                  <div class="col-md-3">
                    <button type="button" class="btn btn-danger" onclick="registerPermittee()">Register Permittee</button>
                  </div>
                  <div class="col-sm-9 text-danger">
                    <i class = "fa fa-warning">
                    </i>
                      This operation will be sent to the API server and recorded permanently & publicly on the blockchain. Check twice, cut once.
                  </div>
                  <div id="registerPermitteeResult" class="rounded p-3 text-wrap text-break" style="display: block;"></div>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div class="separator" style="margin-top:25px;"></div>

        <div class="col-6" style="min-width: 370px;">
          <div class="card">
            <div class="card-header">
              <h3>Biosamples</h3>
            </div>
            <div class="card-body">
              <h4>Create a biosample activation URL</h4>
              <small class="__web-inspector-hide-shortcut__">done by <i class="fa fa-user-circle"></i>administrator</small>
              <div class="mermaid" data-processed="true"><svg id="mermaid-1670858503255" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="126.921875" style="max-width: 489.234375px;" viewBox="0 0 489.234375 126.921875"><style>#mermaid-1670858503255{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#mermaid-1670858503255 .error-icon{fill:#552222;}#mermaid-1670858503255 .error-text{fill:#552222;stroke:#552222;}#mermaid-1670858503255 .edge-thickness-normal{stroke-width:2px;}#mermaid-1670858503255 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1670858503255 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1670858503255 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1670858503255 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1670858503255 .marker{fill:#333333;}#mermaid-1670858503255 .marker.cross{stroke:#333333;}#mermaid-1670858503255 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-1670858503255 .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#mermaid-1670858503255 .label text{fill:#333;}#mermaid-1670858503255 .node rect,#mermaid-1670858503255 .node circle,#mermaid-1670858503255 .node ellipse,#mermaid-1670858503255 .node polygon,#mermaid-1670858503255 .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-1670858503255 .node .label{text-align:center;}#mermaid-1670858503255 .node.clickable{cursor:pointer;}#mermaid-1670858503255 .arrowheadPath{fill:#333333;}#mermaid-1670858503255 .edgePath .path{stroke:#333333;stroke-width:1.5px;}#mermaid-1670858503255 .flowchart-link{stroke:#333333;fill:none;}#mermaid-1670858503255 .edgeLabel{background-color:#e8e8e8;text-align:center;}#mermaid-1670858503255 .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#mermaid-1670858503255 .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#mermaid-1670858503255 .cluster text{fill:#333;}#mermaid-1670858503255 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80,100%,96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1670858503255:root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}#mermaid-1670858503255 flowchart-v2{fill:apa;}</style><g transform="translate(0, 0)"><marker id="flowchart-pointEnd" class="marker flowchart" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="flowchart-pointStart" class="marker flowchart" viewBox="0 0 10 10" refX="0" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="flowchart-circleEnd" class="marker flowchart" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="flowchart-circleStart" class="marker flowchart" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="flowchart-crossEnd" class="marker cross flowchart" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="flowchart-crossStart" class="marker cross flowchart" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><g class="root"><g class="clusters"><g class="cluster default" id="R"><rect style="" rx="0" ry="0" x="155.703125" y="8.9609375" width="128.140625" height="109"></rect><g class="cluster-label" transform="translate(184.1953125, 13.9609375)"><foreignObject width="71.15625" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span class="nodeLabel">Retail box</span></div></foreignObject></g></g></g><g class="edgePaths"><path d="M105.703125,63.4609375L109.86979166666667,63.4609375C114.03645833333333,63.4609375,122.36979166666667,63.4609375,130.703125,63.4609375C139.03645833333334,63.4609375,147.36979166666666,63.4609375,155.703125,63.4609375C164.03645833333334,63.4609375,172.36979166666666,63.4609375,176.53645833333334,63.4609375L180.703125,63.4609375" id="L-A-B" class=" edge-thickness-normal edge-pattern-solid flowchart-link LS-A LE-B" style="fill:none;" marker-end="url(#flowchart-pointEnd)"></path><path d="M283.84375,63.4609375L283.84375,63.4609375C283.84375,63.4609375,283.84375,63.4609375,291.0494791666667,63.4609375C298.2552083333333,63.4609375,312.6666666666667,63.4609375,327.1614583333333,63.544270833333336C341.65625,63.627604166666664,356.234375,63.794270833333336,363.5234375,63.877604166666664L370.8125,63.9609375" id="L-R-C" class=" edge-thickness-normal edge-pattern-solid flowchart-link LS-R LE-C" style="fill:none;" marker-end="url(#flowchart-pointEnd)"></path></g><g class="edgeLabels"><g class="edgeLabel"><g class="label" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel" transform="translate(327.078125, 63.4609375)"><g class="label" transform="translate(-18.234375, -12)"><foreignObject width="36.46875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span class="edgeLabel">Scan</span></div></foreignObject></g></g></g><g class="nodes"><g class="node default" id="flowchart-B-40" transform="translate(219.7734375, 63.4609375)"><rect class="basic label-container" style="" rx="0" ry="0" x="-39.0703125" y="-19.5" width="78.140625" height="39"></rect><g class="label" style="" transform="translate(-31.5703125, -12)"><foreignObject width="63.140625" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span class="nodeLabel">QR code</span></div></foreignObject></g></g><g class="node default" id="flowchart-A-39" transform="translate(56.8515625, 63.4609375)"><rect class="basic label-container" style="fill:lightblue;" rx="0" ry="0" x="-48.8515625" y="-19.5" width="97.703125" height="39"></rect><g class="label" style="" transform="translate(-41.3515625, -12)"><foreignObject width="82.703125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span class="nodeLabel">Secret URL</span></div></foreignObject></g></g><g class="node default" id="flowchart-C-43" transform="translate(425.7734375, 63.4609375)"><polygon points="55.4609375,0 110.921875,-55.4609375 55.4609375,-110.921875 0,-55.4609375" class="label-container" transform="translate(-55.4609375,55.4609375)"></polygon><g class="label" style="" transform="translate(-28.4609375, -12)"><foreignObject width="56.921875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span class="nodeLabel">Activate</span></div></foreignObject></g></g></g></g></g></svg></div>
              <p>This is a secret URL that the donor will use to activate their biosample.</p>
              <h4>Instructions</h4>
              <ol>
                <li>Check your Fulfillment/Biosamples file to decide which biosample ID you want</li>
                <li>Fill in and submit form</li>
                <li>Record to the file</li>
                <li class="text-danger">NOT DOCUMENTED YET / CALL WILL: Generate activation QR code with this URL and stick in the box.</li>
                <li class="text-danger">NOT DOCUMENTED YET / CALL WILL: Generate laboratory QR code with this URL and stick in the box.</li>
              </ol>
            </div>
          </div>
        </div>
        <div class="col-6" style="min-width: 370px;">
          <div class="card">
            <div class="card-header">
              <h3>Create Biosample</h3>
            </div>
            <div class="card-body">
            <form>
                <div class="form-group">
                  <label for="createBiosampleUrlBase"><i class="fa fa-globe"></i> Activation URL base</label>
                  <select id="createBiosampleUrlBase" class="form-control">
                  </select>
                  <small class="form-text text-muted">This is part of the URL the donor will access to activate the biosample. This URL must be on the same network as you are using on this page. Also it should match the branding/product detail for the biosample ID you are creating.</small>
                </div>
                <div class="form-group">
                  <label for="createBiosampleBiosampleId"><i class="fa fa-qrcode"></i> Biosample ID</label>
                  <input type="number" min="0" max="281474976710655" class="form-control" id="createBiosampleBiosampleId">
                  <small class="form-text text-muted">Any integer is acceptable between 0 and 2<sup>48</sup>–1. Be sure that you record this somewhere so that you do not create the same activation URL twice and give it out to two different people.</small>
                  <div id="createBiosampleBiosampleIdValidation"></div>
                </div>
                <div class="form-group">
                  <label for="createBiosamplePhysicalId"><i class="fa fa-barcode"></i> Physical ID</label>
                  <input type="text" class="form-control" id="createBiosamplePhysicalId">
                  <small class="form-text text-muted">Any text can be pasted here. This represents the number/text which is barcoded and printed physically on the biosample collection container.</small>
                </div>
                <div class="form-group">
                  <label for="createBiosamplePermitteeId"><i class="fa fa-arrow-right"></i> Permittee ID</label>
                  <select id="createBiosamplePermitteeId" class="form-control">
                  
                  </select>
                  <small class="form-text text-muted">When the donor activates this biosample they will permit this entity to use their data.</small>
                </div>
                <div class="form-group">
                  <label for="createBiosampleApplicationSecret"><i class="fa fa-lock"></i> Application secret</label>
                  <input type="password" class="form-control" id="createBiosampleApplicationSecret">
                  <small class="form-text text-warning"><i class="fa fa-warning"></i> This same secret is installed on the API server. If you enter the wrong secret here then no error will be produced and the URLs you generate will not work.</small>
                </div>
                
                <div class="form-group row">
                  <div class="col-md-3">
                    <button onclick="createBiosample()" type="button" class="btn btn-info">Generate URL</button>
                    ## <button onclick="createQRURL()" type="button" class="btn btn-info">Generate URL</button>
                  </div>
                  <div class="col-sm-9">
                    This operation will be sent to the API server. You can only generate URL for a biosample ONCE so make sure to copy it!
                  </div>
                </div>
              
                <div id="createBiosampleResult" class="rounded p-3 text-wrap text-break"></div>
                <div id="qrCode" class="col-md-12 d-flex justify-content-center align-items-center"></div>
                ## <div id="imageDownloader"></div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>