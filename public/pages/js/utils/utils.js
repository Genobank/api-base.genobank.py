function urlFactory(baseURL, params) {
	const url = new URL(baseURL);
	Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
	return url.toString();
}



function interpolateColor(color1, color2, factor) {
	const result = color1.slice(1).match(/.{2}/g)
	  .map((hex, index) => {
		const c1 = parseInt(hex, 16);
		const c2 = parseInt(color2.slice(1).match(/.{2}/g)[index], 16);
		return Math.round(c1 + (c2 - c1) * factor).toString(16).padStart(2, '0');
	  });
	return `#${result.join('')}`;
  }
  
  function getProgressColor(percent) {
	if (percent <= 25) {
	  return '#b03c96';
	} else if (percent <= 50) {
	  return interpolateColor('#b03c96', '#344da1', (percent - 25) / 25);
	} else if (percent <= 75) {
	  return interpolateColor('#344da1', '#009abb', (percent - 50) / 25);
	} else {
	  return interpolateColor('#009abb', '#49ba80', (percent - 75) / 25);
	}
  }


  function isEmpty(value) {
    if (value == null) {
      return true;
    }
    const type = typeof value;
    if (type === 'string' || Array.isArray(value)) {
      return value.length === 0;
    }
    if (type === 'object') {
      return Object.keys(value).length === 0;
    }
    if (type === 'boolean' || type === 'number') {
      return !value;
    }
    return false;
  }