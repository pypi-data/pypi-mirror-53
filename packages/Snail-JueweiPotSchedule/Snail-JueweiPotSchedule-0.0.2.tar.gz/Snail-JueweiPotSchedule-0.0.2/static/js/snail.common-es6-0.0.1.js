/**
 * Author: Snail(snail_email@163.com)
 */
;var Snail = (function(_Snail, _win, _doc, undefined){
	
	return _Snail = _Snail || (_win['Snail'] = {
		
		isBlank: function(obj){
			
			if(null == obj || undefined == obj){
				return true;
			}
			
			if(/\S+/.test(obj)){
				return false;
			}
			
			return true;
		},
		
		isFunction: function(obj){
			return Object.prototype.toString.call(obj) === '[object Function]';
		},
		
		isArray: function( obj ) {
			return Object.prototype.toString.call(obj) === '[object Array]';
		},
		
		isObject: function(obj){
			return Object.prototype.toString.call(obj) === '[object Object]';
		},
		
		isNumber: function(obj){
			return Object.prototype.toString.call(obj) === '[object Number]';
		},
		
		isString: function(obj){
			return Object.prototype.toString.call(obj) === '[object String]';
		}, 
		
		extend: function() {
			
			if(arguments.length < 1){
				return ;
			}
			
			var _o = Snail;
			var obj = null;
			
			if(1 == arguments.length){
				obj = arguments[0];
			} else if(2 == arguments.length){
				
				if(Snail.isString(arguments[0])) {
					
					if(Snail[arguments[0]]){
						return;
					}
					
					_o = Snail[arguments[0]] = {};
					
				} else if(Snail.isObject(arguments[0])){
					_o = arguments[0];
				} else {
					return ;
				}
				
				obj = arguments[1];
			} else {
				return ;
			}
			
			if(Snail.isFunction(obj)) {
				obj = obj(_Snail, _win, _doc);
			}
			
			if(!Snail.isObject(obj)){
				return ;
			}
			
			
			for(let name in obj){
				
				if(Snail.isObject(obj[name])
					&& Snail.isObject(_o[name])){
					
					String.extend(_o[name], obj[name]);
					
					continue;
				}
				
				_o[name] = obj[name];
			}
		}
		
	});
	
})(Snail, window, document);



