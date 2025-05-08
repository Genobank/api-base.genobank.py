<%page args="section, env"/>
<%
	perm_sec = "nav-link "
	prof_sec = "nav-link "
	if section == "Permittees":
		perm_sec = perm_sec + "active"
	elif section == "Profiles":
		prof_sec = prof_sec + "active"
%>
<head>
	## <meta charset="utf-8">
	## <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	## <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,700" rel="stylesheet">
	## <link rel="stylesheet" href="./static/pages/js/bootstrap/fonts/icomoon/style.css">
	## <link rel="stylesheet" href="./static/pages/js/bootstrap/css/owl.carousel.min.css">
	## <!-- Bootstrap CSS -->
	## <link rel="stylesheet" href="./static/pages/js/bootstrap/css/bootstrap.min.css">
	## <!-- Style -->
	## <link rel="stylesheet" href="./static/pages/js/bootstrap/css/style.css">
	## <script src="./static/pages/js/bootstrap/js/jquery-3.3.1.min.js"></script>
	## <script src="./static/pages/js/bootstrap/js/popper.min.js"></script>
	## <script src="./static/pages/js/bootstrap/js/bootstrap.min.js"></script>
	## <script src="./static/pages/js/bootstrap/js/jquery.sticky.js"></script>
	## <script src="./static/pages/js/bootstrap/js/main.js"></script>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/web3/3.0.0-rc.5/web3.min.js" integrity="sha512-jRzb6jM5wynT5UHyMW2+SD+yLsYPEU5uftImpzOcVTdu1J7VsynVmiuFTsitsoL5PJVQi+OtWbrpWq/I+kkF4Q==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous"
          referrerpolicy="no-referrer" />
		<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://getbootstrap.com/docs/5.2/assets/css/docs.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js"></script>
		<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
		<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>
		<script src="https://code.jquery.com/jquery-3.6.0.js" integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=" crossorigin="anonymous"></script>
		<script>
				window.environment = "${env}";
		</script>
	
    <script src="/js/env.js"></script>
    <script src="/js/detail.js"></script>
		
		<link rel = "icon" href = "/images/favicon-32x32.png" type = "image/x-icon">
