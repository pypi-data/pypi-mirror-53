/*
 * wq.app v1.2.0b1 - @wq/app 1.2.0-beta.1
 * Utilizes @wq/store and @wq/router to dynamically load and render content from a wq.db-compatible REST service
 * (c) 2012-2019, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['regenerator-runtime', 'jquery.mobile', './store', './model', './outbox', './template', './router', './spinner'], function (_regeneratorRuntime, jQM, ds, modelModule, outbox, tmpl, router, spinner) { 'use strict';

_regeneratorRuntime = _regeneratorRuntime && _regeneratorRuntime.hasOwnProperty('default') ? _regeneratorRuntime['default'] : _regeneratorRuntime;
jQM = jQM && jQM.hasOwnProperty('default') ? jQM['default'] : jQM;
ds = ds && ds.hasOwnProperty('default') ? ds['default'] : ds;
modelModule = modelModule && modelModule.hasOwnProperty('default') ? modelModule['default'] : modelModule;
outbox = outbox && outbox.hasOwnProperty('default') ? outbox['default'] : outbox;
tmpl = tmpl && tmpl.hasOwnProperty('default') ? tmpl['default'] : tmpl;
router = router && router.hasOwnProperty('default') ? router['default'] : router;
spinner = spinner && spinner.hasOwnProperty('default') ? spinner['default'] : spinner;

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

function _arrayWithHoles(arr) {
  if (Array.isArray(arr)) return arr;
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

function _nonIterableRest() {
  throw new TypeError("Invalid attempt to destructure non-iterable instance");
}

var app = {
    OFFLINE: 'offline',
    FAILURE: 'failure',
    ERROR: 'error',

    get wq_config() {
        return this.getAuthState().config || this.config;
    },

    get user() {
        return this.getAuthState().user;
    },

    get csrftoken() {
        return this.getAuthState().csrftoken;
    }

};
var SERVER = '@@SERVER',
    LOGIN_SUCCESS = 'LOGIN_SUCCESS',
    LOGIN_RELOAD = 'LOGIN_RELOAD',
    CSRFTOKEN = 'CSRFTOKEN',
    LOGOUT = '@@LOGOUT';
app.models = {};
app.plugins = {};
var _register = {},
    _onShow = {};
var $, jqm;

app.init = function (config) {
    app.jQuery = $ = config.jQuery || window.jQuery || jQM();
    jqm = $.mobile || jQM().mobile;
    app.use(spinner);
    app.use(syncRefresh);
    app.use(showOutboxErrors);
    router.addContext(function () {
        return spinner.start() && {};
    });
    router.addContext(_getRouteInfo);
    router.addContext(app.userInfo);
    router.addContext(_getSyncInfo);
    router.addThunk(LOGIN_SUCCESS, _refreshUserInfo);
    router.addThunk(LOGIN_RELOAD, _refreshUserInfo);
    router.addThunk(LOGOUT, _refreshUserInfo);
    router.addThunk(CSRFTOKEN, _refreshCSRFToken); // Router (wq/router.js) configuration

    if (!config.router) {
        config.router = {
            base_url: ''
        };
    }

    config.router.getTemplateName = getTemplateName; // Store (wq/store.js) configuration

    if (!config.store) {
        config.store = {
            service: config.router.base_url,
            defaults: {
                format: 'json'
            }
        };
    }

    if (!config.store.fetchFail) {
        config.fetchFail = _fetchFail;
    }

    ds.addReducer('auth', _authReducer, true);
    Object.entries(app.plugins).forEach(function (_ref) {
        var _ref2 = _slicedToArray(_ref, 2),
            name = _ref2[0],
            plugin = _ref2[1];

        if (plugin.ajax) {
            config.store.ajax = plugin.ajax;
        }

        if (plugin.reducer) {
            ds.addReducer(name, function (state, action) {
                return plugin.reducer(state, action);
            });
        }

        if (plugin.render) {
            router.addRender(function (state) {
                return plugin.render(state);
            });
        }

        if (plugin.actions) {
            Object.assign(plugin, ds.bindActionCreators(plugin.actions));
        }

        if (plugin.thunks) {
            router.addThunks(plugin.thunks);
        }
    });
    app.spin = {
        start: function start(msg, duration, opts) {
            return spinner.start(msg, duration, opts);
        },
        forSeconds: function forSeconds(duration) {
            return spinner.start(null, duration);
        },
        stop: function stop() {
            return spinner.stop();
        }
    }; // Outbox (wq/outbox.js) configuration

    if (!config.outbox) {
        config.outbox = {};
    } // Propagate debug setting to other modules


    if (config.debug) {
        config.router.debug = config.debug;
        config.store.debug = config.debug;
        config.template.debug = config.debug;
    } // Copy jQuery to plugins (in case not set globally)


    ['router', 'template'].concat(Object.keys(app.plugins)).forEach(function (key) {
        if (!config[key]) {
            config[key] = {};
        }

        config[key].jQuery = $;
    }); // Load missing (non-local) content as JSON, or as server-rendered HTML?
    // Default (as of 1.0) is to load JSON and render on client.

    config.loadMissingAsJson = config.loadMissingAsJson || !config.loadMissingAsHtml;
    config.loadMissingAsHtml = !config.loadMissingAsJson; // After a form submission, sync in the background, or wait before
    // continuing?  Default is to sync in the background.

    config.backgroundSync = config.backgroundSync || !config.noBackgroundSync;
    config.noBackgroundSync = !config.backgroundSync;
    app.config = config;
    app['native'] = !!window.cordova;
    app.can_login = !!config.pages.login; // Initialize wq/router.js

    router.init(config.router);
    app.base_url = router.base_url;
    app.store = ds;
    app.outbox = outbox;
    outbox.app = app;
    app.router = router; // Initialize wq/template.js

    tmpl.init(config.template); // Option to submit forms in the background rather than wait for each post

    if (config.backgroundSync) {
        if (config.backgroundSync === -1) {
            outbox.pause();
        }
    } // Deprecated hooks


    var deprecated = {
        postsave: 'a postsaveurl() plugin hook or a postsave page config',
        saveerror: 'an onsync() plugin hook',
        showOutboxErrors: 'an onsync() and/or run() hook',
        _addOutboxItemsToContext: "@wq/outbox's IMMEDIATE mode",
        presync: 'the template context',
        postsync: 'the template context or an onsync() plugin hook'
    };
    Object.entries(deprecated).forEach(function (_ref3) {
        var _ref4 = _slicedToArray(_ref3, 2),
            hook = _ref4[0],
            alternative = _ref4[1];

        // TODO: Make this an error in 2.0
        if (config[hook]) {
            console.warn(new Error("config.".concat(hook, " has no effect.  Use ").concat(alternative, " instead.  See wq.app 1.2 release notes for more info.")));
        }
    });

    if (app.hasPlugin('onsave')) {
        console.warn(new Error('An onsave() plugin hook has no effect.  Use an onsync() hook instead.  See wq.app 1.2 release notes for more info.'));
    } // Configure jQuery Mobile transitions


    if (config.transitions) {
        var def = 'default';

        if (config.transitions[def]) {
            jqm.defaultPageTransition = config.transitions[def];
        }

        if (config.transitions.dialog) {
            jqm.defaultDialogTransition = config.transitions.dialog;
        }

        jqm.maxTransitionWidth = config.transitions.maxwidth || 800;
    }

    Object.keys(app.config.pages).forEach(function (page) {
        app.config.pages[page].name = page;
    });
    app.callPlugins('init'); // Register routes with wq/router.js

    var root = false;
    Object.keys(app.config.pages).forEach(function (page) {
        var conf = _getBaseConf(page);

        if (!conf.url) {
            root = true;
        }

        if (conf.list) {
            conf.modes.forEach(function (mode) {
                var register = _register[mode] || _register.detail;
                var onShow = _onShow[mode] || _onShow.detail;
                register(page, mode);
                onShow(page, mode);
            });
            (conf.server_modes || []).forEach(function (mode) {
                _register.detail(page, mode, _serverContext);

                var onShow = _onShow[mode] || _onShow.detail;
                onShow(page, mode);
            });
            app.models[page] = modelModule(conf);
        } else if (conf) {
            _registerOther(page);

            _onShowOther(page);
        }
    }); // Register outbox

    router.register('outbox', 'outbox', function () {
        return outbox.loadItems();
    });
    router.onShow('outbox', app.runPlugins);
    router.register('outbox/<slug>', 'outbox_detail', _renderOutboxItem);
    router.register('outbox/<slug>/edit', 'outbox_edit', _renderOutboxItem);
    router.onShow('outbox_detail', app.runPlugins);
    router.onShow('outbox_edit', app.runPlugins); // Fallback index page

    if (!root && !app.config.pages.index && config.template.templates.index) {
        router.registerLast('', 'index', function (ctx) {
            var context = {};
            context.pages = Object.keys(app.config.pages).map(function (page) {
                var conf = app.config.pages[page];
                return {
                    name: page,
                    url: conf.url,
                    list: conf.list
                };
            });
            return context;
        });
    } // Fallback for all other URLs


    router.registerLast(':path*', SERVER, _serverContext); // Handle form events

    $(document).on('submit', 'form', _handleForm);
    $(document).on('click', 'form [type=submit]', _submitClick);
    Object.entries(app.plugins).forEach(function (_ref5) {
        var _ref6 = _slicedToArray(_ref5, 2),
            name = _ref6[0],
            plugin = _ref6[1];

        if (plugin.context) {
            router.addContext(function (ctx) {
                return plugin.context(ctx, ctx.router_info);
            });
        }
    });
    router.addContext(function () {
        return spinner.stop() && {};
    }); // Initialize wq/store.js and wq/outbox.js

    ds.init(config.store);
    app.service = ds.service;
    var ready = ds.ready.then(function () {
        return outbox.init(config.outbox);
    });

    if (app.can_login) {
        // Initialize authentication, if applicable
        router.register('logout', 'logout', app.logout);
        ready = ready.then(function () {
            app.outbox.setCSRFToken(app.csrftoken);
        }).then(_checkLogin);
    }

    if (app.config.jqmInit) {
        ready = ready.then(app.jqmInit);
    }

    return ready;
};

var pcount = 0;

app.use = function (plugin) {
    pcount++;

    if (!plugin.name) {
        plugin.name = 'plugin' + pcount;
    }

    app.plugins[plugin.name] = plugin;
    plugin.app = app;
};

app.prefetchAll = function () {
    return Promise.all(Object.keys(app.models).map(function (name) {
        return app.models[name].prefetch();
    }));
};

app.jqmInit = router.jqmInit;

app.logout = function () {
    if (!app.can_login || !app.user) {
        return;
    }

    ds.dispatch({
        type: LOGOUT
    }); // Notify server (don't need to wait for this)

    ds.fetch('/logout').then(function (result) {
        ds.dispatch({
            type: CSRFTOKEN,
            payload: result
        });
    });
};

app.userInfo = function () {
    return {
        user: app.user,
        is_authenticated: !!app.user,
        app_config: app.config,
        wq_config: app.wq_config,
        csrf_token: app.csrftoken
    };
};

function _refreshUserInfo(_x, _x2) {
    return _refreshUserInfo2.apply(this, arguments);
}

function _refreshUserInfo2() {
    _refreshUserInfo2 = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee4(dispatch, getState) {
        var context;
        return _regeneratorRuntime.wrap(function _callee4$(_context4) {
            while (1) {
                switch (_context4.prev = _context4.next) {
                    case 0:
                        _context4.next = 2;
                        return _refreshCSRFToken();

                    case 2:
                        context = getState().context || {};
                        router.render(_objectSpread2({}, context, {}, app.userInfo()), true); // FIXME: Better way to do this?

                        app.spin.start();
                        _context4.next = 7;
                        return app.prefetchAll();

                    case 7:
                        app.spin.stop();
                        _context4.next = 10;
                        return router.reload();

                    case 10:
                    case "end":
                        return _context4.stop();
                }
            }
        }, _callee4);
    }));
    return _refreshUserInfo2.apply(this, arguments);
}

function _refreshCSRFToken() {
    return _refreshCSRFToken2.apply(this, arguments);
}

function _refreshCSRFToken2() {
    _refreshCSRFToken2 = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee5() {
        return _regeneratorRuntime.wrap(function _callee5$(_context5) {
            while (1) {
                switch (_context5.prev = _context5.next) {
                    case 0:
                        outbox.setCSRFToken(app.csrftoken);

                    case 1:
                    case "end":
                        return _context5.stop();
                }
            }
        }, _callee5);
    }));
    return _refreshCSRFToken2.apply(this, arguments);
}

function _getSyncInfo() {
    return _getSyncInfo2.apply(this, arguments);
}

function _getSyncInfo2() {
    _getSyncInfo2 = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee6() {
        var unsynced;
        return _regeneratorRuntime.wrap(function _callee6$(_context6) {
            while (1) {
                switch (_context6.prev = _context6.next) {
                    case 0:
                        _context6.next = 2;
                        return outbox.unsynced();

                    case 2:
                        unsynced = _context6.sent;
                        return _context6.abrupt("return", {
                            syncing: app.syncing,
                            unsynced: unsynced
                        });

                    case 4:
                    case "end":
                        return _context6.stop();
                }
            }
        }, _callee6);
    }));
    return _getSyncInfo2.apply(this, arguments);
}

app.go = function () {
    throw new Error('app.go() has been removed.  Use app.nav() instead');
}; // Run any/all plugins on the specified page


app.runPlugins = function (arg) {
    if (arg) {
        throw new Error('runPlugins() now loads args from context');
    }

    var state = router.store.getState(),
        context = state.context;
    var routeInfo = context.router_info;
    var getItem;

    if (context.outbox_id) {
        getItem = Promise.resolve(context);
    } else if (routeInfo.item_id) {
        if (context.local) {
            getItem = Promise.resolve(context);
        } else {
            getItem = app.models[routeInfo.page].find(routeInfo.item_id);
        }
    } else {
        getItem = Promise.resolve({});
    }

    getItem.then(function (item) {
        routeInfo = _objectSpread2({}, routeInfo, {
            item: item,
            context: context
        });

        if (window.MSApp && window.MSApp.execUnsafeLocalFunction) {
            window.MSApp.execUnsafeLocalFunction(function () {
                app.callPlugins('run', [jqm.activePage, routeInfo]);
            });
        } else {
            app.callPlugins('run', [jqm.activePage, routeInfo]);
        }
    });
}; // Sync outbox and handle result


app.sync = function (retryAll) {
    if (retryAll) {
        console.warn('app.sync(true) renamed to app.retryAll()');
        app.retryAll();
    } else {
        throw new Error('app.sync() no longer used.');
    }
};

app.retryAll = function () {
    app.outbox.unsynced().then(function (unsynced) {
        if (!unsynced) {
            return;
        }

        app.outbox.retryAll();
    });
};

app.emptyOutbox = function (confirmFirst) {
    /* global confirm */
    if (confirmFirst) {
        if (navigator.notification && navigator.notification.confirm) {
            navigator.notification.confirm('Empty Outbox?', function (button) {
                if (button == 1) {
                    app.emptyOutbox();
                }
            });
            return;
        } else {
            if (!confirm('Empty Outbox?')) {
                return;
            }
        }
    }

    return outbox.empty();
};