/* 扩展对HTML元素操作 */
Snail.extend({
	
	/**
	 * 对HTML元素赋值
	 * 	样例：
	 * 		Snail.setEleValue('#id', 'XXX');
	 * 		Snail.setEleValue('span', '文本');
	 */
	setEleValue: function(selector, value){
		
		if(Snail.isBlank(selector)){
			return;
		}
		
		var eles = document.querySelectorAll(selector);
		
		if(null == eles || 0 == eles.length){
			return;
		}
		
		for(let i=0, len=eles.length; i<len; i++){
			
			let ele = eles[i];
			
			let key = ele.id || ele.name || ele.tagName;
			
			if('INPUT' == ele.tagName){
				
				if('radio' == ele.type 
					|| 'checkbox' == ele.type){
					
					ele.checked = (value == ele.value);
					
				} else {
					ele.value = value;
				}
				
			}else if('SELECT' == ele.tagName){
				
				let opts = ele.options;
				
				if(ele.multiple){
					vals[key] = [];
				}
				
				for(let j=0, jlen=opts.length; j<jlen; j++){
					
					if(opts[j].selected){
						
						if(ele.multiple){
							vals[key].push(opts[j].value);
						}else{
							vals[key] = opts[j].value;
						}
					}
				}
			}else if('TEXTAREA' == ele.tagName){
				ele.value = value;
			}else{
				ele.innerHTML = ele.value;
			}
		}
	},
	
	/**
	 * 获取HTML元素值
	 * 	样例：
	 * 		Snail.getEleValue('#id');
	 * 		Snail.getEleValue('span');
	 */
	getEleValue: function(selector){
		
		if(Snail.isBlank(selector)){
			return null;
		}
		
		var eles = document.querySelectorAll(selector);
		
		if(null == eles || 0 == eles.length){
			return null;
		}
		
		var vals = {};
		var len = eles.length;
		var key = null;
		
		for(let i=0; i<len; i++){
			
			let ele = eles[i];
			
			key = ele.id || ele.name || ele.tagName;
			
			if('INPUT' == ele.tagName){
				
				if('radio' == ele.type){
					
					if(ele.checked){
						vals[key] = ele.value;
					}
					
				} else if('checkbox' == ele.type){
					
					if(ele.checked){
						vals[key] = vals[key] || [];
						vals[key].push(ele.value);
					}
					
				} else {
					vals[key] = ele.value;
				}
				
			}else if('SELECT' == ele.tagName){
				
				let opts = ele.options;
				
				if(ele.multiple){
					vals[key] = [];
				}
				
				for(let j=0, jlen=opts.length; j<jlen; j++){
					
					if(opts[j].selected){
						
						if(ele.multiple){
							vals[key].push(opts[j].value);
						}else{
							vals[key] = opts[j].value;
						}
					}
				}
			}else if('TEXTAREA' == ele.tagName){
				vals[key] = ele.value;
			}else{
				vals[key] = ele.innerHTML;
			}
		}
		
		return ((1 == len) ? vals[key] : vals);
	},
	
	/**
	 * 绑定事件
	 * 	样例：
	 * 		Snail.bindEvent('#id', 'click', fun);
	 * 		Snail.bindEvent('span', 'click', fun);
	 */
	bindEvent: function(selector, event, fun){
		
		if(Snail.isBlank(selector) 
			|| Snail.isBlank(event) 
			|| null == fun
			|| !Snail.isFunction(fun)){
			return ;
		}
		
		var eles = document.querySelectorAll(selector);
		
		if(null == eles){
			return;
		}
		
		for(let i=0, len=eles.length; i<len; i++){
			
			let ele = eles[i];
			
			ele.addEventListener(event, fun);
			
			ele['__snail_cache_events'] = ele['__snail_cache_events'] || []; 
			ele['__snail_cache_events'].push(fun);
		}
	},
	
	/**
	 * 移除事件
	 * 	样例：
	 * 		Snail.removeEvent('span', 'click');
	 */
	removeEvent: function(selector, event){
		
		if(Snail.isBlank(selector) 
			|| Snail.isBlank(event)){
			return ;
		}
		
		var eles = document.querySelectorAll(selector);
		
		if(null == eles || 1 > eles.length){
			return;
		}
		
		for(let i=0, len=eles.length; i<len; i++){
			
			let ele = eles[i];
			let funs = ele['__snail_cache_events'];
			
			if(null == funs){
				return;	
			}
			
			for(let j=0,jlen=funs.length; i<jlen; j++){
				
				let fun = funs[j];
				
				if(Snail.isFunction(fun)){
					ele.removeEventListener(event, fun);
				}
			}
		}
	},
	
	/**
	 * 在元素内部未尾追加HTML
	 * 	样例：
	 * 		Snail.appendHtml('span', '<span>测试</span>');
	 */
	appendHtml: function(selector, html){
		
		if(Snail.isBlank(selector)
			|| Snail.isBlank(html)){
			return ;
		}
		
		var eles = document.querySelectorAll(selector);
		
		if(null == eles || 1 > eles.length){
			return;
		}
		
		var tempEle = document.createElement('div');
		var fragment = document.createDocumentFragment();
		
		tempEle.innerHTML = html;
		
		var nodes = tempEle.childNodes;
		
		for(let i=0, len=nodes.length; i<len; i++){
			fragment.appendChild(nodes[0]);
		}
		
		for(let i=0, len=eles.length; i<len; i++){
			eles[i].appendChild(fragment);
		}
	},
	
	/**
	 * 在元素内部HTML
	 * 	样例：
	 * 		Snail.cleanHtml('span');
	 */
	cleanHtml: function(selector){
		
		if(Snail.isBlank(selector)){
			return ;
		}
		
		var eles = document.querySelectorAll(selector);
		
		if(null == eles || 1 > eles.length){
			return;
		}
		
		for(let i=0, len=eles.length; i<len; i++){
			eles[i].innerHTML = '';
		}
		
	},
	
	/**
	 * 添加CLASS
	 * 	样例：
	 * 		Snail.appendClass('span', 'cls');
	 */
	appendClass: function(selector, className){
		
		
		if(Snail.isBlank(selector)
			|| Snail.isBlank(className)){
			return ;
		}
		
		var eles = document.querySelectorAll(selector);
		
		if(null == eles || 1 > eles.length){
			return;
		}
		
		for(let i=0, len=eles.length; i<len; i++){
			
			let cname = eles[i].getAttribute('class');
			
			if(Snail.isBlank(cname)){
				cname = clasName;
			}else{
				cname += ' ' + className;
			}
			
			eles[i].setAttribute('class', cname);
		}
	},
	
	/**
	 * 移除CLASS
	 * 	样例：
	 * 		Snail.removeClass('span', 'cls');
	 */
	removeClass: function(selector, className){
		
		
		if(Snail.isBlank(selector)
			|| Snail.isBlank(className)){
			return ;
		}
		
		var eles = document.querySelectorAll(selector);
		
		if(null == eles || 1 > eles.length){
			return;
		}
		
		for(let i=0, len=eles.length; i<len; i++){
			
			let cname = eles[i].getAttribute('class');
			
			if(Snail.isBlank(cname)){
				continue;
			}else{
				cname = style.replace(new RegExp(className + '\s*', 'g'), '');
			}
			
			eles[i].setAttribute('class', cname);
		}
	},
	
	/**
	 * 设置CSS
	 * 	样例：
	 * 		Snail.setCSS('span', {'background-color': '#ffffff'});
	 */
	setCSS: function(selector, css={}){
		
		
		if(Snail.isBlank(selector)){
			return ;
		}
		
		var eles = document.querySelectorAll(selector);
		
		if(null == eles || 1 > eles.length){
			return;
		}
		
		for(let i=0, len=eles.length; i<len; i++){
			
			let style = eles[i].getAttribute('style');
			
			if(Snail.isBlank(style)){
				style = '';
			}
			
			for(let n in css){
				
				let part = n + ': ' + css[n] + ';';
				
				if(-1 != style.indexOf(n)){
					style.replace(new RegExp(n + '\s*:\s*[^;]+;', 'g'), part);
				}else{
					style += part;
				}
			}
			
			eles[i].setAttribute('style', style);
		}
	}
});


Snail.extend('http', function(){
	
	function http(url, method, data, header){
		
		var xhr = new XMLHttpRequest();
		xhr.open(method, url, false);
		
		var isJsonRequest = false;
		var isJsonResponse = false;
		
		if(Snail.isObject(header)){
						
			for(let n in header){
				xhr.setRequestHeader(n, header[n]);
				if('content-type' == n.toLowerCase()){
					if(-1 != header[n].toLowerCase().indexOf('json')){
						isRequestJson = true;
					}
				}else if('accept' == n.toLowerCase()){
					if(-1 != header[n].toLowerCase().indexOf('json')){
						isJsonResponse = true;
					}
				}
			}
		}
		
		if(!Snail.isBlank(data)){
			
			if(isRequestJson){
				
				if(Snail.isObject(data)){
					data = new Blob([Snail.toJSONString(data)], {type : 'application/json'});
				}
				
				xhr.send(data);
				
			}else{
				
				if(Snail.isObject(data)){
					
					var formData = new FormData();
					
					for(let n in data){
						formData.append(n, data[n]);
					}
					
					xhr.send(formData);
					
				}else{
					xhr.send(data);
				}
			}
		}else{
			xhr.send();
		}
		
		if(isJsonResponse){
			return Snail.toJSON(xhr.responseText);
		}
		
		return xhr.responseText;
    }
	
	function upload(url, file, fun){
		
		var formData = new FormData();
		formData.append('file', file);

		var xhr = new XMLHttpRequest();
		xhr.open('POST', url, (fun ? true : false));
		xhr.onreadystatechange = fun
		xhr.send(formData);
		
		return xhr.responseText;
	}

    return {
        get: function(url, data, header){
	
			if(Snail.isObject(data)){
				for(let n in data){
					url = Snail.request.join(url, n, data[n]);
				}
			}
			
			return http(url, 'GET', null, header);
		},
		
		post: function(url, data, header){			
			return http(url, 'POST', data, header);
		},
		
		put: function(url, data, header){			
			return http(url, 'PUT', data, header);
		},
		
		delete: function(url, data, header){			
			return http(url, 'DELETE', data, header);
		},
		
		upload: upload
    }
});


