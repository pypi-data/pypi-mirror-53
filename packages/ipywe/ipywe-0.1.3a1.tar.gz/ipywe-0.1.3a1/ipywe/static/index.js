define(["jupyter-js-widgets"], function(__WEBPACK_EXTERNAL_MODULE_3__) { return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;
/******/
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

	// Entry point for the notebook bundle containing custom model definitions.
	//
	// Setup notebook base URL
	//
	// Some static assets may be required by the custom widget javascript. The base
	// url for the notebook is not known at build time and is therefore computed
	// dynamically.
	__webpack_require__.p = document.querySelector('body').getAttribute('data-base-url') + 'nbextensions/ipywe/';
	
	// Export widget models and views, and the npm package version number.
	module.exports = __webpack_require__(1);
	
	// Export widget models and views, and the npm package version number.
	module.exports['version'] = __webpack_require__(8).version;


/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

	// Export widget models and views, and the npm package version number.
	module.exports = {};
	
	var loadedModules = [
	    __webpack_require__(2),
	    __webpack_require__(12),
	    __webpack_require__(10),
	    __webpack_require__(11),
	    __webpack_require__(13),
	    __webpack_require__(14),
	];
	
	for (var i in loadedModules) {
	    if (loadedModules.hasOwnProperty(i)) {
		var loadedModule = loadedModules[i];
		for (var target_name in loadedModule) {
		    if (loadedModule.hasOwnProperty(target_name)) {
			module.exports[target_name] = loadedModule[target_name];
		    }
		}
	    }
	}


/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;// var devel=1;
	var devel=0;
	var widgets = __webpack_require__(3);
	var _ = __webpack_require__(4);
	
	// Custom Model. Custom widgets models must at least provide default values
	// for model attributes, including
	//
	//  - `_view_name`
	//  - `_view_module`
	//  - `_view_module_version`
	//
	//  - `_model_name`
	//  - `_model_module`
	//  - `_model_module_version`
	//
	//  when different from the base class.
	
	// When serialiazing the entire widget state for embedding, only values that
	// differ from the defaults will be specified.
	var HelloModel = widgets.DOMWidgetModel.extend({
	    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
		_model_name : 'HelloModel',
		_view_name : 'HelloView',
		_model_module : 'ipywe',
		_view_module : 'ipywe',
		_model_module_version : '0.1.0',
		_view_module_version : '0.1.0',
		value : 'Hello World'
	    })
	});
	
	
	// Custom View. Renders the widget model.
	var HelloView = widgets.DOMWidgetView.extend({
	    render: function() {
		this.value_changed();
		this.model.on('change:value', this.value_changed, this);
	    },
	
	    value_changed: function() {
		this.el.textContent = this.model.get('value');
	    }
	});
	
	
	if (devel) {
	    __webpack_require__(6).undef("example");
	    !(__WEBPACK_AMD_DEFINE_ARRAY__ = [__webpack_require__(3)], __WEBPACK_AMD_DEFINE_RESULT__ = function(widgets) {
		return {
		    HelloView: HelloView,
		    HelloModel: HelloModel
		}
	    }.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
	} else {
	    module.exports = {
		HelloModel : HelloModel,
		HelloView : HelloView
	    };
	}
	
	


/***/ }),
/* 3 */
/***/ (function(module, exports) {

	module.exports = __WEBPACK_EXTERNAL_MODULE_3__;

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;/* WEBPACK VAR INJECTION */(function(global, module) {//     Underscore.js 1.9.1
	//     http://underscorejs.org
	//     (c) 2009-2018 Jeremy Ashkenas, DocumentCloud and Investigative Reporters & Editors
	//     Underscore may be freely distributed under the MIT license.
	
	(function() {
	
	  // Baseline setup
	  // --------------
	
	  // Establish the root object, `window` (`self`) in the browser, `global`
	  // on the server, or `this` in some virtual machines. We use `self`
	  // instead of `window` for `WebWorker` support.
	  var root = typeof self == 'object' && self.self === self && self ||
	            typeof global == 'object' && global.global === global && global ||
	            this ||
	            {};
	
	  // Save the previous value of the `_` variable.
	  var previousUnderscore = root._;
	
	  // Save bytes in the minified (but not gzipped) version:
	  var ArrayProto = Array.prototype, ObjProto = Object.prototype;
	  var SymbolProto = typeof Symbol !== 'undefined' ? Symbol.prototype : null;
	
	  // Create quick reference variables for speed access to core prototypes.
	  var push = ArrayProto.push,
	      slice = ArrayProto.slice,
	      toString = ObjProto.toString,
	      hasOwnProperty = ObjProto.hasOwnProperty;
	
	  // All **ECMAScript 5** native function implementations that we hope to use
	  // are declared here.
	  var nativeIsArray = Array.isArray,
	      nativeKeys = Object.keys,
	      nativeCreate = Object.create;
	
	  // Naked function reference for surrogate-prototype-swapping.
	  var Ctor = function(){};
	
	  // Create a safe reference to the Underscore object for use below.
	  var _ = function(obj) {
	    if (obj instanceof _) return obj;
	    if (!(this instanceof _)) return new _(obj);
	    this._wrapped = obj;
	  };
	
	  // Export the Underscore object for **Node.js**, with
	  // backwards-compatibility for their old module API. If we're in
	  // the browser, add `_` as a global object.
	  // (`nodeType` is checked to ensure that `module`
	  // and `exports` are not HTML elements.)
	  if (typeof exports != 'undefined' && !exports.nodeType) {
	    if (typeof module != 'undefined' && !module.nodeType && module.exports) {
	      exports = module.exports = _;
	    }
	    exports._ = _;
	  } else {
	    root._ = _;
	  }
	
	  // Current version.
	  _.VERSION = '1.9.1';
	
	  // Internal function that returns an efficient (for current engines) version
	  // of the passed-in callback, to be repeatedly applied in other Underscore
	  // functions.
	  var optimizeCb = function(func, context, argCount) {
	    if (context === void 0) return func;
	    switch (argCount == null ? 3 : argCount) {
	      case 1: return function(value) {
	        return func.call(context, value);
	      };
	      // The 2-argument case is omitted because we’re not using it.
	      case 3: return function(value, index, collection) {
	        return func.call(context, value, index, collection);
	      };
	      case 4: return function(accumulator, value, index, collection) {
	        return func.call(context, accumulator, value, index, collection);
	      };
	    }
	    return function() {
	      return func.apply(context, arguments);
	    };
	  };
	
	  var builtinIteratee;
	
	  // An internal function to generate callbacks that can be applied to each
	  // element in a collection, returning the desired result — either `identity`,
	  // an arbitrary callback, a property matcher, or a property accessor.
	  var cb = function(value, context, argCount) {
	    if (_.iteratee !== builtinIteratee) return _.iteratee(value, context);
	    if (value == null) return _.identity;
	    if (_.isFunction(value)) return optimizeCb(value, context, argCount);
	    if (_.isObject(value) && !_.isArray(value)) return _.matcher(value);
	    return _.property(value);
	  };
	
	  // External wrapper for our callback generator. Users may customize
	  // `_.iteratee` if they want additional predicate/iteratee shorthand styles.
	  // This abstraction hides the internal-only argCount argument.
	  _.iteratee = builtinIteratee = function(value, context) {
	    return cb(value, context, Infinity);
	  };
	
	  // Some functions take a variable number of arguments, or a few expected
	  // arguments at the beginning and then a variable number of values to operate
	  // on. This helper accumulates all remaining arguments past the function’s
	  // argument length (or an explicit `startIndex`), into an array that becomes
	  // the last argument. Similar to ES6’s "rest parameter".
	  var restArguments = function(func, startIndex) {
	    startIndex = startIndex == null ? func.length - 1 : +startIndex;
	    return function() {
	      var length = Math.max(arguments.length - startIndex, 0),
	          rest = Array(length),
	          index = 0;
	      for (; index < length; index++) {
	        rest[index] = arguments[index + startIndex];
	      }
	      switch (startIndex) {
	        case 0: return func.call(this, rest);
	        case 1: return func.call(this, arguments[0], rest);
	        case 2: return func.call(this, arguments[0], arguments[1], rest);
	      }
	      var args = Array(startIndex + 1);
	      for (index = 0; index < startIndex; index++) {
	        args[index] = arguments[index];
	      }
	      args[startIndex] = rest;
	      return func.apply(this, args);
	    };
	  };
	
	  // An internal function for creating a new object that inherits from another.
	  var baseCreate = function(prototype) {
	    if (!_.isObject(prototype)) return {};
	    if (nativeCreate) return nativeCreate(prototype);
	    Ctor.prototype = prototype;
	    var result = new Ctor;
	    Ctor.prototype = null;
	    return result;
	  };
	
	  var shallowProperty = function(key) {
	    return function(obj) {
	      return obj == null ? void 0 : obj[key];
	    };
	  };
	
	  var has = function(obj, path) {
	    return obj != null && hasOwnProperty.call(obj, path);
	  }
	
	  var deepGet = function(obj, path) {
	    var length = path.length;
	    for (var i = 0; i < length; i++) {
	      if (obj == null) return void 0;
	      obj = obj[path[i]];
	    }
	    return length ? obj : void 0;
	  };
	
	  // Helper for collection methods to determine whether a collection
	  // should be iterated as an array or as an object.
	  // Related: http://people.mozilla.org/~jorendorff/es6-draft.html#sec-tolength
	  // Avoids a very nasty iOS 8 JIT bug on ARM-64. #2094
	  var MAX_ARRAY_INDEX = Math.pow(2, 53) - 1;
	  var getLength = shallowProperty('length');
	  var isArrayLike = function(collection) {
	    var length = getLength(collection);
	    return typeof length == 'number' && length >= 0 && length <= MAX_ARRAY_INDEX;
	  };
	
	  // Collection Functions
	  // --------------------
	
	  // The cornerstone, an `each` implementation, aka `forEach`.
	  // Handles raw objects in addition to array-likes. Treats all
	  // sparse array-likes as if they were dense.
	  _.each = _.forEach = function(obj, iteratee, context) {
	    iteratee = optimizeCb(iteratee, context);
	    var i, length;
	    if (isArrayLike(obj)) {
	      for (i = 0, length = obj.length; i < length; i++) {
	        iteratee(obj[i], i, obj);
	      }
	    } else {
	      var keys = _.keys(obj);
	      for (i = 0, length = keys.length; i < length; i++) {
	        iteratee(obj[keys[i]], keys[i], obj);
	      }
	    }
	    return obj;
	  };
	
	  // Return the results of applying the iteratee to each element.
	  _.map = _.collect = function(obj, iteratee, context) {
	    iteratee = cb(iteratee, context);
	    var keys = !isArrayLike(obj) && _.keys(obj),
	        length = (keys || obj).length,
	        results = Array(length);
	    for (var index = 0; index < length; index++) {
	      var currentKey = keys ? keys[index] : index;
	      results[index] = iteratee(obj[currentKey], currentKey, obj);
	    }
	    return results;
	  };
	
	  // Create a reducing function iterating left or right.
	  var createReduce = function(dir) {
	    // Wrap code that reassigns argument variables in a separate function than
	    // the one that accesses `arguments.length` to avoid a perf hit. (#1991)
	    var reducer = function(obj, iteratee, memo, initial) {
	      var keys = !isArrayLike(obj) && _.keys(obj),
	          length = (keys || obj).length,
	          index = dir > 0 ? 0 : length - 1;
	      if (!initial) {
	        memo = obj[keys ? keys[index] : index];
	        index += dir;
	      }
	      for (; index >= 0 && index < length; index += dir) {
	        var currentKey = keys ? keys[index] : index;
	        memo = iteratee(memo, obj[currentKey], currentKey, obj);
	      }
	      return memo;
	    };
	
	    return function(obj, iteratee, memo, context) {
	      var initial = arguments.length >= 3;
	      return reducer(obj, optimizeCb(iteratee, context, 4), memo, initial);
	    };
	  };
	
	  // **Reduce** builds up a single result from a list of values, aka `inject`,
	  // or `foldl`.
	  _.reduce = _.foldl = _.inject = createReduce(1);
	
	  // The right-associative version of reduce, also known as `foldr`.
	  _.reduceRight = _.foldr = createReduce(-1);
	
	  // Return the first value which passes a truth test. Aliased as `detect`.
	  _.find = _.detect = function(obj, predicate, context) {
	    var keyFinder = isArrayLike(obj) ? _.findIndex : _.findKey;
	    var key = keyFinder(obj, predicate, context);
	    if (key !== void 0 && key !== -1) return obj[key];
	  };
	
	  // Return all the elements that pass a truth test.
	  // Aliased as `select`.
	  _.filter = _.select = function(obj, predicate, context) {
	    var results = [];
	    predicate = cb(predicate, context);
	    _.each(obj, function(value, index, list) {
	      if (predicate(value, index, list)) results.push(value);
	    });
	    return results;
	  };
	
	  // Return all the elements for which a truth test fails.
	  _.reject = function(obj, predicate, context) {
	    return _.filter(obj, _.negate(cb(predicate)), context);
	  };
	
	  // Determine whether all of the elements match a truth test.
	  // Aliased as `all`.
	  _.every = _.all = function(obj, predicate, context) {
	    predicate = cb(predicate, context);
	    var keys = !isArrayLike(obj) && _.keys(obj),
	        length = (keys || obj).length;
	    for (var index = 0; index < length; index++) {
	      var currentKey = keys ? keys[index] : index;
	      if (!predicate(obj[currentKey], currentKey, obj)) return false;
	    }
	    return true;
	  };
	
	  // Determine if at least one element in the object matches a truth test.
	  // Aliased as `any`.
	  _.some = _.any = function(obj, predicate, context) {
	    predicate = cb(predicate, context);
	    var keys = !isArrayLike(obj) && _.keys(obj),
	        length = (keys || obj).length;
	    for (var index = 0; index < length; index++) {
	      var currentKey = keys ? keys[index] : index;
	      if (predicate(obj[currentKey], currentKey, obj)) return true;
	    }
	    return false;
	  };
	
	  // Determine if the array or object contains a given item (using `===`).
	  // Aliased as `includes` and `include`.
	  _.contains = _.includes = _.include = function(obj, item, fromIndex, guard) {
	    if (!isArrayLike(obj)) obj = _.values(obj);
	    if (typeof fromIndex != 'number' || guard) fromIndex = 0;
	    return _.indexOf(obj, item, fromIndex) >= 0;
	  };
	
	  // Invoke a method (with arguments) on every item in a collection.
	  _.invoke = restArguments(function(obj, path, args) {
	    var contextPath, func;
	    if (_.isFunction(path)) {
	      func = path;
	    } else if (_.isArray(path)) {
	      contextPath = path.slice(0, -1);
	      path = path[path.length - 1];
	    }
	    return _.map(obj, function(context) {
	      var method = func;
	      if (!method) {
	        if (contextPath && contextPath.length) {
	          context = deepGet(context, contextPath);
	        }
	        if (context == null) return void 0;
	        method = context[path];
	      }
	      return method == null ? method : method.apply(context, args);
	    });
	  });
	
	  // Convenience version of a common use case of `map`: fetching a property.
	  _.pluck = function(obj, key) {
	    return _.map(obj, _.property(key));
	  };
	
	  // Convenience version of a common use case of `filter`: selecting only objects
	  // containing specific `key:value` pairs.
	  _.where = function(obj, attrs) {
	    return _.filter(obj, _.matcher(attrs));
	  };
	
	  // Convenience version of a common use case of `find`: getting the first object
	  // containing specific `key:value` pairs.
	  _.findWhere = function(obj, attrs) {
	    return _.find(obj, _.matcher(attrs));
	  };
	
	  // Return the maximum element (or element-based computation).
	  _.max = function(obj, iteratee, context) {
	    var result = -Infinity, lastComputed = -Infinity,
	        value, computed;
	    if (iteratee == null || typeof iteratee == 'number' && typeof obj[0] != 'object' && obj != null) {
	      obj = isArrayLike(obj) ? obj : _.values(obj);
	      for (var i = 0, length = obj.length; i < length; i++) {
	        value = obj[i];
	        if (value != null && value > result) {
	          result = value;
	        }
	      }
	    } else {
	      iteratee = cb(iteratee, context);
	      _.each(obj, function(v, index, list) {
	        computed = iteratee(v, index, list);
	        if (computed > lastComputed || computed === -Infinity && result === -Infinity) {
	          result = v;
	          lastComputed = computed;
	        }
	      });
	    }
	    return result;
	  };
	
	  // Return the minimum element (or element-based computation).
	  _.min = function(obj, iteratee, context) {
	    var result = Infinity, lastComputed = Infinity,
	        value, computed;
	    if (iteratee == null || typeof iteratee == 'number' && typeof obj[0] != 'object' && obj != null) {
	      obj = isArrayLike(obj) ? obj : _.values(obj);
	      for (var i = 0, length = obj.length; i < length; i++) {
	        value = obj[i];
	        if (value != null && value < result) {
	          result = value;
	        }
	      }
	    } else {
	      iteratee = cb(iteratee, context);
	      _.each(obj, function(v, index, list) {
	        computed = iteratee(v, index, list);
	        if (computed < lastComputed || computed === Infinity && result === Infinity) {
	          result = v;
	          lastComputed = computed;
	        }
	      });
	    }
	    return result;
	  };
	
	  // Shuffle a collection.
	  _.shuffle = function(obj) {
	    return _.sample(obj, Infinity);
	  };
	
	  // Sample **n** random values from a collection using the modern version of the
	  // [Fisher-Yates shuffle](http://en.wikipedia.org/wiki/Fisher–Yates_shuffle).
	  // If **n** is not specified, returns a single random element.
	  // The internal `guard` argument allows it to work with `map`.
	  _.sample = function(obj, n, guard) {
	    if (n == null || guard) {
	      if (!isArrayLike(obj)) obj = _.values(obj);
	      return obj[_.random(obj.length - 1)];
	    }
	    var sample = isArrayLike(obj) ? _.clone(obj) : _.values(obj);
	    var length = getLength(sample);
	    n = Math.max(Math.min(n, length), 0);
	    var last = length - 1;
	    for (var index = 0; index < n; index++) {
	      var rand = _.random(index, last);
	      var temp = sample[index];
	      sample[index] = sample[rand];
	      sample[rand] = temp;
	    }
	    return sample.slice(0, n);
	  };
	
	  // Sort the object's values by a criterion produced by an iteratee.
	  _.sortBy = function(obj, iteratee, context) {
	    var index = 0;
	    iteratee = cb(iteratee, context);
	    return _.pluck(_.map(obj, function(value, key, list) {
	      return {
	        value: value,
	        index: index++,
	        criteria: iteratee(value, key, list)
	      };
	    }).sort(function(left, right) {
	      var a = left.criteria;
	      var b = right.criteria;
	      if (a !== b) {
	        if (a > b || a === void 0) return 1;
	        if (a < b || b === void 0) return -1;
	      }
	      return left.index - right.index;
	    }), 'value');
	  };
	
	  // An internal function used for aggregate "group by" operations.
	  var group = function(behavior, partition) {
	    return function(obj, iteratee, context) {
	      var result = partition ? [[], []] : {};
	      iteratee = cb(iteratee, context);
	      _.each(obj, function(value, index) {
	        var key = iteratee(value, index, obj);
	        behavior(result, value, key);
	      });
	      return result;
	    };
	  };
	
	  // Groups the object's values by a criterion. Pass either a string attribute
	  // to group by, or a function that returns the criterion.
	  _.groupBy = group(function(result, value, key) {
	    if (has(result, key)) result[key].push(value); else result[key] = [value];
	  });
	
	  // Indexes the object's values by a criterion, similar to `groupBy`, but for
	  // when you know that your index values will be unique.
	  _.indexBy = group(function(result, value, key) {
	    result[key] = value;
	  });
	
	  // Counts instances of an object that group by a certain criterion. Pass
	  // either a string attribute to count by, or a function that returns the
	  // criterion.
	  _.countBy = group(function(result, value, key) {
	    if (has(result, key)) result[key]++; else result[key] = 1;
	  });
	
	  var reStrSymbol = /[^\ud800-\udfff]|[\ud800-\udbff][\udc00-\udfff]|[\ud800-\udfff]/g;
	  // Safely create a real, live array from anything iterable.
	  _.toArray = function(obj) {
	    if (!obj) return [];
	    if (_.isArray(obj)) return slice.call(obj);
	    if (_.isString(obj)) {
	      // Keep surrogate pair characters together
	      return obj.match(reStrSymbol);
	    }
	    if (isArrayLike(obj)) return _.map(obj, _.identity);
	    return _.values(obj);
	  };
	
	  // Return the number of elements in an object.
	  _.size = function(obj) {
	    if (obj == null) return 0;
	    return isArrayLike(obj) ? obj.length : _.keys(obj).length;
	  };
	
	  // Split a collection into two arrays: one whose elements all satisfy the given
	  // predicate, and one whose elements all do not satisfy the predicate.
	  _.partition = group(function(result, value, pass) {
	    result[pass ? 0 : 1].push(value);
	  }, true);
	
	  // Array Functions
	  // ---------------
	
	  // Get the first element of an array. Passing **n** will return the first N
	  // values in the array. Aliased as `head` and `take`. The **guard** check
	  // allows it to work with `_.map`.
	  _.first = _.head = _.take = function(array, n, guard) {
	    if (array == null || array.length < 1) return n == null ? void 0 : [];
	    if (n == null || guard) return array[0];
	    return _.initial(array, array.length - n);
	  };
	
	  // Returns everything but the last entry of the array. Especially useful on
	  // the arguments object. Passing **n** will return all the values in
	  // the array, excluding the last N.
	  _.initial = function(array, n, guard) {
	    return slice.call(array, 0, Math.max(0, array.length - (n == null || guard ? 1 : n)));
	  };
	
	  // Get the last element of an array. Passing **n** will return the last N
	  // values in the array.
	  _.last = function(array, n, guard) {
	    if (array == null || array.length < 1) return n == null ? void 0 : [];
	    if (n == null || guard) return array[array.length - 1];
	    return _.rest(array, Math.max(0, array.length - n));
	  };
	
	  // Returns everything but the first entry of the array. Aliased as `tail` and `drop`.
	  // Especially useful on the arguments object. Passing an **n** will return
	  // the rest N values in the array.
	  _.rest = _.tail = _.drop = function(array, n, guard) {
	    return slice.call(array, n == null || guard ? 1 : n);
	  };
	
	  // Trim out all falsy values from an array.
	  _.compact = function(array) {
	    return _.filter(array, Boolean);
	  };
	
	  // Internal implementation of a recursive `flatten` function.
	  var flatten = function(input, shallow, strict, output) {
	    output = output || [];
	    var idx = output.length;
	    for (var i = 0, length = getLength(input); i < length; i++) {
	      var value = input[i];
	      if (isArrayLike(value) && (_.isArray(value) || _.isArguments(value))) {
	        // Flatten current level of array or arguments object.
	        if (shallow) {
	          var j = 0, len = value.length;
	          while (j < len) output[idx++] = value[j++];
	        } else {
	          flatten(value, shallow, strict, output);
	          idx = output.length;
	        }
	      } else if (!strict) {
	        output[idx++] = value;
	      }
	    }
	    return output;
	  };
	
	  // Flatten out an array, either recursively (by default), or just one level.
	  _.flatten = function(array, shallow) {
	    return flatten(array, shallow, false);
	  };
	
	  // Return a version of the array that does not contain the specified value(s).
	  _.without = restArguments(function(array, otherArrays) {
	    return _.difference(array, otherArrays);
	  });
	
	  // Produce a duplicate-free version of the array. If the array has already
	  // been sorted, you have the option of using a faster algorithm.
	  // The faster algorithm will not work with an iteratee if the iteratee
	  // is not a one-to-one function, so providing an iteratee will disable
	  // the faster algorithm.
	  // Aliased as `unique`.
	  _.uniq = _.unique = function(array, isSorted, iteratee, context) {
	    if (!_.isBoolean(isSorted)) {
	      context = iteratee;
	      iteratee = isSorted;
	      isSorted = false;
	    }
	    if (iteratee != null) iteratee = cb(iteratee, context);
	    var result = [];
	    var seen = [];
	    for (var i = 0, length = getLength(array); i < length; i++) {
	      var value = array[i],
	          computed = iteratee ? iteratee(value, i, array) : value;
	      if (isSorted && !iteratee) {
	        if (!i || seen !== computed) result.push(value);
	        seen = computed;
	      } else if (iteratee) {
	        if (!_.contains(seen, computed)) {
	          seen.push(computed);
	          result.push(value);
	        }
	      } else if (!_.contains(result, value)) {
	        result.push(value);
	      }
	    }
	    return result;
	  };
	
	  // Produce an array that contains the union: each distinct element from all of
	  // the passed-in arrays.
	  _.union = restArguments(function(arrays) {
	    return _.uniq(flatten(arrays, true, true));
	  });
	
	  // Produce an array that contains every item shared between all the
	  // passed-in arrays.
	  _.intersection = function(array) {
	    var result = [];
	    var argsLength = arguments.length;
	    for (var i = 0, length = getLength(array); i < length; i++) {
	      var item = array[i];
	      if (_.contains(result, item)) continue;
	      var j;
	      for (j = 1; j < argsLength; j++) {
	        if (!_.contains(arguments[j], item)) break;
	      }
	      if (j === argsLength) result.push(item);
	    }
	    return result;
	  };
	
	  // Take the difference between one array and a number of other arrays.
	  // Only the elements present in just the first array will remain.
	  _.difference = restArguments(function(array, rest) {
	    rest = flatten(rest, true, true);
	    return _.filter(array, function(value){
	      return !_.contains(rest, value);
	    });
	  });
	
	  // Complement of _.zip. Unzip accepts an array of arrays and groups
	  // each array's elements on shared indices.
	  _.unzip = function(array) {
	    var length = array && _.max(array, getLength).length || 0;
	    var result = Array(length);
	
	    for (var index = 0; index < length; index++) {
	      result[index] = _.pluck(array, index);
	    }
	    return result;
	  };
	
	  // Zip together multiple lists into a single array -- elements that share
	  // an index go together.
	  _.zip = restArguments(_.unzip);
	
	  // Converts lists into objects. Pass either a single array of `[key, value]`
	  // pairs, or two parallel arrays of the same length -- one of keys, and one of
	  // the corresponding values. Passing by pairs is the reverse of _.pairs.
	  _.object = function(list, values) {
	    var result = {};
	    for (var i = 0, length = getLength(list); i < length; i++) {
	      if (values) {
	        result[list[i]] = values[i];
	      } else {
	        result[list[i][0]] = list[i][1];
	      }
	    }
	    return result;
	  };
	
	  // Generator function to create the findIndex and findLastIndex functions.
	  var createPredicateIndexFinder = function(dir) {
	    return function(array, predicate, context) {
	      predicate = cb(predicate, context);
	      var length = getLength(array);
	      var index = dir > 0 ? 0 : length - 1;
	      for (; index >= 0 && index < length; index += dir) {
	        if (predicate(array[index], index, array)) return index;
	      }
	      return -1;
	    };
	  };
	
	  // Returns the first index on an array-like that passes a predicate test.
	  _.findIndex = createPredicateIndexFinder(1);
	  _.findLastIndex = createPredicateIndexFinder(-1);
	
	  // Use a comparator function to figure out the smallest index at which
	  // an object should be inserted so as to maintain order. Uses binary search.
	  _.sortedIndex = function(array, obj, iteratee, context) {
	    iteratee = cb(iteratee, context, 1);
	    var value = iteratee(obj);
	    var low = 0, high = getLength(array);
	    while (low < high) {
	      var mid = Math.floor((low + high) / 2);
	      if (iteratee(array[mid]) < value) low = mid + 1; else high = mid;
	    }
	    return low;
	  };
	
	  // Generator function to create the indexOf and lastIndexOf functions.
	  var createIndexFinder = function(dir, predicateFind, sortedIndex) {
	    return function(array, item, idx) {
	      var i = 0, length = getLength(array);
	      if (typeof idx == 'number') {
	        if (dir > 0) {
	          i = idx >= 0 ? idx : Math.max(idx + length, i);
	        } else {
	          length = idx >= 0 ? Math.min(idx + 1, length) : idx + length + 1;
	        }
	      } else if (sortedIndex && idx && length) {
	        idx = sortedIndex(array, item);
	        return array[idx] === item ? idx : -1;
	      }
	      if (item !== item) {
	        idx = predicateFind(slice.call(array, i, length), _.isNaN);
	        return idx >= 0 ? idx + i : -1;
	      }
	      for (idx = dir > 0 ? i : length - 1; idx >= 0 && idx < length; idx += dir) {
	        if (array[idx] === item) return idx;
	      }
	      return -1;
	    };
	  };
	
	  // Return the position of the first occurrence of an item in an array,
	  // or -1 if the item is not included in the array.
	  // If the array is large and already in sort order, pass `true`
	  // for **isSorted** to use binary search.
	  _.indexOf = createIndexFinder(1, _.findIndex, _.sortedIndex);
	  _.lastIndexOf = createIndexFinder(-1, _.findLastIndex);
	
	  // Generate an integer Array containing an arithmetic progression. A port of
	  // the native Python `range()` function. See
	  // [the Python documentation](http://docs.python.org/library/functions.html#range).
	  _.range = function(start, stop, step) {
	    if (stop == null) {
	      stop = start || 0;
	      start = 0;
	    }
	    if (!step) {
	      step = stop < start ? -1 : 1;
	    }
	
	    var length = Math.max(Math.ceil((stop - start) / step), 0);
	    var range = Array(length);
	
	    for (var idx = 0; idx < length; idx++, start += step) {
	      range[idx] = start;
	    }
	
	    return range;
	  };
	
	  // Chunk a single array into multiple arrays, each containing `count` or fewer
	  // items.
	  _.chunk = function(array, count) {
	    if (count == null || count < 1) return [];
	    var result = [];
	    var i = 0, length = array.length;
	    while (i < length) {
	      result.push(slice.call(array, i, i += count));
	    }
	    return result;
	  };
	
	  // Function (ahem) Functions
	  // ------------------
	
	  // Determines whether to execute a function as a constructor
	  // or a normal function with the provided arguments.
	  var executeBound = function(sourceFunc, boundFunc, context, callingContext, args) {
	    if (!(callingContext instanceof boundFunc)) return sourceFunc.apply(context, args);
	    var self = baseCreate(sourceFunc.prototype);
	    var result = sourceFunc.apply(self, args);
	    if (_.isObject(result)) return result;
	    return self;
	  };
	
	  // Create a function bound to a given object (assigning `this`, and arguments,
	  // optionally). Delegates to **ECMAScript 5**'s native `Function.bind` if
	  // available.
	  _.bind = restArguments(function(func, context, args) {
	    if (!_.isFunction(func)) throw new TypeError('Bind must be called on a function');
	    var bound = restArguments(function(callArgs) {
	      return executeBound(func, bound, context, this, args.concat(callArgs));
	    });
	    return bound;
	  });
	
	  // Partially apply a function by creating a version that has had some of its
	  // arguments pre-filled, without changing its dynamic `this` context. _ acts
	  // as a placeholder by default, allowing any combination of arguments to be
	  // pre-filled. Set `_.partial.placeholder` for a custom placeholder argument.
	  _.partial = restArguments(function(func, boundArgs) {
	    var placeholder = _.partial.placeholder;
	    var bound = function() {
	      var position = 0, length = boundArgs.length;
	      var args = Array(length);
	      for (var i = 0; i < length; i++) {
	        args[i] = boundArgs[i] === placeholder ? arguments[position++] : boundArgs[i];
	      }
	      while (position < arguments.length) args.push(arguments[position++]);
	      return executeBound(func, bound, this, this, args);
	    };
	    return bound;
	  });
	
	  _.partial.placeholder = _;
	
	  // Bind a number of an object's methods to that object. Remaining arguments
	  // are the method names to be bound. Useful for ensuring that all callbacks
	  // defined on an object belong to it.
	  _.bindAll = restArguments(function(obj, keys) {
	    keys = flatten(keys, false, false);
	    var index = keys.length;
	    if (index < 1) throw new Error('bindAll must be passed function names');
	    while (index--) {
	      var key = keys[index];
	      obj[key] = _.bind(obj[key], obj);
	    }
	  });
	
	  // Memoize an expensive function by storing its results.
	  _.memoize = function(func, hasher) {
	    var memoize = function(key) {
	      var cache = memoize.cache;
	      var address = '' + (hasher ? hasher.apply(this, arguments) : key);
	      if (!has(cache, address)) cache[address] = func.apply(this, arguments);
	      return cache[address];
	    };
	    memoize.cache = {};
	    return memoize;
	  };
	
	  // Delays a function for the given number of milliseconds, and then calls
	  // it with the arguments supplied.
	  _.delay = restArguments(function(func, wait, args) {
	    return setTimeout(function() {
	      return func.apply(null, args);
	    }, wait);
	  });
	
	  // Defers a function, scheduling it to run after the current call stack has
	  // cleared.
	  _.defer = _.partial(_.delay, _, 1);
	
	  // Returns a function, that, when invoked, will only be triggered at most once
	  // during a given window of time. Normally, the throttled function will run
	  // as much as it can, without ever going more than once per `wait` duration;
	  // but if you'd like to disable the execution on the leading edge, pass
	  // `{leading: false}`. To disable execution on the trailing edge, ditto.
	  _.throttle = function(func, wait, options) {
	    var timeout, context, args, result;
	    var previous = 0;
	    if (!options) options = {};
	
	    var later = function() {
	      previous = options.leading === false ? 0 : _.now();
	      timeout = null;
	      result = func.apply(context, args);
	      if (!timeout) context = args = null;
	    };
	
	    var throttled = function() {
	      var now = _.now();
	      if (!previous && options.leading === false) previous = now;
	      var remaining = wait - (now - previous);
	      context = this;
	      args = arguments;
	      if (remaining <= 0 || remaining > wait) {
	        if (timeout) {
	          clearTimeout(timeout);
	          timeout = null;
	        }
	        previous = now;
	        result = func.apply(context, args);
	        if (!timeout) context = args = null;
	      } else if (!timeout && options.trailing !== false) {
	        timeout = setTimeout(later, remaining);
	      }
	      return result;
	    };
	
	    throttled.cancel = function() {
	      clearTimeout(timeout);
	      previous = 0;
	      timeout = context = args = null;
	    };
	
	    return throttled;
	  };
	
	  // Returns a function, that, as long as it continues to be invoked, will not
	  // be triggered. The function will be called after it stops being called for
	  // N milliseconds. If `immediate` is passed, trigger the function on the
	  // leading edge, instead of the trailing.
	  _.debounce = function(func, wait, immediate) {
	    var timeout, result;
	
	    var later = function(context, args) {
	      timeout = null;
	      if (args) result = func.apply(context, args);
	    };
	
	    var debounced = restArguments(function(args) {
	      if (timeout) clearTimeout(timeout);
	      if (immediate) {
	        var callNow = !timeout;
	        timeout = setTimeout(later, wait);
	        if (callNow) result = func.apply(this, args);
	      } else {
	        timeout = _.delay(later, wait, this, args);
	      }
	
	      return result;
	    });
	
	    debounced.cancel = function() {
	      clearTimeout(timeout);
	      timeout = null;
	    };
	
	    return debounced;
	  };
	
	  // Returns the first function passed as an argument to the second,
	  // allowing you to adjust arguments, run code before and after, and
	  // conditionally execute the original function.
	  _.wrap = function(func, wrapper) {
	    return _.partial(wrapper, func);
	  };
	
	  // Returns a negated version of the passed-in predicate.
	  _.negate = function(predicate) {
	    return function() {
	      return !predicate.apply(this, arguments);
	    };
	  };
	
	  // Returns a function that is the composition of a list of functions, each
	  // consuming the return value of the function that follows.
	  _.compose = function() {
	    var args = arguments;
	    var start = args.length - 1;
	    return function() {
	      var i = start;
	      var result = args[start].apply(this, arguments);
	      while (i--) result = args[i].call(this, result);
	      return result;
	    };
	  };
	
	  // Returns a function that will only be executed on and after the Nth call.
	  _.after = function(times, func) {
	    return function() {
	      if (--times < 1) {
	        return func.apply(this, arguments);
	      }
	    };
	  };
	
	  // Returns a function that will only be executed up to (but not including) the Nth call.
	  _.before = function(times, func) {
	    var memo;
	    return function() {
	      if (--times > 0) {
	        memo = func.apply(this, arguments);
	      }
	      if (times <= 1) func = null;
	      return memo;
	    };
	  };
	
	  // Returns a function that will be executed at most one time, no matter how
	  // often you call it. Useful for lazy initialization.
	  _.once = _.partial(_.before, 2);
	
	  _.restArguments = restArguments;
	
	  // Object Functions
	  // ----------------
	
	  // Keys in IE < 9 that won't be iterated by `for key in ...` and thus missed.
	  var hasEnumBug = !{toString: null}.propertyIsEnumerable('toString');
	  var nonEnumerableProps = ['valueOf', 'isPrototypeOf', 'toString',
	    'propertyIsEnumerable', 'hasOwnProperty', 'toLocaleString'];
	
	  var collectNonEnumProps = function(obj, keys) {
	    var nonEnumIdx = nonEnumerableProps.length;
	    var constructor = obj.constructor;
	    var proto = _.isFunction(constructor) && constructor.prototype || ObjProto;
	
	    // Constructor is a special case.
	    var prop = 'constructor';
	    if (has(obj, prop) && !_.contains(keys, prop)) keys.push(prop);
	
	    while (nonEnumIdx--) {
	      prop = nonEnumerableProps[nonEnumIdx];
	      if (prop in obj && obj[prop] !== proto[prop] && !_.contains(keys, prop)) {
	        keys.push(prop);
	      }
	    }
	  };
	
	  // Retrieve the names of an object's own properties.
	  // Delegates to **ECMAScript 5**'s native `Object.keys`.
	  _.keys = function(obj) {
	    if (!_.isObject(obj)) return [];
	    if (nativeKeys) return nativeKeys(obj);
	    var keys = [];
	    for (var key in obj) if (has(obj, key)) keys.push(key);
	    // Ahem, IE < 9.
	    if (hasEnumBug) collectNonEnumProps(obj, keys);
	    return keys;
	  };
	
	  // Retrieve all the property names of an object.
	  _.allKeys = function(obj) {
	    if (!_.isObject(obj)) return [];
	    var keys = [];
	    for (var key in obj) keys.push(key);
	    // Ahem, IE < 9.
	    if (hasEnumBug) collectNonEnumProps(obj, keys);
	    return keys;
	  };
	
	  // Retrieve the values of an object's properties.
	  _.values = function(obj) {
	    var keys = _.keys(obj);
	    var length = keys.length;
	    var values = Array(length);
	    for (var i = 0; i < length; i++) {
	      values[i] = obj[keys[i]];
	    }
	    return values;
	  };
	
	  // Returns the results of applying the iteratee to each element of the object.
	  // In contrast to _.map it returns an object.
	  _.mapObject = function(obj, iteratee, context) {
	    iteratee = cb(iteratee, context);
	    var keys = _.keys(obj),
	        length = keys.length,
	        results = {};
	    for (var index = 0; index < length; index++) {
	      var currentKey = keys[index];
	      results[currentKey] = iteratee(obj[currentKey], currentKey, obj);
	    }
	    return results;
	  };
	
	  // Convert an object into a list of `[key, value]` pairs.
	  // The opposite of _.object.
	  _.pairs = function(obj) {
	    var keys = _.keys(obj);
	    var length = keys.length;
	    var pairs = Array(length);
	    for (var i = 0; i < length; i++) {
	      pairs[i] = [keys[i], obj[keys[i]]];
	    }
	    return pairs;
	  };
	
	  // Invert the keys and values of an object. The values must be serializable.
	  _.invert = function(obj) {
	    var result = {};
	    var keys = _.keys(obj);
	    for (var i = 0, length = keys.length; i < length; i++) {
	      result[obj[keys[i]]] = keys[i];
	    }
	    return result;
	  };
	
	  // Return a sorted list of the function names available on the object.
	  // Aliased as `methods`.
	  _.functions = _.methods = function(obj) {
	    var names = [];
	    for (var key in obj) {
	      if (_.isFunction(obj[key])) names.push(key);
	    }
	    return names.sort();
	  };
	
	  // An internal function for creating assigner functions.
	  var createAssigner = function(keysFunc, defaults) {
	    return function(obj) {
	      var length = arguments.length;
	      if (defaults) obj = Object(obj);
	      if (length < 2 || obj == null) return obj;
	      for (var index = 1; index < length; index++) {
	        var source = arguments[index],
	            keys = keysFunc(source),
	            l = keys.length;
	        for (var i = 0; i < l; i++) {
	          var key = keys[i];
	          if (!defaults || obj[key] === void 0) obj[key] = source[key];
	        }
	      }
	      return obj;
	    };
	  };
	
	  // Extend a given object with all the properties in passed-in object(s).
	  _.extend = createAssigner(_.allKeys);
	
	  // Assigns a given object with all the own properties in the passed-in object(s).
	  // (https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)
	  _.extendOwn = _.assign = createAssigner(_.keys);
	
	  // Returns the first key on an object that passes a predicate test.
	  _.findKey = function(obj, predicate, context) {
	    predicate = cb(predicate, context);
	    var keys = _.keys(obj), key;
	    for (var i = 0, length = keys.length; i < length; i++) {
	      key = keys[i];
	      if (predicate(obj[key], key, obj)) return key;
	    }
	  };
	
	  // Internal pick helper function to determine if `obj` has key `key`.
	  var keyInObj = function(value, key, obj) {
	    return key in obj;
	  };
	
	  // Return a copy of the object only containing the whitelisted properties.
	  _.pick = restArguments(function(obj, keys) {
	    var result = {}, iteratee = keys[0];
	    if (obj == null) return result;
	    if (_.isFunction(iteratee)) {
	      if (keys.length > 1) iteratee = optimizeCb(iteratee, keys[1]);
	      keys = _.allKeys(obj);
	    } else {
	      iteratee = keyInObj;
	      keys = flatten(keys, false, false);
	      obj = Object(obj);
	    }
	    for (var i = 0, length = keys.length; i < length; i++) {
	      var key = keys[i];
	      var value = obj[key];
	      if (iteratee(value, key, obj)) result[key] = value;
	    }
	    return result;
	  });
	
	  // Return a copy of the object without the blacklisted properties.
	  _.omit = restArguments(function(obj, keys) {
	    var iteratee = keys[0], context;
	    if (_.isFunction(iteratee)) {
	      iteratee = _.negate(iteratee);
	      if (keys.length > 1) context = keys[1];
	    } else {
	      keys = _.map(flatten(keys, false, false), String);
	      iteratee = function(value, key) {
	        return !_.contains(keys, key);
	      };
	    }
	    return _.pick(obj, iteratee, context);
	  });
	
	  // Fill in a given object with default properties.
	  _.defaults = createAssigner(_.allKeys, true);
	
	  // Creates an object that inherits from the given prototype object.
	  // If additional properties are provided then they will be added to the
	  // created object.
	  _.create = function(prototype, props) {
	    var result = baseCreate(prototype);
	    if (props) _.extendOwn(result, props);
	    return result;
	  };
	
	  // Create a (shallow-cloned) duplicate of an object.
	  _.clone = function(obj) {
	    if (!_.isObject(obj)) return obj;
	    return _.isArray(obj) ? obj.slice() : _.extend({}, obj);
	  };
	
	  // Invokes interceptor with the obj, and then returns obj.
	  // The primary purpose of this method is to "tap into" a method chain, in
	  // order to perform operations on intermediate results within the chain.
	  _.tap = function(obj, interceptor) {
	    interceptor(obj);
	    return obj;
	  };
	
	  // Returns whether an object has a given set of `key:value` pairs.
	  _.isMatch = function(object, attrs) {
	    var keys = _.keys(attrs), length = keys.length;
	    if (object == null) return !length;
	    var obj = Object(object);
	    for (var i = 0; i < length; i++) {
	      var key = keys[i];
	      if (attrs[key] !== obj[key] || !(key in obj)) return false;
	    }
	    return true;
	  };
	
	
	  // Internal recursive comparison function for `isEqual`.
	  var eq, deepEq;
	  eq = function(a, b, aStack, bStack) {
	    // Identical objects are equal. `0 === -0`, but they aren't identical.
	    // See the [Harmony `egal` proposal](http://wiki.ecmascript.org/doku.php?id=harmony:egal).
	    if (a === b) return a !== 0 || 1 / a === 1 / b;
	    // `null` or `undefined` only equal to itself (strict comparison).
	    if (a == null || b == null) return false;
	    // `NaN`s are equivalent, but non-reflexive.
	    if (a !== a) return b !== b;
	    // Exhaust primitive checks
	    var type = typeof a;
	    if (type !== 'function' && type !== 'object' && typeof b != 'object') return false;
	    return deepEq(a, b, aStack, bStack);
	  };
	
	  // Internal recursive comparison function for `isEqual`.
	  deepEq = function(a, b, aStack, bStack) {
	    // Unwrap any wrapped objects.
	    if (a instanceof _) a = a._wrapped;
	    if (b instanceof _) b = b._wrapped;
	    // Compare `[[Class]]` names.
	    var className = toString.call(a);
	    if (className !== toString.call(b)) return false;
	    switch (className) {
	      // Strings, numbers, regular expressions, dates, and booleans are compared by value.
	      case '[object RegExp]':
	      // RegExps are coerced to strings for comparison (Note: '' + /a/i === '/a/i')
	      case '[object String]':
	        // Primitives and their corresponding object wrappers are equivalent; thus, `"5"` is
	        // equivalent to `new String("5")`.
	        return '' + a === '' + b;
	      case '[object Number]':
	        // `NaN`s are equivalent, but non-reflexive.
	        // Object(NaN) is equivalent to NaN.
	        if (+a !== +a) return +b !== +b;
	        // An `egal` comparison is performed for other numeric values.
	        return +a === 0 ? 1 / +a === 1 / b : +a === +b;
	      case '[object Date]':
	      case '[object Boolean]':
	        // Coerce dates and booleans to numeric primitive values. Dates are compared by their
	        // millisecond representations. Note that invalid dates with millisecond representations
	        // of `NaN` are not equivalent.
	        return +a === +b;
	      case '[object Symbol]':
	        return SymbolProto.valueOf.call(a) === SymbolProto.valueOf.call(b);
	    }
	
	    var areArrays = className === '[object Array]';
	    if (!areArrays) {
	      if (typeof a != 'object' || typeof b != 'object') return false;
	
	      // Objects with different constructors are not equivalent, but `Object`s or `Array`s
	      // from different frames are.
	      var aCtor = a.constructor, bCtor = b.constructor;
	      if (aCtor !== bCtor && !(_.isFunction(aCtor) && aCtor instanceof aCtor &&
	                               _.isFunction(bCtor) && bCtor instanceof bCtor)
	                          && ('constructor' in a && 'constructor' in b)) {
	        return false;
	      }
	    }
	    // Assume equality for cyclic structures. The algorithm for detecting cyclic
	    // structures is adapted from ES 5.1 section 15.12.3, abstract operation `JO`.
	
	    // Initializing stack of traversed objects.
	    // It's done here since we only need them for objects and arrays comparison.
	    aStack = aStack || [];
	    bStack = bStack || [];
	    var length = aStack.length;
	    while (length--) {
	      // Linear search. Performance is inversely proportional to the number of
	      // unique nested structures.
	      if (aStack[length] === a) return bStack[length] === b;
	    }
	
	    // Add the first object to the stack of traversed objects.
	    aStack.push(a);
	    bStack.push(b);
	
	    // Recursively compare objects and arrays.
	    if (areArrays) {
	      // Compare array lengths to determine if a deep comparison is necessary.
	      length = a.length;
	      if (length !== b.length) return false;
	      // Deep compare the contents, ignoring non-numeric properties.
	      while (length--) {
	        if (!eq(a[length], b[length], aStack, bStack)) return false;
	      }
	    } else {
	      // Deep compare objects.
	      var keys = _.keys(a), key;
	      length = keys.length;
	      // Ensure that both objects contain the same number of properties before comparing deep equality.
	      if (_.keys(b).length !== length) return false;
	      while (length--) {
	        // Deep compare each member
	        key = keys[length];
	        if (!(has(b, key) && eq(a[key], b[key], aStack, bStack))) return false;
	      }
	    }
	    // Remove the first object from the stack of traversed objects.
	    aStack.pop();
	    bStack.pop();
	    return true;
	  };
	
	  // Perform a deep comparison to check if two objects are equal.
	  _.isEqual = function(a, b) {
	    return eq(a, b);
	  };
	
	  // Is a given array, string, or object empty?
	  // An "empty" object has no enumerable own-properties.
	  _.isEmpty = function(obj) {
	    if (obj == null) return true;
	    if (isArrayLike(obj) && (_.isArray(obj) || _.isString(obj) || _.isArguments(obj))) return obj.length === 0;
	    return _.keys(obj).length === 0;
	  };
	
	  // Is a given value a DOM element?
	  _.isElement = function(obj) {
	    return !!(obj && obj.nodeType === 1);
	  };
	
	  // Is a given value an array?
	  // Delegates to ECMA5's native Array.isArray
	  _.isArray = nativeIsArray || function(obj) {
	    return toString.call(obj) === '[object Array]';
	  };
	
	  // Is a given variable an object?
	  _.isObject = function(obj) {
	    var type = typeof obj;
	    return type === 'function' || type === 'object' && !!obj;
	  };
	
	  // Add some isType methods: isArguments, isFunction, isString, isNumber, isDate, isRegExp, isError, isMap, isWeakMap, isSet, isWeakSet.
	  _.each(['Arguments', 'Function', 'String', 'Number', 'Date', 'RegExp', 'Error', 'Symbol', 'Map', 'WeakMap', 'Set', 'WeakSet'], function(name) {
	    _['is' + name] = function(obj) {
	      return toString.call(obj) === '[object ' + name + ']';
	    };
	  });
	
	  // Define a fallback version of the method in browsers (ahem, IE < 9), where
	  // there isn't any inspectable "Arguments" type.
	  if (!_.isArguments(arguments)) {
	    _.isArguments = function(obj) {
	      return has(obj, 'callee');
	    };
	  }
	
	  // Optimize `isFunction` if appropriate. Work around some typeof bugs in old v8,
	  // IE 11 (#1621), Safari 8 (#1929), and PhantomJS (#2236).
	  var nodelist = root.document && root.document.childNodes;
	  if (typeof /./ != 'function' && typeof Int8Array != 'object' && typeof nodelist != 'function') {
	    _.isFunction = function(obj) {
	      return typeof obj == 'function' || false;
	    };
	  }
	
	  // Is a given object a finite number?
	  _.isFinite = function(obj) {
	    return !_.isSymbol(obj) && isFinite(obj) && !isNaN(parseFloat(obj));
	  };
	
	  // Is the given value `NaN`?
	  _.isNaN = function(obj) {
	    return _.isNumber(obj) && isNaN(obj);
	  };
	
	  // Is a given value a boolean?
	  _.isBoolean = function(obj) {
	    return obj === true || obj === false || toString.call(obj) === '[object Boolean]';
	  };
	
	  // Is a given value equal to null?
	  _.isNull = function(obj) {
	    return obj === null;
	  };
	
	  // Is a given variable undefined?
	  _.isUndefined = function(obj) {
	    return obj === void 0;
	  };
	
	  // Shortcut function for checking if an object has a given property directly
	  // on itself (in other words, not on a prototype).
	  _.has = function(obj, path) {
	    if (!_.isArray(path)) {
	      return has(obj, path);
	    }
	    var length = path.length;
	    for (var i = 0; i < length; i++) {
	      var key = path[i];
	      if (obj == null || !hasOwnProperty.call(obj, key)) {
	        return false;
	      }
	      obj = obj[key];
	    }
	    return !!length;
	  };
	
	  // Utility Functions
	  // -----------------
	
	  // Run Underscore.js in *noConflict* mode, returning the `_` variable to its
	  // previous owner. Returns a reference to the Underscore object.
	  _.noConflict = function() {
	    root._ = previousUnderscore;
	    return this;
	  };
	
	  // Keep the identity function around for default iteratees.
	  _.identity = function(value) {
	    return value;
	  };
	
	  // Predicate-generating functions. Often useful outside of Underscore.
	  _.constant = function(value) {
	    return function() {
	      return value;
	    };
	  };
	
	  _.noop = function(){};
	
	  // Creates a function that, when passed an object, will traverse that object’s
	  // properties down the given `path`, specified as an array of keys or indexes.
	  _.property = function(path) {
	    if (!_.isArray(path)) {
	      return shallowProperty(path);
	    }
	    return function(obj) {
	      return deepGet(obj, path);
	    };
	  };
	
	  // Generates a function for a given object that returns a given property.
	  _.propertyOf = function(obj) {
	    if (obj == null) {
	      return function(){};
	    }
	    return function(path) {
	      return !_.isArray(path) ? obj[path] : deepGet(obj, path);
	    };
	  };
	
	  // Returns a predicate for checking whether an object has a given set of
	  // `key:value` pairs.
	  _.matcher = _.matches = function(attrs) {
	    attrs = _.extendOwn({}, attrs);
	    return function(obj) {
	      return _.isMatch(obj, attrs);
	    };
	  };
	
	  // Run a function **n** times.
	  _.times = function(n, iteratee, context) {
	    var accum = Array(Math.max(0, n));
	    iteratee = optimizeCb(iteratee, context, 1);
	    for (var i = 0; i < n; i++) accum[i] = iteratee(i);
	    return accum;
	  };
	
	  // Return a random integer between min and max (inclusive).
	  _.random = function(min, max) {
	    if (max == null) {
	      max = min;
	      min = 0;
	    }
	    return min + Math.floor(Math.random() * (max - min + 1));
	  };
	
	  // A (possibly faster) way to get the current timestamp as an integer.
	  _.now = Date.now || function() {
	    return new Date().getTime();
	  };
	
	  // List of HTML entities for escaping.
	  var escapeMap = {
	    '&': '&amp;',
	    '<': '&lt;',
	    '>': '&gt;',
	    '"': '&quot;',
	    "'": '&#x27;',
	    '`': '&#x60;'
	  };
	  var unescapeMap = _.invert(escapeMap);
	
	  // Functions for escaping and unescaping strings to/from HTML interpolation.
	  var createEscaper = function(map) {
	    var escaper = function(match) {
	      return map[match];
	    };
	    // Regexes for identifying a key that needs to be escaped.
	    var source = '(?:' + _.keys(map).join('|') + ')';
	    var testRegexp = RegExp(source);
	    var replaceRegexp = RegExp(source, 'g');
	    return function(string) {
	      string = string == null ? '' : '' + string;
	      return testRegexp.test(string) ? string.replace(replaceRegexp, escaper) : string;
	    };
	  };
	  _.escape = createEscaper(escapeMap);
	  _.unescape = createEscaper(unescapeMap);
	
	  // Traverses the children of `obj` along `path`. If a child is a function, it
	  // is invoked with its parent as context. Returns the value of the final
	  // child, or `fallback` if any child is undefined.
	  _.result = function(obj, path, fallback) {
	    if (!_.isArray(path)) path = [path];
	    var length = path.length;
	    if (!length) {
	      return _.isFunction(fallback) ? fallback.call(obj) : fallback;
	    }
	    for (var i = 0; i < length; i++) {
	      var prop = obj == null ? void 0 : obj[path[i]];
	      if (prop === void 0) {
	        prop = fallback;
	        i = length; // Ensure we don't continue iterating.
	      }
	      obj = _.isFunction(prop) ? prop.call(obj) : prop;
	    }
	    return obj;
	  };
	
	  // Generate a unique integer id (unique within the entire client session).
	  // Useful for temporary DOM ids.
	  var idCounter = 0;
	  _.uniqueId = function(prefix) {
	    var id = ++idCounter + '';
	    return prefix ? prefix + id : id;
	  };
	
	  // By default, Underscore uses ERB-style template delimiters, change the
	  // following template settings to use alternative delimiters.
	  _.templateSettings = {
	    evaluate: /<%([\s\S]+?)%>/g,
	    interpolate: /<%=([\s\S]+?)%>/g,
	    escape: /<%-([\s\S]+?)%>/g
	  };
	
	  // When customizing `templateSettings`, if you don't want to define an
	  // interpolation, evaluation or escaping regex, we need one that is
	  // guaranteed not to match.
	  var noMatch = /(.)^/;
	
	  // Certain characters need to be escaped so that they can be put into a
	  // string literal.
	  var escapes = {
	    "'": "'",
	    '\\': '\\',
	    '\r': 'r',
	    '\n': 'n',
	    '\u2028': 'u2028',
	    '\u2029': 'u2029'
	  };
	
	  var escapeRegExp = /\\|'|\r|\n|\u2028|\u2029/g;
	
	  var escapeChar = function(match) {
	    return '\\' + escapes[match];
	  };
	
	  // JavaScript micro-templating, similar to John Resig's implementation.
	  // Underscore templating handles arbitrary delimiters, preserves whitespace,
	  // and correctly escapes quotes within interpolated code.
	  // NB: `oldSettings` only exists for backwards compatibility.
	  _.template = function(text, settings, oldSettings) {
	    if (!settings && oldSettings) settings = oldSettings;
	    settings = _.defaults({}, settings, _.templateSettings);
	
	    // Combine delimiters into one regular expression via alternation.
	    var matcher = RegExp([
	      (settings.escape || noMatch).source,
	      (settings.interpolate || noMatch).source,
	      (settings.evaluate || noMatch).source
	    ].join('|') + '|$', 'g');
	
	    // Compile the template source, escaping string literals appropriately.
	    var index = 0;
	    var source = "__p+='";
	    text.replace(matcher, function(match, escape, interpolate, evaluate, offset) {
	      source += text.slice(index, offset).replace(escapeRegExp, escapeChar);
	      index = offset + match.length;
	
	      if (escape) {
	        source += "'+\n((__t=(" + escape + "))==null?'':_.escape(__t))+\n'";
	      } else if (interpolate) {
	        source += "'+\n((__t=(" + interpolate + "))==null?'':__t)+\n'";
	      } else if (evaluate) {
	        source += "';\n" + evaluate + "\n__p+='";
	      }
	
	      // Adobe VMs need the match returned to produce the correct offset.
	      return match;
	    });
	    source += "';\n";
	
	    // If a variable is not specified, place data values in local scope.
	    if (!settings.variable) source = 'with(obj||{}){\n' + source + '}\n';
	
	    source = "var __t,__p='',__j=Array.prototype.join," +
	      "print=function(){__p+=__j.call(arguments,'');};\n" +
	      source + 'return __p;\n';
	
	    var render;
	    try {
	      render = new Function(settings.variable || 'obj', '_', source);
	    } catch (e) {
	      e.source = source;
	      throw e;
	    }
	
	    var template = function(data) {
	      return render.call(this, data, _);
	    };
	
	    // Provide the compiled source as a convenience for precompilation.
	    var argument = settings.variable || 'obj';
	    template.source = 'function(' + argument + '){\n' + source + '}';
	
	    return template;
	  };
	
	  // Add a "chain" function. Start chaining a wrapped Underscore object.
	  _.chain = function(obj) {
	    var instance = _(obj);
	    instance._chain = true;
	    return instance;
	  };
	
	  // OOP
	  // ---------------
	  // If Underscore is called as a function, it returns a wrapped object that
	  // can be used OO-style. This wrapper holds altered versions of all the
	  // underscore functions. Wrapped objects may be chained.
	
	  // Helper function to continue chaining intermediate results.
	  var chainResult = function(instance, obj) {
	    return instance._chain ? _(obj).chain() : obj;
	  };
	
	  // Add your own custom functions to the Underscore object.
	  _.mixin = function(obj) {
	    _.each(_.functions(obj), function(name) {
	      var func = _[name] = obj[name];
	      _.prototype[name] = function() {
	        var args = [this._wrapped];
	        push.apply(args, arguments);
	        return chainResult(this, func.apply(_, args));
	      };
	    });
	    return _;
	  };
	
	  // Add all of the Underscore functions to the wrapper object.
	  _.mixin(_);
	
	  // Add all mutator Array functions to the wrapper.
	  _.each(['pop', 'push', 'reverse', 'shift', 'sort', 'splice', 'unshift'], function(name) {
	    var method = ArrayProto[name];
	    _.prototype[name] = function() {
	      var obj = this._wrapped;
	      method.apply(obj, arguments);
	      if ((name === 'shift' || name === 'splice') && obj.length === 0) delete obj[0];
	      return chainResult(this, obj);
	    };
	  });
	
	  // Add all accessor Array functions to the wrapper.
	  _.each(['concat', 'join', 'slice'], function(name) {
	    var method = ArrayProto[name];
	    _.prototype[name] = function() {
	      return chainResult(this, method.apply(this._wrapped, arguments));
	    };
	  });
	
	  // Extracts the result from a wrapped and chained object.
	  _.prototype.value = function() {
	    return this._wrapped;
	  };
	
	  // Provide unwrapping proxy for some methods used in engine operations
	  // such as arithmetic and JSON stringification.
	  _.prototype.valueOf = _.prototype.toJSON = _.prototype.value;
	
	  _.prototype.toString = function() {
	    return String(this._wrapped);
	  };
	
	  // AMD registration happens at the end for compatibility with AMD loaders
	  // that may not enforce next-turn semantics on modules. Even though general
	  // practice for AMD registration is to be anonymous, underscore registers
	  // as a named module because, like jQuery, it is a base library that is
	  // popular enough to be bundled in a third party lib, but not be part of
	  // an AMD load request. Those cases could generate an error when an
	  // anonymous define() is called outside of a loader request.
	  if (true) {
	    !(__WEBPACK_AMD_DEFINE_ARRAY__ = [], __WEBPACK_AMD_DEFINE_RESULT__ = function() {
	      return _;
	    }.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
	  }
	}());
	
	/* WEBPACK VAR INJECTION */}.call(exports, (function() { return this; }()), __webpack_require__(5)(module)))

/***/ }),
/* 5 */
/***/ (function(module, exports) {

	module.exports = function(module) {
		if(!module.webpackPolyfill) {
			module.deprecate = function() {};
			module.paths = [];
			// module.parent = undefined by default
			module.children = [];
			module.webpackPolyfill = 1;
		}
		return module;
	}


/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

	var map = {
		"./embed": 7,
		"./embed.js": 7,
		"./example": 2,
		"./example.js": 2,
		"./extension": 9,
		"./extension.js": 9,
		"./imageslider": 10,
		"./imageslider.js": 10,
		"./imgdatagraph": 11,
		"./imgdatagraph.js": 11,
		"./imgdisplay": 12,
		"./imgdisplay.js": 12,
		"./loadwidgets": 1,
		"./loadwidgets.js": 1,
		"./tomvizjs": 13,
		"./tomvizjs.js": 13,
		"./vtkjs": 14,
		"./vtkjs.js": 14
	};
	function webpackContext(req) {
		return __webpack_require__(webpackContextResolve(req));
	};
	function webpackContextResolve(req) {
		return map[req] || (function() { throw new Error("Cannot find module '" + req + "'.") }());
	};
	webpackContext.keys = function webpackContextKeys() {
		return Object.keys(map);
	};
	webpackContext.resolve = webpackContextResolve;
	module.exports = webpackContext;
	webpackContext.id = 6;


/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

	// Entry point for the unpkg bundle containing custom model definitions.
	//
	// It differs from the notebook bundle in that it does not need to define a
	// dynamic baseURL for the static assets and may load some css that would
	// already be loaded by the notebook otherwise.
	
	// add ligher styles here
	module.exports = __webpack_require__(1);
	// module.exports = require('./example.js');
	module.exports['version'] = __webpack_require__(8).version;


/***/ }),
/* 8 */
/***/ (function(module, exports) {

	module.exports = {"name":"ipywe","version":"0.1.3-alpha.1","description":"ipywidgets extensions","author":"ipywe team","main":"src/index.js","repository":{"type":"git","url":"https://github.com/neutrons/ipywe.git"},"keywords":["jupyter","widgets","ipython","ipywidgets"],"scripts":{"prepublish":"webpack","test":"echo \"Error: no test specified\" && exit 1"},"devDependencies":{"json-loader":"^0.5.4","webpack":"^1.12.14"},"dependencies":{"jupyter-js-widgets":"^2.1.4","underscore":"^1.8.3"}}

/***/ }),
/* 9 */
/***/ (function(module, exports) {

	// This file contains the javascript that is run when the notebook is loaded.
	// It contains some requirejs configuration and the `load_ipython_extension`
	// which is required for any notebook extension.
	
	// Configure requirejs
	if (window.require) {
	    window.require.config({
	        map: {
	            "*" : {
	                "ipywe": "nbextensions/ipywe/index",
	                "jupyter-js-widgets": "nbextensions/jupyter-js-widgets/extension"
	            }
	        }
	    });
	}
	
	// Export the required load_ipython_extention
	module.exports = {
	    load_ipython_extension: function() {}
	};


/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

	var widgets = __webpack_require__(3);
	var _ = __webpack_require__(4);
	var semver_range = "^" + __webpack_require__(8).version;
	
	var ImgSliderModel = widgets.DOMWidgetModel.extend({
	    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
	        _model_name : 'ImgSliderModel',
	        _view_name : 'ImgSliderView',
	        _model_module : 'ipywe',
	        _view_module : 'ipywe',
	        _model_module_version : semver_range,
	        _view_module_version : semver_range
	    })
	});
	
	
	var ImgSliderView = widgets.DOMWidgetView.extend({
		
	    //Overrides the default render method to allow for custom widget creation
	    
	    render: function() {
	
	        //Sets all the values needed for creating the sliders. wid is created to allow model values to be obtained in functions within this render function.
	        var wid = this;
	        var img_index_max = this.model.get("_N_images") - 1;
	        var vrange_min = this.model.get("_img_min");
	        var vrange_max = this.model.get("_img_max");
	        var vrange_step = (vrange_max - vrange_min)/100;
	        var vrange = [vrange_min, vrange_max];
	
	        /*Creates the flexbox that will store the widget and the two flexitems that it will contain. Also formats all of them.
	          img_vbox stores the image and the horizontal (Image Selector) slider.
	          data_vbox stores the html text element (displays the XY coordinates of the mouse and that position's value) and the vertical (Z range) slider.*/
	
	        var widget_area = $('<div class="flex-container">');
	        
	        widget_area.css("display", "-webkit-flex"); widget_area.css("display", "flex");
	        widget_area.css("justifyContent", "flex-start"); widget_area.width(1000); widget_area.height(this.model.get("height") * 1.3);
	        
	        var img_vbox = $('<div class="flex-item-img img-box">');
	
	        img_vbox.width(this.model.get("width") * 1.1); img_vbox.height(this.model.get("height") * 1.25); img_vbox.css("padding", "5px");
	
	        var data_vbox = $('<div class="flex-item-data data-box">');
	
	        data_vbox.width(1000 - this.model.get("width") * 1.1 - 25); data_vbox.height(this.model.get("height") * 1.25); data_vbox.css("padding", "5px");
	
	        //Adds the img_vbox and data_vbox to the overall flexbox.
	
	        widget_area.append(img_vbox);
	        widget_area.append(data_vbox);
	
	        //Adds the widget to the display area.
	        this.$el.append(widget_area);
	
	        //Add a container for the image and the selection box
	        var img_container = $('<div class="img-container">');
	        img_vbox.append(img_container);
	        img_container.css({
	            position: "relative",
	            width: this.model.get("width"),
	            height: this.model.get("height")
	            //padding: "10px"
	        });
	
	        //Creates the image stored in the initial value of _b64value and adds it to img_vbox.
	        var img = $('<img class="curr-img">');
	        var image_src = "data:image/" + this.model.get("_format") + ";base64," + this.model.get("_b64value")
	        img.attr("src", image_src);
	        
	        img.width(this.model.get("width")); img.height(this.model.get("height"));
	        img_container.append(img);
	
	        //Creates a read-only input field with no border to dynamically display the value of the horizontal slider.
	        var hslide_label = $('<input class="hslabel" type="text" readonly style="border:0">'); 
	        //Creates the horizontal slider using JQuery UI
	        var hslide_html = $('<div class="hslider">');
	        hslide_html.slider({
	            value: 0,
	            min: 0,
	            max: img_index_max,
	            /*When the handle slides, this function is called to update hslide_label 
	              and change _img_index on the backend (triggers the update_image_index function on the backend)*/
	            slide: function(event, ui) {
	                hslide_label.val( ui.value );
	                console.log("Executed!");
	                wid.model.set("_img_index", ui.value);
	                wid.touch();
	            }
	        });
	        
	        //Sets the label's initial value to the initial value of the slider and adds a left margin to the label
	        hslide_label.val(hslide_html.slider("value"));
	        hslide_label.width("15%");
	        //Makes the slider's handle a blue circle and adds a 10 pixel margin to the slider
	        var hslide_handle = hslide_html.find(".ui-slider-handle");
	        hslide_handle.css("borderRadius", "50%");
	        hslide_handle.css("background", "#0099e6");
	        hslide_html.width(this.model.get("width"));
	        hslide_html.css("marginLeft", "7px");
	        hslide_html.css("marginBottom", "5px");
	        hslide_html.css("marginTop", "20px");
	        //Adds hslide_html (the slider) and hslide_label (the label) to img_vbox
	        img_vbox.append(hslide_html);
	        img_vbox.append(hslide_label);
	
	        //Creates and adds a button after hslide_label for zooming into a single image
	        var zoom_button = $('<button class="zoom-button">');
	        zoom_button.button({
	            label: "Zoom",
	            disabled: false
	        });
	        zoom_button.css("margin", "10px");
	        img_vbox.append(zoom_button);
	        /*When zoom_button is clicked, the ROI is passed back to the python side.
	          This triggeres the zoom_image python function. The selection box is also removed.
	        */
	        zoom_button.click(function() {
		    ; //
		    var ROI = select.data("ROI");
		    console.log(ROI);
		    if (typeof ROI == 'undefined') return;
		    wid.model.set("_ROI", ROI);
		    wid.touch();
	            select.remove();
	            console.log("Zoomed");
	        });
	
	        //Creates and adds a button after zoomall_button for reseting all displayed images.
	        var reset_button = $('<button class="reset-button">')
	        reset_button.button({
	            label: "Reset",
	            disabled: false
	        });
	        reset_button.css("margin", "10px");
	        img_vbox.append(reset_button);
	        /*When reset_button is clicked, ROI is set to negative numbers.
	          This triggers the zoom_image python function. The selection box is also removed.
	        */
	        reset_button.click(function() {
		    wid.model.set("_ROI", [-1,-1,-1,-1]);
	            wid.touch();
	            select.remove();
	            console.log("Image reset");
	        });
	
	        //Creates the selection box's div.
	        var select = $('<div class="selection-box">');
	
	        //Prevents the displayed image from being dragged (done to prevent issues with the following code.
	        img.on("dragstart", false);
	
	        //Controls creating, changing, and displaying the selection box.
	        img_container.on("mousedown", function(event) {
	            console.log("Click 1");
	            var click_x = event.offsetX;
	            var click_y = event.offsetY;
	            
	            //Initializes the selection box and adds it to img_container
	            select.css({
	                "top": click_y,
	                "left": click_x,
	                "width": 0,
	                "height": 0,
	                "position": "absolute",
	                "pointerEvents": "none"
	            });
	
	            
	            select.appendTo(img_container);
	
	            img_container.on("mousemove", function(event) {
	                console.log("Mouse moving");
	                var move_x = event.offsetX;
	                var move_y = event.offsetY;
	                var width = Math.abs(move_x - click_x);
	                var height = Math.abs(move_y - click_y);
	                var new_x, new_y;
	
	                /*The logic that allows the creation of a selection box where the final
	                  mouse position is up and left from the initial position.
	                */
	                new_x = (move_x < click_x) ? (click_x - width) : click_x;
	                new_y = (move_y < click_y) ? (click_y - height) : click_y;
	
	                /*As the mouse moves, this statement dynamically resizes the selection
	                  box.
	                */
	                select.css({
	                    "width": width,
	                    "height": height,
	                    "top": new_y,
	                    "left": new_x,
	                    "background": "transparent",
	                    "border": "2px solid red"
	                });
	
	                //Sets the variables used to splice the image's data on the backend
			select.data("ROI", 
				    [parseInt(select.css("left"), 10), //_offXtop
				     parseInt(select.css("top"), 10),  //_offYtop
				     parseInt(select.css("left"), 10) + select.width(), // _offXbottom
				     parseInt(select.css("top"), 10) + select.height()  // _offYbottom
				     ]);
	            }).on("mouseup", function(event) {
	                //Turns the mousemove event off to stop resizing the selection box.
	                console.log("Click 2");
	                img_container.off("mousemove");
	            });
	        });
		    // wid.model.set("_offXbottom"
	        console.log(img_vbox);
	        console.log("done with img box");
	
	        //Creates the fields (divs and spans) for the current mouse position and that position's value and adds them to data_vbox.
	        var text_content = $('<div class="widget-html-content">');
	        var xy = $("<div>"); xy.text("X,Y: ");
	        var x_coord = $('<span class="img-offsetx">');
	        var y_coord = $('<span class="img-offsety">');
	        xy.append(x_coord); xy.append(", "); xy.append(y_coord);
	        var value = $("<div>"); value.text("Value: ");
	        var val = $('<span class="img-value">');
	        value.append(val);
	        var roi = $("<div>"); roi.text("ROI: ");
	        var corners = $('<span class="roi">');
	        roi.append(corners);
	        corners.css("whiteSpace", "pre");
	        text_content.append(xy); text_content.append(value); text_content.append(roi);
	        data_vbox.append(text_content);
	        console.log(data_vbox);
	        
	        //Creates the label for the vertical slider with a static value of "Z range" (done in the same way as the other label)
	        var vslide_label = $('<div class="vslabel" type="text" readonly style="border:0">');
	        vslide_label.text("Z range: ");
	        vslide_label.css("marginTop", "10px");
	        vslide_label.css("marginBottom", "10px");
	        var vslide_labeldata = $('<span class="vslabel_data">');
	        var vlabel_content = "Max Range: " + vrange + "\n              Current Range: " + vrange;
	        vslide_labeldata.text(vlabel_content);
	        vslide_labeldata.css("whiteSpace", "pre");
	        vslide_label.append(vslide_labeldata);
	        //Creates the vertical slider using JQuery UI
	        var vslide_html = $('<div class="vslider">');
	        vslide_html.slider({
	            range: true,
	            orientation: "vertical",
	            min: vrange_min,
	            max: vrange_max,
	            values: vrange,
	            step: vrange_step,
	            /*When either handle slides, this function updates this slider's label to reflect the new contrast range. It also sets _img_min and/or _img_max on the backend to the handles' values.
	              This triggers the update_image_div_data function on the backend.*/
	            slide: function(event, ui) {
	                vlabel_content = "Max Range: " + vrange + "\n              Current Range: " + ui.values;
	                wid.$el.find(".vslabel_data").text(vlabel_content);
	                wid.model.set("_img_min", ui.values[0]);
	                wid.model.set("_img_max", ui.values[1]);
	                wid.touch();
	            }
	        });
	
	        
	        //Explicitly sets the slider's background color to white. Also, changes the handles to blue circles
	        var vslide_bar = vslide_html.find(".ui-widget-header");
	        vslide_bar.css("background", "#ffffff");
	        vslide_bar.siblings().css("borderRadius", "50%");
	        vslide_bar.siblings().css("background", "#0099e6");
	        //Adds vslide_label and vslide_html to data_vbox. At this point, the widget can be successfully displayed.
	        if (this.model.get("height") >= 150) {
	            vslide_html.height(this.model.get("height") - 100);
	        }
	        else {
	            vslide_html.height(50);
	        }
	        data_vbox.append(vslide_label);
	        data_vbox.append(vslide_html);
	        console.log(data_vbox);
	        console.log("done with data box");
	
	        
	        /*This function sets _offsetX and _offsetY on the backend to the event-specific offset values whenever
	          the mouse moves over the image. It then calculates the data-based XY coordinates and displays them
	          in the x_coord and y_coord span fields.*/
	        img.mousemove(function(event){
	            wid.model.set("_offsetX", event.offsetX);
	            wid.model.set("_offsetY", event.offsetY);
	            wid.touch();
	
	            //console.log(wid.model.get("_extrarows"), wid.model.get("_extracols"));
	            var yrows_top, yrows_bottom, xcols_left, xcols_right, x_coordinate, y_coordinate;
	            x_coordinate = Math.floor(event.offsetX*1./(wid.model.get("width"))*(wid.model.get("_ncols_currimg")));
	            y_coordinate = Math.floor(event.offsetY*1./(wid.model.get("height"))*(wid.model.get("_nrows_currimg")));
	
	            //All of this logic is used to get the correct coordinates for images containing buffer rows/columns.
	            if (wid.model.get("_extrarows") == 0 && wid.model.get("_extracols") == 0) {
	                //console.log("No extra rows/cols");
	                yrows_top = 0;
	                yrows_bottom = Number.MAX_SAFE_INTEGER;
	                xcols_left = 0;
	                xcols_right = Number.MAX_SAFE_INTEGER;
	            }
	            else if (wid.model.get("_extrarows") != 0 && wid.model.get("_extracols") == 0) {
	                //console.log("Extra Rows");
	                if (wid.model.get("_extrarows") % 2 == 0) {
	                    yrows_top = parseInt(wid.model.get("_extrarows") / 2);
	                    yrows_bottom = parseInt(wid.model.get("_extrarows") / 2);
	                }
	                else {
	                    yrows_top = parseInt(wid.model.get("_extrarows") / 2 + 1);
	                    yrows_bottom = parseInt(wid.model.get("_extrarows") / 2);
	                }
	                xcols_left = 0;
	                xcols_right = Number.MAX_SAFE_INTEGER;
	            }
	            else if (wid.model.get("_extrarows") == 0 && wid.model.get("_extracols") != 0) {
	                //console.log("Extra Cols");
	                if (wid.model.get("_extracols") % 2 == 0) {
	                    xcols_left = parseInt(wid.model.get("_extracols") / 2);
	                    xcols_right = parseInt(wid.model.get("_extracols") / 2);
	                }
	                else {
	                    xcols_left = parseInt(wid.model.get("_extracols") / 2 + 1);
	                    xcols_right = parseInt(wid.model.get("_extracols") / 2);
	                }
	                yrows_top = 0;
	                yrows_bottom = Number.MAX_SAFE_INTEGER;
	            }
	            else {
	                //console.log("Extra Rows/Cols");
	                if (wid.model.get("_extrarows") % 2 == 0) {
	                    yrows_top = parseInt(wid.model.get("_extrarows") / 2);
	                    yrows_bottom = parseInt(wid.model.get("_extrarows") / 2);
	                }
	                else {
	                    yrows_top = parseInt(wid.model.get("_extrarows") / 2 + 1);
	                    yrows_bottom = parseInt(wid.model.get("_extrarows") / 2);
	                }
	                if (wid.model.get("_extracols") % 2 == 0) {
	                    xcols_left = parseInt(wid.model.get("_extracols") / 2);
	                    xcols_right = parseInt(wid.model.get("_extracols") / 2);
	                }
	                else {
	                    xcols_left = parseInt(wid.model.get("_extracols") / 2 + 1);
	                    xcols_right = parseInt(wid.model.get("_extracols") / 2);
	                }
	            }
	
	            /*If the mouse is in a buffer area, the text for the x_coord and y_coord HTML fields are set to empty strings.
	              Otherwise, these text elements are set to be a string containing the mouse position relative to the 
	              original, un-zoomed image.
	            */
	            if (y_coordinate < yrows_top || (y_coordinate > wid.model.get("_nrows_currimg") - yrows_bottom && yrows_bottom != Number.MAX_SAFE_INTEGER) || x_coordinate < xcols_left || (x_coordinate > wid.model.get("_ncols_currimg") - xcols_right && xcols_right != Number.MAX_SAFE_INTEGER)) {
	                x_coord.text("");
	                y_coord.text("");
	            }
	            else {
	                x_coord.text((x_coordinate - xcols_left) + wid.model.get("_xcoord_absolute"));
	                y_coord.text((y_coordinate - yrows_top) + wid.model.get("_ycoord_absolute"));
	            }
	        });
	
	        this.calc_roi();
	
	        //Triggers on_pixval_change and on_img_change when the backend values of _pix_val and _b64value change.
	        this.model.on("change:_pix_val", this.on_pixval_change, this);
	        this.model.on("change:_b64value", this.on_img_change, this);
	        this.model.on("change:_b64value", this.calc_roi, this);
	        this.model.on("change:_vslide_reset", this.reset_vslide, this);
	    },
	
	    /*If the text of the coordinate fields (x_coord and y_coord) contain empty strings, the value field will 
	      also be set to an empty string. Otherwise, if there is no custom error message, this field will be
	      set to the image's value at the mouse's position. If there is a custom error message, it will be
	      displayed in the value field.
	    */
	    on_pixval_change: function() {
	        //console.log("Executing on_pixval_change");
	        if (this.$el.find(".img-offsetx").text() == "" && this.$el.find(".img-offsety").text() == "") {
	            this.$el.find(".img-value").text("");
	        }
	        else {
	            if (this.model.get("_err") == "") {
	                this.$el.find(".img-value").text(this.model.get("_pix_val"));
	            }
	            else {
	                this.$el.find(".img-value").text(this.model.get("_err"));
	            }
	        }
	    },
	
	    /*When _b64value changes on the backend, this function creates a new source string for the image (based
	      on the new value of _b64value). This new source then replaces the old source of the image.*/
	    on_img_change: function() {
	        //console.log("Executing on_img_change");
	        var src = "data:image/" + this.model.get("_format") + ";base64," + this.model.get("_b64value");
	        this.$el.find(".curr-img").attr("src", src);
	    },
	
	    /*When _b64value changes on the backend, this function will calculate and display the coordinates of the left, right, top, and bottom borders of the currently displayed image. Note that these coordinates are based on the original, un-zoomed image.
	     */
	    calc_roi: function() {
	        /*var top = this.model.get("_ycoord_absolute");
	        var left = this.model.get("_xcoord_absolute");
	        var right = this.model.get("_xcoord_absolute") + this.model.get("_ncols_currimg") - this.model.get("_extracols");
	        var bottom = this.model.get("_ycoord_absolute") + this.model.get("_nrows_currimg") - this.model.get("_extrarows");*/
	        var corns = "Top = " + this.model.get("_ycoord_absolute") + "   Bottom = " + this.model.get("_ycoord_max_roi") + "\n         Left = " + this.model.get("_xcoord_absolute") + "   Right = " + this.model.get("_xcoord_max_roi");
	        console.log(corns);
	        this.$el.find(".roi").text(corns);
	    },
	
	    /*When the reset button is pressed, this function will reset the vertical slider's handle positions and values to what they were originally. It also resets the value of the vertical slider's label to its default.
	     */
	    reset_vslide: function() {
	        $(".vslider").slider("values", 0, this.model.get("_img_min"));
	        $(".vslider").slider("values", 1, this.model.get("_img_max"));
	        var vrange_str = this.model.get("_img_min") + "," + this.model.get("_img_max");
	        $(".vslabel_data").text("Max Range: " + vrange_str + "\n              Current Range: " + vrange_str);
	    }
	    
	});
	
	module.exports = {
	    ImgSliderView : ImgSliderView,
	    ImgSliderModel : ImgSliderModel
	};


/***/ }),
/* 11 */
/***/ (function(module, exports, __webpack_require__) {

	var widgets = __webpack_require__(3);
	var _ = __webpack_require__(4);
	var semver_range = "^" + __webpack_require__(8).version;
	
	var ImgDataGraphModel = widgets.DOMWidgetModel.extend({
	    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
	        _model_name : 'ImgDataGraphModel',
	        _view_name : 'ImgDataGraphView',
	        _model_module : 'ipywe',
	        _view_module : 'ipywe',
	        _model_module_version : semver_range,
	        _view_module_version : semver_range
	    })
	});
	
	var ImgDataGraphView = widgets.DOMWidgetView.extend({
	
	    //Overrides the default render method to allow for custom widget creation
	    render: function() {
	        //Wid is created to allow the model or DOM elements to be changed within enclosed functions.
	        var wid = this;
	
	        /*Creates the flexbox that will store the widget and the three flexitems that it will contain. This code also formats all of these items.
	        widget_area is the overall flexbox that stores the entire widget.
	        img_vbox is the flexitem that contains the image, canvas element, horizontal slider, horizontal slider label, and graph button.
	        bin_vbox is the flexitem that contains the vertical slider and its label.
	        graph_vbox is the flexitem that contains the graph created by the Python code.
	        */
	        var widget_area = $('<div class="flex-container">');
	            
	        widget_area.css("display", "-webkit-flex"); widget_area.css("display", "flex");
	        widget_area.css("justifyContent", "flex-start"); widget_area.width(1000); widget_area.height(this.model.get("height") * 1.3);
	            
	        var img_vbox = $('<div class="flex-item-img img-box">');
	
	        img_vbox.width(this.model.get("width") * 1.1); img_vbox.height(this.model.get("height") * 1.25); img_vbox.css("padding", "5px");
	
	        var bin_vbox = $('<div class="flex-item-bin bin-box">');
	        bin_vbox.width(150); bin_vbox.height(this.model.get("height") * 1.25); bin_vbox.css("padding", "5px");
	
	        var graph_vbox = $('<div class="flex-item-graph graph-box">');
	
	        graph_vbox.width(1000 - this.model.get("width") * 1.1 - 85); graph_vbox.height(this.model.get("height") * 1.25); graph_vbox.css("padding", "5px");
	
	        //Adds the flexitems to the flexbox.
	        widget_area.append(img_vbox);
	        widget_area.append(bin_vbox);
	        widget_area.append(graph_vbox);
	        //Adds the flexbox to the display area.
	        this.$el.append(widget_area);
	
	        //Creates, formats, and adds the container for the image and canvas element.
	        var img_container = $('<div class="img-container">');
	        img_vbox.append(img_container);
	        img_container.width(this.model.get("width")); img_container.height(this.model.get("height"));
	
	        //Creates and formats the initial image
	        var img = $('<img class="curr-img">');
	        var image_src = "data:image/" + this.model.get("_format") + ";base64," + this.model.get("_b64value")
	        img.attr("src", image_src);
	        img_container.append(img);
	        img.css("position", "absolute");
	        img.width(this.model.get("width")); img.height(this.model.get("height"));
	
	        //Creates the canvas element and stores the Rendering Context of the canvas in ctx for later use.
	        var canvas = $('<canvas class="img-canvas">');
	        canvas.prop({
	            width: this.model.get("width"),
	            height: this.model.get("height")
	        });
	        canvas.css("position", "absolute");
	        img_container.append(canvas);
	        var can = canvas[0];
	        var ctx = can.getContext('2d');
	        console.log(ctx);
	
	        //Creates a read-only label input field with no border to dynamically display the value of the horizontal slider.
	        var linewidth_label = $('<input class="lwidth-label" type="text" readonly style="border:0">');        
	
	        //Calculates the maximum line width allowed
	        var max_linewidth;
	        if (this.model.get("width") < this.model.get("height")) {
	            max_linewidth = this.model.get("width") / 4;
	        }
	        else {
	            max_linewidth = this.model.get("height") / 4;
	        }
	        //Creates the horizontal slider using jQuery UI
	        var width_slider = $('<div class="width-slider">');
	        width_slider.slider({
	            value: 1,
	            min: 1,
	            max: max_linewidth,
	            /*When the handle is moved, this function updates the horizontal slider label and changes _linepix_width to whatever the slider's value is.
	            */
	            slide: function(event, ui) {
	                linewidth_label.val("Line Width: " + ui.value + " px");
	                wid.model.set("_linepix_width", ui.value);
	                wid.touch();
	            }
	        });
	
	        //Sets the initial value of the horizontal slider label and formats the label.
	        linewidth_label.val("Line Width: " + width_slider.slider("value") + " px");
	        linewidth_label.width("40%");
	        //Formats the horizontal slider handle
	        var width_slider_handle = width_slider.find(".ui-slider-handle");
	        width_slider_handle.css("borderRadius", "50%");
	        width_slider_handle.css("background", "#0099e6");
	        //Formats the horizontal slider.
	        width_slider.width(this.model.get("width"));
	        width_slider.css({
	            "marginLeft": "7px",
	            "marginBottom": "5px",
	            "marginTop": "20px"
	        });
	            
	        //Adds the horizontal slider and its label to img_vbox
	        img_vbox.append(width_slider);
	        img_vbox.append(linewidth_label);
	
	        //Creates, formats, and adds the graph button
	        var graph_button = $('<button class="graph-button">');
	        graph_button.button({
	            label: "Graph",
	            disabled: false
	        });
	        graph_button.css("marginLeft", "10px");
	        img_vbox.append(graph_button);
	        /*When this button is clicked, the _graph_click variable is updated (triggers the graph_data() Python function).
	        */
	        graph_button.click(function() {
	            var graph_val = wid.model.get("_graph_click");
	            if (graph_val < Number.MAX_SAFE_INTEGER) {
	                graph_val++;
	            }
	            else {
	                graph_val = 0;
	            }
	            wid.model.set("_graph_click", graph_val);
	            wid.touch();
	        });
	
	        //Prevents the displayed image from deing dragged.
	        img.on("dragstart", false);
	            
	        //Controls creating, changing, and displaying the currently drawn line
	        canvas.on("mousedown", function(event) {
	            //Resets the canvas, and stores the coordinates of the mousedown event in _offsetX1 and _offsetY1
	            console.log("mousedown");
	            ctx.clearRect(0, 0, wid.model.get("width"), wid.model.get("height"));
	            var offx = event.offsetX;
	            var offy = event.offsetY;
	            wid.model.set("_offsetX1", offx);
	            wid.model.set("_offsetY1", offy);
	            wid.touch();
	            canvas.on("mousemove", function(event) {
	                /*Resets the canvas. If the ctrl key is not pressed, stores the coordinates of the mouse in _offsetX2 and _offsetY2. Otherwise, one of those variables will be set to the corresponding mouse coordinate, while the other one will be set so that it is the same as _offsetX1/_offsetY1.
	               */
	                console.log("mousemove");
	                ctx.clearRect(0, 0, wid.model.get("width"), wid.model.get("height"));
	                var currx = event.offsetX;
	                var curry = event.offsetY;
	                var slope = Math.abs((curry - offy) / (currx - offx))
	                if (event.ctrlKey) {
	                    if (slope <= 1) {
	                        curry = offy
	                    }
	                    else {
	                        currx = offx
	                    }
	                    }
	                wid.model.set("_offsetX2", currx);
	                wid.model.set("_offsetY2", curry);
	                wid.touch();
	                //Draws the line on the canvas
	                ctx.beginPath();
	                ctx.moveTo(offx, offy);
	                ctx.lineTo(currx, curry);
	                ctx.lineWidth = wid.model.get("_linepix_width") + 1;
	                ctx.strokeStyle = "#ff0000";
	                ctx.stroke();
	            }).on("mouseup", function(event) {
	                //Ends the mousemove event
	                console.log("mouseup");
	                canvas.off("mousemove");
	            });
	        });
	
	        //Creats the vertical slider label
	        var bin_slider_label = $('<input class="binslide-label" type="text" readonly style="border:0">');
	        //Creates the vertical slider using jQuery UI
	        var bin_slider = $('<div class="bin-slider">');
	        bin_slider.slider({
	            value: 1,
	            min: 1,
	            max: 100,
	            orientation: "vertical",
	        /*When the handle is moved, updates the vertical slider label, and sets the value of _num_bins.
	            */
	            slide: function(event, ui) {
	                wid.model.set("_num_bins", ui.value);
	                wid.touch();
	                bin_slider_label.val("Number of Bins: " + ui.value);
	            }
	        });
	
	        //Sets the initial value of the vertical slider label
	        bin_slider_label.val("Histogram Bins: 1");
	        //Formats the vertical slider
	        bin_slider.height(this.model.get("height") * 0.9);
	        bin_slider.css("marginTop", "5px");
	        //Formats the vertical slider's handle
	        var bin_slider_handle = bin_slider.find(".ui-slider-handle");
	        bin_slider_handle.css("borderRadius", "50%");
	        bin_slider_handle.css("background", "#0099e6");
	
	        //Adds the vertical slider and its handle to bin_vbox
	        bin_vbox.append(bin_slider_label);
	        bin_vbox.append(bin_slider);
	
	        //Creates, formats, and adds the graph. Note that the initial graph is simply a clear box.
	        var graph_img = $('<img class="graph-img">');
	        var graph_src = "data:image/" + this.model.get("_format") + ";base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==";
	        graph_img.attr("src", graph_src);
	        graph_vbox.append(graph_img);
	        graph_img.css("position", "absolute");
	        if (graph_vbox.width() <= graph_img.width()) {
	            graph_img.width(graph_vbox.width() - 50);
	        }
	
	        //Triggers the functions below when the corresponding variable values change
	        this.model.on("change:_b64value", this.on_img_change, this);
	        this.model.on("change:_graphb64", this.on_graph_change, this);
	        this.model.on("change:_linepix_width", this.on_linewidth_change, this);
	    },
	
	    /*When _b64value changes, this function creates a new source string for the image and replaces the old one with the new one.
	    */
	    on_img_change: function() {
	        var src = "data:image/" + this.model.get("_format") + ";base64," + this.model.get("_b64value");
	        this.$el.find(".curr-img").attr("src", src);
	    },
	
	    /*When _graphb64 changes, this function creates a new source string for the graph and replaces the old one with the new one.
	    */
	    on_graph_change: function() {
	        var src = "data:image/" + this.model.get("_format") + ";base64," + this.model.get("_graphb64");
	        this.$el.find(".graph-img").attr("src", src);
	    },
	
	    /*When _linepix_width changes, this function creates a new line with the same endpoints as the currently displayed line, but with a width equal to the new value. 
	    */
	    on_linewidth_change: function() {
	        var canvas = this.$el.find(".img-canvas")[0];
	        var ctx = canvas.getContext('2d');
	        ctx.clearRect(0, 0, this.model.get("width"), this.model.get("height"));
	        ctx.beginPath();
	        ctx.moveTo(this.model.get("_offsetX1"), this.model.get("_offsetY1"));
	        ctx.lineTo(this.model.get("_offsetX2"), this.model.get("_offsetY2"));
	        ctx.lineWidth = this.model.get("_linepix_width") + 1;
	        ctx.strokeStyle = "#ff0000";
	        ctx.stroke();
	    }
	
	});
	
	module.exports = {
	    ImgDataGraphView : ImgDataGraphView,
	    ImgDataGraphModel : ImgDataGraphModel
	};
	