app.confirmSubmit = function (form, message) {
    /* global confirm */
    var $form;

    if (navigator.notification && navigator.notification.confirm) {
        $form = $(form);

        if ($form.data('wq-confirm-submit')) {
            return true;
        }

        navigator.notification.confirm(message, function (button) {
            if (button == 1) {
                $form.data('wq-confirm-submit', true);
                $form.trigger('submit');
            }
        });
    } else {
        if (confirm(message)) {
            return true;
        }
    }

    return false;
}; // Handle navigation after form submission


app.postSaveNav = function (item, alreadySynced) {
    var url;
    var pluginUrl = app.callPlugins('postsaveurl', [item, alreadySynced]).filter(function (item) {
        return !!item;
    });

    if (pluginUrl.length) {
        url = pluginUrl[0];
    } else {
        url = app.postsaveurl(item, alreadySynced);
    } // Navigate to computed URL


    if (app.config.debug) {
        console.log('Successfully saved; continuing to ' + url);
    }

    router.push(url);
};

app.postsaveurl = function (item, alreadySynced) {
    var postsave, pconf, match, mode, url, itemid, modelConf; // conf.postsave can be set redirect to another page

    modelConf = item.options.modelConf;

    if (item.deletedId) {
        postsave = modelConf.postdelete;
    } else {
        postsave = modelConf.postsave;
    }

    if (!postsave) {
        // Otherwise, default is to return the page for the item just saved
        if (!alreadySynced || item.deletedId) {
            // If backgroundSync, return to list view while syncing
            postsave = modelConf.name + '_list';
        } else {
            // If noBackgroundSync, return to the newly synced item
            postsave = modelConf.name + '_detail';
        }
    } // conf.postsave should explicitly indicate which template mode to use

    /* eslint no-useless-escape: off */


    match = postsave.match(/^([^\/]+)_([^_\/]+)$/);

    if (match) {
        postsave = match[1];
        mode = match[2];
    } // Retrieve configuration for postsave page, if any


    pconf = _getConf(postsave, true); // Compute URL

    if (!pconf) {
        // If conf.postsave is not the name of a list page, assume it's a
        // simple page or a URL
        var urlContext;

        if (item.deletedId) {
            urlContext = _objectSpread2({
                deleted: true
            }, router.store.getState().context);
        } else {
            urlContext = _objectSpread2({}, item.data, {}, item.result);
        }

        url = app.base_url + '/' + tmpl.render(postsave, urlContext);
    } else if (!pconf.list) {
        url = app.base_url + '/' + pconf.url;
    } else {
        if (pconf.modes.indexOf(mode) == -1) {
            throw 'Unknown template mode!';
        } // For list pages, the url can differ depending on the mode


        url = app.base_url + '/' + pconf.url + '/';

        if (mode != 'list') {
            // Detail or edit view; determine item id and add to url
            if (postsave == modelConf.name && !item.synced) {
                // Config indicates return to detail/edit view of the model
                // that was just saved, but the item hasn't been synced yet.
                // Navigate to outbox URL instead.
                url = app.base_url + '/outbox/' + item.id;

                if (mode != 'edit' && item.error) {
                    // Return to edit form if there was an error
                    mode = 'edit';
                }
            } else {
                // Item has been successfully synced
                if (postsave == modelConf.name) {
                    // If postsave page is the same as the item's page, use the
                    // new id
                    itemid = item.result && item.result.id;
                } else {
                    // Otherwise, look for a foreign key reference
                    // FIXME: what if the foreign key has a different name?
                    itemid = item.result && item.result[postsave + '_id'];
                }

                if (!itemid) {
                    throw 'Could not find ' + postsave + ' id in result!';
                }

                url += itemid;
            }

            if (mode != 'detail') {
                url += '/' + mode;
            }
        }
    }

    return url;
}; // Hook for handling navigation / alerts after a submission error
// (only used when noBackgroundSync is set)