/* 扩展方法 */
Snail.extend({

	/**
	 * 将字符串转化为日期
	 * 样例：
	 * Snail.toDate('2018-08-10') 
	 * Snail.toDate('2018-08-10 13:55:03.89') 
	 */
	toDate: function(sDate, fmt){
		
		try {
			
			var times = Date.parse(sDate);
			
			if(isNaN(times)) {
				throw 'Invalid Date';
			}
			
			return new Date(times);

		} catch(error) {
			
			if(Snail.isBlank(sDate)){
				return null;
			}
			
			if(Snail.isBlank(fmt)){
				fmt = 'yyyy-MM-dd';
			}
			
			var part = {
					'y': function(date, fn){ // 年
						
						var num = fn('y', 4);
						
						if(0 == num){
							return ;
						}
						
						date.setYear(num);
					},			
					'M' : function(date, fn){ // 月
						
						var num = fn('M', 2);
						date.setMonth(num > 0 ? num - 1 : 0);
					},
					'd' : function(date, fn){ // 日 
						
						date.setDate(fn('d', 2));
					},	  
					'H' : function(date, fn){ // 时
						
						date.setHours(fn('H', 2));
					},				    
					'm' : function(date, fn){ // 分
						
						date.setMinutes(fn('m', 2));
					},			   
					's' : function(date, fn){ // 秒
						
						date.setSeconds(fn('s', 2));
					},			  
					'S' : function(date, fn){ // 毫秒
						
						date.setMilliseconds(fn('S', 3));
					}		   
			};
			
			var fn = function(type, len){
				
				var i = fmt.indexOf(type);
				
				if(-1 == i){
					return 0;
				}
				
				var l = fmt.lastIndexOf(type);
				
				while((l - i + 1) < len){ // 优化日期格式化字符串
					fmt = fmt.substring(0, i) + type + fmt.substring(i);
					l++;
				}
				
				var str = sDate.substring(i);
				str = str.substring(0, (((l = str.search(/[^\d]/)) == -1) ? str.length : l));
				
				if(null == str || '' === str){
					throw 'Invalid Date';
				}
				
				while(str.length < len){ // 优化日期字符串
					sDate = sDate.substring(0, i) + '0' + sDate.substring(i);
					str = '0' + str;
				}
				
				if(/[^\d]/.test(str)){
					throw 'Invalid Date';
				}
				
				return new Number(str);
			};
			
			var date = new Date();
			
			for(let p in part){
				part[p](date, fn);
			}
			
			return date;				
		}
		
	},

	/**
	 * 日期格式化
	 * 样例：
	 * Snail.dateFormat(new Date(), 'yyyy-MM-dd')	-> 2018-08-10
	 * Snail.dateFormat(new Date(), 'yyyy/MM/dd')	-> 2018/08/10
	 * Snail.dateFormat(new Date(), 'yyyy年M月d日')	-> 2018年8月10日
	 * Snail.dateFormat(new Date(), 'yy年MM月dd日')	-> 08年08月10日
	 * Snail.dateFormat(new Date(), 'yyyy年第q季度')	-> 2018年第3季度
	 * Snail.dateFormat(new Date(), 'yyyy-MM-dd HH:mm:ss')		-> 2018-08-10 13:55:03
	 * Snail.dateFormat(new Date(), 'yyyy-MM-dd HH:mm:ss.S')	-> 2018-08-10 13:55:03.89
	 * Snail.dateFormat(new Date())	-> 2018-08-10
	 */
	dateFormat: function(date, fmt){
		
		if(Snail.isBlank(date)){
			return null;
		}
		
		if(Snail.isBlank(fmt)){
			fmt = 'yyyy-MM-dd';
		}
		
		var tem = 0;
		
		var part = {
				'y{4}': date.getFullYear(),			// 年份(4位)
				'y{2}': date.getFullYear() % 10,	// 年份(2位)
				'y': date.getFullYear(),			// 年份(4位)
				'q' : Math.floor((date.getMonth() + 3) / 3),	// 季度  
				'M{2}' : ((tem = (date.getMonth() + 1)) < 10 ? ('0' + tem) : tem),	// 月份
				'M' : date.getMonth() + 1,			// 月份   
				'd{2}' : ((tem = date.getDate()) < 10 ? ('0' + tem) : tem),			// 日
				'd' : date.getDate(),				// 日   
				'H{2}' : ((tem = date.getHours()) < 10 ? ('0' + tem) : tem),		// 小时  
				'H' : date.getHours(),				// 小时    
				'm{2}' : ((tem = date.getMinutes()) < 10 ? ('0' + tem) : tem),		// 分  
				'm' : date.getMinutes(),			// 分   
				's{2}' : ((tem = date.getSeconds()) < 10 ? ('0' + tem) : tem),		// 秒 
				's' : date.getSeconds(),			// 秒  
				'S' : date.getMilliseconds()		// 毫秒   
		};
		
		for(let p in part){
			fmt = fmt.replace(new RegExp(p), part[p]);
		}
		
		return fmt;
	},
	
	
	/**
	 * 修改日期
	 * 样例：
	 * Snail.plusDate(new Date(), 'S', 300)	-> 2018-08-10 13:55:03.8 -> 2018-08-10 13:55:03.308
	 * Snail.plusDate(new Date(), 's', 30)	-> 2018-08-10 13:55:03.8 -> 2018-08-10 13:55:33.8
	 * Snail.plusDate(new Date(), 'm', 3)	-> 2018-08-10 13:55:03.8 -> 2018-08-10 13:58:03.8
	 * Snail.plusDate(new Date(), 'H', 3)	-> 2018-08-10 13:55:03.8 -> 2018-08-10 16:55:03.8
	 * Snail.plusDate(new Date(), 'd', 3)	-> 2018-08-10 13:55:03.8 -> 2018-08-13 13:55:03.8
	 * Snail.plusDate(new Date(), 'M', 3)	-> 2018-08-10 13:55:03.8 -> 2018-11-10 13:55:03.8
	 * Snail.plusDate(new Date(), 'Y', 3)	-> 2018-08-10 13:55:03.8 -> 2021-08-10 13:55:03.8
	 */
	plusDate: function(date, fmt, num){
		
		if(null == date){
			date = new Date();
		} else{
			var times = date.getTime();
			date = new Date();
			date.setTime(times);
		}
		
		if(Snail.isBlank(fmt)){
			fmt = 'S';
		}
		
		if(null == num || 0 == num){
			return date;
		}
		
		var times = date.getTime();
		
		switch(fmt){
			case 's':{
				times += num * 1000;
				break;
			}
			case 'm':{
				times += num * 60 * 1000;
				break;
			}
			case 'H':{
				times += num * 60* 60 * 1000;
				break;
			}
			case 'd':{
				times += num * 24 * 60* 60 * 1000;
				break;
			}
			case 'M':{
				
				if(0 < num){
					num = date.getMonth() + num;
					
					if(11 >= num){
						date.setMonth(num);
					}else{
						y = Math.floor(num / 11);
						date.setFullYear(date.getFullYear() + y);
						date.setMonth(num % 11);
					}
					
				}else{
					
					num = date.getMonth() + num;
					
					if(0 <= num){
						date.setMonth(num);
					}else{
						num = Math.abs(num);
						y = Math.floor(num / 11);
						date.setFullYear(date.getFullYear() - (y + 1));
						date.setMonth((12 - (num % 11)));
					}
				}
				
				return date;
			}
			case 'y':{
				date.setFullYear(date.getFullYear() + num);
				return date;
			}
			default:
				times += num;
		}
		
		date.setTime(times);
		
		return date;
	},
	
	
	__CACHE__: Snail.__CACHE__ || {},
	
	/**
	 * 加入到缓存
	 */
	put: function(key, value){
		
		if(!key){
			return ;
		}
		
		Snail.__CACHE__[key] = value;
		
		// 深度缓存，缓存到Cookie
		if(arguments.length == 3 && true == arguments[2]){
			Snail.cookie.setCookie(key, value);
		}
	}, 
	
	/**
	 * 从缓存中提取数据
	 */
	get: function(key){
		
		if(!key){
			return null;
		}
		
		return Snail.__CACHE__[key] || Snail.cookie.getCookie(key);
	}, 
	
	logger: function(txt){
		
		try {
			console.log(txt);	
		} catch(e){}
	},
	
	/**
	 * 将JSON对象转JSON字符串
	 */
	toJSONString: function(obj){
		
		if(obj.toJSONString){
			
			return obj.toJSONString();
			
		} else if(JSON && JSON.stringify){
			
			return JSON.stringify(obj);
		}

		
		/* Begin:简单实现JSON对象转JSON字符串  */
		var strJson = '';
		var depth = (2 == arguments.length && Snail.isNumber(arguments[1])) ? arguments[1] : 0;
		
		if(Snail.isObject(obj)){
			
			for(let name in obj){
				
				if(Snail.isObject(obj[name]) || Snail.isArray(obj[name])){
					
					if(depth < 100) {
						strJson += ', "' + name + '": ' + Snail.toJSONString(obj[name], depth++);
					} else {
						strJson += ', "' + name + '": "[ TOO DEPTH OBJECT ]"';
					}
				} else {
					strJson += ', "' + name + '": "' + obj[name] + '"';
				}
				
			}
			
			strJson = '{' + strJson.substring(2) + '}';

			return strJson;
		} else if(Snail.isArray(obj)){
			
			for(let name in obj){
				
				if(Snail.isObject([name]) || Snail.isArray(obj[name])){
					if(depth < 100) {
						strJson += ', ' + Snail.toJSONString(obj[name], depth++);
					} else {
						strJson += ', "' + obj[name] + '"';
					}
				} else {
					strJson += ', "[ TOO DEPTH OBJECT ]"';
				}
				
			}
			
			strJson = '[' + strJson.substring(2) + ']';
			
			return strJson;
		}
		/* End */
		
		return Object.prototype.toString.call(obj);
	}, 
	
	/**
	 * 将字符串解析成JSON对象
	 */
	toJSON: function(str){
		
		if(JSON && JSON.parse){
			return JSON.parse(str);
		}
		
		return (new Function("return " + str))(); 
	}, 
	
	/**
	 * Begin:
	 * 循环执行fn函数，直到fn函数返回true。（或执行fn函数超10次后中断）
	 * 
	 * 样例：
	 * function test(){
	 * 
	 *     var i = Math.random();
	 *     
	 *     alert(i);
	 *     
	 *     if(i > 0.1){
	 *         return false;
	 *     }
	 * 
	 *     alert('执行结束。');
	 * 
	 *     return true;
	 * }
	 * 
	 * Snail.run(test); // 或 Snail.run('test()');
	 */
	__SET_TIMEOUT__: Snail.__SET_TIMEOUT__ || {},
	run: function(fn){
		
		var sleeptimes = Snail.__SET_TIMEOUT__[fn] = Snail.__SET_TIMEOUT__[fn] || 0;
		
		if((sleeptimes += 500) > 5000){
			return;
		}
		
		window.setTimeout(function(){
			
			var runState = false;
			
			try {
				
				if(Snail.isString(fn)){
				
					runState = eval(fn);
				
				} else if(Snail.isFunction(fn)){
					
					runState = fn();
				}	
				
			} catch(error){
				alert(error);
			}
					
			if(false === runState){
				Snail.run(fn);
			}
				
		}, sleeptimes);
		
		Snail.__SET_TIMEOUT__[fn] = sleeptimes;
	},
	/* End */
	
	
	/**
	 * 将字符串编码成16进值文本
	 */
	encodeHex: function(txt){
		
		if(!txt){
			return txt;
		}
		
		var etxt = "";
		
		for(let i = 0; i < txt.length; i++){
			etxt += "%" + txt.charCodeAt(i).toString(16);
		}
		
		return etxt;
	},
	
	/**
	 * 解码16进值文本
	 */
	decodeHex: function(txt){
		
		if(!txt){
			return txt;
		}
		
		var dtxt = "";
		var arrtxt = txt.split("%");
		
		for(let i = 1; i < arrtxt.length; i++){
			dtxt += String.fromCharCode(parseInt(arrtxt[i], 16));
		}
		
		return dtxt;
	},
	
	/**
	 * byte数组换为16进制字符串
	 * 	样例：Snail.byteArrayToHexString([-74, 90, 87, 112, 67]);
	 * 		->: ca5a577043
	 */
	byteArrayToHexString: function(bytes){
		
		if(null == bytes){
			return;
		}
		
		if(!Snail.isArray(bytes)){
			throw '非byte数组数据！';
		}
		
		var hex = '';
		
		for(let i = 0, len = bytes.length; i < len; i++){
					
			let b = bytes[i];
			
			if(!Snail.isNumber(b)){
				throw '非byte数组数据！(' + b + ')';
			}
			
			if(-128 <= b && b < 0){
				
				hex += ((b * -1) | 0x80).toString(16);
				
			}else if(0 == b){
				
				hex += '00';
				
			}else if(0 < b && b <= 15){
				hex += ('0' + b.toString(16));
			}else if(15 < b && b <= 127){
				hex += b.toString(16);
			}else{
				throw '非byte(-127<b<127)数组数据！(无效byte数据：' + b + ')';
			}
		}
		
		return hex;
	},
	
	/**
	 * 16进制字符串换为byte数组
	 * 	样例：Snail.hexStringToByteArray('ca5a577043');
	 * 		->: [-74, 90, 87, 112, 67]
	 */
	hexStringToByteArray: function(str){
		
		if(null == str){
			return;
		}
				
		var bytes = [];
		
		for(let i = 0, len = str.length; i < len;){
			
			let b = parseInt(str.substring(i, i+=2), 16);
			
			if(b > 127){ // 负数
				b = ((b & 0x7F) * -1)
			}
			
			bytes.push(b);
		}
		
		return bytes;
	},

	/**
	 * 生成20位随机数
	 */
	random20L: function(){
		
		var now = new Date();
		var yStr = now.getFullYear().toString();
		var mStr = ((now.getMonth() < 9 ? '0' : '') + (now.getMonth() + 1));
		var dStr = ((now.getDate() < 10 ? '0' : '') + now.getDate());
		var hStr = ((now.getHours() < 10 ? '0' : '') + now.getHours());
		var miStr = ((now.getMinutes() < 10 ? '0' : '') + now.getMinutes());
		var sStr = ((now.getSeconds() < 10 ? '0' : '') + now.getSeconds());
		
		var ranStr = Math.random().toString();
		ranStr = '000000' + ranStr.substring(2);
		ranStr = ranStr.substring(ranStr.length - 6);
		
		return yStr + mStr + dStr + hStr + miStr + sStr + ranStr;
	},
	
	/**
	 * 数据转中文大写（整数）
	 * 样例：
	 * Snail.numberToUpperCase('8000200021000678') -> 捌仟万零贰仟亿零贰仟壹佰万零陆佰柒拾捌
	 * Snail.numberToUpperCase('8111200021000678') -> 捌仟壹佰壹拾壹万贰仟亿零贰仟壹佰万零陆佰柒拾捌
	 * Snail.numberToUpperCase('8555211121987799') -> 捌仟伍佰伍拾伍万贰仟壹佰壹拾壹亿贰仟壹佰玖拾捌万柒仟柒佰玖拾玖
	 * Snail.numberToUpperCase('8000000000000099') -> 捌仟万亿零玖拾玖
	 * Snail.numberToUpperCase('800000000000') -> 捌仟亿
	 */
	numberToUpperCase: function(num){
		
		if(Snail.isBlank(num)){
			
			return '零';
		}
		
		if(Snail.isNumber(num)){
			num = num.toString();
		}
		
		if(-1 != num.indexOf('.')){
			return num + ', 非整数 !';
		}
		
		var len = num.length;
		
		if(len > 16){
			return num + ', 位数过大 !';
		}
		
		num = num.replace(",","") // 去“,”
		num = num.replace(" ","") // 去空格
		
		var num_char = {
			'0': '零', '1': '壹', '2': '贰', '3': '叁', '4': '肆',
			'5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖'
		};
		
		var num_bit = [
			'_', '拾', '佰', '仟', '_万', '拾', '佰', '仟', 
			'_亿', '拾', '佰', '仟', '_万', '拾', '佰', '仟'
		]
		
		var numStr = '';
		
		for(var i = len; i > 0; i--){
			numStr = num_char[num[i - 1]] + num_bit[len - i] + numStr;
		}
	
		// 去‘_’
		numStr = numStr.replace(/零[_]/g, ''); 
		numStr = numStr.replace(/[_]/g, ''); 

		// 去中部的‘零’
		numStr = numStr.replace(/(零[^零])+/g, '零');
		numStr = numStr.replace(/零亿/g, '亿零');
		numStr = numStr.replace(/零万/g, '万零');
		numStr = numStr.replace(/零+/g, '零');
		numStr = numStr.replace(/零亿/g, '亿');
		numStr = numStr.replace(/零万/g, '万');

		// 为亿以上数字时，去尾部的‘万’(多余)
		numStr = numStr.replace(/亿万/g, '亿');
	
		// 去尾部的‘零’
		numStr = (numStr + '_').replace(/零?_/, '');
		
		return numStr;
	},

	/**
	 * 是否为身份证号
	 * 
	 * 样例：Snail.isIdentityCode('123456789012345678')
	 * 
	 * 身份证号码中的校验码是身份证号码的最后一位，是根据GB 11643-1999中有关公民身份号码的规定，根据精密的
	 * 计算公式计算出来的，公民身份号码是特征组合码，由十七位数字本体码和一位数字校验码组成。排列顺序从左至
	 * 右依次为：六位数字地址码，八位数字出生日期码，三位数字顺序码，最后一位是数字校验码。
	 */
	isIdentityCode: function(code){
		
		if(Snail.isBlank(code)){
			return false;
		}
		
		code = code.toUpperCase();
		
		if(!/\d{6}(18|19|20)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]\d{3}(\d|X))/i.test(code)){ // 身份证号格式错误
			// alert('身份证号格式错误');
			return false;
		}
		
		switch(code.substring(10,12)){
		case '02':{
			
			if(0 == (code.substring(6,10) % 4)){
				
				if(29 < code.substring(12,14)){ // 二月与日不匹配
					// alert('二月与日不匹配');
					return false;
				}
			} else {
				if(28 < code.substring(12,14)){ // 二月与日不匹配
					// alert('二月与日不匹配');
					return false;
				}
			}
			
			break;
		}
		case '04':
		case '06':
		case '09':
		case '11':
			if('31' == code.substring(12,14)){ // 月与日不匹配
				// alert('月与日不匹配');
				return false;
			}
		}
		
		//加权因子
		var factor = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2 ];
		//校验位
		var parity = [ 1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2 ];
		
		var sum = 0;
		
		for(var i = 0; i < 17; i++){
			sum += (factor[i] * code.charAt(i));
		}
		
		var x = sum % 11;
		
		if(parity[x] != code.charAt(17)){ // 校验位错误
			// alert('校验位错误');
			return false;
		}

		return true;
	}
	
});