/***/ }),
/* 12 */
/***/ (function(module, exports, __webpack_require__) {

	var widgets = __webpack_require__(3);
	var _ = __webpack_require__(4);
	var semver_range = "^" + __webpack_require__(8).version;
	
	var ImgDisplayModel = widgets.DOMWidgetModel.extend({
	    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
	        _model_name : 'ImgDisplayModel',
	        _view_name : 'ImgDisplayView',
	        _model_module : 'ipywe',
	        _view_module : 'ipywe',
	        _model_module_version : semver_range,
	        _view_module_version : semver_range
	    })
	});
	
	
	var ImgDisplayView = widgets.DOMWidgetView.extend({
	    
	    render: function() {
	        var wid = this;
	
	        var widget_area = $('<div class="flex-container">');
	
	        widget_area.css("display", "-webkit-flex"); widget_area.css("display", "flex");
	        widget_area.css("jusitfyContent", "flex-start"); widget_area.width(1000);
	        widget_area.height(this.model.get("height") * 1.3);
	
	        var img_vbox = $('<div class="flex-item-img img-box">');
	
	        img_vbox.width(this.model.get("width") * 1.1); img_vbox.height(this.model.get("height") * 1.25); img_vbox.css("padding", "5px");
	
	        var roi_vbox = $('<div class="flex-item-roi roi-box">');
	
	        roi_vbox.width(1000 - (this.model.get("width") * 1.1) - 25); roi_vbox.height(this.model.get("height") * 1.25); roi_vbox.css("padding", "5px");
	
	        widget_area.append(img_vbox);
	        widget_area.append(roi_vbox);
	
	        this.$el.append(widget_area);
	
	        var img_container = $('<div class="img-container">');
	        img_vbox.append(img_container);
	        img_container.css({
	            position: "relative",
	            width: this.model.get("width"),
	            height: this.model.get("height")
	        });
	        
	        var img = $('<img class="curr-img">');
	        var image_src = "data:image/" + this.model.get("_format") + ";base64," + this.model.get("_b64value")
	        img.attr("src", image_src);
	        img.width(this.model.get("width")); img.height(this.model.get("height"));
	        img_container.append(img);
	        //this.$el.append(img);
	
	        var zoom_button = $('<button class="zoom-button">');
	        zoom_button.button({
	            label: "Zoom",
	            disabled: false
	        });
	        zoom_button.css("margin", "10px");
	        zoom_button.css("marginLeft", "0px");
	        img_vbox.append(zoom_button);
	        zoom_button.click(function() {
	            var zoom_val = wid.model.get("_zoom_click");
	            if (zoom_val < Number.MAX_SAFE_INTEGER) {
	                zoom_val++;
	            }
	            else {
	                zoom_val = 0;
	            }
	            wid.model.set("_zoom_click", zoom_val);
	            wid.touch();
	            select.remove();
	            console.log("Select removed");
	        });
	
	        var reset_button = $('<button class="reset-button">')
	        reset_button.button({
	            label: "Reset",
	            disabled: false
	        });
	        reset_button.css("margin", "10px");
	        img_vbox.append(reset_button);
	        reset_button.click(function() {
	            var reset_val = wid.model.get("_reset_click");
	            if (reset_val < Number.MAX_SAFE_INTEGER) {
	                reset_val++;
	            }
	            else {
	                reset_val = 0;
	            }
	            wid.model.set("_reset_click", reset_val);
	            wid.touch();
	            select.remove();
	            console.log("Image reset");
	        });
	
	        var select = $('<div class="selection-box">');
	        select.appendTo(img_container);
	
	        if (this.model.get("_offXtop") != 0 && this.model.get("_offXbottom") != 0 && this.model.get("_offYtop") != 0 && this.model.get("_offYbottom") != 0) {
	            //console.log(this.model.get("_offXtop"));
	            //console.log(this.model.get("_offXbottom"));
	            //console.log(this.model.get("_offYtop"));
	            //console.log(this.model.get("_offYbottom"));
	            console.log("entered")
	            var sel_width = this.model.get("_offXbottom") - this.model.get("_offXtop");
	            var sel_height = this.model.get("_offYbottom") - this.model.get("_offYtop");
	            select.css({
	                "top": this.model.get("_offYtop"),
	                "left": this.model.get("_offXtop"),
	                "width": sel_width,
	                "height": sel_height,
	                "position": "absolute",
	                "pointerEvents": "none",
	                "background": "transparent",
	                "border": "2px solid red"
	            });
	        }
	
	        img.on("dragstart", false);
	
	        img.on("mousedown", function(event) {
	            console.log("Click 1");
	            var click_x = event.offsetX;
	            var click_y = event.offsetY;
	            
	            select.css({
	                "top": click_y,
	                "left": click_x,
	                "width": 0,
	                "height": 0,
	                "position": "absolute",
	                "pointerEvents": "none"
	            });
	
	            select.appendTo(img_container);
	
	            img.on("mousemove", function(event) {
	                console.log("Mouse moving");
	                var move_x = event.offsetX;
	                var move_y = event.offsetY;
	                var width = Math.abs(move_x - click_x);
	                var height = Math.abs(move_y - click_y);
	                var new_x, new_y;
	
	                new_x = (move_x < click_x) ? (click_x - width) : click_x;
	                new_y = (move_y < click_y) ? (click_y - height) : click_y;
	
	                select.css({
	                    "width": width,
	                    "height": height,
	                    "top": new_y,
	                    "left": new_x,
	                    "background": "transparent",
	                    "border": "2px solid red"
	                });
	
	                console.log(select);
	
	                wid.model.set("_offXtop", parseInt(select.css("left"), 10));
	                wid.model.set("_offYtop", parseInt(select.css("top"), 10));
	                wid.model.set("_offXbottom", parseInt(select.css("left"), 10) + select.width());
	                wid.model.set("_offYbottom", parseInt(select.css("top"), 10) + select.height());
	                wid.touch();
	
	            }).on("mouseup", function(event) {
	                console.log("Click 2");
	                img.off("mousemove");
	            });
	        });
	
	        var roi = $("<div>"); roi.text("ROI: ");
	        var corners = $('<span class="roi">');
	        roi.append(corners);
	        corners.css("whiteSpace", "pre");
	        roi_vbox.append(roi);
	
	        this.calc_roi();
	        
	        this.model.on("change:_b64value", this.calc_roi, this);
	        this.model.on("change:_b64value", this.on_img_change, this);
	    },
	
	    on_img_change: function() {
	        var src = "data:image/" + this.model.get("_format") + ";base64," + this.model.get("_b64value");
	        this.$el.find(".curr-img").attr("src", src);
	    },
	
	    calc_roi: function() {
	        /*var top = this.model.get("_ycoord_absolute");
	        var left = this.model.get("_xcoord_absolute");
	        var right = this.model.get("_xcoord_absolute") + this.model.get("_ncols_currimg") - this.model.get("_extracols");
	        var bottom = this.model.get("_ycoord_absolute") + this.model.get("_nrows_currimg") - this.model.get("_extrarows");*/
	        var corns = "Top = " + this.model.get("_ycoord_absolute") + "   Bottom = " + this.model.get("_ycoord_max_roi") + "\n         Left = " + this.model.get("_xcoord_absolute") + "   Right = " + this.model.get("_xcoord_max_roi");
	        console.log(corns);
	        this.$el.find(".roi").text(corns);
	    }
	
	});
	
	module.exports = {
	    ImgDisplayView : ImgDisplayView,
	    ImgDisplayModel : ImgDisplayModel
	};


