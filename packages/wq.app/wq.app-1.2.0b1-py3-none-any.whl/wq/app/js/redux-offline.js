define(['exports', 'redux', 'redux-persist'], function (exports, redux, reduxPersist) { 'use strict';

redux = redux && redux.hasOwnProperty('default') ? redux['default'] : redux;
reduxPersist = reduxPersist && reduxPersist.hasOwnProperty('default') ? reduxPersist['default'] : reduxPersist;

function unwrapExports (x) {
	return x && x.__esModule && Object.prototype.hasOwnProperty.call(x, 'default') ? x['default'] : x;
}

function createCommonjsModule(fn, module) {
	return module = { exports: {} }, fn(module, module.exports), module.exports;
}

var interopRequireDefault = createCommonjsModule(function (module) {
function _interopRequireDefault(obj) {
  return obj && obj.__esModule ? obj : {
    "default": obj
  };
}

module.exports = _interopRequireDefault;
});

unwrapExports(interopRequireDefault);

var _typeof_1 = createCommonjsModule(function (module) {
function _typeof2(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof2 = function _typeof2(obj) { return typeof obj; }; } else { _typeof2 = function _typeof2(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof2(obj); }

function _typeof(obj) {
  if (typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol") {
    module.exports = _typeof = function _typeof(obj) {
      return _typeof2(obj);
    };
  } else {
    module.exports = _typeof = function _typeof(obj) {
      return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : _typeof2(obj);
    };
  }

  return _typeof(obj);
}

module.exports = _typeof;
});

var constants = createCommonjsModule(function (module, exports) {

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.DEFAULT_ROLLBACK = exports.DEFAULT_COMMIT = exports.JS_ERROR = exports.PERSIST_REHYDRATE = exports.RESET_STATE = exports.OFFLINE_BUSY = exports.OFFLINE_SEND = exports.OFFLINE_COMPLETE_RETRY = exports.OFFLINE_SCHEDULE_RETRY = exports.OFFLINE_STATUS_CHANGED = void 0;
// Literal ACTION typing allows to ensure a stricter type than string
var OFFLINE_STATUS_CHANGED = 'Offline/STATUS_CHANGED';
exports.OFFLINE_STATUS_CHANGED = OFFLINE_STATUS_CHANGED;
var OFFLINE_SCHEDULE_RETRY = 'Offline/SCHEDULE_RETRY';
exports.OFFLINE_SCHEDULE_RETRY = OFFLINE_SCHEDULE_RETRY;
var OFFLINE_COMPLETE_RETRY = 'Offline/COMPLETE_RETRY';
exports.OFFLINE_COMPLETE_RETRY = OFFLINE_COMPLETE_RETRY;
var OFFLINE_SEND = 'Offline/SEND';
exports.OFFLINE_SEND = OFFLINE_SEND;
var OFFLINE_BUSY = 'Offline/BUSY';
exports.OFFLINE_BUSY = OFFLINE_BUSY;
var RESET_STATE = 'Offline/RESET_STATE';
exports.RESET_STATE = RESET_STATE;
var PERSIST_REHYDRATE = 'persist/REHYDRATE';
exports.PERSIST_REHYDRATE = PERSIST_REHYDRATE;
var JS_ERROR = 'Offline/JS_ERROR';
exports.JS_ERROR = JS_ERROR;
var DEFAULT_COMMIT = 'Offline/DEFAULT_COMMIT';
exports.DEFAULT_COMMIT = DEFAULT_COMMIT;
var DEFAULT_ROLLBACK = 'Offline/DEFAULT_ROLLBACK';
exports.DEFAULT_ROLLBACK = DEFAULT_ROLLBACK;
});

unwrapExports(constants);
var constants_1 = constants.DEFAULT_ROLLBACK;
var constants_2 = constants.DEFAULT_COMMIT;
var constants_3 = constants.JS_ERROR;
var constants_4 = constants.PERSIST_REHYDRATE;
var constants_5 = constants.RESET_STATE;
var constants_6 = constants.OFFLINE_BUSY;
var constants_7 = constants.OFFLINE_SEND;
var constants_8 = constants.OFFLINE_COMPLETE_RETRY;
var constants_9 = constants.OFFLINE_SCHEDULE_RETRY;
var constants_10 = constants.OFFLINE_STATUS_CHANGED;

var actions = createCommonjsModule(function (module, exports) {



Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.busy = exports.completeRetry = exports.scheduleRetry = exports.networkStatusChanged = void 0;

var _typeof2 = interopRequireDefault(_typeof_1);



var networkStatusChanged = function networkStatusChanged(params) {
  var payload;

  if ((0, _typeof2.default)(params) === 'object') {
    payload = params;
  } else {
    payload = {
      online: params
    };
  }

  return {
    type: constants.OFFLINE_STATUS_CHANGED,
    payload: payload
  };
};

exports.networkStatusChanged = networkStatusChanged;

var scheduleRetry = function scheduleRetry() {
  var delay = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;
  return {
    type: constants.OFFLINE_SCHEDULE_RETRY,
    payload: {
      delay: delay
    }
  };
};

exports.scheduleRetry = scheduleRetry;

var completeRetry = function completeRetry(action) {
  return {
    type: constants.OFFLINE_COMPLETE_RETRY,
    payload: action
  };
};

exports.completeRetry = completeRetry;

var busy = function busy(isBusy) {
  return {
    type: constants.OFFLINE_BUSY,
    payload: {
      busy: isBusy
    }
  };
};

exports.busy = busy;
});

unwrapExports(actions);
var actions_1 = actions.busy;
var actions_2 = actions.completeRetry;
var actions_3 = actions.scheduleRetry;
var actions_4 = actions.networkStatusChanged;

var runtime_1 = createCommonjsModule(function (module) {
/**
 * Copyright (c) 2014-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

var runtime = (function (exports) {

  var Op = Object.prototype;
  var hasOwn = Op.hasOwnProperty;
  var undefined$1; // More compressible than void 0.
  var $Symbol = typeof Symbol === "function" ? Symbol : {};
  var iteratorSymbol = $Symbol.iterator || "@@iterator";
  var asyncIteratorSymbol = $Symbol.asyncIterator || "@@asyncIterator";
  var toStringTagSymbol = $Symbol.toStringTag || "@@toStringTag";

  function wrap(innerFn, outerFn, self, tryLocsList) {
    // If outerFn provided and outerFn.prototype is a Generator, then outerFn.prototype instanceof Generator.
    var protoGenerator = outerFn && outerFn.prototype instanceof Generator ? outerFn : Generator;
    var generator = Object.create(protoGenerator.prototype);
    var context = new Context(tryLocsList || []);

    // The ._invoke method unifies the implementations of the .next,
    // .throw, and .return methods.
    generator._invoke = makeInvokeMethod(innerFn, self, context);

    return generator;
  }
  exports.wrap = wrap;

  // Try/catch helper to minimize deoptimizations. Returns a completion
  // record like context.tryEntries[i].completion. This interface could
  // have been (and was previously) designed to take a closure to be
  // invoked without arguments, but in all the cases we care about we
  // already have an existing method we want to call, so there's no need
  // to create a new function object. We can even get away with assuming
  // the method takes exactly one argument, since that happens to be true
  // in every case, so we don't have to touch the arguments object. The
  // only additional allocation required is the completion record, which
  // has a stable shape and so hopefully should be cheap to allocate.
  function tryCatch(fn, obj, arg) {
    try {
      return { type: "normal", arg: fn.call(obj, arg) };
    } catch (err) {
      return { type: "throw", arg: err };
    }
  }

  var GenStateSuspendedStart = "suspendedStart";
  var GenStateSuspendedYield = "suspendedYield";
  var GenStateExecuting = "executing";
  var GenStateCompleted = "completed";

  // Returning this object from the innerFn has the same effect as
  // breaking out of the dispatch switch statement.
  var ContinueSentinel = {};

  // Dummy constructor functions that we use as the .constructor and
  // .constructor.prototype properties for functions that return Generator
  // objects. For full spec compliance, you may wish to configure your
  // minifier not to mangle the names of these two functions.
  function Generator() {}
  function GeneratorFunction() {}
  function GeneratorFunctionPrototype() {}

  // This is a polyfill for %IteratorPrototype% for environments that
  // don't natively support it.
  var IteratorPrototype = {};
  IteratorPrototype[iteratorSymbol] = function () {
    return this;
  };

  var getProto = Object.getPrototypeOf;
  var NativeIteratorPrototype = getProto && getProto(getProto(values([])));
  if (NativeIteratorPrototype &&
      NativeIteratorPrototype !== Op &&
      hasOwn.call(NativeIteratorPrototype, iteratorSymbol)) {
    // This environment has a native %IteratorPrototype%; use it instead
    // of the polyfill.
    IteratorPrototype = NativeIteratorPrototype;
  }

  var Gp = GeneratorFunctionPrototype.prototype =
    Generator.prototype = Object.create(IteratorPrototype);
  GeneratorFunction.prototype = Gp.constructor = GeneratorFunctionPrototype;
  GeneratorFunctionPrototype.constructor = GeneratorFunction;
  GeneratorFunctionPrototype[toStringTagSymbol] =
    GeneratorFunction.displayName = "GeneratorFunction";

  // Helper for defining the .next, .throw, and .return methods of the
  // Iterator interface in terms of a single ._invoke method.
  function defineIteratorMethods(prototype) {
    ["next", "throw", "return"].forEach(function(method) {
      prototype[method] = function(arg) {
        return this._invoke(method, arg);
      };
    });
  }

  exports.isGeneratorFunction = function(genFun) {
    var ctor = typeof genFun === "function" && genFun.constructor;
    return ctor
      ? ctor === GeneratorFunction ||
        // For the native GeneratorFunction constructor, the best we can
        // do is to check its .name property.
        (ctor.displayName || ctor.name) === "GeneratorFunction"
      : false;
  };

  exports.mark = function(genFun) {
    if (Object.setPrototypeOf) {
      Object.setPrototypeOf(genFun, GeneratorFunctionPrototype);
    } else {
      genFun.__proto__ = GeneratorFunctionPrototype;
      if (!(toStringTagSymbol in genFun)) {
        genFun[toStringTagSymbol] = "GeneratorFunction";
      }
    }
    genFun.prototype = Object.create(Gp);
    return genFun;
  };

  // Within the body of any async function, `await x` is transformed to
  // `yield regeneratorRuntime.awrap(x)`, so that the runtime can test
  // `hasOwn.call(value, "__await")` to determine if the yielded value is
  // meant to be awaited.
  exports.awrap = function(arg) {
    return { __await: arg };
  };

  function AsyncIterator(generator) {
    function invoke(method, arg, resolve, reject) {
      var record = tryCatch(generator[method], generator, arg);
      if (record.type === "throw") {
        reject(record.arg);
      } else {
        var result = record.arg;
        var value = result.value;
        if (value &&
            typeof value === "object" &&
            hasOwn.call(value, "__await")) {
          return Promise.resolve(value.__await).then(function(value) {
            invoke("next", value, resolve, reject);
          }, function(err) {
            invoke("throw", err, resolve, reject);
          });
        }

        return Promise.resolve(value).then(function(unwrapped) {
          // When a yielded Promise is resolved, its final value becomes
          // the .value of the Promise<{value,done}> result for the
          // current iteration.
          result.value = unwrapped;
          resolve(result);
        }, function(error) {
          // If a rejected Promise was yielded, throw the rejection back
          // into the async generator function so it can be handled there.
          return invoke("throw", error, resolve, reject);
        });
      }
    }

    var previousPromise;

    function enqueue(method, arg) {
      function callInvokeWithMethodAndArg() {
        return new Promise(function(resolve, reject) {
          invoke(method, arg, resolve, reject);
        });
      }

      return previousPromise =
        // If enqueue has been called before, then we want to wait until
        // all previous Promises have been resolved before calling invoke,
        // so that results are always delivered in the correct order. If
        // enqueue has not been called before, then it is important to
        // call invoke immediately, without waiting on a callback to fire,
        // so that the async generator function has the opportunity to do
        // any necessary setup in a predictable way. This predictability
        // is why the Promise constructor synchronously invokes its
        // executor callback, and why async functions synchronously
        // execute code before the first await. Since we implement simple
        // async functions in terms of async generators, it is especially
        // important to get this right, even though it requires care.
        previousPromise ? previousPromise.then(
          callInvokeWithMethodAndArg,
          // Avoid propagating failures to Promises returned by later
          // invocations of the iterator.
          callInvokeWithMethodAndArg
        ) : callInvokeWithMethodAndArg();
    }

    // Define the unified helper method that is used to implement .next,
    // .throw, and .return (see defineIteratorMethods).
    this._invoke = enqueue;
  }

  defineIteratorMethods(AsyncIterator.prototype);
  AsyncIterator.prototype[asyncIteratorSymbol] = function () {
    return this;
  };
  exports.AsyncIterator = AsyncIterator;

  // Note that simple async functions are implemented on top of
  // AsyncIterator objects; they just return a Promise for the value of
  // the final result produced by the iterator.
  exports.async = function(innerFn, outerFn, self, tryLocsList) {
    var iter = new AsyncIterator(
      wrap(innerFn, outerFn, self, tryLocsList)
    );

    return exports.isGeneratorFunction(outerFn)
      ? iter // If outerFn is a generator, return the full iterator.
      : iter.next().then(function(result) {
          return result.done ? result.value : iter.next();
        });
  };

  function makeInvokeMethod(innerFn, self, context) {
    var state = GenStateSuspendedStart;

    return function invoke(method, arg) {
      if (state === GenStateExecuting) {
        throw new Error("Generator is already running");
      }

      if (state === GenStateCompleted) {
        if (method === "throw") {
          throw arg;
        }

        // Be forgiving, per 25.3.3.3.3 of the spec:
        // https://people.mozilla.org/~jorendorff/es6-draft.html#sec-generatorresume
        return doneResult();
      }

      context.method = method;
      context.arg = arg;

      while (true) {
        var delegate = context.delegate;
        if (delegate) {
          var delegateResult = maybeInvokeDelegate(delegate, context);
          if (delegateResult) {
            if (delegateResult === ContinueSentinel) continue;
            return delegateResult;
          }
        }

        if (context.method === "next") {
          // Setting context._sent for legacy support of Babel's
          // function.sent implementation.
          context.sent = context._sent = context.arg;

        } else if (context.method === "throw") {
          if (state === GenStateSuspendedStart) {
            state = GenStateCompleted;
            throw context.arg;
          }

          context.dispatchException(context.arg);

        } else if (context.method === "return") {
          context.abrupt("return", context.arg);
        }

        state = GenStateExecuting;

        var record = tryCatch(innerFn, self, context);
        if (record.type === "normal") {
          // If an exception is thrown from innerFn, we leave state ===
          // GenStateExecuting and loop back for another invocation.
          state = context.done
            ? GenStateCompleted
            : GenStateSuspendedYield;

          if (record.arg === ContinueSentinel) {
            continue;
          }

          return {
            value: record.arg,
            done: context.done
          };

        } else if (record.type === "throw") {
          state = GenStateCompleted;
          // Dispatch the exception by looping back around to the
          // context.dispatchException(context.arg) call above.
          context.method = "throw";
          context.arg = record.arg;
        }
      }
    };
  }

  // Call delegate.iterator[context.method](context.arg) and handle the
  // result, either by returning a { value, done } result from the
  // delegate iterator, or by modifying context.method and context.arg,
  // setting context.delegate to null, and returning the ContinueSentinel.
  function maybeInvokeDelegate(delegate, context) {
    var method = delegate.iterator[context.method];
    if (method === undefined$1) {
      // A .throw or .return when the delegate iterator has no .throw
      // method always terminates the yield* loop.
      context.delegate = null;

      if (context.method === "throw") {
        // Note: ["return"] must be used for ES3 parsing compatibility.
        if (delegate.iterator["return"]) {
          // If the delegate iterator has a return method, give it a
          // chance to clean up.
          context.method = "return";
          context.arg = undefined$1;
          maybeInvokeDelegate(delegate, context);

          if (context.method === "throw") {
            // If maybeInvokeDelegate(context) changed context.method from
            // "return" to "throw", let that override the TypeError below.
            return ContinueSentinel;
          }
        }

        context.method = "throw";
        context.arg = new TypeError(
          "The iterator does not provide a 'throw' method");
      }

      return ContinueSentinel;
    }

    var record = tryCatch(method, delegate.iterator, context.arg);

    if (record.type === "throw") {
      context.method = "throw";
      context.arg = record.arg;
      context.delegate = null;
      return ContinueSentinel;
    }

    var info = record.arg;

    if (! info) {
      context.method = "throw";
      context.arg = new TypeError("iterator result is not an object");
      context.delegate = null;
      return ContinueSentinel;
    }

    if (info.done) {
      // Assign the result of the finished delegate to the temporary
      // variable specified by delegate.resultName (see delegateYield).
      context[delegate.resultName] = info.value;

      // Resume execution at the desired location (see delegateYield).
      context.next = delegate.nextLoc;

      // If context.method was "throw" but the delegate handled the
      // exception, let the outer generator proceed normally. If
      // context.method was "next", forget context.arg since it has been
      // "consumed" by the delegate iterator. If context.method was
      // "return", allow the original .return call to continue in the
      // outer generator.
      if (context.method !== "return") {
        context.method = "next";
        context.arg = undefined$1;
      }

    } else {
      // Re-yield the result returned by the delegate method.
      return info;
    }

    // The delegate iterator is finished, so forget it and continue with
    // the outer generator.
    context.delegate = null;
    return ContinueSentinel;
  }

  // Define Generator.prototype.{next,throw,return} in terms of the
  // unified ._invoke helper method.
  defineIteratorMethods(Gp);

  Gp[toStringTagSymbol] = "Generator";

  // A Generator should always return itself as the iterator object when the
  // @@iterator function is called on it. Some browsers' implementations of the
  // iterator prototype chain incorrectly implement this, causing the Generator
  // object to not be returned from this call. This ensures that doesn't happen.
  // See https://github.com/facebook/regenerator/issues/274 for more details.
  Gp[iteratorSymbol] = function() {
    return this;
  };

  Gp.toString = function() {
    return "[object Generator]";
  };

  function pushTryEntry(locs) {
    var entry = { tryLoc: locs[0] };

    if (1 in locs) {
      entry.catchLoc = locs[1];
    }

    if (2 in locs) {
      entry.finallyLoc = locs[2];
      entry.afterLoc = locs[3];
    }

    this.tryEntries.push(entry);
  }

  function resetTryEntry(entry) {
    var record = entry.completion || {};
    record.type = "normal";
    delete record.arg;
    entry.completion = record;
  }

  function Context(tryLocsList) {
    // The root entry object (effectively a try statement without a catch
    // or a finally block) gives us a place to store values thrown from
    // locations where there is no enclosing try statement.
    this.tryEntries = [{ tryLoc: "root" }];
    tryLocsList.forEach(pushTryEntry, this);
    this.reset(true);
  }

  exports.keys = function(object) {
    var keys = [];
    for (var key in object) {
      keys.push(key);
    }
    keys.reverse();

    // Rather than returning an object with a next method, we keep
    // things simple and return the next function itself.
    return function next() {
      while (keys.length) {
        var key = keys.pop();
        if (key in object) {
          next.value = key;
          next.done = false;
          return next;
        }
      }

      // To avoid creating an additional object, we just hang the .value
      // and .done properties off the next function object itself. This
      // also ensures that the minifier will not anonymize the function.
      next.done = true;
      return next;
    };
  };

  function values(iterable) {
    if (iterable) {
      var iteratorMethod = iterable[iteratorSymbol];
      if (iteratorMethod) {
        return iteratorMethod.call(iterable);
      }

      if (typeof iterable.next === "function") {
        return iterable;
      }

      if (!isNaN(iterable.length)) {
        var i = -1, next = function next() {
          while (++i < iterable.length) {
            if (hasOwn.call(iterable, i)) {
              next.value = iterable[i];
              next.done = false;
              return next;
            }
          }

          next.value = undefined$1;
          next.done = true;

          return next;
        };

        return next.next = next;
      }
    }

    // Return an iterator with no values.
    return { next: doneResult };
  }
  exports.values = values;

  function doneResult() {
    return { value: undefined$1, done: true };
  }

  Context.prototype = {
    constructor: Context,

    reset: function(skipTempReset) {
      this.prev = 0;
      this.next = 0;
      // Resetting context._sent for legacy support of Babel's
      // function.sent implementation.
      this.sent = this._sent = undefined$1;
      this.done = false;
      this.delegate = null;

      this.method = "next";
      this.arg = undefined$1;

      this.tryEntries.forEach(resetTryEntry);

      if (!skipTempReset) {
        for (var name in this) {
          // Not sure about the optimal order of these conditions:
          if (name.charAt(0) === "t" &&
              hasOwn.call(this, name) &&
              !isNaN(+name.slice(1))) {
            this[name] = undefined$1;
          }
        }
      }
    },

    stop: function() {
      this.done = true;

      var rootEntry = this.tryEntries[0];
      var rootRecord = rootEntry.completion;
      if (rootRecord.type === "throw") {
        throw rootRecord.arg;
      }

      return this.rval;
    },

    dispatchException: function(exception) {
      if (this.done) {
        throw exception;
      }

      var context = this;
      function handle(loc, caught) {
        record.type = "throw";
        record.arg = exception;
        context.next = loc;

        if (caught) {
          // If the dispatched exception was caught by a catch block,
          // then let that catch block handle the exception normally.
          context.method = "next";
          context.arg = undefined$1;
        }

        return !! caught;
      }

      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        var record = entry.completion;

        if (entry.tryLoc === "root") {
          // Exception thrown outside of any try block that could handle
          // it, so set the completion value of the entire function to
          // throw the exception.
          return handle("end");
        }

        if (entry.tryLoc <= this.prev) {
          var hasCatch = hasOwn.call(entry, "catchLoc");
          var hasFinally = hasOwn.call(entry, "finallyLoc");

          if (hasCatch && hasFinally) {
            if (this.prev < entry.catchLoc) {
              return handle(entry.catchLoc, true);
            } else if (this.prev < entry.finallyLoc) {
              return handle(entry.finallyLoc);
            }

          } else if (hasCatch) {
            if (this.prev < entry.catchLoc) {
              return handle(entry.catchLoc, true);
            }

          } else if (hasFinally) {
            if (this.prev < entry.finallyLoc) {
              return handle(entry.finallyLoc);
            }

          } else {
            throw new Error("try statement without catch or finally");
          }
        }
      }
    },

    abrupt: function(type, arg) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.tryLoc <= this.prev &&
            hasOwn.call(entry, "finallyLoc") &&
            this.prev < entry.finallyLoc) {
          var finallyEntry = entry;
          break;
        }
      }

      if (finallyEntry &&
          (type === "break" ||
           type === "continue") &&
          finallyEntry.tryLoc <= arg &&
          arg <= finallyEntry.finallyLoc) {
        // Ignore the finally entry if control is not jumping to a
        // location outside the try/catch block.
        finallyEntry = null;
      }

      var record = finallyEntry ? finallyEntry.completion : {};
      record.type = type;
      record.arg = arg;

      if (finallyEntry) {
        this.method = "next";
        this.next = finallyEntry.finallyLoc;
        return ContinueSentinel;
      }

      return this.complete(record);
    },

    complete: function(record, afterLoc) {
      if (record.type === "throw") {
        throw record.arg;
      }

      if (record.type === "break" ||
          record.type === "continue") {
        this.next = record.arg;
      } else if (record.type === "return") {
        this.rval = this.arg = record.arg;
        this.method = "return";
        this.next = "end";
      } else if (record.type === "normal" && afterLoc) {
        this.next = afterLoc;
      }

      return ContinueSentinel;
    },

    finish: function(finallyLoc) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.finallyLoc === finallyLoc) {
          this.complete(entry.completion, entry.afterLoc);
          resetTryEntry(entry);
          return ContinueSentinel;
        }
      }
    },

    "catch": function(tryLoc) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.tryLoc === tryLoc) {
          var record = entry.completion;
          if (record.type === "throw") {
            var thrown = record.arg;
            resetTryEntry(entry);
          }
          return thrown;
        }
      }

      // The context.catch method must only be called with a location
      // argument that corresponds to a known catch block.
      throw new Error("illegal catch attempt");
    },

    delegateYield: function(iterable, resultName, nextLoc) {
      this.delegate = {
        iterator: values(iterable),
        resultName: resultName,
        nextLoc: nextLoc
      };

      if (this.method === "next") {
        // Deliberately forget the last sent value so that we don't
        // accidentally pass it on to the delegate.
        this.arg = undefined$1;
      }

      return ContinueSentinel;
    }
  };

  // Regardless of whether this script is executing as a CommonJS module
  // or not, return the runtime object so that we can declare the variable
  // regeneratorRuntime in the outer scope, which allows this module to be
  // injected easily by `bin/regenerator --include-runtime script.js`.
  return exports;

}(
  // If this script is executing as a CommonJS module, use module.exports
  // as the regeneratorRuntime namespace. Otherwise create a new empty
  // object. Either way, the resulting object will be used to initialize
  // the regeneratorRuntime variable at the top of this file.
   module.exports 
));

try {
  regeneratorRuntime = runtime;
} catch (accidentalStrictMode) {
  // This module should not be running in strict mode, so the above
  // assignment should always work unless something is misconfigured. Just
  // in case runtime.js accidentally runs in strict mode, we can escape
  // strict mode using a global Function call. This could conceivably fail
  // if a Content Security Policy forbids using Function, but in that case
  // the proper solution is to fix the accidental strict mode problem. If
  // you've misconfigured your bundler to force strict mode and applied a
  // CSP to forbid Function, and you're not willing to fix either of those
  // problems, please detail your unique predicament in a GitHub issue.
  Function("r", "regeneratorRuntime = r")(runtime);
}
});

var regenerator = runtime_1;

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

var asyncToGenerator = _asyncToGenerator;

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

var defineProperty = _defineProperty;

var send_1 = createCommonjsModule(function (module, exports) {



Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _regenerator = interopRequireDefault(regenerator);

var _asyncToGenerator2 = interopRequireDefault(asyncToGenerator);

var _defineProperty2 = interopRequireDefault(defineProperty);





function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(source, true).forEach(function (key) { (0, _defineProperty2.default)(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(source).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

var complete = function complete(action, result, offlineAction, config) {
  var _config$offlineAction = config.offlineActionTracker,
      resolveAction = _config$offlineAction.resolveAction,
      rejectAction = _config$offlineAction.rejectAction;

  if (result.success) {
    resolveAction(offlineAction.meta.transaction, result.payload);
  } else if (result.payload) {
    rejectAction(offlineAction.meta.transaction, result.payload);
  }

  return _objectSpread({}, action, {
    payload: result.payload,
    meta: _objectSpread({}, action.meta, {
      success: result.success,
      completed: true
    })
  });
};

var handleJsError = function handleJsError(error) {
  return {
    type: constants.JS_ERROR,
    meta: {
      error: error,
      success: false,
      completed: true
    }
  };
};

var send = function send(action, dispatch, config) {
  var retries = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : 0;
  var metadata = action.meta.offline;
  dispatch((0, actions.busy)(true));
  return config.effect(metadata.effect, action).then(function (result) {
    var commitAction = metadata.commit || _objectSpread({}, config.defaultCommit, {
      meta: _objectSpread({}, config.defaultCommit.meta, {
        offlineAction: action
      })
    });

    try {
      return dispatch(complete(commitAction, {
        success: true,
        payload: result
      }, action, config));
    } catch (error) {
      return dispatch(handleJsError(error));
    }
  }).catch(
  /*#__PURE__*/
  function () {
    var _ref = (0, _asyncToGenerator2.default)(
    /*#__PURE__*/
    _regenerator.default.mark(function _callee(error) {
      var rollbackAction, mustDiscard, delay;
      return _regenerator.default.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              rollbackAction = metadata.rollback || _objectSpread({}, config.defaultRollback, {
                meta: _objectSpread({}, config.defaultRollback.meta, {
                  offlineAction: action
                })
              }); // discard

              mustDiscard = true;
              _context.prev = 2;
              _context.next = 5;
              return config.discard(error, action, retries);

            case 5:
              mustDiscard = _context.sent;
              _context.next = 11;
              break;

            case 8:
              _context.prev = 8;
              _context.t0 = _context["catch"](2);
              console.warn(_context.t0);

            case 11:
              if (mustDiscard) {
                _context.next = 15;
                break;
              }

              delay = config.retry(action, retries);

              if (!(delay != null)) {
                _context.next = 15;
                break;
              }

              return _context.abrupt("return", dispatch((0, actions.scheduleRetry)(delay)));

            case 15:
              return _context.abrupt("return", dispatch(complete(rollbackAction, {
                success: false,
                payload: error
              }, action, config)));

            case 16:
            case "end":
              return _context.stop();
          }
        }
      }, _callee, null, [[2, 8]]);
    }));

    return function (_x) {
      return _ref.apply(this, arguments);
    };
  }()).finally(function () {
    return dispatch((0, actions.busy)(false));
  });
};