/* 扩展对Cookie的操作 */ 
Snail.extend('cookie', {
	

	getCookie: function(key){
		
		var startIndex = 0;
		var endIndex = 0;
		
		if (document.cookie.length > 0){
			
			startIndex = document.cookie.indexOf(key + "=");
			
			if (startIndex != -1) {
			
				startIndex = startIndex + key.length + 1;
				endIndex = document.cookie.indexOf(";", startIndex);
				
				if(endIndex == -1){
					endIndex = document.cookie.length;
				}
		
				return  startIndex == endIndex ? null : unescape(document.cookie.substring(startIndex, endIndex));
			}
		}

		return null;
	},
	
	/**
	 * 添加Cookie
	 * 
	 * 样例：
	 * 	Snail.setCookie('skey', '12345678');
	 * 	Snail.setCookie('skey', '12345678', (365 * 24 * 60 * 60 * 1000));
	 * 	Snail.setCookie('skey', '12345678', {expires: (365 * 24 * 60 * 60 * 1000), path: '/', domain:'snail.com', secure: true });
	 * 	Snail.setCookie('skey', '12345678', 'expires=Wed, 29 Aug 2018 00:27:38 GMT; path=/; domain=snail.com, secure=true');
	 */
	setCookie: function (key, value) {
		
		var txt = (key + "=" + escape(Snail.isObject(value) ? Snail.toJSONString(value) : value));
		
		if(2 == arguments.length){
			
			var expiredays = new Date();
			expiredays.setTime(expiredays.getTime() + (24 * 60 * 60 * 1000));
			
			txt += ('; expires=' + expiredays.toGMTString());
			txt += '; path=/';
			
		} else if(3 == arguments.length){
			
			if(Snail.isNumber(arguments[2])){
				
				var expiredays = new Date();
				expiredays.setTime(expiredays.getTime() + arguments[2]);
				
				txt += ('; expires=' + expiredays.toGMTString());
				txt += '; path=/';
				
			} else if(Snail.isObject(arguments[2])){
				
				var val = null;
				
				for(let name in arguments[2]){
					
					val = arguments[2][name];
					
					if('expires' === name){
						
						var expiredays = new Date();
						expiredays.setTime(expiredays.getTime() + (Snail.isNumber(val) ? val : new Number(val)));
						
						txt += ('; expires=' + expiredays.toGMTString());
					} else {
						txt += ('; ' + name + '=' + val);
					}
				}
			} else {
				txt += ('; ' + arguments[2]);
			}	
			
		} 
		
				
		document.cookie = txt;
	},
	
	delCookie: function (key) {
		
		var value = getCookie(key);
		
		if(null == value || "" == value){
			return;
		}
		
		var expiredays = new Date();
		expiredays.setDate(expiredays.getDate() - 1);
		
		document.cookie = key + "=" + escape(value) + ";expires=" + expiredays.toGMTString();
		
		return value;
	}
});