/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

	// var devel=1;
	var devel=0;
	var widgets = __webpack_require__(3);
	var _ = __webpack_require__(4);
	
	// Custom Model. Custom widgets models must at least provide default values
	// for model attributes, including
	//
	//  - `_view_name`
	//  - `_view_module`
	//  - `_view_module_version`
	//
	//  - `_model_name`
	//  - `_model_module`
	//  - `_model_module_version`
	//
	//  when different from the base class.
	
	// When serialiazing the entire widget state for embedding, only values that
	// differ from the defaults will be specified.
	var TomvizJsModel = widgets.DOMWidgetModel.extend({
	    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
		_model_name : 'TomvizJsModel',
		_view_name : 'TomvizJsView',
		_model_module : 'ipywe',
		_view_module : 'ipywe',
		_model_module_version : '0.1.0',
		_view_module_version : '0.1.0',
		value : 'Hello World'
	    })
	});
	
	
	// Custom View. Renders the widget model.
	var TomvizJsView = widgets.DOMWidgetView.extend({
	    render: function() {
	        var s= '<div class="tomviz-data-viewer" data-url="' + this.model.get("url") + '" '
	            + 'data-viewport="100%x500" '
	            + 'data-no-ui data-initialization="zoom=1.5" data-step="azimuth=10" data-animation="azimuth=100" /> ';
	        var js = '<script type="text/javascript" src="https://unpkg.com/tomvizweb"></script>';
	        var widget_area = $(s);
	        this.$el.append(widget_area);
	        $.getScript('https://unpkg.com/tomvizweb');
	    }
	});
	
	
	module.exports = {
	    TomvizJsModel : TomvizJsModel,
	    TomvizJsView : TomvizJsView
	};


