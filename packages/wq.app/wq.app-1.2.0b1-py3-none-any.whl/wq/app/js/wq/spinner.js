/*
 * wq.app v1.2.0b1 - @wq/app/spinner 1.2.0-beta.1
 * Wrapper for jQuery Mobile's spinner
 * (c) 2012-2019, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['regenerator-runtime'], function (_regeneratorRuntime) { 'use strict';

_regeneratorRuntime = _regeneratorRuntime && _regeneratorRuntime.hasOwnProperty('default') ? _regeneratorRuntime['default'] : _regeneratorRuntime;

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

var jqm;
var SPIN_START = 'SPIN_START';
var SPIN_STOP = 'SPIN_STOP';

function startSpin(_x, _x2, _x3) {
    return _startSpin.apply(this, arguments);
}

function _startSpin() {
    _startSpin = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee(dispatch, getState, bag) {
        var action, duration;
        return _regeneratorRuntime.wrap(function _callee$(_context) {
            while (1) {
                switch (_context.prev = _context.next) {
                    case 0:
                        action = bag.action, duration = action.payload.duration;

                        if (!duration) {
                            _context.next = 5;
                            break;
                        }

                        _context.next = 4;
                        return new Promise(function (resolve) {
                            return setTimeout(resolve, duration * 1000);
                        });

                    case 4:
                        dispatch({
                            type: SPIN_STOP
                        });

                    case 5:
                    case "end":
                        return _context.stop();
                }
            }
        }, _callee);
    }));
    return _startSpin.apply(this, arguments);
}

function reducer() {
    var context = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var action = arguments.length > 1 ? arguments[1] : undefined;

    if (action.type === SPIN_START) {
        context = _objectSpread2({
            active: true
        }, action.payload);
    } else if (action.type === SPIN_STOP) {
        context = {};
    }

    return context;
}

function render(state) {
    if (!jqm) {
        return;
    }

    if (state.spinner && state.spinner.active) {
        var _state$spinner = state.spinner,
            opts = _state$spinner.options,
            msg = _state$spinner.message;

        if (!opts) {
            opts = {};
        }

        if (msg) {
            opts.text = msg;
            opts.textVisible = true;
        }

        jqm.loading('show', opts);
    } else {
        jqm.loading('hide');
    }
}

var spinner = {
    name: 'spinner',
    init: function init() {
        jqm = this.app.jQuery && this.app.jQuery.mobile;
    },
    actions: {
        start: function start(msg, duration, opts) {
            return {
                type: SPIN_START,
                payload: {
                    message: msg,
                    duration: duration,
                    opts: opts
                }
            };
        },
        stop: function stop() {
            return {
                type: SPIN_STOP
            };
        }
    },
    thunks: {
        SPIN_START: startSpin
    },
    reducer: reducer,
    render: render
};

return spinner;

});
//# sourceMappingURL=spinner.js.map