/* 扩展对HTTP请求（request）的操作 */ 
Snail.extend('request', {

	/**
	 * 从URL中提取数据
	 * 样例：
	 * 		URL: http://www.i8yun.com/app?name=snail&code=S001
	 * 		
	 * 		Snail.request.getParament('code');
	 * 			-> S001
	 * 
	 */
	getParament: function (key, defaultValue){
		
		var url = window.location.href;
		
		var si = 0, ei = 0;
		
		si = url.indexOf(key + "=");
		
		if (si != -1) {
			
			si = si + key.length + 1;
			
			ei = url.indexOf("&", si);
		}
		
		if(ei == -1){
			ei = url.length;
		}
		
		return  si == ei ? defaultValue : url.substring(si, ei);
	},
	
	/* 返回：http://172.16.0.234:8080 */
	getHostUrl: function(){
		return Snail.request.getProtocol() + '://' + Snail.request.getHost() + ':' + Snail.request.getPort();
	},
	
	/* 返回：http */
	getProtocol: function (){
		return window.location.protocol.substring(0, (window.location.protocol.length - 1));
	},
	
	/* 返回：172.16.0.234 */
	getHost: function (){
		return window.location.hostname;
	},
	
	/* 返回：8080 */
	getPort: function (){
		return window.location.port ? window.location.port : ('https' === Snail.request.getProtocol() ? '443' : '80');
	},
	
	/**
	 * 拼接URL
	 * 样例：
	 * 		Snail.request.join('code', 'S001');
	 * 			-> http://www.i8yun.com/app?code=S001
	 * 		Snail.request.join('http://www.i8yun.com/app?name=snail', 'code', 'S001');
	 * 			-> http://www.i8yun.com/app?name=snail&code=S001
	 */
	join: function (){
		
		var url = null;
		var key = null;
		var value = null;
		
		if(2 == arguments.length){
			url = window.location.href;
			key = arguments[0];
			value = arguments[1];
		} else if(3 == arguments.length){
			url = arguments[0];
			key = arguments[1];
			value = arguments[2];
		}else{
			return null;
		}
		
		return url + (-1 == url.indexOf('?') ? '?' : '&') + key + '=' + encodeURIComponent(value);
	}
});