/***/ }),
/* 14 */
/***/ (function(module, exports, __webpack_require__) {

	// var devel=1;
	var devel=0;
	var widgets = __webpack_require__(3);
	var _ = __webpack_require__(4);
	
	// Custom Model. Custom widgets models must at least provide default values
	// for model attributes, including
	//
	//  - `_view_name`
	//  - `_view_module`
	//  - `_view_module_version`
	//
	//  - `_model_name`
	//  - `_model_module`
	//  - `_model_module_version`
	//
	//  when different from the base class.
	
	// When serialiazing the entire widget state for embedding, only values that
	// differ from the defaults will be specified.
	var VtkJsModel = widgets.DOMWidgetModel.extend({
	    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
		_model_name : 'VtkJsModel',
		_view_name : 'VtkJsView',
		_model_module : 'ipywe',
		_view_module : 'ipywe',
		_model_module_version : '0.1.0',
		_view_module_version : '0.1.0',
		value : 'Hello World'
	    })
	});
	
	
	// Custom View. Renders the widget model.
	var VtkJsView = widgets.DOMWidgetView.extend({
	    render: function() {
	        var widget_area = $('<div>');
	        this.$el.append(widget_area);
	        var container = widget_area.get(0);
		var url = this.model.get("url");
	
	        $.getScript('https://unpkg.com/vtk.js').done(function(){
	
			var vtkColorTransferFunction = vtk.Rendering.Core.vtkColorTransferFunction;
			var vtkFullScreenRenderWindow = vtk.Rendering.Misc.vtkFullScreenRenderWindow;
			var  vtkHttpDataSetReader  = vtk.IO.Core.vtkHttpDataSetReader;
			var  vtkXMLImageDataReader  = vtk.IO.XML.vtkXMLImageDataReader;
			var vtkPiecewiseFunction = vtk.Common.DataModel.vtkPiecewiseFunction;
			var  vtkVolume = vtk.Rendering.Core.vtkVolume;
			var  vtkVolumeMapper = vtk.Rendering.Core.vtkVolumeMapper;
			//
			// Standard rendering code setup
			var renderWindow = vtk.Rendering.Core.vtkRenderWindow.newInstance();
			var renderer = vtk.Rendering.Core.vtkRenderer.newInstance({ background: [0.2, 0.3, 0.4] });
			renderWindow.addRenderer(renderer);
	    
			// different data needs different reader. 
			// const reader = vtkHttpDataSetReader.newInstance({ fetchGzip: true });
			// VTI reader
			const reader = vtkXMLImageDataReader.newInstance();
			const actor = vtkVolume.newInstance();
			const mapper = vtkVolumeMapper.newInstance();
			mapper.setSampleDistance(1.1);
			actor.setMapper(mapper);
			// create color and opacity transfer functions
			const ctfun = vtkColorTransferFunction.newInstance();
			ctfun.addRGBPoint(0, 85 / 255.0, 0, 0);
			ctfun.addRGBPoint(95, 1.0, 1.0, 1.0);
			ctfun.addRGBPoint(225, 0.66, 0.66, 0.5);
			ctfun.addRGBPoint(255, 0.3, 1.0, 0.5);
			const ofun = vtkPiecewiseFunction.newInstance();
			ofun.addPoint(0.0, 0.0);
			ofun.addPoint(255.0, 1.0);
	
			// reader.setUrl(`/~lj7/LIDC2.vti`).then(() => {
			reader.setUrl(url).then(() => {
				reader.loadData().then(() => {
					//
					const source = reader.getOutputData(0);
					// mapper.setInputConnection(reader.getOutputPort());
					console.log(source);
					mapper.setInputData(source);
					const dataArray = source.getPointData().getScalars() || source.getPointData().getArrays()[0];
					const dataRange = dataArray.getRange();
					console.log("dataRange=", dataRange);
					actor.getProperty().setRGBTransferFunction(0, ctfun);
					actor.getProperty().setScalarOpacity(0, ofun);
					actor.getProperty().setScalarOpacityUnitDistance(0, 3.0);
					actor.getProperty().setInterpolationTypeToLinear();
					actor.getProperty().setUseGradientOpacity(0, true);
					actor.getProperty().setGradientOpacityMinimumValue(0, 0);
					actor.getProperty().setGradientOpacityMinimumOpacity(0, 0.0);
					actor.getProperty().setGradientOpacityMaximumValue(0, (dataRange[1] - dataRange[0]) * 0.05);
					actor.getProperty().setGradientOpacityMaximumOpacity(0, 1.0);
					actor.getProperty().setShade(true);
					actor.getProperty().setAmbient(0.2);
					actor.getProperty().setDiffuse(0.7);
					actor.getProperty().setSpecular(0.3);
					actor.getProperty().setSpecularPower(8.0);
	
					renderer.addVolume(actor);
					renderer.resetCamera();
	
					var openglRenderWindow = vtk.Rendering.OpenGL.vtkRenderWindow.newInstance();
					renderWindow.addView(openglRenderWindow);
					openglRenderWindow.setContainer(container);
	
					renderer.getActiveCamera().zoom(1.5);
					renderer.getActiveCamera().elevation(70);
	
					var interactor =     vtk.Rendering.Core.vtkRenderWindowInteractor.newInstance();
					interactor.setView(openglRenderWindow);
					interactor.initialize();
					interactor.setDesiredUpdateRate(15.0);
					interactor.bindEvents(container);
	
					renderWindow.render();
				    });
			    });
			// end of setUrl
	
		    }); // end of getScript
		
	    }
	});
	
	
	module.exports = {
	    VtkJsModel : VtkJsModel,
	    VtkJsView : VtkJsView
	};


/***/ })
/******/ ])});;
//# sourceMappingURL=index.js.map