app.saveerror = function (item, reason, $form) {
    // Save failed for some reason, perhaps due to being offline
    // (override to customize behavior, e.g. display an outbox)
    if (app.config.debug) {
        console.warn('Could not save: ' + reason);
    }

    if (reason == app.OFFLINE) {
        app.postSaveNav(item, false);
    } else {
        app.showOutboxErrors(item, $form);
    }
};

var syncRefresh = {
    onsync: function onsync(obitem) {
        var _this$app$store$getSt = this.app.store.getState(),
            context = _this$app$store$getSt.context,
            routeInfo = context.router_info,
            full_path = routeInfo.full_path,
            item_id = routeInfo.item_id,
            parent_id = routeInfo.parent_id,
            _ref7 = obitem || {},
            outboxId = _ref7.id,
            result = _ref7.result,
            _ref8 = result || {},
            resultId = _ref8.id,
            outboxSlug = "outbox-".concat(outboxId);

        if (resultId && (item_id === outboxSlug || parent_id === outboxSlug)) {
            router.push(full_path.replace(outboxSlug, resultId));
        } else if (jqm.activePage.data('wq-sync-refresh')) {
            router.reload();
        }
    }
}; // Return a list of all foreign key fields

app.getParents = function (page) {
    var conf = _getBaseConf(page);

    return conf.form.filter(function (field) {
        return field['wq:ForeignKey'];
    }).map(function (field) {
        return field['wq:ForeignKey'];
    });
}; // Shortcuts for $.mobile.changePage


app.nav = function (url) {
    url = app.base_url + '/' + url;
    router.push(url);
};

app.replaceState = function (url) {
    throw new Error('app.replaceState() no longer supported.');
};

app.refresh = function () {
    router.refresh();
};

app.hasPlugin = function (method) {
    var plugin,
        fn,
        hasPlugin = false;

    for (plugin in app.plugins) {
        fn = app.plugins[plugin][method];

        if (fn) {
            hasPlugin = true;
        }
    }

    return hasPlugin;
};

app.callPlugins = function (method, args) {
    var plugin,
        fn,
        fnArgs,
        queue = [];

    for (plugin in app.plugins) {
        fn = app.plugins[plugin][method];

        if (args) {
            fnArgs = args;
        } else {
            fnArgs = [app.config[plugin]];
        }

        if (fn) {
            queue.push(fn.apply(app.plugins[plugin], fnArgs));
        }
    }

    return queue;
}; // Internal variables and functions


function _splitRoute(routeName) {
    var match = routeName.match(/^(.+)_([^_]+)$/);
    var page, mode, variant;

    if (match) {
        page = match[1];
        mode = match[2];

        if (mode.indexOf(':') > -1) {
            var _mode$split = mode.split(':');

            var _mode$split2 = _slicedToArray(_mode$split, 2);

            mode = _mode$split2[0];
            variant = _mode$split2[1];
        } else {
            variant = null;
        }
    } else {
        page = routeName;
        mode = null;
        variant = null;
    }

    return [page, mode, variant];
}

function _joinRoute(page, mode, variant) {
    if (variant) {
        return page + '_' + mode + ':' + variant;
    } else if (mode) {
        return page + '_' + mode;
    } else {
        return page;
    }
}