/**
 *  基于第三方MD5工具封装 
 *  
 *  样例：
 *  Snail.hex_md5('ASDFGHJKL') 						-> a125f852854bff5d6d876183b1a2562c
 *  Snail.hex_hmac_md5('ASDFGHJKL','123456') 		-> e79cd0e9f528c32b28e5d06b8f57427c
 *  Snail.base64_md5('ASDFGHJKL') 					-> oSX4UoVL/11th2GDsaJWLA
 *  Snail.base64_hmac_md5('ASDFGHJKL','123456') 	-> 55zQ6fUowyso5dBrj1dCfA
 */
Snail.extend(function(){
	
	/*
	 * A JavaScript implementation of the RSA Data Security, Inc. MD5 Message
	 * Digest Algorithm, as defined in RFC 1321.
	 * Version 2.1 Copyright (C) Paul Johnston 1999 - 2002.
	 * Other contributors: Greg Holt, Andrew Kepert, Ydnar, Lostinet
	 * Distributed under the BSD License
	 * See http://pajhome.org.uk/crypt/md5 for more info.
	 */
	var hexcase=0;var b64pad="";var chrsz=8;function hex_md5(a){return binl2hex(core_md5(str2binl(a),a.length*chrsz))}function b64_md5(a){return binl2b64(core_md5(str2binl(a),a.length*chrsz))}function str_md5(a){return binl2str(core_md5(str2binl(a),a.length*chrsz))}function hex_hmac_md5(a,b){return binl2hex(core_hmac_md5(a,b))}function b64_hmac_md5(a,b){return binl2b64(core_hmac_md5(a,b))}function str_hmac_md5(a,b){return binl2str(core_hmac_md5(a,b))}function core_md5(p,k){p[k>>5]|=128<<((k)%32);p[(((k+64)>>>9)<<4)+14]=k;var o=1732584193;var n=-271733879;var m=-1732584194;var l=271733878;for(var g=0;g<p.length;g+=16){var j=o;var h=n;var f=m;var e=l;o=md5_ff(o,n,m,l,p[g+0],7,-680876936);l=md5_ff(l,o,n,m,p[g+1],12,-389564586);m=md5_ff(m,l,o,n,p[g+2],17,606105819);n=md5_ff(n,m,l,o,p[g+3],22,-1044525330);o=md5_ff(o,n,m,l,p[g+4],7,-176418897);l=md5_ff(l,o,n,m,p[g+5],12,1200080426);m=md5_ff(m,l,o,n,p[g+6],17,-1473231341);n=md5_ff(n,m,l,o,p[g+7],22,-45705983);o=md5_ff(o,n,m,l,p[g+8],7,1770035416);l=md5_ff(l,o,n,m,p[g+9],12,-1958414417);m=md5_ff(m,l,o,n,p[g+10],17,-42063);n=md5_ff(n,m,l,o,p[g+11],22,-1990404162);o=md5_ff(o,n,m,l,p[g+12],7,1804603682);l=md5_ff(l,o,n,m,p[g+13],12,-40341101);m=md5_ff(m,l,o,n,p[g+14],17,-1502002290);n=md5_ff(n,m,l,o,p[g+15],22,1236535329);o=md5_gg(o,n,m,l,p[g+1],5,-165796510);l=md5_gg(l,o,n,m,p[g+6],9,-1069501632);m=md5_gg(m,l,o,n,p[g+11],14,643717713);n=md5_gg(n,m,l,o,p[g+0],20,-373897302);o=md5_gg(o,n,m,l,p[g+5],5,-701558691);l=md5_gg(l,o,n,m,p[g+10],9,38016083);m=md5_gg(m,l,o,n,p[g+15],14,-660478335);n=md5_gg(n,m,l,o,p[g+4],20,-405537848);o=md5_gg(o,n,m,l,p[g+9],5,568446438);l=md5_gg(l,o,n,m,p[g+14],9,-1019803690);m=md5_gg(m,l,o,n,p[g+3],14,-187363961);n=md5_gg(n,m,l,o,p[g+8],20,1163531501);o=md5_gg(o,n,m,l,p[g+13],5,-1444681467);l=md5_gg(l,o,n,m,p[g+2],9,-51403784);m=md5_gg(m,l,o,n,p[g+7],14,1735328473);n=md5_gg(n,m,l,o,p[g+12],20,-1926607734);o=md5_hh(o,n,m,l,p[g+5],4,-378558);l=md5_hh(l,o,n,m,p[g+8],11,-2022574463);m=md5_hh(m,l,o,n,p[g+11],16,1839030562);n=md5_hh(n,m,l,o,p[g+14],23,-35309556);o=md5_hh(o,n,m,l,p[g+1],4,-1530992060);l=md5_hh(l,o,n,m,p[g+4],11,1272893353);m=md5_hh(m,l,o,n,p[g+7],16,-155497632);n=md5_hh(n,m,l,o,p[g+10],23,-1094730640);o=md5_hh(o,n,m,l,p[g+13],4,681279174);l=md5_hh(l,o,n,m,p[g+0],11,-358537222);m=md5_hh(m,l,o,n,p[g+3],16,-722521979);n=md5_hh(n,m,l,o,p[g+6],23,76029189);o=md5_hh(o,n,m,l,p[g+9],4,-640364487);l=md5_hh(l,o,n,m,p[g+12],11,-421815835);m=md5_hh(m,l,o,n,p[g+15],16,530742520);n=md5_hh(n,m,l,o,p[g+2],23,-995338651);o=md5_ii(o,n,m,l,p[g+0],6,-198630844);l=md5_ii(l,o,n,m,p[g+7],10,1126891415);m=md5_ii(m,l,o,n,p[g+14],15,-1416354905);n=md5_ii(n,m,l,o,p[g+5],21,-57434055);o=md5_ii(o,n,m,l,p[g+12],6,1700485571);l=md5_ii(l,o,n,m,p[g+3],10,-1894986606);m=md5_ii(m,l,o,n,p[g+10],15,-1051523);n=md5_ii(n,m,l,o,p[g+1],21,-2054922799);o=md5_ii(o,n,m,l,p[g+8],6,1873313359);l=md5_ii(l,o,n,m,p[g+15],10,-30611744);m=md5_ii(m,l,o,n,p[g+6],15,-1560198380);n=md5_ii(n,m,l,o,p[g+13],21,1309151649);o=md5_ii(o,n,m,l,p[g+4],6,-145523070);l=md5_ii(l,o,n,m,p[g+11],10,-1120210379);m=md5_ii(m,l,o,n,p[g+2],15,718787259);n=md5_ii(n,m,l,o,p[g+9],21,-343485551);o=safe_add(o,j);n=safe_add(n,h);m=safe_add(m,f);l=safe_add(l,e)}return Array(o,n,m,l)}function md5_cmn(h,e,d,c,g,f){return safe_add(bit_rol(safe_add(safe_add(e,h),safe_add(c,f)),g),d)}function md5_ff(g,f,k,j,e,i,h){return md5_cmn((f&k)|((~f)&j),g,f,e,i,h)}function md5_gg(g,f,k,j,e,i,h){return md5_cmn((f&j)|(k&(~j)),g,f,e,i,h)}function md5_hh(g,f,k,j,e,i,h){return md5_cmn(f^k^j,g,f,e,i,h)}function md5_ii(g,f,k,j,e,i,h){return md5_cmn(k^(f|(~j)),g,f,e,i,h)}function core_hmac_md5(c,f){var e=str2binl(c);if(e.length>16){e=core_md5(e,c.length*chrsz)}var a=Array(16),d=Array(16);for(var b=0;b<16;b++){a[b]=e[b]^909522486;d[b]=e[b]^1549556828}var g=core_md5(a.concat(str2binl(f)),512+f.length*chrsz);return core_md5(d.concat(g),512+128)}function safe_add(a,d){var c=(a&65535)+(d&65535);var b=(a>>16)+(d>>16)+(c>>16);return(b<<16)|(c&65535)}function bit_rol(a,b){return(a<<b)|(a>>>(32-b))}function str2binl(d){var c=Array();var a=(1<<chrsz)-1;for(var b=0;b<d.length*chrsz;b+=chrsz){c[b>>5]|=(d.charCodeAt(b/chrsz)&a)<<(b%32)}return c}function binl2str(c){var d="";var a=(1<<chrsz)-1;for(var b=0;b<c.length*32;b+=chrsz){d+=String.fromCharCode((c[b>>5]>>>(b%32))&a)}return d}function binl2hex(c){var b=hexcase?"0123456789ABCDEF":"0123456789abcdef";var d="";for(var a=0;a<c.length*4;a++){d+=b.charAt((c[a>>2]>>((a%4)*8+4))&15)+b.charAt((c[a>>2]>>((a%4)*8))&15)}return d}function binl2b64(d){var c="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";var f="";for(var b=0;b<d.length*4;b+=3){var e=(((d[b>>2]>>8*(b%4))&255)<<16)|(((d[b+1>>2]>>8*((b+1)%4))&255)<<8)|((d[b+2>>2]>>8*((b+2)%4))&255);for(var a=0;a<4;a++){if(b*8+a*6>d.length*32){f+=b64pad}else{f+=c.charAt((e>>6*(3-a))&63)}}}return f};

	return {
		hex_md5: hex_md5,
		base64_md5: b64_md5,
		hex_hmac_md5: hex_hmac_md5,
		base64_hmac_md5: b64_hmac_md5
	};
});


