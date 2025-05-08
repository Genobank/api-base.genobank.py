(function() {
const url = new URL(location.href);
// window.test = url.pathname.substr(10, 5) == '/test';
window.test = window.environment == 'test';
const local = (url.hostname == 'localhost' || url.hostname == '127.0.0.1')
window.HOST = url.host
window.ENV = test ? 'test' : 'main';
window.WWW_BASE = test ? 'https://genobank.io/test' : 'https://genobank.io';
window.WWW_BASE = local ? "http://127.0.0.1:5500/test" : window.WWW_BASE 
// window.WWW_LOCAL_BASE = "http://127.0.0.1:5500/test"
// window.API_BASE = test ? 'https://api-test.genobank.io' : 'https://api.genobank.io';
window.API_BASE = url.origin
window.NAMESPACE = test ? 'io.genobank.test' : 'io.genobank';

window.BIOSAMPLE_ACTIVATION_BASE = test ? [
  `${window.WWW_BASE}/activate`,
	'https://adn.docinway.com.mx/test/activate'
] : [
  `${window.WWW_BASE}/activate`,
  `https://start.somosancestria.com`,

];

window.favicon = test ? './../static/images/favicon-32x32.png':'./static/images/favicon-32x32.png';
window.NEWAPIBASE = url.origin
})();


/**
 * Draws a bar at the top of the webiste indicating when working in the testing
 * environment.
 */
(function() {
  if (window.ENV !== 'test') {
    return;
  } else {
    $([
      `<div style="display: block; background: red; padding: 5px 5px 8px 5px; text-align: center; color: white">`,
        `This website runs in test environment.`,
      `</div>`
    ].join('')).prependTo($('body'));
  }
})();