function _getRouteInfo(ctx, arg) {
    if (arg) {
        throw new Error('_getRouteInfo() now auto-created from context');
    }

    var routeInfo = ctx.router_info,
        routeName = routeInfo.name,
        itemid = routeInfo.slugs.slug || null;

    var _splitRoute2 = _splitRoute(routeName),
        _splitRoute3 = _slicedToArray(_splitRoute2, 3),
        page = _splitRoute3[0],
        mode = _splitRoute3[1],
        variant = _splitRoute3[2],
        conf = _getConf(page, true),
        pageid = null;

    if (conf) {
        if (mode && mode !== 'list') {
            pageid = page + '_' + mode + (variant ? '_' + variant : '') + (itemid ? '_' + itemid : '') + '-page';
        }
    } else {
        page = routeName;
        mode = null;
        conf = {
            name: page,
            page: page,
            form: [],
            modes: []
        };
    }

    return {
        svc: app.service,
        native: app['native'],
        page_config: conf,
        router_info: _objectSpread2({}, routeInfo, {
            page: page,
            page_config: conf,
            mode: mode,
            variant: variant,
            item_id: itemid,
            dom_id: pageid
        })
    };
}

function getTemplateName(name, context) {
    if (context.template) {
        return context.template;
    } else {
        return name.split(':')[0];
    }
} // Generate list view context and render with [url]_list template;
// handles requests for [url] and [url]/


_register.list = function (page) {
    var conf = _getBaseConf(page),
        register = conf.url === '' ? router.registerLast : router.register;

    register(conf.url, _joinRoute(page, 'list'), function (ctx) {
        return _displayList(ctx);
    }); // Special handling for /[parent_list_url]/[parent_id]/[url]

    app.getParents(page).forEach(function (ppage) {
        var pconf = _getBaseConf(ppage);

        var url = pconf.url;
        var registerParent;

        if (url === '') {
            registerParent = router.registerLast;
        } else {
            registerParent = router.register;
            url += '/';
        }

        url += ':parent_id/' + conf.url;
        registerParent(url, _joinRoute(page, 'list', ppage), parentContext);
    });

    function parentContext(_x3) {
        return _parentContext.apply(this, arguments);
    }

    function _parentContext() {
        _parentContext = _asyncToGenerator(
        /*#__PURE__*/
        _regeneratorRuntime.mark(function _callee(ctx) {
            var routeInfo, page, ppage, parent_id, pconf, pitem, parentUrl, info;
            return _regeneratorRuntime.wrap(function _callee$(_context) {
                while (1) {
                    switch (_context.prev = _context.next) {
                        case 0:
                            routeInfo = ctx.router_info;
                            page = routeInfo.page;
                            ppage = routeInfo.variant;
                            parent_id = routeInfo.slugs.parent_id;
                            pconf = _getConf(ppage);
                            _context.next = 7;
                            return app.models[ppage].find(parent_id);

                        case 7:
                            pitem = _context.sent;

                            if (pitem) {
                                parentUrl = pconf.url + '/' + pitem.id;
                            } else if (parent_id.indexOf('outbox-') == -1) {
                                parentUrl = 'outbox/' + parent_id.split('-')[1];
                            } else {
                                parentUrl = null;
                            }

                            info = {
                                parent_id: parent_id,
                                parent_url: parentUrl,
                                parent_label: pitem && pitem.label,
                                parent_page: ppage,
                                router_info: _objectSpread2({}, routeInfo, {
                                    parent_id: parent_id,
                                    parent_page: ppage,
                                    parent_url: parentUrl
                                })
                            };
                            info['parent_is_' + ppage] = true;
                            return _context.abrupt("return", _displayList(ctx, info));

                        case 12:
                        case "end":
                            return _context.stop();
                    }
                }
            }, _callee);
        }));
        return _parentContext.apply(this, arguments);
    }
};

_onShow.list = function (page) {
    router.onShow(_joinRoute(page, 'list'), app.runPlugins); // Special handling for /[parent_list_url]/[parent_id]/[url]

    app.getParents(page).forEach(function (ppage) {
        router.onShow(_joinRoute(page, 'list', ppage), app.runPlugins);
    });
};

app._addOutboxItemsToContext = function (context, unsyncedItems) {
    // Add any outbox items to context
    context.unsynced = unsyncedItems.length;
    context.unsyncedItems = unsyncedItems;
};

function _displayList(_x4, _x5) {
    return _displayList2.apply(this, arguments);
} // Generate item detail view context and render with [url]_detail template;
// handles requests for [url]/[id]


function _displayList2() {
    _displayList2 = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee8(ctx, parentInfo) {
        var routeInfo, page, params, url, conf, model, pnum, next, prev, filter, key, getData, getUnsynced, _getUnsynced, unsynced1, data1, unsynced2, data, unsyncedItems, prevIsLocal, currentIsLocal, prevp, nextp, context;

        return _regeneratorRuntime.wrap(function _callee8$(_context8) {
            while (1) {
                switch (_context8.prev = _context8.next) {
                    case 0:
                        _getUnsynced = function _ref13() {
                            _getUnsynced = _asyncToGenerator(
                            /*#__PURE__*/
                            _regeneratorRuntime.mark(function _callee7() {
                                return _regeneratorRuntime.wrap(function _callee7$(_context7) {
                                    while (1) {
                                        switch (_context7.prev = _context7.next) {
                                            case 0:
                                                if (!(pnum == model.opts.page || pnum == 1 && !model.opts.client)) {
                                                    _context7.next = 4;
                                                    break;
                                                }

                                                return _context7.abrupt("return", model.unsyncedItems());

                                            case 4:
                                                return _context7.abrupt("return", []);

                                            case 5:
                                            case "end":
                                                return _context7.stop();
                                        }
                                    }
                                }, _callee7);
                            }));
                            return _getUnsynced.apply(this, arguments);
                        };

                        getUnsynced = function _ref12() {
                            return _getUnsynced.apply(this, arguments);
                        };

                        getData = function _ref11() {
                            if (filter) {
                                return model.filterPage(filter);
                            } else if (pnum > model.opts.page) {
                                return model.page(pnum);
                            } else {
                                return model.load();
                            }
                        };

                        routeInfo = ctx.router_info, page = routeInfo.page, params = routeInfo.params, url = routeInfo.full_path, conf = _getConf(page), model = app.models[page];
                        pnum = model.opts.page, next = null, prev = null;

                        if (params || parentInfo) {
                            if (params && params.page) {
                                pnum = params.page;
                            }

                            filter = {};

                            for (key in params || {}) {
                                if (key != 'page') {
                                    filter[key] = params[key];
                                }
                            }

                            if (parentInfo) {
                                conf.form.forEach(function (field) {
                                    if (field['wq:ForeignKey'] == parentInfo.parent_page) {
                                        filter[field.name + '_id'] = parentInfo.parent_id;
                                    }
                                });
                            }
                        }

                        if (filter && !Object.keys(filter).length) {
                            filter = null;
                        } // Load from server if data might not exist locally


                        if (!app.config.loadMissingAsHtml) {
                            _context8.next = 16;
                            break;
                        }

                        if (model.opts.client) {
                            _context8.next = 10;
                            break;
                        }

                        return _context8.abrupt("return", _loadFromServer(url));

                    case 10:
                        if (!(filter && model.opts.server)) {
                            _context8.next = 12;
                            break;
                        }

                        return _context8.abrupt("return", _loadFromServer(url));

                    case 12:
                        if (!(pnum > model.opts.page)) {
                            _context8.next = 14;
                            break;
                        }

                        return _context8.abrupt("return", _loadFromServer(url));

                    case 14:
                        _context8.next = 17;
                        break;

                    case 16:
                        if (filter && pnum > model.opts.page) {
                            filter.page = pnum;
                        }

                    case 17:
                        if (!pnum && (!model.opts.client || filter)) {
                            pnum = 1;
                        }

                        _context8.next = 20;
                        return getUnsynced();

                    case 20:
                        unsynced1 = _context8.sent;
                        _context8.next = 23;
                        return getData();

                    case 23:
                        data1 = _context8.sent;
                        _context8.next = 26;
                        return getUnsynced();

                    case 26:
                        unsynced2 = _context8.sent;

                        if (!(unsynced1 && unsynced2 && unsynced1.length != unsynced2.length)) {
                            _context8.next = 33;
                            break;
                        }

                        _context8.next = 30;
                        return getData();

                    case 30:
                        data = _context8.sent;
                        _context8.next = 34;
                        break;

                    case 33:
                        data = data1;

                    case 34:
                        unsyncedItems = unsynced2;

                        if (pnum > model.opts.page && (model.opts.client || pnum > 1)) {
                            if (+pnum - 1 > model.opts.page && (model.opts.client || pnum > 2)) {
                                prevp = filter ? _objectSpread2({}, filter) : {};
                                prevp.page = +pnum - 1;
                                prev = conf.url + '/?' + $.param(prevp);
                            } else if (pnum == 1 && !filter) {
                                prev = conf.url + '/';
                                prevIsLocal = true;
                            }
                        }

                        if (pnum < data.pages && (model.opts.server || pnum)) {
                            nextp = filter ? _objectSpread2({}, filter) : {};
                            nextp.page = +pnum + 1;
                            next = conf.url + '/?' + $.param(nextp);

                            if (nextp.page == 1) {
                                currentIsLocal = true;
                            }
                        }

                        context = _objectSpread2({}, data, {}, parentInfo, {
                            previous: prev ? '/' + prev : null,
                            next: next ? '/' + next : null,
                            multiple: prev || next ? true : false,
                            previous_is_local: prevIsLocal,
                            current_is_local: currentIsLocal
                        });

                        app._addOutboxItemsToContext(context, unsyncedItems);

                        return _context8.abrupt("return", _addLookups(page, context, false));

                    case 40:
                    case "end":
                        return _context8.stop();
                }
            }
        }, _callee8);
    }));
    return _displayList2.apply(this, arguments);
}