/**
 *  基于第三方BASE64工具封装 
 *  
 *  样例：
 *  Snail.base64_encode('1234567890QWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()_+{}:"<>?') 
 *  	-> MTIzNDU2Nzg5MFFXRVJUWVVJT1BBU0RGR0hKS0xaWENWQk5NIUAjJCVeJiooKV8re306Ijw+Pw==
 *  
 *  Snail.base64_decode('MTIzNDU2Nzg5MFFXRVJUWVVJT1BBU0RGR0hKS0xaWENWQk5NIUAjJCVeJiooKV8re306Ijw+Pw==') 
 *  	-> 1234567890QWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()_+{}:"<>?
 */
Snail.extend(function(){
	
	var _BASE64_KEY_CHAR_="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";function encode(c){var a="";var k,h,f,j,g,e,d;var b=0;c=_utf8_encode(c);while(b<c.length){k=c.charCodeAt(b++);h=c.charCodeAt(b++);f=c.charCodeAt(b++);j=k>>2;g=((k&3)<<4)|(h>>4);e=((h&15)<<2)|(f>>6);d=f&63;if(isNaN(h)){e=d=64}else{if(isNaN(f)){d=64}}a=a+_BASE64_KEY_CHAR_.charAt(j)+_BASE64_KEY_CHAR_.charAt(g)+_BASE64_KEY_CHAR_.charAt(e)+_BASE64_KEY_CHAR_.charAt(d)}return a}function decode(c){var a="";var k,h,f;var j,g,e,d;var b=0;c=c.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(b<c.length){j=_BASE64_KEY_CHAR_.indexOf(c.charAt(b++));g=_BASE64_KEY_CHAR_.indexOf(c.charAt(b++));e=_BASE64_KEY_CHAR_.indexOf(c.charAt(b++));d=_BASE64_KEY_CHAR_.indexOf(c.charAt(b++));k=(j<<2)|(g>>4);h=((g&15)<<4)|(e>>2);f=((e&3)<<6)|d;a=a+String.fromCharCode(k);if(e!=64){a=a+String.fromCharCode(h)}if(d!=64){a=a+String.fromCharCode(f)}}a=_utf8_decode(a);return a}function _utf8_encode(a){a=a.replace(/\r\n/g,"\n");var b="";for(var e=0;e<a.length;e++){var d=a.charCodeAt(e);if(d<128){b+=String.fromCharCode(d)}else{if((d>127)&&(d<2048)){b+=String.fromCharCode((d>>6)|192);b+=String.fromCharCode((d&63)|128)}else{b+=String.fromCharCode((d>>12)|224);b+=String.fromCharCode(((d>>6)&63)|128);b+=String.fromCharCode((d&63)|128)}}}return b}function _utf8_decode(b){var a="";var d=0;var e=c1=c2=0;while(d<b.length){e=b.charCodeAt(d);if(e<128){a+=String.fromCharCode(e);d++}else{if((e>191)&&(e<224)){c2=b.charCodeAt(d+1);a+=String.fromCharCode(((e&31)<<6)|(c2&63));d+=2}else{c2=b.charCodeAt(d+1);c3=b.charCodeAt(d+2);a+=String.fromCharCode(((e&15)<<12)|((c2&63)<<6)|(c3&63));d+=3}}}return a};
	
	return {
		base64_encode: encode,
		base64_decode: decode
	};
});



//export default Snail;
