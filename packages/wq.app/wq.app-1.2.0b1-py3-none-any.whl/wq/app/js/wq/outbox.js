/*
 * wq.app v1.2.0b1 - @wq/outbox 1.2.0-beta.1
 * A simple model API for working with stored lists
 * (c) 2012-2019, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['exports', 'regenerator-runtime', './store', './model', 'json-forms', 'redux-offline'], function (exports, _regeneratorRuntime, ds, model, jsonForms, reduxOffline) { 'use strict';

_regeneratorRuntime = _regeneratorRuntime && _regeneratorRuntime.hasOwnProperty('default') ? _regeneratorRuntime['default'] : _regeneratorRuntime;
ds = ds && ds.hasOwnProperty('default') ? ds['default'] : ds;
model = model && model.hasOwnProperty('default') ? model['default'] : model;

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

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _defineProperties(target, props) {
  for (var i = 0; i < props.length; i++) {
    var descriptor = props[i];
    descriptor.enumerable = descriptor.enumerable || false;
    descriptor.configurable = true;
    if ("value" in descriptor) descriptor.writable = true;
    Object.defineProperty(target, descriptor.key, descriptor);
  }
}

function _createClass(Constructor, protoProps, staticProps) {
  if (protoProps) _defineProperties(Constructor.prototype, protoProps);
  if (staticProps) _defineProperties(Constructor, staticProps);
  return Constructor;
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

function _classPrivateFieldGet(receiver, privateMap) {
  var descriptor = privateMap.get(receiver);

  if (!descriptor) {
    throw new TypeError("attempted to get private field on non-instance");
  }

  if (descriptor.get) {
    return descriptor.get.call(receiver);
  }

  return descriptor.value;
}

function _classPrivateFieldSet(receiver, privateMap, value) {
  var descriptor = privateMap.get(receiver);

  if (!descriptor) {
    throw new TypeError("attempted to set private field on non-instance");
  }

  if (descriptor.set) {
    descriptor.set.call(receiver, value);
  } else {
    if (!descriptor.writable) {
      throw new TypeError("attempted to set read only private field");
    }

    descriptor.value = value;
  }

  return value;
}

var defaultDiscard = reduxOffline.offlineConfig.discard,
    defaultRetry = reduxOffline.offlineConfig.retry;
var REMOVE_ITEMS = '@@REMOVE_OUTBOX_ITEMS',
    RETRY_ITEMS = '@@RETRY_OUTBOX_ITEMS',
    POST = 'POST',
    DELETE = 'DELETE',
    SUBMIT = 'SUBMIT',
    SUCCESS = 'SUCCESS',
    UPDATE = 'UPDATE',
    ERROR = 'ERROR',
    FORM_SUBMIT = 'FORM_SUBMIT',
    FORM_SUCCESS = 'FORM_SUCCESS',
    FORM_ERROR = 'FORM_ERROR',
    BATCH_SUBMIT = '@@BATCH_SUBMIT',
    BATCH_SUCCESS = '@@BATCH_SUCCESS',
    BATCH_ERROR = '@@BATCH_ERROR',
    ON_SUCCESS = 'ON_SUCCESS',
    IMMEDIATE = 'IMMEDIATE',
    LOCAL_ONLY = 'LOCAL_ONLY';
var _outboxes = {};

var Outbox =
/*#__PURE__*/
function () {
    function Outbox(store) {
        var _this = this;

        _classCallCheck(this, Outbox);

        _waiting.set(this, {
            writable: true,
            value: {}
        });

        _lastOutbox.set(this, {
            writable: true,
            value: []
        });

        _memoryItems.set(this, {
            writable: true,
            value: {}
        });

        _outboxes[store.name] = this;
        this.store = store;
        store.outbox = this;

        var _createOffline = reduxOffline.createOffline(_objectSpread2({}, reduxOffline.offlineConfig, {
            effect: function effect(_effect2, action) {
                return _this._effect(_effect2, action);
            },
            discard: function discard(error, action, retries) {
                return _this._discard(error, action, retries);
            },
            retry: function retry(action, retries) {
                return _this._retry(action, retries);
            },
            queue: {
                enqueue: function enqueue(array, item, context) {
                    return _this._enqueue(array, item, context);
                },
                dequeue: function dequeue(array, item, context) {
                    return _this._dequeue(array, item, context);
                },
                peek: function peek(array, item, context) {
                    return _this._peek(array, item, context);
                }
            },
            persist: false // Handled in store

        })),
            middleware = _createOffline.middleware,
            enhanceReducer = _createOffline.enhanceReducer,
            enhanceStore = _createOffline.enhanceStore;

        store.addMiddleware(middleware);
        store.addEnhanceReducer('offline', enhanceReducer, function (state) {
            return _this._serialize(state);
        }, function (state) {
            return _this._deserialize(state);
        });
        store.addEnhancer(enhanceStore);
        store.subscribe(function () {
            return _this._onUpdate();
        });
        this.syncMethod = POST;
        this.batchService = null;
        this.batchSizeMin = 2;
        this.batchSizeMax = 50;
        this.applyState = ON_SUCCESS;
        this.cleanOutbox = true;
        this.maxRetries = 10;
        this.csrftoken = null;
        this.csrftokenField = 'csrfmiddlewaretoken';
    }

    _createClass(Outbox, [{
        key: "init",
        value: function init(opts) {
            var _this2 = this;

            var optlist = [// Default to store values but allow overriding
            'service', 'formatKeyword', 'defaults', 'debugNetwork', 'debugValues', // Outbox-specific options
            'syncMethod', 'applyState', 'cleanOutbox', 'maxRetries', 'batchService', 'batchSizeMin', 'batchSizeMax', 'csrftokenField', // Outbox functions
            'validate', 'applyResult', 'updateModels'];
            optlist.forEach(function (opt) {
                if (_this2.store.hasOwnProperty(opt)) {
                    _this2[opt] = _this2.store[opt];
                }

                if (opts && opts.hasOwnProperty(opt)) {
                    _this2[opt] = opts[opt];
                }
            });

            if (opts.parseBatchResult) {
                throw new Error('parseBatchResult() no longer supported.  Use ajax() hook instead.');
            }

            if (this.cleanOutbox) {
                // Clear out successfully synced items from previous runs, if any
                // FIXME: should we hold up init until this is done?
                this.loadItems().then(function (items) {
                    _this2.removeItems(items.list.filter(function (item) {
                        return item.synced || item.options.storage === 'temporary' && !item.options.desiredStorage;
                    }).map(function (item) {
                        return item.id;
                    }));
                }).then(function () {
                    return _this2._cleanUpItemData;
                });
            }

            if (this.batchService) {
                this.store.addThunk(BATCH_SUCCESS, function (dispatch, getState, bag) {
                    return _this2._dispatchBatchResponse(bag.action, dispatch);
                });
                this.store.addThunk(BATCH_ERROR, function (dispatch, getState, bag) {
                    return _this2._dispatchBatchResponse(bag.action, dispatch);
                });
            }
        }
    }, {
        key: "setCSRFToken",
        value: function setCSRFToken(csrftoken) {
            this.csrftoken = csrftoken;
        } // Queue data for server use; use outbox to cache unsynced items

    }, {
        key: "save",
        value: function () {
            var _save = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee(data, options, noSend) {
                var outboxId, item, currentId, match, type, payload, commitType, rollbackType, model, applyState, name, items;
                return _regeneratorRuntime.wrap(function _callee$(_context) {
                    while (1) {
                        switch (_context.prev = _context.next) {
                            case 0:
                                if (!noSend) {
                                    _context.next = 2;
                                    break;
                                }

                                throw new Error('outbox.save() noSend arg no longer supported; use outbox.pause() instead');

                            case 2:
                                if (options) {
                                    options = _objectSpread2({}, options);
                                } else {
                                    options = {};
                                }

                                if (options.storage === 'inline') {
                                    delete options.storage;
                                }

                                if (options.storage === 'temporary') {
                                    options.once = true;
                                }

                                if (this.validate(data, options)) {
                                    _context.next = 7;
                                    break;
                                }

                                return _context.abrupt("return", null);

                            case 7:
                                // FIXME: What if next id changes during await?
                                outboxId = options.id || (this.store.getState().offline.lastTransaction || 0) + 1;
                                _context.next = 10;
                                return this._updateItemData({
                                    id: outboxId,
                                    data: data,
                                    options: options
                                });

                            case 10:
                                item = _context.sent;
                                data = item.data;
                                options = item.options;

                                if (data && data.id) {
                                    currentId = data.id;
                                } else if (options.url && options.modelConf && options.modelConf.url) {
                                    match = options.url.match(options.modelConf.url + '/(.+)');

                                    if (match) {
                                        if (!isNaN(+match[1])) {
                                            currentId = +match[1];
                                        } else {
                                            currentId = match[1];
                                        }
                                    }
                                }

                                model = this._getModel(options.modelConf);

                                if (!model) {
                                    _context.next = 64;
                                    break;
                                }

                                applyState = options.applyState || this.applyState;

                                if (!(options.method === DELETE && currentId)) {
                                    _context.next = 40;
                                    break;
                                }

                                if (!(applyState === ON_SUCCESS)) {
                                    _context.next = 24;
                                    break;
                                }

                                commitType = model.expandActionType(DELETE);
                                type = commitType + SUBMIT;
                                rollbackType = commitType + ERROR;
                                _context.next = 37;
                                break;

                            case 24:
                                if (!(applyState === IMMEDIATE)) {
                                    _context.next = 30;
                                    break;
                                }

                                type = model.expandActionType(DELETE);
                                commitType = type + SUCCESS;
                                rollbackType = type + ERROR;
                                _context.next = 37;
                                break;

                            case 30:
                                if (!(applyState === LOCAL_ONLY)) {
                                    _context.next = 36;
                                    break;
                                }

                                type = model.expandActionType(DELETE);
                                commitType = null;
                                rollbackType = null;
                                _context.next = 37;
                                break;

                            case 36:
                                throw new Error('Unknown applyState ' + applyState);

                            case 37:
                                payload = currentId;
                                _context.next = 62;
                                break;

                            case 40:
                                if (!(applyState === ON_SUCCESS)) {
                                    _context.next = 47;
                                    break;
                                }

                                type = model.expandActionType(SUBMIT);
                                commitType = model.expandActionType(UPDATE);
                                rollbackType = model.expandActionType(ERROR);
                                payload = null;
                                _context.next = 62;
                                break;

                            case 47:
                                if (!(applyState === IMMEDIATE)) {
                                    _context.next = 54;
                                    break;
                                }

                                type = model.expandActionType(UPDATE);
                                commitType = model.expandActionType(SUCCESS);
                                rollbackType = model.expandActionType(ERROR);
                                payload = this._localUpdate(data, currentId, outboxId);
                                _context.next = 62;
                                break;

                            case 54:
                                if (!(applyState === LOCAL_ONLY)) {
                                    _context.next = 61;
                                    break;
                                }

                                type = model.expandActionType(UPDATE);
                                commitType = null;
                                rollbackType = null;
                                payload = this._localUpdate(data, currentId);
                                _context.next = 62;
                                break;

                            case 61:
                                throw new Error('Unknown applyState ' + applyState);

                            case 62:
                                _context.next = 65;
                                break;

                            case 64:
                                if (options.modelConf) {
                                    name = options.modelConf.name.toUpperCase();
                                    type = "".concat(name, "_").concat(SUBMIT);
                                    commitType = "".concat(name, "_").concat(SUCCESS);
                                    rollbackType = "".concat(name, "_").concat(ERROR);
                                } else {
                                    type = FORM_SUBMIT;
                                    commitType = FORM_SUCCESS;
                                    rollbackType = FORM_ERROR;
                                }

                            case 65:
                                if (!commitType) {
                                    _context.next = 73;
                                    break;
                                }

                                this.store.dispatch({
                                    type: type,
                                    payload: payload,
                                    meta: {
                                        offline: {
                                            effect: {
                                                data: data,
                                                options: options
                                            },
                                            commit: {
                                                type: commitType
                                            },
                                            rollback: {
                                                type: rollbackType
                                            }
                                        }
                                    }
                                });
                                _context.next = 69;
                                return this.loadItems();

                            case 69:
                                items = _context.sent;
                                return _context.abrupt("return", items.list[0]);

                            case 73:
                                this.store.dispatch({
                                    type: type,
                                    payload: payload
                                });
                                return _context.abrupt("return", null);

                            case 75:
                            case "end":
                                return _context.stop();
                        }
                    }
                }, _callee, this);
            }));

            function save(_x, _x2, _x3) {
                return _save.apply(this, arguments);
            }

            return save;
        }()
    }, {
        key: "_enqueue",
        value: function _enqueue(array, action, context) {
            var offline = action.meta.offline,
                _offline$effect = offline.effect,
                data = _offline$effect.data,
                options = _offline$effect.options;

            if (options.id) {
                var exist = array.find(function (act) {
                    return act.meta.outboxId === options.id;
                });

                if (exist) {
                    (options.preserve || []).forEach(function (field) {
                        if (data[field] === undefined) {
                            data[field] = exist.meta.offline.effect.data[field];
                        }
                    });
                    array = array.filter(function (act) {
                        return act.meta.outboxId !== options.id;
                    });
                }
            } else {
                options.id = action.meta.transaction;
            }

            action.meta.outboxId = options.id;

            if (!offline.commit) {
                offline.commit = {
                    type: "".concat(action.type, "_").concat(SUCCESS)
                };
            }

            if (!offline.commit.meta) {
                offline.commit.meta = {};
            }

            if (!offline.rollback) {
                offline.rollback = {
                    type: "".concat(action.type, "_").concat(ERROR)
                };
            }

            if (!offline.rollback.meta) {
                offline.rollback.meta = {};
            } // Copy action but exclude commit/rollback (to avoid recursive nesting)


            var offlineAction = _objectSpread2({}, action, {
                meta: _objectSpread2({}, action.meta, {
                    offline: {
                        effect: offline.effect
                    }
                })
            });

            offline.commit.meta.offlineAction = offlineAction;
            offline.rollback.meta.offlineAction = offlineAction;
            var currentId = action.payload && action.payload.id;

            if (currentId) {
                offline.commit.meta.currentId = currentId;
                offline.rollback.meta.currentId = currentId;
            }

            Object.keys(data || {}).forEach(function (key) {
                var match = data[key].match && data[key].match(/^outbox-(\d+)$/);

                if (match) {
                    if (!action.meta.parents) {
                        action.meta.parents = [];
                    }

                    action.meta.parents.push(+match[1]);
                }
            });
            return [].concat(_toConsumableArray(array), [action]);
        } // Validate a record before adding it to the outbox

    }, {
        key: "validate",
        value: function validate(data, options) {
            /* eslint no-unused-vars: off */
            return true;
        } // Send a single item from the outbox to the server

    }, {
        key: "sendItem",
        value: function sendItem() {
            throw new Error('sendItem() no longer supported; use waitForItem() instead');
        }
    }, {
        key: "_peek",
        value: function _peek(array, action, context) {
            var pending = array.filter(function (act) {
                if (act.meta.completed) {
                    return false;
                }

                if (act.meta.parents && act.meta.parents.length) {
                    return false;
                }

                return true;
            });

            if (this.batchService && pending.length && pending.length >= this.batchSizeMin) {
                var _action = this._createBatchAction(pending.slice(0, this.batchSizeMax));

                if (_action) {
                    return _action;
                }
            }

            return pending[0];
        }
    }, {
        key: "_effect",
        value: function () {
            var _effect3 = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee2(_ref, action) {
                var data, options, item, url, method, headers, csrftoken, defaults, urlObj;
                return _regeneratorRuntime.wrap(function _callee2$(_context2) {
                    while (1) {
                        switch (_context2.prev = _context2.next) {
                            case 0:
                                data = _ref.data, options = _ref.options;
                                _context2.next = 3;
                                return this._loadItemData({
                                    id: options.id,
                                    data: data,
                                    options: options
                                });

                            case 3:
                                item = _context2.sent;
                                data = item.data;
                                url = this.service;

                                if (options.url) {
                                    url = url + '/' + options.url;
                                }

                                method = options.method || this.syncMethod;
                                headers = {}; // Use current CSRF token in case it's changed since item was saved

                                csrftoken = this.csrftoken || options.csrftoken;

                                if (csrftoken) {
                                    headers['X-CSRFToken'] = csrftoken;

                                    if (!options.json) {
                                        data = _objectSpread2({}, data, _defineProperty({}, this.csrftokenField, csrftoken));
                                    }
                                }

                                defaults = _objectSpread2({}, this.defaults);

                                if (defaults.format && !this.formatKeyword) {
                                    url = url.replace(/\/$/, '');
                                    url += '.' + defaults.format;
                                    delete defaults.format;
                                }

                                urlObj = new URL(url, window.location.origin);
                                Object.entries(defaults).forEach(function (_ref2) {
                                    var _ref3 = _slicedToArray(_ref2, 2),
                                        key = _ref3[0],
                                        value = _ref3[1];

                                    return urlObj.searchParams.append(key, value);
                                });

                                if (this.debugNetwork) {
                                    console.log('Sending item to ' + urlObj.href);

                                    if (this.debugValues) {
                                        console.log(data);
                                    }
                                }

                                if (options.json) {
                                    headers['Content-Type'] = 'application/json';
                                    data = JSON.stringify(data);
                                } else {
                                    data = this._createFormData(data);
                                }

                                return _context2.abrupt("return", this.store.ajax(urlObj, data, method, headers).then(function (res) {
                                    if (!res && method === DELETE) {
                                        return action.payload;
                                    } else {
                                        return res;
                                    }
                                }));

                            case 18:
                            case "end":
                                return _context2.stop();
                        }
                    }
                }, _callee2, this);
            }));

            function _effect(_x4, _x5) {
                return _effect3.apply(this, arguments);
            }

            return _effect;
        }()
    }, {
        key: "_createFormData",
        value: function _createFormData(data) {
            var _this3 = this;

            // Use a FormData object to submit
            var formData = new FormData();
            Object.entries(data).forEach(function (_ref4) {
                var _ref5 = _slicedToArray(_ref4, 2),
                    key = _ref5[0],
                    val = _ref5[1];

                if (Array.isArray(val)) {
                    val.forEach(appendValue.bind(_this3, key));
                } else {
                    appendValue(key, val);
                }
            });

            function appendValue(key, val) {
                if (val && val.name && val.type && val.body) {
                    // File (Blob) record; add with filename
                    var blob = val.body;

                    if (!blob.type) {
                        // Serialized blobs lose their type
                        var slice = blob.slice || blob.webkitSlice;
                        blob = slice.call(blob, 0, blob.size, val.type);
                    }

                    formData.append(key, blob, val.name);
                } else {
                    // Add regular form fields
                    formData.append(key, val);
                }
            }

            return formData;
        }
    }, {
        key: "_createBatchAction",
        value: function _createBatchAction(actions) {
            var _this4 = this;

            var loadEffect = function loadEffect(action) {
                var effect = action.meta.offline.effect,
                    options = effect.options;
                var data;

                if (!options.storage) {
                    data = effect.data;
                } else if (options.storage === 'temporary') {
                    data = _classPrivateFieldGet(_this4, _memoryItems)[options.id];
                } else {
                    throw new Error('Binary submissions not currently supported in batch mode.');
                }

                data = _this4._parseJsonForm({
                    data: data
                }).data;
                return {
                    data: data,
                    options: options
                };
            };

            var effects;

            try {
                effects = actions.map(loadEffect);
            } catch (e) {
                console.warn(e);
                return false;
            }

            return {
                type: BATCH_SUBMIT,
                meta: {
                    offline: {
                        effect: {
                            data: effects.map(function (effect) {
                                var data = effect.data,
                                    options = effect.options;
                                return {
                                    url: _this4.store.service + '/' + options.url,
                                    method: options.method || _this4.syncMethod,
                                    headers: {
                                        'Content-Type': 'application/json',
                                        Accept: 'application/json',
                                        'X-CSRFToken': _this4.csrftoken
                                    },
                                    body: JSON.stringify(data)
                                };
                            }),
                            options: {
                                url: this.batchService,
                                json: true
                            }
                        },
                        commit: {
                            type: BATCH_SUCCESS,
                            meta: {
                                actions: actions
                            }
                        },
                        rollback: {
                            type: BATCH_ERROR,
                            meta: {
                                actions: actions
                            }
                        }
                    }
                }
            };
        }
    }, {
        key: "_processBatchResponse",
        value: function _processBatchResponse(batchAction) {
            var responses, batchError;

            if (batchAction.type == BATCH_SUCCESS) {
                if (Array.isArray(batchAction.payload)) {
                    responses = batchAction.payload;
                }
            } else {
                // batchAction.type == BATCH_ERROR
                if (batchAction.payload) {
                    batchError = batchAction.payload;
                } else {
                    batchError = new Error('Batch submission error');
                }
            }

            return batchAction.meta.actions.map(function (action, i) {
                var resp = responses ? responses[i] : null,
                    offline = action.meta.offline,
                    commit = offline.commit,
                    rollback = offline.rollback;
                var nextAction;

                if (resp && resp.status_code >= 200 && resp.status_code <= 299) {
                    var payload;

                    try {
                        payload = JSON.parse(resp.body);
                    } catch (e) {
                        payload = resp.body;
                    }

                    nextAction = _objectSpread2({}, commit, {
                        payload: payload,
                        meta: _objectSpread2({}, commit.meta, {
                            success: true
                        })
                    });
                } else {
                    var error;

                    if (resp && resp.body) {
                        error = new Error();

                        try {
                            error.json = JSON.parse(resp.body);
                        } catch (e) {
                            error.text = resp.body;
                        }

                        error.status = resp.status_code;
                    } else if (batchError) {
                        error = batchError;
                    } else {
                        error = new Error('Missing from batch response');
                    }

                    nextAction = _objectSpread2({}, rollback, {
                        payload: error,
                        meta: _objectSpread2({}, rollback.meta, {
                            success: false
                        })
                    });
                }

                return nextAction;
            });
        }
    }, {
        key: "_dispatchBatchResponse",
        value: function _dispatchBatchResponse(batchAction, dispatch) {
            this._processBatchResponse(batchAction).forEach(function (nextAction) {
                var action = _objectSpread2({}, nextAction, {
                    meta: _objectSpread2({}, nextAction.meta)
                }); // Avoid double-dequeue


                delete action.meta.offlineAction;
                dispatch(action);
            });
        }
    }, {
        key: "_localUpdate",
        value: function _localUpdate(data, currentId, outboxId) {
            data = this._parseJsonForm({
                data: data
            }).data;

            if (!data.hasOwnProperty('id')) {
                if (currentId) {
                    data.id = currentId;
                } else if (outboxId) {
                    data.id = 'outbox-' + outboxId;
                }
            }

            return data;
        }
    }, {
        key: "_updateParents",
        value: function _updateParents(item, outboxId, resultId) {
            if (item.meta.parents.indexOf(outboxId) === -1) {
                return item;
            }

            var data = _objectSpread2({}, item.meta.offline.effect.data);

            Object.keys(data).forEach(function (key) {
                if (data[key] === 'outbox-' + outboxId) {
                    data[key] = resultId;
                }
            });
            return _objectSpread2({}, item, {
                meta: _objectSpread2({}, item.meta, {
                    offline: _objectSpread2({}, item.meta.offline, {
                        effect: _objectSpread2({}, item.meta.offline.effect, {
                            data: data
                        })
                    }),
                    parents: item.meta.parents.filter(function (pid) {
                        return pid != outboxId;
                    })
                })
            });
        }
    }, {
        key: "_discard",
        value: function _discard(error, action, retries) {
            var options = action.meta.offline.effect.options;

            if (this.debugNetwork) {
                console.warn('Error sending item to ' + options.url);
                console.error(error);
            }

            return defaultDiscard(error, action, retries || 0);
        }
    }, {
        key: "_retry",
        value: function _retry(action, retries) {
            var options = action.meta.offline.effect.options;

            if (options.once) {
                return null;
            } else if (retries > this.maxRetries) {
                return null;
            }

            return defaultRetry(action, retries);
        }
    }, {
        key: "removeItem",
        value: function removeItem(id) {
            return this.removeItems([id]);
        }
    }, {
        key: "removeItems",
        value: function removeItems(ids) {
            return this.store.dispatch({
                type: REMOVE_ITEMS,
                payload: ids,
                meta: {
                    completed: true
                }
            });
        }
    }, {
        key: "empty",
        value: function () {
            var _empty = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee3() {
                return _regeneratorRuntime.wrap(function _callee3$(_context3) {
                    while (1) {
                        switch (_context3.prev = _context3.next) {
                            case 0:
                                this.store.dispatch({
                                    type: reduxOffline.RESET_STATE
                                });
                                _context3.next = 3;
                                return this._cleanUpItemData();

                            case 3:
                            case "end":
                                return _context3.stop();
                        }
                    }
                }, _callee3, this);
            }));

            function empty() {
                return _empty.apply(this, arguments);
            }

            return empty;
        }()
    }, {
        key: "retryItem",
        value: function retryItem(id) {
            return this.retryItems([id]);
        }
    }, {
        key: "retryItems",
        value: function retryItems(ids) {
            return this.store.dispatch({
                type: RETRY_ITEMS,
                payload: ids,
                meta: {
                    completed: true
                }
            });
        }
    }, {
        key: "retryAll",
        value: function () {
            var _retryAll = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee4() {
                var unsynced;
                return _regeneratorRuntime.wrap(function _callee4$(_context4) {
                    while (1) {
                        switch (_context4.prev = _context4.next) {
                            case 0:
                                _context4.next = 2;
                                return this.unsyncedItems();

                            case 2:
                                unsynced = _context4.sent;
                                this.retryItems(unsynced.map(function (item) {
                                    return item.id;
                                }));
                                _context4.next = 6;
                                return this.waitForAll();

                            case 6:
                            case "end":
                                return _context4.stop();
                        }
                    }
                }, _callee4, this);
            }));

            function retryAll() {
                return _retryAll.apply(this, arguments);
            }

            return retryAll;
        }()
    }, {
        key: "sendAll",
        value: function sendAll() {
            throw new Error('sendall() no longer supported; use retryAll() and/or waitForAll() instead');
        }
    }, {
        key: "_dequeue",
        value: function _dequeue(array, action, context) {
            var _this5 = this;

            if (action.type === REMOVE_ITEMS) {
                return array.filter(function (item) {
                    return action.payload.indexOf(item.meta.outboxId) === -1;
                });
            } else if (action.type === RETRY_ITEMS) {
                return array.map(function (item) {
                    if (action.payload.indexOf(item.meta.outboxId) === -1) {
                        return item;
                    } else {
                        return _objectSpread2({}, item, {
                            meta: _objectSpread2({}, item.meta, {
                                completed: false,
                                success: undefined
                            })
                        });
                    }
                });
            } else if (action.type == BATCH_SUCCESS || action.type == BATCH_ERROR) {
                this._processBatchResponse(action).forEach(function (nextAction) {
                    array = _this5._dequeue(array, nextAction, context);
                });

                return array;
            } else if (action.meta.offlineAction) {
                // Mark status but don't remove item completely
                var outboxId = action.meta.offlineAction.meta.outboxId;

                if (!outboxId) {
                    return array;
                }

                return array.map(function (item) {
                    if (item.meta.outboxId === outboxId) {
                        return _this5._applyResult(item, action);
                    } else if (item.meta.parents && action.meta.success) {
                        return _this5._updateParents(item, outboxId, action.payload.id);
                    } else {
                        return item;
                    }
                });
            } else {
                return array;
            }
        }
    }, {
        key: "pause",
        value: function pause() {
            this.store.dispatch(reduxOffline.busy(true));
        }
    }, {
        key: "resume",
        value: function resume() {
            this.store.dispatch(reduxOffline.busy(false));
        }
    }, {
        key: "waitForAll",
        value: function waitForAll() {
            return this.waitForItem('ALL');
        }
    }, {
        key: "waitForItem",
        value: function waitForItem(id) {
            var resolve;
            var promise = new Promise(function (res) {
                return resolve = res;
            });

            if (!_classPrivateFieldGet(this, _waiting)[id]) {
                _classPrivateFieldGet(this, _waiting)[id] = [];
            }

            _classPrivateFieldGet(this, _waiting)[id].push(resolve);

            return promise;
        }
    }, {
        key: "_onUpdate",
        value: function () {
            var _onUpdate2 = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee5() {
                var _this6 = this;

                var state, offline, outbox, lastIds, pending, pendingById, checkIds;
                return _regeneratorRuntime.wrap(function _callee5$(_context5) {
                    while (1) {
                        switch (_context5.prev = _context5.next) {
                            case 0:
                                state = this.store.getState(), offline = state.offline, outbox = offline.outbox;

                                if (!(outbox === _classPrivateFieldGet(this, _lastOutbox))) {
                                    _context5.next = 3;
                                    break;
                                }

                                return _context5.abrupt("return");

                            case 3:
                                lastIds = {};

                                _classPrivateFieldGet(this, _lastOutbox).forEach(function (action) {
                                    lastIds[action.meta.offline.effect.options.id] = true;
                                });

                                _classPrivateFieldSet(this, _lastOutbox, outbox);

                                _context5.next = 8;
                                return this._allPendingItems();

                            case 8:
                                pending = _context5.sent;

                                if (!pending.length && _classPrivateFieldGet(this, _waiting)['ALL']) {
                                    this._resolveWaiting('ALL');
                                }

                                pendingById = {};
                                pending.forEach(function (item) {
                                    return pendingById[item.id] = true;
                                });
                                checkIds = Object.keys(lastIds).concat(Object.keys(_classPrivateFieldGet(this, _waiting)));
                                checkIds.forEach(function (id) {
                                    if (!pendingById[id] && id != 'ALL') {
                                        _this6._resolveWaiting(id);
                                    }
                                });

                            case 14:
                            case "end":
                                return _context5.stop();
                        }
                    }
                }, _callee5, this);
            }));

            function _onUpdate() {
                return _onUpdate2.apply(this, arguments);
            }

            return _onUpdate;
        }()
    }, {
        key: "_resolveWaiting",
        value: function () {
            var _resolveWaiting2 = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee6(id) {
                var waiting, item;
                return _regeneratorRuntime.wrap(function _callee6$(_context6) {
                    while (1) {
                        switch (_context6.prev = _context6.next) {
                            case 0:
                                waiting = _classPrivateFieldGet(this, _waiting)[id];

                                if (!(!waiting && !(this.app && this.app.hasPlugin('onsync')))) {
                                    _context6.next = 3;
                                    break;
                                }

                                return _context6.abrupt("return");

                            case 3:
                                if (!(id === 'ALL')) {
                                    _context6.next = 7;
                                    break;
                                }

                                _context6.t0 = null;
                                _context6.next = 10;
                                break;

                            case 7:
                                _context6.next = 9;
                                return this.loadItem(+id);

                            case 9:
                                _context6.t0 = _context6.sent;

                            case 10:
                                item = _context6.t0;

                                if (this.app && id != 'ALL') {
                                    this.app.callPlugins('onsync', [item]);
                                }

                                if (waiting) {
                                    waiting.forEach(function (fn) {
                                        return fn(item);
                                    });
                                    delete _classPrivateFieldGet(this, _waiting)[id];
                                }

                            case 13:
                            case "end":
                                return _context6.stop();
                        }
                    }
                }, _callee6, this);
            }));

            function _resolveWaiting(_x6) {
                return _resolveWaiting2.apply(this, arguments);
            }

            return _resolveWaiting;
        }() // Process service send() results

    }, {
        key: "_applyResult",
        value: function _applyResult(item, action) {
            if (this.applyResult) {
                console.warn('applyResult() override no longer called');
            }

            var newItem = _objectSpread2({}, item, {
                meta: _objectSpread2({}, item.meta, {
                    success: action.meta.success,
                    completed: true
                })
            });

            if (newItem.meta.success) {
                if (this.debugNetwork) {
                    console.log('Item successfully sent to ' + item.meta.offline.effect.options.url);
                }

                newItem.meta.result = action.payload;
            } else {
                newItem.meta.error = action.payload;
            }

            return newItem;
        }
    }, {
        key: "_getModel",
        value: function _getModel(conf) {
            if (!conf || !conf.name || !conf.list) {
                return null;
            }

            return model(_objectSpread2({
                store: this.store
            }, conf));
        }
    }, {
        key: "loadItems",
        value: function () {
            var _loadItems = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee7() {
                var actions, items;
                return _regeneratorRuntime.wrap(function _callee7$(_context7) {
                    while (1) {
                        switch (_context7.prev = _context7.next) {
                            case 0:
                                actions = this.store.getState().offline.outbox;
                                items = actions.map(function (action) {
                                    var _action$meta$offline$ = action.meta.offline.effect,
                                        data = _action$meta$offline$.data,
                                        options = _action$meta$offline$.options;
                                    var item = {
                                        id: options.id,
                                        data: data,
                                        options: _objectSpread2({}, options),
                                        synced: !!action.meta.success
                                    };
                                    delete item.options.id;

                                    if (action.meta.parents) {
                                        item.parents = action.meta.parents;
                                    }

                                    if (action.meta.success) {
                                        item.result = action.meta.result;
                                    } else if (action.meta.completed) {
                                        var error = action.meta.error;

                                        if (error) {
                                            item.error = error.json || error.text || error.status || '' + error;
                                        } else {
                                            item.error = 'Error';
                                        }
                                    }

                                    return item;
                                }).sort(function (a, b) {
                                    return b.id - a.id;
                                });
                                return _context7.abrupt("return", {
                                    list: items,
                                    count: items.length,
                                    pages: 1,
                                    per_page: items.length
                                });

                            case 3:
                            case "end":
                                return _context7.stop();
                        }
                    }
                }, _callee7, this);
            }));

            function loadItems() {
                return _loadItems.apply(this, arguments);
            }

            return loadItems;
        }() // Count of unsynced outbox items (never synced, or sync was unsuccessful)

    }, {
        key: "unsynced",
        value: function () {
            var _unsynced = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee8(modelConf) {
                var items;
                return _regeneratorRuntime.wrap(function _callee8$(_context8) {
                    while (1) {
                        switch (_context8.prev = _context8.next) {
                            case 0:
                                _context8.next = 2;
                                return this.unsyncedItems(modelConf);

                            case 2:
                                items = _context8.sent;
                                return _context8.abrupt("return", items.length);

                            case 4:
                            case "end":
                                return _context8.stop();
                        }
                    }
                }, _callee8, this);
            }));

            function unsynced(_x7) {
                return _unsynced.apply(this, arguments);
            }

            return unsynced;
        }() // Actual unsynced items

    }, {
        key: "unsyncedItems",
        value: function () {
            var _unsyncedItems = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee9(modelConf, withData) {
                var _this7 = this;

                var items;
                return _regeneratorRuntime.wrap(function _callee9$(_context9) {
                    while (1) {
                        switch (_context9.prev = _context9.next) {
                            case 0:
                                _context9.next = 2;
                                return this.loadItems();

                            case 2:
                                _context9.t0 = function (item) {
                                    return !item.synced;
                                };

                                items = _context9.sent.list.filter(_context9.t0);
                                // Exclude temporary items from list
                                items = items.filter(function (item) {
                                    if (item.options.storage == 'temporary') {
                                        if (item.options.desiredStorage) {
                                            return true;
                                        }

                                        return false;
                                    } else {
                                        return true;
                                    }
                                });
                                if (modelConf) // Only match items corresponding to the specified list
                                    items = items.filter(function (item) {
                                        if (!item.options.modelConf) {
                                            return false;
                                        }

                                        for (var key in modelConf) {
                                            if (item.options.modelConf[key] != modelConf[key]) {
                                                return false;
                                            }
                                        }

                                        return true;
                                    });

                                if (!withData) {
                                    _context9.next = 12;
                                    break;
                                }

                                _context9.next = 9;
                                return Promise.all(items.map(function (item) {
                                    return _this7._loadItemData(item);
                                }));

                            case 9:
                                return _context9.abrupt("return", _context9.sent);

                            case 12:
                                return _context9.abrupt("return", items);

                            case 13:
                            case "end":
                                return _context9.stop();
                        }
                    }
                }, _callee9, this);
            }));

            function unsyncedItems(_x8, _x9) {
                return _unsyncedItems.apply(this, arguments);
            }

            return unsyncedItems;
        }() // Unsynced items that have not been attempted (or retried)

    }, {
        key: "pendingItems",
        value: function () {
            var _pendingItems = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee10(modelConf, withData) {
                var unsynced;
                return _regeneratorRuntime.wrap(function _callee10$(_context10) {
                    while (1) {
                        switch (_context10.prev = _context10.next) {
                            case 0:
                                _context10.next = 2;
                                return this.unsyncedItems(modelConf, withData);

                            case 2:
                                unsynced = _context10.sent;
                                return _context10.abrupt("return", unsynced.filter(function (item) {
                                    return !item.hasOwnProperty('error');
                                }));

                            case 4:
                            case "end":
                                return _context10.stop();
                        }
                    }
                }, _callee10, this);
            }));

            function pendingItems(_x10, _x11) {
                return _pendingItems.apply(this, arguments);
            }

            return pendingItems;
        }()
    }, {
        key: "_pendingTempItems",
        value: function () {
            var _pendingTempItems2 = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee11() {
                return _regeneratorRuntime.wrap(function _callee11$(_context11) {
                    while (1) {
                        switch (_context11.prev = _context11.next) {
                            case 0:
                                _context11.next = 2;
                                return this.loadItems();

                            case 2:
                                _context11.t0 = function (item) {
                                    return item.options.storage === 'temporary' && !item.synced && !item.error;
                                };

                                return _context11.abrupt("return", _context11.sent.list.filter(_context11.t0));

                            case 4:
                            case "end":
                                return _context11.stop();
                        }
                    }
                }, _callee11, this);
            }));

            function _pendingTempItems() {
                return _pendingTempItems2.apply(this, arguments);
            }

            return _pendingTempItems;
        }()
    }, {
        key: "_allPendingItems",
        value: function () {
            var _allPendingItems2 = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee12() {
                var pendingStore, pendingTemp;
                return _regeneratorRuntime.wrap(function _callee12$(_context12) {
                    while (1) {
                        switch (_context12.prev = _context12.next) {
                            case 0:
                                _context12.next = 2;
                                return this.pendingItems();

                            case 2:
                                pendingStore = _context12.sent;
                                _context12.next = 5;
                                return this._pendingTempItems();

                            case 5:
                                pendingTemp = _context12.sent;
                                return _context12.abrupt("return", pendingStore.concat(pendingTemp));

                            case 7:
                            case "end":
                                return _context12.stop();
                        }
                    }
                }, _callee12, this);
            }));

            function _allPendingItems() {
                return _allPendingItems2.apply(this, arguments);
            }

            return _allPendingItems;
        }()
    }, {
        key: "loadItem",
        value: function () {
            var _loadItem = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee13(itemId) {
                var item;
                return _regeneratorRuntime.wrap(function _callee13$(_context13) {
                    while (1) {
                        switch (_context13.prev = _context13.next) {
                            case 0:
                                _context13.next = 2;
                                return this.loadItems();

                            case 2:
                                _context13.t0 = function (item) {
                                    return item.id === itemId;
                                };

                                item = _context13.sent.list.find(_context13.t0);
                                _context13.next = 6;
                                return this._loadItemData(item);

                            case 6:
                                item = _context13.sent;
                                return _context13.abrupt("return", this._parseJsonForm(item));

                            case 8:
                            case "end":
                                return _context13.stop();
                        }
                    }
                }, _callee13, this);
            }));

            function loadItem(_x12) {
                return _loadItem.apply(this, arguments);
            }

            return loadItem;
        }()
    }, {
        key: "_loadItemData",
        value: function () {
            var _loadItemData2 = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee14(item) {
                var setData;
                return _regeneratorRuntime.wrap(function _callee14$(_context14) {
                    while (1) {
                        switch (_context14.prev = _context14.next) {
                            case 0:
                                setData = function _ref6(obj, data) {
                                    if (data) {
                                        obj.data = data;
                                    } else {
                                        obj.label = '[Form Data Missing]';
                                        obj.missing = true;
                                    }

                                    return obj;
                                };

                                if (!(!item || !item.options || !item.options.storage)) {
                                    _context14.next = 5;
                                    break;
                                }

                                return _context14.abrupt("return", item);

                            case 5:
                                if (!(item.options.storage == 'temporary')) {
                                    _context14.next = 9;
                                    break;
                                }

                                return _context14.abrupt("return", setData(item, _classPrivateFieldGet(this, _memoryItems)[item.id]));

                            case 9:
                                return _context14.abrupt("return", this.store.lf.getItem('outbox_' + item.id).then(function (data) {
                                    return setData(item, data);
                                }, function () {
                                    return setData(item, null);
                                }));

                            case 10:
                            case "end":
                                return _context14.stop();
                        }
                    }
                }, _callee14, this);
            }));

            function _loadItemData(_x13) {
                return _loadItemData2.apply(this, arguments);
            }

            return _loadItemData;
        }()
    }, {
        key: "_parseJsonForm",
        value: function _parseJsonForm(item) {
            if (!item || !item.data) {
                return item;
            }

            var values = [],
                key;

            for (key in item.data) {
                values.push({
                    name: key,
                    value: item.data[key]
                });
            }

            item.data = jsonForms.convert(values);

            for (key in item.data) {
                if (Array.isArray(item.data[key])) {
                    item.data[key].forEach(function (row, i) {
                        row['@index'] = i;
                    });
                }
            }

            return item;
        }
    }, {
        key: "_updateItemData",
        value: function () {
            var _updateItemData2 = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee15(item) {
                var _this8 = this;

                return _regeneratorRuntime.wrap(function _callee15$(_context15) {
                    while (1) {
                        switch (_context15.prev = _context15.next) {
                            case 0:
                                if (item.data) {
                                    _context15.next = 2;
                                    break;
                                }

                                return _context15.abrupt("return", item);

                            case 2:
                                if (!(!item.options || !item.options.storage)) {
                                    _context15.next = 4;
                                    break;
                                }

                                return _context15.abrupt("return", item);

                            case 4:
                                if (!(item.options.storage == 'temporary')) {
                                    _context15.next = 9;
                                    break;
                                }

                                _classPrivateFieldGet(this, _memoryItems)[item.id] = item.data;
                                return _context15.abrupt("return", this._withoutData(item));

                            case 9:
                                return _context15.abrupt("return", this.store.lf.setItem('outbox_' + item.id, item.data).then(function () {
                                    return _this8._withoutData(item);
                                }, function () {
                                    console.warn('could not save form contents to storage');
                                    item.options.desiredStorage = item.options.storage;
                                    item.options.storage = 'temporary';
                                    return _this8._updateItemData(item);
                                }));

                            case 10:
                            case "end":
                                return _context15.stop();
                        }
                    }
                }, _callee15, this);
            }));

            function _updateItemData(_x14) {
                return _updateItemData2.apply(this, arguments);
            }

            return _updateItemData;
        }()
    }, {
        key: "_withoutData",
        value: function _withoutData(item) {
            if (!item.data) {
                return item;
            }

            if (!item.options || !item.options.storage) {
                return item;
            }

            var obj = {};
            Object.keys(item).filter(function (key) {
                return key != 'data';
            }).forEach(function (key) {
                obj[key] = item[key];
            });
            return obj;
        }
    }, {
        key: "_cleanUpItemData",
        value: function () {
            var _cleanUpItemData2 = _asyncToGenerator(
            /*#__PURE__*/
            _regeneratorRuntime.mark(function _callee16() {
                var _this9 = this;

                var validId, validItems, keys;
                return _regeneratorRuntime.wrap(function _callee16$(_context16) {
                    while (1) {
                        switch (_context16.prev = _context16.next) {
                            case 0:
                                validId = {};
                                _context16.next = 3;
                                return this.loadItems();

                            case 3:
                                validItems = _context16.sent.list;
                                validItems.forEach(function (item) {
                                    validId[item.id] = true;
                                });
                                Object.keys(_classPrivateFieldGet(this, _memoryItems)).forEach(function (itemId) {
                                    if (!validId[itemId]) {
                                        delete _classPrivateFieldGet(_this9, _memoryItems)[itemId];
                                    }
                                });
                                _context16.next = 8;
                                return this.store.lf.keys();

                            case 8:
                                keys = _context16.sent;
                                _context16.next = 11;
                                return Promise.all(keys.filter(function (key) {
                                    return key.indexOf('outbox_') === 0;
                                }).map(function (key) {
                                    return key.replace('outbox_', '');
                                }).filter(function (itemId) {
                                    return !validId[itemId];
                                }).map(function (itemId) {
                                    return _this9.store.lf.removeItem('outbox_' + itemId);
                                }));

                            case 11:
                            case "end":
                                return _context16.stop();
                        }
                    }
                }, _callee16, this);
            }));

            function _cleanUpItemData() {
                return _cleanUpItemData2.apply(this, arguments);
            }

            return _cleanUpItemData;
        }()
    }, {
        key: "_serialize",
        value: function _serialize(state) {
            var _this10 = this;

            return _objectSpread2({}, state, {
                outbox: state.outbox.map(function (action) {
                    return _this10._serializeAction(action);
                })
            });
        }
    }, {
        key: "_serializeAction",
        value: function _serializeAction(action) {
            if (!action.meta || !action.meta.error) {
                return action;
            }

            var error = {};
            ['json', 'text', 'status'].forEach(function (key) {
                if (key in action.meta.error) {
                    error[key] = action.meta.error[key];
                }
            });

            if (!Object.keys(error).length) {
                error.text = '' + action.meta.error;
            }

            return _objectSpread2({}, action, {
                meta: _objectSpread2({}, action.meta, {
                    error: error
                })
            });
        }
    }, {
        key: "_deserialize",
        value: function _deserialize(state) {
            return state;
        }
    }]);

    return Outbox;
}();

var _waiting = new WeakMap();

var _lastOutbox = new WeakMap();

var _memoryItems = new WeakMap();

var outbox = new Outbox(ds);

function getOutbox(store) {
    if (_outboxes[store.name]) {
        return _outboxes[store.name];
    } else {
        return new Outbox(store);
    }
}

outbox.getOutbox = getOutbox;

exports.Outbox = Outbox;
exports.default = outbox;
exports.getOutbox = getOutbox;

Object.defineProperty(exports, '__esModule', { value: true });

});
//# sourceMappingURL=outbox.js.map