_register.detail = function (page, mode) {
    var contextFn = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : _displayItem;

    var conf = _getBaseConf(page);

    var url = _getDetailUrl(conf.url, mode);

    var register = conf.url === '' ? router.registerLast : router.register;
    register(url, _joinRoute(page, mode), contextFn);
}; // Register an onshow event for item detail views


_onShow.detail = function (page, mode) {
    router.onShow(_joinRoute(page, mode), app.runPlugins);
};

function _getDetailUrl(url, mode) {
    if (url) {
        url += '/';
    }

    url += '<slug>';

    if (mode != 'detail') {
        url += '/' + mode;
    }

    return url;
} // Generate item edit context and render with [url]_edit template;
// handles requests for [url]/[id]/edit and [url]/new


_register.edit = function (page) {
    var conf = _getBaseConf(page);

    var register = conf.url === '' ? router.registerLast : router.register;
    register(_getDetailUrl(conf.url, 'edit'), _joinRoute(page, 'edit'), _displayItem);
    router.registerFirst(conf.url + '/new', _joinRoute(page, 'edit', 'new'), _displayItem);
}; // Register an onshow event for item edit views


_onShow.edit = function (page) {
    router.onShow(_joinRoute(page, 'edit'), app.runPlugins);
    router.onShow(_joinRoute(page, 'edit', 'new'), app.runPlugins);
};

function _displayItem(_x6) {
    return _displayItem2.apply(this, arguments);
} // Render non-list pages with with [url] template;
// handles requests for [url] and [url]/


function _displayItem2() {
    _displayItem2 = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee9(ctx) {
        var routeInfo, itemid, page, mode, variant, url, conf, model, item, localOnly;
        return _regeneratorRuntime.wrap(function _callee9$(_context9) {
            while (1) {
                switch (_context9.prev = _context9.next) {
                    case 0:
                        routeInfo = ctx.router_info, itemid = routeInfo.item_id, page = routeInfo.page, mode = routeInfo.mode, variant = routeInfo.variant, url = routeInfo.full_path, conf = _getConf(page), model = app.models[page];

                        if (!(mode == 'edit' && variant == 'new')) {
                            _context9.next = 5;
                            break;
                        }

                        item = _objectSpread2({}, routeInfo.params, {}, conf.defaults);
                        _context9.next = 15;
                        break;

                    case 5:
                        localOnly = !app.config.loadMissingAsJson;
                        _context9.next = 8;
                        return model.find(itemid, localOnly);

                    case 8:
                        item = _context9.sent;

                        if (item) {
                            _context9.next = 15;
                            break;
                        }

                        if (!(model.opts.server && app.config.loadMissingAsHtml)) {
                            _context9.next = 14;
                            break;
                        }

                        return _context9.abrupt("return", _loadFromServer(url));

                    case 14:
                        return _context9.abrupt("return", router.notFound());

                    case 15:
                        if (!item) {
                            _context9.next = 28;
                            break;
                        }

                        item.local = true;

                        if (!(mode == 'edit')) {
                            _context9.next = 25;
                            break;
                        }

                        if (!(variant == 'new')) {
                            _context9.next = 22;
                            break;
                        }

                        return _context9.abrupt("return", _addLookups(page, item, 'new'));

                    case 22:
                        return _context9.abrupt("return", _addLookups(page, item, true));

                    case 23:
                        _context9.next = 26;
                        break;

                    case 25:
                        return _context9.abrupt("return", _addLookups(page, item, false));

                    case 26:
                        _context9.next = 33;
                        break;

                    case 28:
                        if (!(model.opts.server && app.config.loadMissingAsHtml)) {
                            _context9.next = 32;
                            break;
                        }

                        return _context9.abrupt("return", _loadFromServer(url));

                    case 32:
                        return _context9.abrupt("return", router.notFound());

                    case 33:
                    case "end":
                        return _context9.stop();
                }
            }
        }, _callee9);
    }));
    return _displayItem2.apply(this, arguments);
}

function _registerOther(page) {
    var conf = _getBaseConf(page);

    router.register(conf.url, page, _displayOther);

    function _displayOther() {
        return _displayOther2.apply(this, arguments);
    }

    function _displayOther2() {
        _displayOther2 = _asyncToGenerator(
        /*#__PURE__*/
        _regeneratorRuntime.mark(function _callee2() {
            return _regeneratorRuntime.wrap(function _callee2$(_context2) {
                while (1) {
                    switch (_context2.prev = _context2.next) {
                        case 0:
                            if (!conf.server_only) {
                                _context2.next = 4;
                                break;
                            }

                            return _context2.abrupt("return", _loadFromServer(app.base_url + '/' + conf.url));

                        case 4:
                            return _context2.abrupt("return", {});

                        case 5:
                        case "end":
                            return _context2.stop();
                    }
                }
            }, _callee2);
        }));
        return _displayOther2.apply(this, arguments);
    }
} // Register an onshow event for non-list single pages


function _onShowOther(page) {
    router.onShow(page, app.runPlugins);
}

function _renderOutboxItem(_x7) {
    return _renderOutboxItem2.apply(this, arguments);
} // Handle form submit from [url]_edit views