</head>
<body onload="init()">
	<nav class="navbar navbar-expand-lg" id="navbar" >
		<div class="container">
			<a class="navbar-brand" href="#">
				## <object data="./static/images/GenoBank.io_logo.svg" width="160" height="30"> </object><br>
				<object data="/images/GenoBank.io_logo.svg" width="160" height="30"> </object><br>
				<h6>Platform Administration</h6>
			</a>
			<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
				<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="navbarNavAltMarkup">
				<div class="navbar-nav">
					<a class="nav-link active" id= "permette-href">Permittees</a>
					<a class="nav-link disabled" id ="profiles-href">Profiles</a>
					## <a class="nav-link disabled" href="#">Permission tokens (Disabled)</a>
					## <a class="nav-link disabled">Files (Disabled)</a>
					## <a class="nav-link disabled">Fulfillment (Disabled)</a>
				</div>
			</div>
		</div>
	</nav>

	<br>
	<div class="container" style="width: 100%;">
  ## ${section}
  
	## <%
	## 	for i in range(10):
	## 		print("\n\n\n\n\n"+a+"\n\n\n\n")
	## %>

	<svg id="mermaid-1659465604003" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="223.9829559326172" style="max-width: 1017.0511474609375px;" viewBox="0.000003814697265625 0 1017.0511474609375 223.9829559326172"><style>#mermaid-1659465604003{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#mermaid-1659465604003 .error-icon{fill:#552222;}#mermaid-1659465604003 .error-text{fill:#552222;stroke:#552222;}#mermaid-1659465604003 .edge-thickness-normal{stroke-width:2px;}#mermaid-1659465604003 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1659465604003 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1659465604003 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1659465604003 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1659465604003 .marker{fill:#333333;}#mermaid-1659465604003 .marker.cross{stroke:#333333;}#mermaid-1659465604003 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-1659465604003 .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#mermaid-1659465604003 .label text{fill:#333;}#mermaid-1659465604003 .node rect,#mermaid-1659465604003 .node circle,#mermaid-1659465604003 .node ellipse,#mermaid-1659465604003 .node polygon,#mermaid-1659465604003 .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-1659465604003 .node .label{text-align:center;}#mermaid-1659465604003 .node.clickable{cursor:pointer;}#mermaid-1659465604003 .arrowheadPath{fill:#333333;}#mermaid-1659465604003 .edgePath .path{stroke:#333333;stroke-width:1.5px;}#mermaid-1659465604003 .flowchart-link{stroke:#333333;fill:none;}#mermaid-1659465604003 .edgeLabel{background-color:#e8e8e8;text-align:center;}#mermaid-1659465604003 .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#mermaid-1659465604003 .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#mermaid-1659465604003 .cluster text{fill:#333;}#mermaid-1659465604003 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80,100%,96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1659465604003:root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}#mermaid-1659465604003 flowchart{fill:apa;}</style><g><g class="output"><g class="clusters"><g class="cluster" id="flowchart-subGraph0-18" transform="translate(587.730094909668,111.9914779663086)" style="opacity: 1;"><rect width="842.6420135498047" height="207.9829559326172" x="-421.32100677490234" y="-103.9914779663086"></rect><g class="label" transform="translate(0, -89.9914779663086)" id="mermaid-1659465604003Text"><g transform="translate(-78.23863220214844,-11.99573802947998)"><foreignObject width="156.47726440429688" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">GenoBank.io Platform</div></foreignObject></g></g></g></g><g class="edgePaths"><g class="edgePath LS-A LE-B" id="L-A-B" style="opacity: 1;"><path class="path" d="M116.40908813476562,111.9914779663086L141.40908813476562,111.9914779663086L166.40908813476562,111.9914779663086L191.40908813476562,111.9914779663086" marker-end="url(#arrowhead39)" style="fill:none"></path><defs><marker id="arrowhead39" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 0 0 L 0 0 z" style="fill: #333"></path></marker></defs></g><g class="edgePath LS-B LE-C2" id="L-B-C2" style="opacity: 1;"><path class="path" d="M357.0766274781618,89.9957389831543L426.1676025390625,64.9957389831543L507.60935974121094,64.9957389831543" marker-end="url(#arrowhead40)" style="fill:none"></path><defs><marker id="arrowhead40" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 0 0 L 0 0 z" style="fill: #333"></path></marker></defs></g><g class="edgePath LS-B LE-C" id="L-B-C" style="opacity: 1;"><path class="path" d="M357.0766274781618,133.9872169494629L426.1676025390625,158.9872169494629L451.1676025390625,158.9872169494629" marker-end="url(#arrowhead41)" style="fill:none"></path><defs><marker id="arrowhead41" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 0 0 L 0 0 z" style="fill: #333"></path></marker></defs></g><g class="edgePath LS-C LE-D" id="L-C-D" style="opacity: 1;"><path class="path" d="M710.7130432128906,158.9872169494629L735.7130432128906,158.9872169494629L760.7130432128906,158.9872169494629" marker-end="url(#arrowhead42)" style="fill:none"></path><defs><marker id="arrowhead42" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 0 0 L 0 0 z" style="fill: #333"></path></marker></defs></g></g><g class="edgeLabels"><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><rect rx="0" ry="0" width="0" height="0"></rect><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-A-B" class="edgeLabel L-LS-A' L-LE-B"></span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><rect rx="0" ry="0" width="0" height="0"></rect><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-B-C2" class="edgeLabel L-LS-B' L-LE-C2"></span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><rect rx="0" ry="0" width="0" height="0"></rect><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-B-C" class="edgeLabel L-LS-B' L-LE-C"></span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><rect rx="0" ry="0" width="0" height="0"></rect><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-C-D" class="edgeLabel L-LS-C' L-LE-D"></span></div></foreignObject></g></g></g><g class="nodes"><g class="node default" id="flowchart-C2-12" transform="translate(580.9403228759766,64.9957389831543)" style="opacity: 1;"><rect rx="0" ry="0" x="-73.33096313476562" y="-21.99573802947998" width="146.66192626953125" height="43.99147605895996" class="label-container"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-63.330963134765625,-11.99573802947998)"><foreignObject width="126.66192626953125" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><i class="fa fa-database"></i> Local database</div></foreignObject></g></g></g><g class="node clickable" id="flowchart-B-10" transform="translate(296.28834533691406,111.9914779663086)" style="opacity: 1;"><a class="clickable" href="https://docs.genobank.io/api/" rel="noopener"><rect rx="0" ry="0" x="-104.87925720214844" y="-21.99573802947998" width="209.75851440429688" height="43.99147605895996" class="label-container"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-94.87925720214844,-11.99573802947998)"><foreignObject width="189.75851440429688" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><i class="fa fa-globe"></i> GenoBank.io API server</div></foreignObject></g></g></a></g><g class="node clickable" id="flowchart-C-14" transform="translate(580.9403228759766,158.9872169494629)" style="opacity: 1;"><a class="clickable" href="https://docs.genobank.io/blockchain/" rel="noopener"><rect rx="0" ry="0" x="-129.77272033691406" y="-21.99573802947998" width="259.5454406738281" height="43.99147605895996" class="label-container"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-119.77272033691406,-11.99573802947998)"><foreignObject width="239.54544067382812" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><i class="fa fa-globe"></i> GenoBank.io blockchain server</div></foreignObject></g></g></a></g><g class="node default" id="flowchart-D-16" transform="translate(872.3820724487305,158.9872169494629)" style="opacity: 1;"><rect rx="0" ry="0" x="-111.66902923583984" y="-21.99573802947998" width="223.3380584716797" height="43.99147605895996" class="label-container"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-101.66902923583984,-11.99573802947998)"><foreignObject width="203.3380584716797" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><i class="fa fa-link"></i> Public blockchain network</div></foreignObject></g></g></g><g class="node default" id="flowchart-A-9" transform="translate(62.20454406738281,111.9914779663086)" style="opacity: 1;"><rect rx="0" ry="0" x="-54.20454406738281" y="-21.99573802947998" width="108.40908813476562" height="43.99147605895996" class="label-container" style="fill:lightblue;"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-44.20454406738281,-11.99573802947998)"><foreignObject width="88.40908813476562" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><i class="fa fa-globe"></i> This page</div></foreignObject></g></g></g></g></g></g></svg>
	<hr>
</div>
</body>