var _default = send;
exports.default = _default;
});

unwrapExports(send_1);

var middleware = createCommonjsModule(function (module, exports) {



Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.createOfflineMiddleware = void 0;





var _send = interopRequireDefault(send_1);

var after = function after() {
  var timeout = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;
  return new Promise(function (resolve) {
    return setTimeout(resolve, timeout);
  });
};

var createOfflineMiddleware = function createOfflineMiddleware(config) {
  return function (store) {
    return function (next) {
      return function (action) {
        // allow other middleware to do their things
        var result = next(action);
        var promise; // find any actions to send, if any

        var state = store.getState();
        var offline = config.offlineStateLens(state).get;
        var context = {
          offline: offline
        };
        var offlineAction = config.queue.peek(offline.outbox, action, context); // create promise to return on enqueue offline action

        if (action.meta && action.meta.offline) {
          var registerAction = config.offlineActionTracker.registerAction;
          promise = registerAction(offline.lastTransaction);
        } // if there are any actions in the queue that we are not
        // yet processing, send those actions


        if (offlineAction && !offline.busy && !offline.retryScheduled && offline.online) {
          (0, _send.default)(offlineAction, store.dispatch, config, offline.retryCount);
        }

        if (action.type === constants.OFFLINE_SCHEDULE_RETRY) {
          after(action.payload.delay).then(function () {
            store.dispatch((0, actions.completeRetry)(offlineAction));
          });
        }

        if (action.type === constants.OFFLINE_SEND && offlineAction && !offline.busy) {
          (0, _send.default)(offlineAction, store.dispatch, config, offline.retryCount);
        }

        return promise || result;
      };
    };
  };
};

exports.createOfflineMiddleware = createOfflineMiddleware;
});