function _renderOutboxItem2() {
    _renderOutboxItem2 = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee10(ctx) {
        var routeInfo, mode, item, id, page, template, idMatch, context;
        return _regeneratorRuntime.wrap(function _callee10$(_context10) {
            while (1) {
                switch (_context10.prev = _context10.next) {
                    case 0:
                        routeInfo = ctx.router_info;
                        mode = routeInfo.page.replace(/^outbox_/, '');
                        _context10.next = 4;
                        return outbox.loadItem(+routeInfo.slugs.slug);

                    case 4:
                        item = _context10.sent;

                        if (!(!item || !item.options || !item.options.modelConf)) {
                            _context10.next = 7;
                            break;
                        }

                        return _context10.abrupt("return", router.notFound());

                    case 7:
                        page = item.options.modelConf.name, template = page + '_' + mode, idMatch = item.options.url.match(new RegExp(item.options.modelConf.url + '/([^/]+)$'));

                        if (item.data.id) {
                            id = item.data.id;
                        } else if (idMatch) {
                            id = idMatch[1];
                        } else {
                            id = 'new';
                        }

                        context = _objectSpread2({
                            outbox_id: item.id,
                            template: template,
                            error: item.error,
                            router_info: _objectSpread2({}, routeInfo, {
                                outbox_id: item.id
                            })
                        }, item.data);

                        if (id != 'new') {
                            context.id = id;
                        }

                        return _context10.abrupt("return", _addLookups(page, context, false));

                    case 12:
                    case "end":
                        return _context10.stop();
                }
            }
        }, _callee10);
    }));
    return _renderOutboxItem2.apply(this, arguments);
}

function _handleForm(_x8) {
    return _handleForm2.apply(this, arguments);
}

function _handleForm2() {
    _handleForm2 = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee11(evt) {
        var $form, $submitVal, backgroundSync, storage, outboxId, preserve, url, conf, vals, $files, has_files, addVal, options, item, error;
        return _regeneratorRuntime.wrap(function _callee11$(_context11) {
            while (1) {
                switch (_context11.prev = _context11.next) {
                    case 0:
                        addVal = function _ref14(name, val) {
                            if (vals[name] !== undefined) {
                                if (!$.isArray(vals[name])) {
                                    vals[name] = [vals[name]];
                                }

                                vals[name].push(val);
                            } else {
                                vals[name] = val;
                            }
                        };

                        $form = $(this);

                        if (!evt.isDefaultPrevented()) {
                            _context11.next = 4;
                            break;
                        }

                        return _context11.abrupt("return");

                    case 4:
                        $form.find('[type=submit]').prop('disabled', true);

                        if ($form.data('wq-submit-button-name')) {
                            $submitVal = $('<input>').attr('name', $form.data('wq-submit-button-name')).attr('value', $form.data('wq-submit-button-value'));
                            $form.append($submitVal);
                        }

                        if (!($form.data('wq-json') !== undefined && !$form.data('wq-json'))) {
                            _context11.next = 9;
                            break;
                        }

                        app.spin.forSeconds(10);
                        return _context11.abrupt("return");

                    case 9:
                        if ($form.data('wq-background-sync') !== undefined) {
                            backgroundSync = $form.data('wq-background-sync');
                        } else {
                            backgroundSync = app.config.backgroundSync;
                        }

                        if ($form.data('wq-storage') !== undefined) {
                            storage = $form.data('wq-storage');
                        }

                        outboxId = $form.data('wq-outbox-id');
                        preserve = $form.data('wq-outbox-preserve');
                        url = $form.attr('action').replace(app.service + '/', '');
                        conf = _getConfByUrl(url, true);
                        vals = {};
                        $files = $form.find('input[type=file]');
                        has_files = false;
                        $files.each(function (i, input) {
                            if ($(input).val().length > 0) {
                                has_files = true;
                            }
                        });

                        if (conf) {
                            _context11.next = 22;
                            break;
                        }

                        // Unrecognized URL; assume a regular form post
                        app.spin.forSeconds(10);
                        return _context11.abrupt("return");

                    case 22:
                        if (!(has_files && !window.Blob)) {
                            _context11.next = 25;
                            break;
                        }

                        // Files present but there's no Blob API.  Looks like we're in a an old
                        // browser that can't upload files via AJAX.  Bypass wq/outbox.js
                        // entirely and hope server is able to respond to regular form posts
                        // with HTML (hint: wq.db is).
                        app.spin.forSeconds(10);
                        return _context11.abrupt("return");

                    case 25:
                        // Modern browser and/or no files present; skip regular form submission,
                        // we're saving this via wq/outbox.js
                        evt.preventDefault(); // Use a simple JSON structure for values, which is better for outbox
                        // serialization.

                        $.each($form.serializeArray(), function (i, v) {
                            addVal(v.name, v.value);
                        }); // Handle <input type=file>.  Use HTML JSON form-style objects, but
                        // with Blob instead of base64 encoding to represent the actual file.

                        if (has_files) {
                            $files.each(function () {
                                var name = this.name,
                                    file,
                                    slice;

                                if (!this.files || !this.files.length) {
                                    return;
                                }

                                for (var i = 0; i < this.files.length; i++) {
                                    file = this.files[i];
                                    slice = file.slice || file.webkitSlice;
                                    addVal(name, {
                                        type: file.type,
                                        name: file.name,
                                        // Convert to blob for better serialization
                                        body: slice.call(file, 0, file.size, file.type)
                                    });
                                }
                            });
                        } // Handle blob-stored files created by (e.g.) wq/photos.js


                        $form.find('input[data-wq-type=file]').each(function () {
                            // wq/photo.js files in memory, copy over to form
                            var name = this.name;
                            var value = this.value;
                            var curVal = $.isArray(vals[name]) ? vals[name][0] : vals[name];
                            var photos = app.plugins.photos;

                            if (curVal && typeof curVal === 'string') {
                                delete vals[name];
                            }

                            if (!value || !photos) {
                                return;
                            }

                            var data = photos._files[value];

                            if (data) {
                                has_files = true;
                                addVal(name, data);
                                delete photos._files[value];
                            }
                        });

                        if ($submitVal) {
                            $submitVal.remove();
                        }

                        options = {
                            url: url
                        };

                        if (storage) {
                            options.storage = storage;
                        } else if (!backgroundSync) {
                            options.storage = 'temporary';
                        } else if (has_files) {
                            options.storage = 'store';
                        }

                        if (outboxId) {
                            options.id = outboxId;

                            if (preserve && preserve.split) {
                                options.preserve = preserve.split(/,/);
                            }
                        }

                        if (vals._method) {
                            options.method = vals._method;
                            delete vals._method;
                        } else {
                            options.method = 'POST';
                        }

                        options.modelConf = conf;

                        if (conf.label_template) {
                            options.label = tmpl.render(conf.label_template, vals);
                        }

                        $form.find('.error').html('');
                        options.csrftoken = app.csrftoken;
                        _context11.next = 40;
                        return outbox.save(vals, options);

                    case 40:
                        item = _context11.sent;

                        if (!backgroundSync) {
                            _context11.next = 44;
                            break;
                        }

                        // Send user to next screen while app syncs in background
                        app.postSaveNav(item, false);
                        return _context11.abrupt("return");

                    case 44:
                        // Submit form immediately and wait for server to respond
                        $form.attr('data-wq-outbox-id', item.id);
                        app.spin.start();
                        _context11.next = 48;
                        return outbox.waitForItem(item.id);

                    case 48:
                        item = _context11.sent;
                        $form.find('[type=submit]').prop('disabled', false);
                        app.spin.stop();

                        if (item) {
                            _context11.next = 53;
                            break;
                        }

                        return _context11.abrupt("return");

                    case 53:
                        if (!item.synced) {
                            _context11.next = 56;
                            break;
                        }

                        // Item was synced
                        app.postSaveNav(item, true);
                        return _context11.abrupt("return");

                    case 56:
                        if (!item.error) {
                            // Save failed without server error: probably offline
                            // FIXME: waitForItem() probably doesn't resolve until back online.
                            error = app.OFFLINE;
                        } else if (typeof item.error === 'string') {
                            // Save failed and error information is not in JSON format
                            // (likely a 500 server failure)
                            error = app.FAILURE;
                        } else {
                            // Save failed and error information is in JSON format
                            // (likely a 400 bad data error)
                            error = app.ERROR;
                        }

                        app.saveerror(item, error, $form);

                    case 58:
                    case "end":
                        return _context11.stop();
                }
            }
        }, _callee11, this);
    }));
    return _handleForm2.apply(this, arguments);
}

