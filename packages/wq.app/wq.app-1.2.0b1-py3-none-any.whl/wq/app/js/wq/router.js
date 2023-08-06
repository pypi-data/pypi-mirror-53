/*
 * wq.app v1.2.0b1 - @wq/router 1.2.0-beta.1
 * Respond to URL changes with locally generated pages and custom events
 * (c) 2012-2019, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['regenerator-runtime', 'redux-first-router', './store', './template'], function (_regeneratorRuntime, reduxFirstRouter, store, tmpl) { 'use strict';

_regeneratorRuntime = _regeneratorRuntime && _regeneratorRuntime.hasOwnProperty('default') ? _regeneratorRuntime['default'] : _regeneratorRuntime;
tmpl = tmpl && tmpl.hasOwnProperty('default') ? tmpl['default'] : tmpl;

function _typeof(obj) {
  if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") {
    _typeof = function (obj) {
      return typeof obj;
    };
  } else {
    _typeof = function (obj) {
      return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
    };
  }

  return _typeof(obj);
}

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) {
  try {
    var info = gen[key](arg);
    var value = info.value;
  } catch (error) {
    reject(error);
    return;
  }

  if (info.done) {
    resolve(value);
  } else {
    Promise.resolve(value).then(_next, _throw);
  }
}

function _asyncToGenerator(fn) {
  return function () {
    var self = this,
        args = arguments;
    return new Promise(function (resolve, reject) {
      var gen = fn.apply(self, args);

      function _next(value) {
        asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value);
      }

      function _throw(err) {
        asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err);
      }

      _next(undefined);
    });
  };
}

function _defineProperty(obj, key, value) {
  if (key in obj) {
    Object.defineProperty(obj, key, {
      value: value,
      enumerable: true,
      configurable: true,
      writable: true
    });
  } else {
    obj[key] = value;
  }

  return obj;
}

function ownKeys(object, enumerableOnly) {
  var keys = Object.keys(object);

  if (Object.getOwnPropertySymbols) {
    var symbols = Object.getOwnPropertySymbols(object);
    if (enumerableOnly) symbols = symbols.filter(function (sym) {
      return Object.getOwnPropertyDescriptor(object, sym).enumerable;
    });
    keys.push.apply(keys, symbols);
  }

  return keys;
}

function _objectSpread2(target) {
  for (var i = 1; i < arguments.length; i++) {
    var source = arguments[i] != null ? arguments[i] : {};

    if (i % 2) {
      ownKeys(source, true).forEach(function (key) {
        _defineProperty(target, key, source[key]);
      });
    } else if (Object.getOwnPropertyDescriptors) {
      Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));
    } else {
      ownKeys(source).forEach(function (key) {
        Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
      });
    }
  }

  return target;
}

function _slicedToArray(arr, i) {
  return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _nonIterableRest();
}

function _toConsumableArray(arr) {
  return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _nonIterableSpread();
}

function _arrayWithoutHoles(arr) {
  if (Array.isArray(arr)) {
    for (var i = 0, arr2 = new Array(arr.length); i < arr.length; i++) arr2[i] = arr[i];

    return arr2;
  }
}

function _arrayWithHoles(arr) {
  if (Array.isArray(arr)) return arr;
}

function _iterableToArray(iter) {
  if (Symbol.iterator in Object(iter) || Object.prototype.toString.call(iter) === "[object Arguments]") return Array.from(iter);
}

function _iterableToArrayLimit(arr, i) {
  if (!(Symbol.iterator in Object(arr) || Object.prototype.toString.call(arr) === "[object Arguments]")) {
    return;
  }

  var _arr = [];
  var _n = true;
  var _d = false;
  var _e = undefined;

  try {
    for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) {
      _arr.push(_s.value);

      if (i && _arr.length === i) break;
    }
  } catch (err) {
    _d = true;
    _e = err;
  } finally {
    try {
      if (!_n && _i["return"] != null) _i["return"]();
    } finally {
      if (_d) throw _e;
    }
  }

  return _arr;
}

function _nonIterableSpread() {
  throw new TypeError("Invalid attempt to spread non-iterable instance");
}

function _nonIterableRest() {
  throw new TypeError("Invalid attempt to destructure non-iterable instance");
}

var strictUriEncode = function strictUriEncode(str) {
    return encodeURIComponent(str).replace(/[!'()*]/g, function (x) {
        return "%".concat(x.charCodeAt(0).toString(16).toUpperCase());
    });
};

var token = '%[a-f0-9]{2}';
var singleMatcher = new RegExp(token, 'gi');
var multiMatcher = new RegExp('(' + token + ')+', 'gi');

function decodeComponents(components, split) {
    try {
        // Try to decode the entire string first
        return decodeURIComponent(components.join(''));
    } catch (err) {// Do nothing
    }

    if (components.length === 1) {
        return components;
    }

    split = split || 1; // Split the array in 2 parts

    var left = components.slice(0, split);
    var right = components.slice(split);
    return Array.prototype.concat.call([], decodeComponents(left), decodeComponents(right));
}

function decode(input) {
    try {
        return decodeURIComponent(input);
    } catch (err) {
        var tokens = input.match(singleMatcher);

        for (var i = 1; i < tokens.length; i++) {
            input = decodeComponents(tokens, i).join('');
            tokens = input.match(singleMatcher);
        }

        return input;
    }
}

function customDecodeURIComponent(input) {
    // Keep track of all the replacements and prefill the map with the `BOM`
    var replaceMap = {
        '%FE%FF': "\uFFFD\uFFFD",
        '%FF%FE': "\uFFFD\uFFFD"
    };
    var match = multiMatcher.exec(input);

    while (match) {
        try {
            // Decode as big chunks as possible
            replaceMap[match[0]] = decodeURIComponent(match[0]);
        } catch (err) {
            var result = decode(match[0]);

            if (result !== match[0]) {
                replaceMap[match[0]] = result;
            }
        }

        match = multiMatcher.exec(input);
    } // Add `%C2` at the end of the map to make sure it does not replace the combinator before everything else


    replaceMap['%C2'] = "\uFFFD";
    var entries = Object.keys(replaceMap);

    for (var i = 0; i < entries.length; i++) {
        // Replace all decoded components
        var key = entries[i];
        input = input.replace(new RegExp(key, 'g'), replaceMap[key]);
    }

    return input;
}

var decodeUriComponent = function decodeUriComponent(encodedURI) {
    if (typeof encodedURI !== 'string') {
        throw new TypeError('Expected `encodedURI` to be of type `string`, got `' + _typeof(encodedURI) + '`');
    }

    try {
        encodedURI = encodedURI.replace(/\+/g, ' '); // Try the built in decoder first

        return decodeURIComponent(encodedURI);
    } catch (err) {
        // Fallback to a more advanced decoder
        return customDecodeURIComponent(encodedURI);
    }
};

var splitOnFirst = function splitOnFirst(string, separator) {
    if (!(typeof string === 'string' && typeof separator === 'string')) {
        throw new TypeError('Expected the arguments to be of type `string`');
    }

    if (separator === '') {
        return [string];
    }

    var separatorIndex = string.indexOf(separator);

    if (separatorIndex === -1) {
        return [string];
    }

    return [string.slice(0, separatorIndex), string.slice(separatorIndex + separator.length)];
};

function encoderForArrayFormat(options) {
    switch (options.arrayFormat) {
        case 'index':
            return function (key) {
                return function (result, value) {
                    var index = result.length;

                    if (value === undefined) {
                        return result;
                    }

                    if (value === null) {
                        return [].concat(_toConsumableArray(result), [[encode(key, options), '[', index, ']'].join('')]);
                    }

                    return [].concat(_toConsumableArray(result), [[encode(key, options), '[', encode(index, options), ']=', encode(value, options)].join('')]);
                };
            };

        case 'bracket':
            return function (key) {
                return function (result, value) {
                    if (value === undefined) {
                        return result;
                    }

                    if (value === null) {
                        return [].concat(_toConsumableArray(result), [[encode(key, options), '[]'].join('')]);
                    }

                    return [].concat(_toConsumableArray(result), [[encode(key, options), '[]=', encode(value, options)].join('')]);
                };
            };

        case 'comma':
            return function (key) {
                return function (result, value, index) {
                    if (value === null || value === undefined || value.length === 0) {
                        return result;
                    }

                    if (index === 0) {
                        return [[encode(key, options), '=', encode(value, options)].join('')];
                    }

                    return [[result, encode(value, options)].join(',')];
                };
            };

        default:
            return function (key) {
                return function (result, value) {
                    if (value === undefined) {
                        return result;
                    }

                    if (value === null) {
                        return [].concat(_toConsumableArray(result), [encode(key, options)]);
                    }

                    return [].concat(_toConsumableArray(result), [[encode(key, options), '=', encode(value, options)].join('')]);
                };
            };
    }
}

function parserForArrayFormat(options) {
    var result;

    switch (options.arrayFormat) {
        case 'index':
            return function (key, value, accumulator) {
                result = /\[(\d*)\]$/.exec(key);
                key = key.replace(/\[\d*\]$/, '');

                if (!result) {
                    accumulator[key] = value;
                    return;
                }

                if (accumulator[key] === undefined) {
                    accumulator[key] = {};
                }

                accumulator[key][result[1]] = value;
            };

        case 'bracket':
            return function (key, value, accumulator) {
                result = /(\[\])$/.exec(key);
                key = key.replace(/\[\]$/, '');

                if (!result) {
                    accumulator[key] = value;
                    return;
                }

                if (accumulator[key] === undefined) {
                    accumulator[key] = [value];
                    return;
                }

                accumulator[key] = [].concat(accumulator[key], value);
            };

        case 'comma':
            return function (key, value, accumulator) {
                var isArray = typeof value === 'string' && value.split('').indexOf(',') > -1;
                var newValue = isArray ? value.split(',') : value;
                accumulator[key] = newValue;
            };

        default:
            return function (key, value, accumulator) {
                if (accumulator[key] === undefined) {
                    accumulator[key] = value;
                    return;
                }

                accumulator[key] = [].concat(accumulator[key], value);
            };
    }
}

function encode(value, options) {
    if (options.encode) {
        return options.strict ? strictUriEncode(value) : encodeURIComponent(value);
    }

    return value;
}

function decode$1(value, options) {
    if (options.decode) {
        return decodeUriComponent(value);
    }

    return value;
}

function keysSorter(input) {
    if (Array.isArray(input)) {
        return input.sort();
    }

    if (_typeof(input) === 'object') {
        return keysSorter(Object.keys(input)).sort(function (a, b) {
            return Number(a) - Number(b);
        }).map(function (key) {
            return input[key];
        });
    }

    return input;
}

function removeHash(input) {
    var hashStart = input.indexOf('#');

    if (hashStart !== -1) {
        input = input.slice(0, hashStart);
    }

    return input;
}

function extract(input) {
    input = removeHash(input);
    var queryStart = input.indexOf('?');

    if (queryStart === -1) {
        return '';
    }

    return input.slice(queryStart + 1);
}

function parseValue(value, options) {
    if (options.parseNumbers && !Number.isNaN(Number(value)) && typeof value === 'string' && value.trim() !== '') {
        value = Number(value);
    } else if (options.parseBooleans && value !== null && (value.toLowerCase() === 'true' || value.toLowerCase() === 'false')) {
        value = value.toLowerCase() === 'true';
    }

    return value;
}

function parse(input, options) {
    options = Object.assign({
        decode: true,
        sort: true,
        arrayFormat: 'none',
        parseNumbers: false,
        parseBooleans: false
    }, options);
    var formatter = parserForArrayFormat(options); // Create an object with no prototype

    var ret = Object.create(null);

    if (typeof input !== 'string') {
        return ret;
    }

    input = input.trim().replace(/^[?#&]/, '');

    if (!input) {
        return ret;
    }

    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
        for (var _iterator = input.split('&')[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
            var param = _step.value;

            var _splitOnFirst = splitOnFirst(param.replace(/\+/g, ' '), '='),
                _splitOnFirst2 = _slicedToArray(_splitOnFirst, 2),
                key = _splitOnFirst2[0],
                value = _splitOnFirst2[1]; // Missing `=` should be `null`:
            // http://w3.org/TR/2012/WD-url-20120524/#collect-url-parameters


            value = value === undefined ? null : decode$1(value, options);
            formatter(decode$1(key, options), value, ret);
        }
    } catch (err) {
        _didIteratorError = true;
        _iteratorError = err;
    } finally {
        try {
            if (!_iteratorNormalCompletion && _iterator.return != null) {
                _iterator.return();
            }
        } finally {
            if (_didIteratorError) {
                throw _iteratorError;
            }
        }
    }

    for (var _i = 0, _Object$keys = Object.keys(ret); _i < _Object$keys.length; _i++) {
        var key = _Object$keys[_i];
        var value = ret[key];

        if (_typeof(value) === 'object' && value !== null) {
            for (var _i2 = 0, _Object$keys2 = Object.keys(value); _i2 < _Object$keys2.length; _i2++) {
                var k = _Object$keys2[_i2];
                value[k] = parseValue(value[k], options);
            }
        } else {
            ret[key] = parseValue(value, options);
        }
    }

    if (options.sort === false) {
        return ret;
    }

    return (options.sort === true ? Object.keys(ret).sort() : Object.keys(ret).sort(options.sort)).reduce(function (result, key) {
        var value = ret[key];

        if (Boolean(value) && _typeof(value) === 'object' && !Array.isArray(value)) {
            // Sort object keys, not values
            result[key] = keysSorter(value);
        } else {
            result[key] = value;
        }

        return result;
    }, Object.create(null));
}

var extract_1 = extract;
var parse_1 = parse;

var stringify = function stringify(object, options) {
    if (!object) {
        return '';
    }

    options = Object.assign({
        encode: true,
        strict: true,
        arrayFormat: 'none'
    }, options);
    var formatter = encoderForArrayFormat(options);
    var keys = Object.keys(object);

    if (options.sort !== false) {
        keys.sort(options.sort);
    }

    return keys.map(function (key) {
        var value = object[key];

        if (value === undefined) {
            return '';
        }

        if (value === null) {
            return encode(key, options);
        }

        if (Array.isArray(value)) {
            return value.reduce(formatter(key), []).join('&');
        }

        return encode(key, options) + '=' + encode(value, options);
    }).filter(function (x) {
        return x.length > 0;
    }).join('&');
};

var parseUrl = function parseUrl(input, options) {
    return {
        url: removeHash(input).split('?')[0] || '',
        query: parse(extract(input), options)
    };
};

var queryString = {
    extract: extract_1,
    parse: parse_1,
    stringify: stringify,
    parseUrl: parseUrl
};

var _validOrder;
var HTML = '@@HTML',
    RENDER = 'RENDER',
    FIRST = '@@FIRST',
    DEFAULT = '@@DEFAULT',
    LAST = '@@LAST',
    validOrder = (_validOrder = {}, _defineProperty(_validOrder, FIRST, true), _defineProperty(_validOrder, DEFAULT, true), _defineProperty(_validOrder, LAST, true), _validOrder); // Exported module object

var router = {
    config: {
        store: 'main',
        tmpl404: '404',
        injectOnce: false,
        debug: false,
        getTemplateName: function getTemplateName(name) {
            return name;
        }
    },
    routesMap: {},
    contextProcessors: [],
    renderers: [render]
};
var $, jqm; // Configuration

router.init = function (config) {
    // Define baseurl (without trailing slash) if it is not /
    if (config && config.base_url) {
        router.base_url = config.base_url;
    }

    router.config = _objectSpread2({}, router.config, {}, config); // Configuration options:
    // Define `tmpl404` if there is not a template named '404'
    // Set `injectOnce`to true to re-use rendered templates
    // Set `debug` to true to log template & context information
    // Set getTemplateName to change how route names are resolved.

    $ = config.jQuery || window.jQuery;
    jqm = $.mobile;

    var _connectRoutes = reduxFirstRouter.connectRoutes({}, {
        querySerializer: queryString,
        initialDispatch: false
    }),
        routeReducer = _connectRoutes.reducer,
        middleware = _connectRoutes.middleware,
        enhancer = _connectRoutes.enhancer,
        initialDispatch = _connectRoutes.initialDispatch;

    router.store = store.getStore(router.config.store);
    router.store.addReducer('location', routeReducer);
    router.store.addReducer('context', contextReducer);
    router.store.addEnhancer(enhancer);
    router.store.addMiddleware(middleware);
    router.store.setThunkHandler(router.addThunk);
    router.store.subscribe(router.go);
    router._initialDispatch = initialDispatch;
};

router.jqmInit = function () {
    if (!router.config) {
        throw new Error('Initialize router first!');
    }

    var orderedRoutes = {};
    [FIRST, DEFAULT, LAST].forEach(function (order) {
        Object.entries(router.routesMap).forEach(function (_ref) {
            var _ref2 = _slicedToArray(_ref, 2),
                name = _ref2[0],
                path = _ref2[1];

            if (path.order === order) {
                orderedRoutes[name] = path;
            }
        });
    });
    router.store.dispatch({
        type: reduxFirstRouter.ADD_ROUTES,
        payload: {
            routes: orderedRoutes
        }
    });

    router._initialDispatch();

    jqm.initializePage();
};

function contextReducer() {
    var context = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var action = arguments.length > 1 ? arguments[1] : undefined;

    if (action.type != RENDER && action.type != reduxFirstRouter.NOT_FOUND) {
        return context;
    }

    if (action.type === RENDER) {
        context = action.payload;
    } else if (action.type === reduxFirstRouter.NOT_FOUND) {
        context = _routeInfo(_objectSpread2({}, action.meta.location.current, {
            prev: action.meta.location.prev
        }));
    }

    return context;
}

function _generateContext(_x, _x2) {
    return _generateContext2.apply(this, arguments);
}

function _generateContext2() {
    _generateContext2 = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee(dispatch, getState) {
        var refresh,
            location,
            context,
            i,
            fn,
            _args = arguments;
        return _regeneratorRuntime.wrap(function _callee$(_context) {
            while (1) {
                switch (_context.prev = _context.next) {
                    case 0:
                        refresh = _args.length > 2 && _args[2] !== undefined ? _args[2] : false;
                        location = getState().location;
                        context = _routeInfo(location);
                        i = 0;

                    case 4:
                        if (!(i < router.contextProcessors.length)) {
                            _context.next = 20;
                            break;
                        }

                        fn = router.contextProcessors[i];
                        _context.t0 = _objectSpread2;
                        _context.t1 = {};
                        _context.t2 = context;
                        _context.t3 = {};
                        _context.next = 12;
                        return fn(context);

                    case 12:
                        _context.t4 = _context.sent;

                        if (_context.t4) {
                            _context.next = 15;
                            break;
                        }

                        _context.t4 = {};

                    case 15:
                        _context.t5 = _context.t4;
                        context = (0, _context.t0)(_context.t1, _context.t2, _context.t3, _context.t5);

                    case 17:
                        i++;
                        _context.next = 4;
                        break;

                    case 20:
                        return _context.abrupt("return", router.render(context, refresh));

                    case 21:
                    case "end":
                        return _context.stop();
                }
            }
        }, _callee);
    }));
    return _generateContext2.apply(this, arguments);
}

router.register = function (path, nameOrContext, context) {
    var order = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : DEFAULT;
    var name;
    var newUsage = ' Usage: router.register(path[, name[, contextFn]])';

    if (!validOrder[order]) {
        // Assume old-style prevent() callback was passed
        throw new Error('prevent() no longer supported.' + newUsage);
    }

    if (context) {
        if (typeof context !== 'function') {
            throw new Error('Unexpected ' + context + ' for contextFn.' + newUsage);
        }
    } else if (typeof nameOrContext === 'function') {
        context = nameOrContext;
        nameOrContext = null;
    }

    if (nameOrContext) {
        name = nameOrContext;

        if (typeof name !== 'string') {
            throw new Error('Unexpected ' + name + ' for route name.' + newUsage);
        }
    } else {
        if (path.indexOf('/') > -1) {
            throw new Error('router.register() now requires a route name if path contains /.' + newUsage);
        } // Assume there is a template with the same name


        name = path;
    }

    if (context && context.length > 1) {
        throw new Error('contextFn should take a single argument (the existing context) and return a new context for merging.  router.go() is now called automatically.');
    }

    router.routesMap[name.toUpperCase()] = {
        path: _normalizePath(path),
        thunk: function thunk(dispatch, getState) {
            return _generateContext(dispatch, getState);
        },
        order: order
    };

    if (context) {
        router.addContextForRoute(name, context);
    }

    return name;
};

router.registerFirst = function (path, name, context) {
    router.register(path, name, context, FIRST);
};

router.registerLast = function (path, name, context) {
    router.register(path, name, context, LAST);
};

router.addThunk = function (name, thunk) {
    router.routesMap[name] = {
        thunk: thunk,
        order: FIRST
    };
};

router.addThunks = function (thunks) {
    Object.entries(thunks).forEach(function (_ref3) {
        var _ref4 = _slicedToArray(_ref3, 2),
            name = _ref4[0],
            thunk = _ref4[1];

        router.addThunk(name, thunk);
    });
};

router.addContext = function (fn) {
    router.contextProcessors.push(fn);
};

router.addContextForRoute = function (pathOrName, fn) {
    var name = _getRouteName(pathOrName);

    function contextForRoute(context) {
        if (context.router_info.name == name) {
            return fn(context);
        } else {
            return {};
        }
    }

    router.addContext(contextForRoute);
};

router.onShow = function (pathOrName, fn) {
    router.addRoute(pathOrName, 's', fn);
};

var jqmEvents = {
    s: 'pageshow',
    c: 'pagecreate',
    i: 'pageinit',
    l: 'pageload' // 'h': 'pagehide',

};

router.addRoute = function (pathOrName, eventCode, fn, obj) {
    if (!jqmEvents[eventCode]) {
        throw new Error("addRoute for '" + eventCode + "' not currently supported");
    }

    if (obj) {
        fn = obj[fn];
    }

    var name = _getRouteName(pathOrName);

    $('body').on(jqmEvents[eventCode] + '.' + name, function () {
        var state = router.store.getState(),
            context = state.context,
            _ref5 = context || {},
            router_info = _ref5.router_info;

        if (router_info && router_info.name == name) {
            fn();
        }
    });
};

router.addRender = function (render) {
    router.renderers.push(render);
};

router.push = function (path) {
    reduxFirstRouter.push(path);
};

router.render = function (context, refresh) {
    if (refresh) {
        if (refresh === true) {
            refresh = (context._refreshCount || 0) + 1;
        }

        context._refreshCount = refresh;
    }

    return router.store.dispatch({
        type: RENDER,
        payload: context
    });
}; // Re-render existing context


router.refresh = function () {
    var context = router.store.getState().context;
    router.render(context, true);
}; // Regenerate context, then re-render page


router.reload = function () {
    var context = router.store.getState().context,
        refresh = (context._refreshCount || 0) + 1;
    return _generateContext(function (action) {
        return router.store.dispatch(action);
    }, function () {
        return router.store.getState();
    }, refresh);
}; // Inject and display page


router.go = function (arg) {
    if (arg) {
        throw new Error('router.go() is now called automatically');
    }

    var state = router.store.getState();
    router.renderers.forEach(function (render) {
        try {
            render(state);
        } catch (e) {
            console.error(e);
        }
    });
};

var _lastPath, _lastRefresh;

function render(state) {
    var location = state.location,
        context = state.context,
        _ref6 = context || {},
        router_info = _ref6.router_info,
        refresh = _ref6._refreshCount,
        _ref7 = router_info || {},
        url = _ref7.full_path,
        pageid = _ref7.dom_id,
        routeName = _ref7.name;
 // FIXME


    if (!routeName || routeName != location.type.toLowerCase()) {
        return;
    }

    if (url === _lastPath && refresh === _lastRefresh) {
        return;
    }

    _lastPath = url;
    _lastRefresh = refresh;
    var template;

    if (location.type === reduxFirstRouter.NOT_FOUND || context[reduxFirstRouter.NOT_FOUND]) {
        template = router.config.tmpl404;
        context.url = url;
    } else {
        template = router.config.getTemplateName(routeName, context);
    }

    var $page,
        role,
        options,
        html = context[HTML];

    if (html) {
        if (router.config.debug) {
            console.log('Injecting pre-rendered HTML:');
            console.log(html);
        }

        $page = tmpl.injectHTML(html, url, pageid);
    } else {
        if (router.config.debug) {
            console.log('Rendering ' + url + " with template '" + template + "' and context:");
            console.log(context);
        }

        if ( router.config.injectOnce) {
            // Only render the template once
            $page = tmpl.injectOnce(template, context, url, pageid);
        } else {
            // Default: render the template every time the page is loaded
            $page = tmpl.inject(template, context, url, pageid);
        }
    }

    $page.on('click', 'a', _handleLink);
    role = $page.jqmData('role') || 'page';

    if (role == 'page') {
        options =  {};
        options.allowSamePageTransition = true;
        jqm.changePage($page, options);
    } else if (role == 'popup') {
        options = {};

        $page.popup('open', options);
    } else if (role == 'panel') {
        $page.panel('open');
    }

    return $page;
}

function _handleLink(evt) {
    var target = evt.currentTarget;

    if (target.rel === 'external') {
        return;
    }

    var href = target.href;

    if (href === undefined) {
        return;
    }

    var url = new URL(href, window.location);

    if (url.origin != window.location.origin) {
        return;
    }

    evt.preventDefault();
    router.push(url.pathname + url.search);
} // Simple 404 page helper


router.notFound = function () {
    return _defineProperty({}, reduxFirstRouter.NOT_FOUND, true);
}; // Use when loading HTML from server


router.rawHTML = function (html) {
    return _defineProperty({}, HTML, html);
};

router.base_url = '';

function _normalizePath(path) {
    path = path.replace('<slug>', ':slug');
    return router.base_url + '/' + path;
}

function _getRouteName(pathOrName) {
    var name;

    if (router.routesMap[pathOrName.toUpperCase()]) {
        name = pathOrName;
    } else {
        Object.entries(router.routesMap).forEach(function (_ref10) {
            var _ref11 = _slicedToArray(_ref10, 2),
                rname = _ref11[0],
                rpath = _ref11[1];

            if (_normalizePath(pathOrName) === rpath.path) {
                name = rname;
            }
        });
    }

    if (!name) {
        throw new Error('Unrecognized route: ' + pathOrName);
    }

    return name.toLowerCase();
}

function _removeBase(pathname) {
    return pathname.replace(router.base_url + '/', '');
}

function _routeInfo(location) {
    var info = {};
    info.name = location.type.toLowerCase();
    info.prev_path = _removeBase(location.prev.pathname);
    info.path = _removeBase(location.pathname);
    info.path_enc = escape(info.path);
    info.full_path = location.pathname + (location.search ? '?' + location.search : '');
    info.full_path_enc = escape(info.full_path);
    info.params = location.query;
    info.slugs = location.payload;
    info.base_url = router.base_url;
    return {
        router_info: info,
        rt: router.base_url
    };
}

return router;

});
//# sourceMappingURL=router.js.map