unwrapExports(middleware);
var middleware_1 = middleware.createOfflineMiddleware;

var updater = createCommonjsModule(function (module, exports) {



Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.enhanceReducer = exports.buildOfflineUpdater = exports.initialState = void 0;

var _defineProperty2 = interopRequireDefault(defineProperty);



function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(source, true).forEach(function (key) { (0, _defineProperty2.default)(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(source).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

var initialState = {
  busy: false,
  lastTransaction: 0,
  online: false,
  outbox: [],
  retryCount: 0,
  retryScheduled: false,
  netInfo: {
    isConnectionExpensive: null,
    reach: 'NONE'
  }
};
exports.initialState = initialState;

var buildOfflineUpdater = function buildOfflineUpdater(dequeue, enqueue) {
  return function offlineUpdater() {
    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : initialState;
    var action = arguments.length > 1 ? arguments[1] : undefined;

    // Update online/offline status
    if (action.type === constants.OFFLINE_STATUS_CHANGED && !action.meta) {
      return _objectSpread({}, state, {
        online: action.payload.online,
        netInfo: action.payload.netInfo
      });
    }

    if (action.type === constants.PERSIST_REHYDRATE && action.payload) {
      return _objectSpread({}, state, {}, action.payload.offline || {}, {
        online: state.online,
        netInfo: state.netInfo,
        retryScheduled: initialState.retryScheduled,
        retryCount: initialState.retryCount,
        busy: initialState.busy
      });
    }

    if (action.type === constants.OFFLINE_SCHEDULE_RETRY) {
      return _objectSpread({}, state, {
        retryScheduled: true,
        retryCount: state.retryCount + 1
      });
    }

    if (action.type === constants.OFFLINE_COMPLETE_RETRY) {
      return _objectSpread({}, state, {
        retryScheduled: false
      });
    }

    if (action.type === constants.OFFLINE_BUSY && !action.meta && action.payload && typeof action.payload.busy === 'boolean') {
      return _objectSpread({}, state, {
        busy: action.payload.busy
      });
    } // Add offline actions to queue


    if (action.meta && action.meta.offline) {
      var transaction = state.lastTransaction + 1;

      var stamped = _objectSpread({}, action, {
        meta: _objectSpread({}, action.meta, {
          transaction: transaction
        })
      });

      var offline = state;
      return _objectSpread({}, state, {
        lastTransaction: transaction,
        outbox: enqueue(offline.outbox, stamped, {
          offline: offline
        })
      });
    } // Remove completed actions from queue (success or fail)


    if (action.meta && action.meta.completed === true) {
      var _offline = state;
      return _objectSpread({}, state, {
        outbox: dequeue(_offline.outbox, action, {
          offline: _offline
        }),
        retryCount: 0
      });
    }

    if (action.type === constants.RESET_STATE) {
      return _objectSpread({}, initialState, {
        online: state.online,
        netInfo: state.netInfo
      });
    }

    return state;
  };
};

exports.buildOfflineUpdater = buildOfflineUpdater;

var enhanceReducer = function enhanceReducer(reducer, config) {
  var _config$queue = config.queue,
      dequeue = _config$queue.dequeue,
      enqueue = _config$queue.enqueue;
  var offlineUpdater = buildOfflineUpdater(dequeue, enqueue);
  return function (state, action) {
    var offlineState;
    var restState;

    if (typeof state !== 'undefined') {
      offlineState = config.offlineStateLens(state).get;
      restState = config.offlineStateLens(state).set();
    }

    return config.offlineStateLens(reducer(restState, action)).set(offlineUpdater(offlineState, action));
  };
};

exports.enhanceReducer = enhanceReducer;
});

unwrapExports(updater);
var updater_1 = updater.enhanceReducer;
var updater_2 = updater.buildOfflineUpdater;
var updater_3 = updater.initialState;

var persist = createCommonjsModule(function (module, exports) {

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;



// flow
var _default = reduxPersist.persistStore;
exports.default = _default;
});

unwrapExports(persist);

var detectNetwork = createCommonjsModule(function (module, exports) {

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

/* global window */
var handle = function handle(callback, online) {
  // NetInfo is not supported in browsers, hence we only pass online status
  if (window.requestAnimationFrame) {
    window.requestAnimationFrame(function () {
      return callback({
        online: online
      });
    });
  } else {
    setTimeout(function () {
      return callback({
        online: online
      });
    }, 0);
  }
};

var _default = function _default(callback) {
  if (typeof window !== 'undefined' && window.addEventListener) {
    window.addEventListener('online', function () {
      return handle(callback, true);
    });
    window.addEventListener('offline', function () {
      return handle(callback, false);
    });
    handle(callback, window.navigator.onLine);
  }
};

exports.default = _default;
});

unwrapExports(detectNetwork);

function _objectWithoutPropertiesLoose(source, excluded) {
  if (source == null) return {};
  var target = {};
  var sourceKeys = Object.keys(source);
  var key, i;

  for (i = 0; i < sourceKeys.length; i++) {
    key = sourceKeys[i];
    if (excluded.indexOf(key) >= 0) continue;
    target[key] = source[key];
  }

  return target;
}

var objectWithoutPropertiesLoose = _objectWithoutPropertiesLoose;

function _objectWithoutProperties(source, excluded) {
  if (source == null) return {};
  var target = objectWithoutPropertiesLoose(source, excluded);
  var key, i;

  if (Object.getOwnPropertySymbols) {
    var sourceSymbolKeys = Object.getOwnPropertySymbols(source);

    for (i = 0; i < sourceSymbolKeys.length; i++) {
      key = sourceSymbolKeys[i];
      if (excluded.indexOf(key) >= 0) continue;
      if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue;
      target[key] = source[key];
    }
  }

  return target;
}

var objectWithoutProperties = _objectWithoutProperties;

var effect = createCommonjsModule(function (module, exports) {



Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.NetworkError = NetworkError;
exports.default = exports.getHeaders = void 0;

var _defineProperty2 = interopRequireDefault(defineProperty);

var _objectWithoutProperties2 = interopRequireDefault(objectWithoutProperties);

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(source, true).forEach(function (key) { (0, _defineProperty2.default)(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(source).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

/* global fetch */
function NetworkError(response, status) {
  this.name = 'NetworkError';
  this.status = status;
  this.response = response;
} // $FlowFixMe


NetworkError.prototype = Error.prototype;

var tryParseJSON = function tryParseJSON(json) {
  if (!json) {
    return null;
  }

  try {
    return JSON.parse(json);
  } catch (e) {
    throw new Error("Failed to parse unexpected JSON response: ".concat(json));
  }
};

var getResponseBody = function getResponseBody(res) {
  var contentType = res.headers.get('content-type') || false;

  if (contentType && contentType.indexOf('json') >= 0) {
    return res.text().then(tryParseJSON);
  }

  return res.text();
};

var getHeaders = function getHeaders(headers) {
  var _ref = headers || {},
      contentTypeCapitalized = _ref['Content-Type'],
      contentTypeLowerCase = _ref['content-type'],
      restOfHeaders = (0, _objectWithoutProperties2.default)(_ref, ["Content-Type", "content-type"]);

  var contentType = contentTypeCapitalized || contentTypeLowerCase || 'application/json';
  return _objectSpread({}, restOfHeaders, {
    'content-type': contentType
  });
}; // eslint-disable-next-line no-unused-vars


exports.getHeaders = getHeaders;

var _default = function _default(effect, _action) {
  var url = effect.url,
      json = effect.json,
      options = (0, _objectWithoutProperties2.default)(effect, ["url", "json"]);
  var headers = getHeaders(options.headers);

  if (json !== null && json !== undefined) {
    try {
      options.body = JSON.stringify(json);
    } catch (e) {
      return Promise.reject(e);
    }
  }

  return fetch(url, _objectSpread({}, options, {
    headers: headers
  })).then(function (res) {
    if (res.ok) {
      return getResponseBody(res);
    }

    return getResponseBody(res).then(function (body) {
      throw new NetworkError(body || '', res.status);
    });
  });
};

exports.default = _default;
});

unwrapExports(effect);
var effect_1 = effect.NetworkError;
var effect_2 = effect.getHeaders;

var retry = createCommonjsModule(function (module, exports) {

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
var decaySchedule = [1000, // After 1 seconds
1000 * 5, // After 5 seconds
1000 * 15, // After 15 seconds
1000 * 30, // After 30 seconds
1000 * 60, // After 1 minute
1000 * 60 * 3, // After 3 minutes
1000 * 60 * 5, // After 5 minutes
1000 * 60 * 10, // After 10 minutes
1000 * 60 * 30, // After 30 minutes
1000 * 60 * 60 // After 1 hour
];

var _default = function _default(action, retries) {
  return decaySchedule[retries] || null;
};

exports.default = _default;
});

unwrapExports(retry);

var discard = createCommonjsModule(function (module, exports) {

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;



var _default = function _default(error, action) {

  // not a network error -> discard
  if (!('status' in error)) {
    return true;
  } // discard http 4xx errors
  // $FlowFixMe


  return error.status >= 400 && error.status < 500;
};

exports.default = _default;
});

unwrapExports(discard);

var defaultCommit_1 = createCommonjsModule(function (module, exports) {

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;



var defaultCommit = {
  type: constants.DEFAULT_COMMIT
};
var _default = defaultCommit;
exports.default = _default;
});

unwrapExports(defaultCommit_1);

var defaultRollback_1 = createCommonjsModule(function (module, exports) {

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;



var defaultRollback = {
  type: constants.DEFAULT_ROLLBACK
};
var _default = defaultRollback;
exports.default = _default;
});

unwrapExports(defaultRollback_1);

var persistAutoRehydrate = createCommonjsModule(function (module, exports) {

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;



var _default = reduxPersist.autoRehydrate;
exports.default = _default;
});

unwrapExports(persistAutoRehydrate);

var offlineStateLens = createCommonjsModule(function (module, exports) {



Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _defineProperty2 = interopRequireDefault(defineProperty);

var _objectWithoutProperties2 = interopRequireDefault(objectWithoutProperties);

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(source, true).forEach(function (key) { (0, _defineProperty2.default)(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(source).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

var _default = function _default(state) {
  var offline = state.offline,
      rest = (0, _objectWithoutProperties2.default)(state, ["offline"]);
  return {
    get: offline,
    set: function set(offlineState) {
      return typeof offlineState === 'undefined' ? rest : _objectSpread({
        offline: offlineState
      }, rest);
    }
  };
};

exports.default = _default;
});

unwrapExports(offlineStateLens);

function _arrayWithHoles(arr) {
  if (Array.isArray(arr)) return arr;
}

var arrayWithHoles = _arrayWithHoles;

function _iterableToArray(iter) {
  if (Symbol.iterator in Object(iter) || Object.prototype.toString.call(iter) === "[object Arguments]") return Array.from(iter);
}

var iterableToArray = _iterableToArray;

function _nonIterableRest() {
  throw new TypeError("Invalid attempt to destructure non-iterable instance");
}

var nonIterableRest = _nonIterableRest;

function _toArray(arr) {
  return arrayWithHoles(arr) || iterableToArray(arr) || nonIterableRest();
}

var toArray = _toArray;

function _arrayWithoutHoles(arr) {
  if (Array.isArray(arr)) {
    for (var i = 0, arr2 = new Array(arr.length); i < arr.length; i++) {
      arr2[i] = arr[i];
    }

    return arr2;
  }
}

var arrayWithoutHoles = _arrayWithoutHoles;

function _nonIterableSpread() {
  throw new TypeError("Invalid attempt to spread non-iterable instance");
}

var nonIterableSpread = _nonIterableSpread;

function _toConsumableArray(arr) {
  return arrayWithoutHoles(arr) || iterableToArray(arr) || nonIterableSpread();
}

var toConsumableArray = _toConsumableArray;

var queue = createCommonjsModule(function (module, exports) {



Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _toArray2 = interopRequireDefault(toArray);

var _toConsumableArray2 = interopRequireDefault(toConsumableArray);

/* eslint-disable no-unused-vars */
function enqueue(array, item, context) {
  return [].concat((0, _toConsumableArray2.default)(array), [item]);
}

function dequeue(array, item, context) {
  var _array = (0, _toArray2.default)(array),
      rest = _array.slice(1);

  return rest;
}

function peek(array, item, context) {
  return array[0];
}

var _default = {
  enqueue: enqueue,
  dequeue: dequeue,
  peek: peek
};
exports.default = _default;
});

unwrapExports(queue);

var defaults = createCommonjsModule(function (module, exports) {



Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _persist = interopRequireDefault(persist);

var _detectNetwork = interopRequireDefault(detectNetwork);

var _effect = interopRequireDefault(effect);

var _retry = interopRequireDefault(retry);

var _discard = interopRequireDefault(discard);

var _defaultCommit = interopRequireDefault(defaultCommit_1);

var _defaultRollback = interopRequireDefault(defaultRollback_1);

var _persistAutoRehydrate = interopRequireDefault(persistAutoRehydrate);

var _offlineStateLens = interopRequireDefault(offlineStateLens);

var _queue = interopRequireDefault(queue);

var _default = {
  rehydrate: true,
  // backward compatibility, TODO remove in the next breaking change version
  persist: _persist.default,
  detectNetwork: _detectNetwork.default,
  effect: _effect.default,
  retry: _retry.default,
  discard: _discard.default,
  defaultCommit: _defaultCommit.default,
  defaultRollback: _defaultRollback.default,
  persistAutoRehydrate: _persistAutoRehydrate.default,
  offlineStateLens: _offlineStateLens.default,
  queue: _queue.default,
  returnPromises: false
};
exports.default = _default;
});

var index = unwrapExports(defaults);

var config = createCommonjsModule(function (module, exports) {



Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.applyDefaults = void 0;

var _defineProperty2 = interopRequireDefault(defineProperty);

var _defaults = interopRequireDefault(defaults);

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(source, true).forEach(function (key) { (0, _defineProperty2.default)(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(source).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

var applyDefaults = function applyDefaults() {
  var config = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
  return _objectSpread({}, _defaults.default, {}, config);
};

exports.applyDefaults = applyDefaults;
});

unwrapExports(config);
var config_1 = config.applyDefaults;

var offlineActionTracker = createCommonjsModule(function (module, exports) {

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
var subscriptions = {};

function registerAction(transaction) {
  return new Promise(function (resolve, reject) {
    subscriptions[transaction] = {
      resolve: resolve,
      reject: reject
    };
  });
}

function resolveAction(transaction, value) {
  var subscription = subscriptions[transaction];

  if (subscription) {
    subscription.resolve(value);
    delete subscriptions[transaction];
  }
}

function rejectAction(transaction, error) {
  var subscription = subscriptions[transaction];

  if (subscription) {
    subscription.reject(error);
    delete subscriptions[transaction];
  }
}

var withPromises = {
  registerAction: registerAction,
  resolveAction: resolveAction,
  rejectAction: rejectAction
};
var withoutPromises = {
  registerAction: function registerAction() {},
  resolveAction: function resolveAction() {},
  rejectAction: function rejectAction() {}
};
var _default = {
  withPromises: withPromises,
  withoutPromises: withoutPromises
};
exports.default = _default;
});

unwrapExports(offlineActionTracker);

var lib = createCommonjsModule(function (module, exports) {



Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.createOffline = exports.offline = void 0;

var _typeof2 = interopRequireDefault(_typeof_1);











var _offlineActionTracker = interopRequireDefault(offlineActionTracker);

/* global $Shape */
// @TODO: Take createStore as config?
var warnIfNotReduxAction = function warnIfNotReduxAction(config, key) {
  var maybeAction = config[key];
  var isNotReduxAction = maybeAction === null || (0, _typeof2.default)(maybeAction) !== 'object' || typeof maybeAction.type !== 'string' || maybeAction.type === '';

  if (isNotReduxAction && console.warn) {
    var msg = "".concat(key, " must be a proper redux action, ") + "i.e. it must be an object and have a non-empty string type. " + "Instead you provided: ".concat(JSON.stringify(maybeAction, null, 2));
    console.warn(msg);
  }
};

var offline = function offline() {
  var userConfig = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
  return function (createStore) {
    return function (reducer, preloadedState) {
      var enhancer = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : function (x) {
        return x;
      };
      var config$1 = (0, config.applyDefaults)(userConfig);
      warnIfNotReduxAction(config$1, 'defaultCommit');
      warnIfNotReduxAction(config$1, 'defaultRollback'); // toggle experimental returned promises

      config$1.offlineActionTracker = config$1.returnPromises ? _offlineActionTracker.default.withPromises : _offlineActionTracker.default.withoutPromises;
      delete config$1.returnPromises; // wraps userland reducer with a top-level
      // reducer that handles offline state updating

      var offlineReducer = (0, updater.enhanceReducer)(reducer, config$1); // $FlowFixMe

      var offlineMiddleware = (0, redux.applyMiddleware)((0, middleware.createOfflineMiddleware)(config$1)); // create autoRehydrate enhancer if required

      var offlineEnhancer = config$1.persist && config$1.rehydrate && config$1.persistAutoRehydrate ? (0, redux.compose)(offlineMiddleware, config$1.persistAutoRehydrate()) : offlineMiddleware; // create store

      var store = offlineEnhancer(createStore)(offlineReducer, preloadedState, enhancer);
      var baseReplaceReducer = store.replaceReducer.bind(store); // $FlowFixMe

      store.replaceReducer = function replaceReducer(nextReducer) {
        return baseReplaceReducer((0, updater.enhanceReducer)(nextReducer, config$1));
      }; // launch store persistor


      if (config$1.persist) {
        config$1.persist(store, config$1.persistOptions, config$1.persistCallback);
      } // launch network detector


      if (config$1.detectNetwork) {
        config$1.detectNetwork(function (online) {
          store.dispatch((0, actions.networkStatusChanged)(online));
        });
      }

      return store;
    };
  };
};

exports.offline = offline;

var createOffline = function createOffline() {
  var userConfig = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
  var config$1 = (0, config.applyDefaults)(userConfig); // toggle experimental returned promises

  config$1.offlineActionTracker = config$1.returnPromises ? _offlineActionTracker.default.withPromises : _offlineActionTracker.default.withoutPromises;
  delete config$1.returnPromises;
  warnIfNotReduxAction(config$1, 'defaultCommit');
  warnIfNotReduxAction(config$1, 'defaultRollback');

  var enhanceStore = function enhanceStore(next) {
    return function (reducer, preloadedState, enhancer) {
      // create autoRehydrate enhancer if required
      var createStore = config$1.persist && config$1.rehydrate && config$1.persistAutoRehydrate ? config$1.persistAutoRehydrate()(next) : next; // create store

      var store = createStore(reducer, preloadedState, enhancer);
      var baseReplaceReducer = store.replaceReducer.bind(store);

      store.replaceReducer = function replaceReducer(nextReducer) {
        return baseReplaceReducer((0, updater.enhanceReducer)(nextReducer, config$1));
      }; // launch store persistor


      if (config$1.persist) {
        config$1.persist(store, config$1.persistOptions, config$1.persistCallback);
      } // launch network detector


      if (config$1.detectNetwork) {
        config$1.detectNetwork(function (online) {
          store.dispatch((0, actions.networkStatusChanged)(online));
        });
      }

      return store;
    };
  };

  return {
    middleware: (0, middleware.createOfflineMiddleware)(config$1),
    enhanceReducer: function enhanceReducer(reducer) {
      return (0, updater.enhanceReducer)(reducer, config$1);
    },
    enhanceStore: enhanceStore
  };
};

exports.createOffline = createOffline;
});

unwrapExports(lib);
var lib_1 = lib.createOffline;
var lib_2 = lib.offline;

exports.RESET_STATE = constants_5;
exports.busy = actions_1;
exports.createOffline = lib_1;
exports.offlineConfig = index;

Object.defineProperty(exports, '__esModule', { value: true });

});