var showOutboxErrors = {
    run: function () {
        var _run = _asyncToGenerator(
        /*#__PURE__*/
        _regeneratorRuntime.mark(function _callee3($page, routeInfo) {
            var name, outbox_id, item;
            return _regeneratorRuntime.wrap(function _callee3$(_context3) {
                while (1) {
                    switch (_context3.prev = _context3.next) {
                        case 0:
                            name = routeInfo.name, outbox_id = routeInfo.outbox_id;

                            if (!(name === 'outbox_edit')) {
                                _context3.next = 6;
                                break;
                            }

                            _context3.next = 4;
                            return outbox.loadItem(routeInfo.outbox_id);

                        case 4:
                            item = _context3.sent;

                            if (item.error) {
                                app.showOutboxErrors(item, $page);
                            }

                        case 6:
                        case "end":
                            return _context3.stop();
                    }
                }
            }, _callee3);
        }));

        function run(_x9, _x10) {
            return _run.apply(this, arguments);
        }

        return run;
    }()
};

app.showOutboxErrors = function (item, $page) {
    if ($page.is('form') && item.options.method == 'DELETE') {
        if (!$page.find('.error').length) {
            // Delete form does not contain error placeholders
            // but main form might
            $page = $page.parents('.ui-page');
        }
    }

    if (!item.error) {
        showError('Error saving data.');
        return;
    } else if (typeof item.error === 'string') {
        showError(item.error);
        return;
    } // Save failed and error information is in JSON format
    // (likely a 400 bad data error)


    var errs = Object.keys(item.error);

    if (errs.length == 1 && errs[0] == 'detail') {
        // General API errors have a single "detail" attribute
        showError(item.error.detail);
    } else {
        // REST API provided per-field error information
        // Form errors (other than non_field_errors) are keyed by fieldname
        errs.forEach(function (f) {
            // FIXME: there may be multiple errors per field
            var err = item.error[f][0];

            if (f == 'non_field_errors') {
                showError(err);
            } else {
                if (_typeof(err) !== 'object') {
                    showError(err, f);
                } else {
                    // Nested object errors (e.g. attachment)
                    item.error[f].forEach(function (err, i) {
                        for (var n in err) {
                            var fid = f + '-' + i + '-' + n;
                            showError(err[n][0], fid);
                        }
                    });
                }
            }
        });

        if (!item.error.non_field_errors) {
            showError('One or more errors were found.');
        }
    }

    function showError(err, field) {
        if (field) {
            field = field + '-';
        } else {
            field = '';
        }

        var sel = '.' + item.options.modelConf.name + '-' + field + 'errors';
        $page.find(sel).html(err);
    }
}; // Remember which submit button was clicked (and its value)


function _submitClick() {
    var $button = $(this),
        $form = $(this.form),
        name = $button.attr('name'),
        value = $button.attr('value');

    if (name !== undefined && value !== undefined) {
        $form.data('wq-submit-button-name', name);
        $form.data('wq-submit-button-value', value);
    }
}

app.getAuthState = function () {
    return this.store.getState().auth || {};
};

function _authReducer() {
    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var action = arguments.length > 1 ? arguments[1] : undefined;

    if (!app.can_login) {
        return state;
    }

    switch (action.type) {
        case LOGIN_SUCCESS:
        case LOGIN_RELOAD:
            {
                var _action$payload = action.payload,
                    user = _action$payload.user,
                    config = _action$payload.config,
                    csrftoken = _action$payload.csrftoken;
                return {
                    user: user,
                    config: config,
                    csrftoken: csrftoken
                };
            }

        case LOGOUT:
            {
                var _ref9 = action.payload || {},
                    _csrftoken = _ref9.csrftoken;

                if (_csrftoken) {
                    return {
                        csrftoken: _csrftoken
                    };
                } else {
                    return {};
                }
            }

        case CSRFTOKEN:
            {
                var _csrftoken2 = action.payload.csrftoken;
                return _objectSpread2({}, state, {
                    csrftoken: _csrftoken2
                });
            }

        default:
            {
                return state;
            }
    }
}

function _checkLogin() {
    setTimeout(function () {
        ds.fetch('/login').then(function (result) {
            if (result && result.user && result.config) {
                ds.dispatch({
                    type: LOGIN_RELOAD,
                    payload: result
                });
            } else {
                var _ref10 = result || {},
                    csrftoken = _ref10.csrftoken;

                ds.dispatch({
                    type: app.user ? LOGOUT : CSRFTOKEN,
                    payload: {
                        csrftoken: csrftoken
                    }
                });
            }
        });
    }, 10);
} // Add various callback functions to context object to automate foreign key
// lookups within templates


function _addLookups(page, context, editable) {
    var conf = _getConf(page);

    var lookups = {};

    function addLookups(field, nested) {
        var fname = nested || field.name; // Choice (select/radio) lookups

        if (field.choices) {
            lookups[fname + '_label'] = _choice_label_lookup(field.name, field.choices);

            if (editable) {
                lookups[fname + '_choices'] = _choice_dropdown_lookup(field.name, field.choices);
            }
        } // Foreign key lookups


        if (field['wq:ForeignKey']) {
            var nkey;

            if (nested) {
                nkey = fname.match(/^\w+\.(\w+)\[(\w+)\]$/);
            } else {
                nkey = fname.match(/^(\w+)\[(\w+)\]$/);
            }

            if (!nkey) {
                if (nested) {
                    lookups[fname] = _this_parent_lookup(field);
                } else {
                    lookups[fname] = _parent_lookup(field, context);
                }

                if (!context[fname + '_label']) {
                    lookups[fname + '_label'] = _parent_label_lookup(field);
                }
            }

            if (editable) {
                lookups[fname + '_list'] = _parent_dropdown_lookup(field, context, nkey);
            }
        } // Load types/initial list of nested forms
        // (i.e. repeats/attachments/EAV/child model)


        if (field.children) {
            field.children.forEach(function (child) {
                var fname = field.name + '.' + child.name;
                addLookups(child, fname);
            });

            if (editable == 'new' && !context[field.name]) {
                lookups[field.name] = _default_attachments(field, context);
            }
        }
    }

    conf.form.forEach(function (field) {
        addLookups(field, false);
    }); // Process lookup functions

    var keys = Object.keys(lookups);
    var queue = keys.map(function (key) {
        return lookups[key];
    });
    return Promise.all(queue).then(function (results) {
        results.forEach(function (result, i) {
            var key = keys[i];
            context[key] = result;
        });
        results.forEach(function (result, i) {
            var parts = keys[i].split('.'),
                nested;

            if (parts.length != 2) {
                return;
            }

            nested = context[parts[0]];

            if (!nested) {
                return;
            }

            if (!$.isArray(nested)) {
                nested = [nested];
            }

            nested.forEach(function (row) {
                row[parts[1]] = row[parts[1]] || result;
            });
        });
    }).then(function () {
        return context;
    });
} // Preset list of choices


function _choice_label_lookup(name, choices) {
    function choiceLabel() {
        if (!this[name]) {
            return;
        }

        var label;
        choices.forEach(function (choice) {
            if (choice.name == this[name]) {
                label = choice.label;
            }
        }, this);
        return label;
    }

    return Promise.resolve(choiceLabel);
}

function _choice_dropdown_lookup(name, choices) {
    choices = choices.map(function (choice) {
        return _objectSpread2({}, choice);
    });

    function choiceDropdown() {
        choices.forEach(function (choice) {
            if (choice.name == this[name]) {
                choice.selected = true;
            } else {
                choice.selected = false;
            }
        }, this);
        return choices;
    }

    return Promise.resolve(choiceDropdown);
} // Simple foreign key lookup


function _parent_lookup(field, context) {
    var model = app.models[field['wq:ForeignKey']];
    var id = context[field.name + '_id'];

    if (id) {
        if (id.match && id.match(/^outbox/)) {
            return _getOutboxRecord(model, id);
        } else {
            return model.find(id);
        }
    } else {
        return null;
    }
} // Foreign key lookup for objects other than root


function _this_parent_lookup(field) {
    var model = app.models[field['wq:ForeignKey']];
    return Promise.all([_getOutboxRecordLookup(model), model.load()]).then(function (results) {
        var obRecords = results[0];
        var existing = {};
        results[1].list.forEach(function (item) {
            existing[item.id] = item;
        });
        return function () {
            var parentId = this[field.name + '_id'];
            return obRecords[parentId] || existing[parentId];
        };
    });
} // Foreign key label


function _parent_label_lookup(field) {
    return _this_parent_lookup(field).then(function (lookup) {
        return function () {
            var p = lookup.call(this);
            return p && p.label;
        };
    });
} // List of all potential foreign key values (useful for generating dropdowns)


function _parent_dropdown_lookup(field, context, nkey) {
    var model = app.models[field['wq:ForeignKey']];
    var result;

    if (field.filter) {
        result = model.filter(_computeFilter(field.filter, context));
    } else {
        result = model.load().then(function (data) {
            return _getOutboxRecords(model).then(function (records) {
                return records.concat(data.list);
            });
        });
    }

    return result.then(function (choices) {
        return function () {
            var parents = [],
                current;

            if (nkey) {
                current = this[nkey[1]] && this[nkey[1]][nkey[2]];
            } else {
                current = this[field.name + '_id'];
            }

            choices.forEach(function (v) {
                var item = _objectSpread2({}, v);

                if (item.id == current) {
                    item.selected = true; // Currently selected item
                }

                parents.push(item);
            }, this);
            return parents;
        };
    });
}

function _getOutboxRecords(model) {
    return model.unsyncedItems().then(function (items) {
        return items.map(function (item) {
            return {
                id: 'outbox-' + item.id,
                label: item.label,
                outbox_id: item.id,
                outbox: true
            };
        });
    });
}

function _getOutboxRecordLookup(model) {
    return _getOutboxRecords(model).then(function (records) {
        var lookup = {};
        records.forEach(function (record) {
            lookup[record.id] = record;
        });
        return lookup;
    });
}

function _getOutboxRecord(model, id) {
    return _getOutboxRecordLookup(model).then(function (records) {
        return records[id];
    });
} // List of empty annotations for new objects


function _default_attachments(field, context) {
    if (field.type != 'repeat') {
        return Promise.resolve({});
    }

    if (!field.initial) {
        return Promise.resolve([]);
    }

    if (typeof field.initial == 'string' || typeof field.initial == 'number') {
        var attachments = [];

        for (var i = 0; i < +field.initial; i++) {
            attachments.push({
                '@index': i,
                new_attachment: true
            });
        }

        return Promise.resolve(attachments);
    }

    var typeField;
    field.children.forEach(function (tf) {
        if (tf.name == field.initial.type_field) {
            typeField = tf;
        }
    });

    if (!typeField) {
        return Promise.resolve([]);
    }

    var model = app.models[typeField['wq:ForeignKey']];
    var filterConf = field.initial.filter;

    if (!filterConf || !Object.keys(filterConf).length) {
        if (typeField.filter) {
            filterConf = typeField.filter;
        }
    }

    var filter = _computeFilter(filterConf, context);

    return model.filter(filter).then(function (types) {
        var attachments = [];
        types.forEach(function (t, i) {
            var obj = {
                '@index': i,
                new_attachment: true
            };
            obj[typeField.name + '_id'] = t.id;
            obj[typeField.name + '_label'] = t.label;
            attachments.push(obj);
        });
        return attachments;
    });
} // Load configuration based on page id


function _getBaseConf(page) {
    return _getConf(page, false, true);
}

function _getConf(page, silentFail, baseConf) {
    var conf = (baseConf ? app.config : app.wq_config).pages[page];

    if (!conf) {
        if (silentFail) {
            return;
        } else {
            throw new Error('Configuration for "' + page + '" not found!');
        }
    }

    return _objectSpread2({
        page: page,
        form: [],
        modes: conf.list ? ['list', 'detail', 'edit'] : []
    }, conf);
} // Helper to load configuration based on URL


function _getConfByUrl(url, silentFail) {
    var parts = url.split('/');
    var conf;

    for (var p in app.wq_config.pages) {
        if (app.wq_config.pages[p].url == parts[0]) {
            conf = app.wq_config.pages[p];
        }
    }

    if (!conf) {
        if (silentFail) {
            return;
        } else {
            throw 'Configuration for "/' + url + '" not found!';
        }
    }

    return conf;
}

function _computeFilter(filter, context) {
    var computedFilter = {};
    Object.keys(filter).forEach(function (key) {
        var values = filter[key];

        if (!$.isArray(values)) {
            values = [values];
        }

        values = values.map(function (value) {
            if (value && value.indexOf && value.indexOf('{{') > -1) {
                value = tmpl.render(value, context);

                if (value === '') {
                    return null;
                } else if (value.match(/^\+\d+$/)) {
                    return +value.substring(1);
                }
            }

            return value;
        });

        if (values.length > 1) {
            computedFilter[key] = values;
        } else {
            computedFilter[key] = values[0];
        }
    });
    return computedFilter;
}

function _loadFromServer(_x11) {
    return _loadFromServer2.apply(this, arguments);
}

function _loadFromServer2() {
    _loadFromServer2 = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee12(url) {
        var response, html;
        return _regeneratorRuntime.wrap(function _callee12$(_context12) {
            while (1) {
                switch (_context12.prev = _context12.next) {
                    case 0:
                        // options = (ui && ui.options) || {};
                        if (app.config.debug) {
                            console.log('Loading ' + url + ' from server');

                            if (app.base_url && url.indexOf(app.base_url) !== 0) {
                                console.warn(url + ' does not include ' + app.base_url);
                            }
                        }

                        _context12.next = 3;
                        return fetch(url);

                    case 3:
                        response = _context12.sent;
                        _context12.next = 6;
                        return response.text();

                    case 6:
                        html = _context12.sent;
                        return _context12.abrupt("return", router.rawHTML(html));

                    case 8:
                    case "end":
                        return _context12.stop();
                }
            }
        }, _callee12);
    }));
    return _loadFromServer2.apply(this, arguments);
}

function _serverContext(ctx) {
    var routeInfo = ctx.router_info,
        url = routeInfo.full_path;
    return _loadFromServer(url);
}

function _fetchFail(query, error) {
    /* eslint no-unused-vars: off */
    app.spin.start('Error Loading Data', 1.5, {
        theme: jqm.pageLoadErrorMessageTheme,
        textonly: true
    });
}

return app;

});
//# sourceMappingURL=app.js.map
