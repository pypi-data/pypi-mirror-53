/*
 * wq.app v1.2.0b1 - @wq/model 1.2.0-beta.1
 * A simple model API for working with stored lists
 * (c) 2012-2019, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['exports', './store', 'redux-orm'], function (exports, ds, reduxOrm) { 'use strict';

ds = ds && ds.hasOwnProperty('default') ? ds['default'] : ds;

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

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function");
  }

  subClass.prototype = Object.create(superClass && superClass.prototype, {
    constructor: {
      value: subClass,
      writable: true,
      configurable: true
    }
  });
  if (superClass) _setPrototypeOf(subClass, superClass);
}

function _getPrototypeOf(o) {
  _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) {
    return o.__proto__ || Object.getPrototypeOf(o);
  };
  return _getPrototypeOf(o);
}

function _setPrototypeOf(o, p) {
  _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) {
    o.__proto__ = p;
    return o;
  };

  return _setPrototypeOf(o, p);
}

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

function _objectWithoutProperties(source, excluded) {
  if (source == null) return {};

  var target = _objectWithoutPropertiesLoose(source, excluded);

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

function _assertThisInitialized(self) {
  if (self === void 0) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }

  return self;
}

function _possibleConstructorReturn(self, call) {
  if (call && (typeof call === "object" || typeof call === "function")) {
    return call;
  }

  return _assertThisInitialized(self);
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

var commonjsGlobal = typeof globalThis !== 'undefined' ? globalThis : typeof window !== 'undefined' ? window : typeof global !== 'undefined' ? global : typeof self !== 'undefined' ? self : {};

function createCommonjsModule(fn, module) {
	return module = { exports: {} }, fn(module, module.exports), module.exports;
}

var runtime_1 = createCommonjsModule(function (module) {
    /**
     * Copyright (c) 2014-present, Facebook, Inc.
     *
     * This source code is licensed under the MIT license found in the
     * LICENSE file in the root directory of this source tree.
     */
    var runtime = function (exports) {

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
            var context = new Context(tryLocsList || []); // The ._invoke method unifies the implementations of the .next,
            // .throw, and .return methods.

            generator._invoke = makeInvokeMethod(innerFn, self, context);
            return generator;
        }

        exports.wrap = wrap; // Try/catch helper to minimize deoptimizations. Returns a completion
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
                return {
                    type: "normal",
                    arg: fn.call(obj, arg)
                };
            } catch (err) {
                return {
                    type: "throw",
                    arg: err
                };
            }
        }

        var GenStateSuspendedStart = "suspendedStart";
        var GenStateSuspendedYield = "suspendedYield";
        var GenStateExecuting = "executing";
        var GenStateCompleted = "completed"; // Returning this object from the innerFn has the same effect as
        // breaking out of the dispatch switch statement.

        var ContinueSentinel = {}; // Dummy constructor functions that we use as the .constructor and
        // .constructor.prototype properties for functions that return Generator
        // objects. For full spec compliance, you may wish to configure your
        // minifier not to mangle the names of these two functions.

        function Generator() {}

        function GeneratorFunction() {}

        function GeneratorFunctionPrototype() {} // This is a polyfill for %IteratorPrototype% for environments that
        // don't natively support it.


        var IteratorPrototype = {};

        IteratorPrototype[iteratorSymbol] = function () {
            return this;
        };

        var getProto = Object.getPrototypeOf;
        var NativeIteratorPrototype = getProto && getProto(getProto(values([])));

        if (NativeIteratorPrototype && NativeIteratorPrototype !== Op && hasOwn.call(NativeIteratorPrototype, iteratorSymbol)) {
            // This environment has a native %IteratorPrototype%; use it instead
            // of the polyfill.
            IteratorPrototype = NativeIteratorPrototype;
        }

        var Gp = GeneratorFunctionPrototype.prototype = Generator.prototype = Object.create(IteratorPrototype);
        GeneratorFunction.prototype = Gp.constructor = GeneratorFunctionPrototype;
        GeneratorFunctionPrototype.constructor = GeneratorFunction;
        GeneratorFunctionPrototype[toStringTagSymbol] = GeneratorFunction.displayName = "GeneratorFunction"; // Helper for defining the .next, .throw, and .return methods of the
        // Iterator interface in terms of a single ._invoke method.

        function defineIteratorMethods(prototype) {
            ["next", "throw", "return"].forEach(function (method) {
                prototype[method] = function (arg) {
                    return this._invoke(method, arg);
                };
            });
        }

        exports.isGeneratorFunction = function (genFun) {
            var ctor = typeof genFun === "function" && genFun.constructor;
            return ctor ? ctor === GeneratorFunction || // For the native GeneratorFunction constructor, the best we can
            // do is to check its .name property.
            (ctor.displayName || ctor.name) === "GeneratorFunction" : false;
        };

        exports.mark = function (genFun) {
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
        }; // Within the body of any async function, `await x` is transformed to
        // `yield regeneratorRuntime.awrap(x)`, so that the runtime can test
        // `hasOwn.call(value, "__await")` to determine if the yielded value is
        // meant to be awaited.


        exports.awrap = function (arg) {
            return {
                __await: arg
            };
        };

        function AsyncIterator(generator) {
            function invoke(method, arg, resolve, reject) {
                var record = tryCatch(generator[method], generator, arg);

                if (record.type === "throw") {
                    reject(record.arg);
                } else {
                    var result = record.arg;
                    var value = result.value;

                    if (value && _typeof(value) === "object" && hasOwn.call(value, "__await")) {
                        return Promise.resolve(value.__await).then(function (value) {
                            invoke("next", value, resolve, reject);
                        }, function (err) {
                            invoke("throw", err, resolve, reject);
                        });
                    }

                    return Promise.resolve(value).then(function (unwrapped) {
                        // When a yielded Promise is resolved, its final value becomes
                        // the .value of the Promise<{value,done}> result for the
                        // current iteration.
                        result.value = unwrapped;
                        resolve(result);
                    }, function (error) {
                        // If a rejected Promise was yielded, throw the rejection back
                        // into the async generator function so it can be handled there.
                        return invoke("throw", error, resolve, reject);
                    });
                }
            }

            var previousPromise;

            function enqueue(method, arg) {
                function callInvokeWithMethodAndArg() {
                    return new Promise(function (resolve, reject) {
                        invoke(method, arg, resolve, reject);
                    });
                }

                return previousPromise = // If enqueue has been called before, then we want to wait until
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
                previousPromise ? previousPromise.then(callInvokeWithMethodAndArg, // Avoid propagating failures to Promises returned by later
                // invocations of the iterator.
                callInvokeWithMethodAndArg) : callInvokeWithMethodAndArg();
            } // Define the unified helper method that is used to implement .next,
            // .throw, and .return (see defineIteratorMethods).


            this._invoke = enqueue;
        }

        defineIteratorMethods(AsyncIterator.prototype);

        AsyncIterator.prototype[asyncIteratorSymbol] = function () {
            return this;
        };

        exports.AsyncIterator = AsyncIterator; // Note that simple async functions are implemented on top of
        // AsyncIterator objects; they just return a Promise for the value of
        // the final result produced by the iterator.

        exports.async = function (innerFn, outerFn, self, tryLocsList) {
            var iter = new AsyncIterator(wrap(innerFn, outerFn, self, tryLocsList));
            return exports.isGeneratorFunction(outerFn) ? iter // If outerFn is a generator, return the full iterator.
            : iter.next().then(function (result) {
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
                    } // Be forgiving, per 25.3.3.3.3 of the spec:
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
                        state = context.done ? GenStateCompleted : GenStateSuspendedYield;

                        if (record.arg === ContinueSentinel) {
                            continue;
                        }

                        return {
                            value: record.arg,
                            done: context.done
                        };
                    } else if (record.type === "throw") {
                        state = GenStateCompleted; // Dispatch the exception by looping back around to the
                        // context.dispatchException(context.arg) call above.

                        context.method = "throw";
                        context.arg = record.arg;
                    }
                }
            };
        } // Call delegate.iterator[context.method](context.arg) and handle the
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
                    context.arg = new TypeError("The iterator does not provide a 'throw' method");
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

            if (!info) {
                context.method = "throw";
                context.arg = new TypeError("iterator result is not an object");
                context.delegate = null;
                return ContinueSentinel;
            }

            if (info.done) {
                // Assign the result of the finished delegate to the temporary
                // variable specified by delegate.resultName (see delegateYield).
                context[delegate.resultName] = info.value; // Resume execution at the desired location (see delegateYield).

                context.next = delegate.nextLoc; // If context.method was "throw" but the delegate handled the
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
            } // The delegate iterator is finished, so forget it and continue with
            // the outer generator.


            context.delegate = null;
            return ContinueSentinel;
        } // Define Generator.prototype.{next,throw,return} in terms of the
        // unified ._invoke helper method.


        defineIteratorMethods(Gp);
        Gp[toStringTagSymbol] = "Generator"; // A Generator should always return itself as the iterator object when the
        // @@iterator function is called on it. Some browsers' implementations of the
        // iterator prototype chain incorrectly implement this, causing the Generator
        // object to not be returned from this call. This ensures that doesn't happen.
        // See https://github.com/facebook/regenerator/issues/274 for more details.

        Gp[iteratorSymbol] = function () {
            return this;
        };

        Gp.toString = function () {
            return "[object Generator]";
        };

        function pushTryEntry(locs) {
            var entry = {
                tryLoc: locs[0]
            };

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
            this.tryEntries = [{
                tryLoc: "root"
            }];
            tryLocsList.forEach(pushTryEntry, this);
            this.reset(true);
        }

        exports.keys = function (object) {
            var keys = [];

            for (var key in object) {
                keys.push(key);
            }

            keys.reverse(); // Rather than returning an object with a next method, we keep
            // things simple and return the next function itself.

            return function next() {
                while (keys.length) {
                    var key = keys.pop();

                    if (key in object) {
                        next.value = key;
                        next.done = false;
                        return next;
                    }
                } // To avoid creating an additional object, we just hang the .value
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
                    var i = -1,
                        next = function next() {
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
            } // Return an iterator with no values.


            return {
                next: doneResult
            };
        }

        exports.values = values;

        function doneResult() {
            return {
                value: undefined$1,
                done: true
            };
        }

        Context.prototype = {
            constructor: Context,
            reset: function reset(skipTempReset) {
                this.prev = 0;
                this.next = 0; // Resetting context._sent for legacy support of Babel's
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
                        if (name.charAt(0) === "t" && hasOwn.call(this, name) && !isNaN(+name.slice(1))) {
                            this[name] = undefined$1;
                        }
                    }
                }
            },
            stop: function stop() {
                this.done = true;
                var rootEntry = this.tryEntries[0];
                var rootRecord = rootEntry.completion;

                if (rootRecord.type === "throw") {
                    throw rootRecord.arg;
                }

                return this.rval;
            },
            dispatchException: function dispatchException(exception) {
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

                    return !!caught;
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
            abrupt: function abrupt(type, arg) {
                for (var i = this.tryEntries.length - 1; i >= 0; --i) {
                    var entry = this.tryEntries[i];

                    if (entry.tryLoc <= this.prev && hasOwn.call(entry, "finallyLoc") && this.prev < entry.finallyLoc) {
                        var finallyEntry = entry;
                        break;
                    }
                }

                if (finallyEntry && (type === "break" || type === "continue") && finallyEntry.tryLoc <= arg && arg <= finallyEntry.finallyLoc) {
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
            complete: function complete(record, afterLoc) {
                if (record.type === "throw") {
                    throw record.arg;
                }

                if (record.type === "break" || record.type === "continue") {
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
            finish: function finish(finallyLoc) {
                for (var i = this.tryEntries.length - 1; i >= 0; --i) {
                    var entry = this.tryEntries[i];

                    if (entry.finallyLoc === finallyLoc) {
                        this.complete(entry.completion, entry.afterLoc);
                        resetTryEntry(entry);
                        return ContinueSentinel;
                    }
                }
            },
            "catch": function _catch(tryLoc) {
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
                } // The context.catch method must only be called with a location
                // argument that corresponds to a known catch block.


                throw new Error("illegal catch attempt");
            },
            delegateYield: function delegateYield(iterable, resultName, nextLoc) {
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
        }; // Regardless of whether this script is executing as a CommonJS module
        // or not, return the runtime object so that we can declare the variable
        // regeneratorRuntime in the outer scope, which allows this module to be
        // injected easily by `bin/regenerator --include-runtime script.js`.

        return exports;
    }( // If this script is executing as a CommonJS module, use module.exports
    // as the regeneratorRuntime namespace. Otherwise create a new empty
    // object. Either way, the resulting object will be used to initialize
    // the regeneratorRuntime variable at the top of this file.
     module.exports );

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

var typeDetect = createCommonjsModule(function (module, exports) {
    (function (global, factory) {
         module.exports = factory() ;
    })(commonjsGlobal, function () {
        /* !
         * type-detect
         * Copyright(c) 2013 jake luer <jake@alogicalparadox.com>
         * MIT Licensed
         */

        var promiseExists = typeof Promise === 'function';
        /* eslint-disable no-undef */

        var globalObject = (typeof self === "undefined" ? "undefined" : _typeof(self)) === 'object' ? self : commonjsGlobal; // eslint-disable-line id-blacklist

        var symbolExists = typeof Symbol !== 'undefined';
        var mapExists = typeof Map !== 'undefined';
        var setExists = typeof Set !== 'undefined';
        var weakMapExists = typeof WeakMap !== 'undefined';
        var weakSetExists = typeof WeakSet !== 'undefined';
        var dataViewExists = typeof DataView !== 'undefined';
        var symbolIteratorExists = symbolExists && typeof Symbol.iterator !== 'undefined';
        var symbolToStringTagExists = symbolExists && typeof Symbol.toStringTag !== 'undefined';
        var setEntriesExists = setExists && typeof Set.prototype.entries === 'function';
        var mapEntriesExists = mapExists && typeof Map.prototype.entries === 'function';
        var setIteratorPrototype = setEntriesExists && Object.getPrototypeOf(new Set().entries());
        var mapIteratorPrototype = mapEntriesExists && Object.getPrototypeOf(new Map().entries());
        var arrayIteratorExists = symbolIteratorExists && typeof Array.prototype[Symbol.iterator] === 'function';
        var arrayIteratorPrototype = arrayIteratorExists && Object.getPrototypeOf([][Symbol.iterator]());
        var stringIteratorExists = symbolIteratorExists && typeof String.prototype[Symbol.iterator] === 'function';
        var stringIteratorPrototype = stringIteratorExists && Object.getPrototypeOf(''[Symbol.iterator]());
        var toStringLeftSliceLength = 8;
        var toStringRightSliceLength = -1;
        /**
         * ### typeOf (obj)
         *
         * Uses `Object.prototype.toString` to determine the type of an object,
         * normalising behaviour across engine versions & well optimised.
         *
         * @param {Mixed} object
         * @return {String} object type
         * @api public
         */

        function typeDetect(obj) {
            /* ! Speed optimisation
             * Pre:
             *   string literal     x 3,039,035 ops/sec ±1.62% (78 runs sampled)
             *   boolean literal    x 1,424,138 ops/sec ±4.54% (75 runs sampled)
             *   number literal     x 1,653,153 ops/sec ±1.91% (82 runs sampled)
             *   undefined          x 9,978,660 ops/sec ±1.92% (75 runs sampled)
             *   function           x 2,556,769 ops/sec ±1.73% (77 runs sampled)
             * Post:
             *   string literal     x 38,564,796 ops/sec ±1.15% (79 runs sampled)
             *   boolean literal    x 31,148,940 ops/sec ±1.10% (79 runs sampled)
             *   number literal     x 32,679,330 ops/sec ±1.90% (78 runs sampled)
             *   undefined          x 32,363,368 ops/sec ±1.07% (82 runs sampled)
             *   function           x 31,296,870 ops/sec ±0.96% (83 runs sampled)
             */
            var typeofObj = _typeof(obj);

            if (typeofObj !== 'object') {
                return typeofObj;
            }
            /* ! Speed optimisation
             * Pre:
             *   null               x 28,645,765 ops/sec ±1.17% (82 runs sampled)
             * Post:
             *   null               x 36,428,962 ops/sec ±1.37% (84 runs sampled)
             */


            if (obj === null) {
                return 'null';
            }
            /* ! Spec Conformance
             * Test: `Object.prototype.toString.call(window)``
             *  - Node === "[object global]"
             *  - Chrome === "[object global]"
             *  - Firefox === "[object Window]"
             *  - PhantomJS === "[object Window]"
             *  - Safari === "[object Window]"
             *  - IE 11 === "[object Window]"
             *  - IE Edge === "[object Window]"
             * Test: `Object.prototype.toString.call(this)``
             *  - Chrome Worker === "[object global]"
             *  - Firefox Worker === "[object DedicatedWorkerGlobalScope]"
             *  - Safari Worker === "[object DedicatedWorkerGlobalScope]"
             *  - IE 11 Worker === "[object WorkerGlobalScope]"
             *  - IE Edge Worker === "[object WorkerGlobalScope]"
             */


            if (obj === globalObject) {
                return 'global';
            }
            /* ! Speed optimisation
             * Pre:
             *   array literal      x 2,888,352 ops/sec ±0.67% (82 runs sampled)
             * Post:
             *   array literal      x 22,479,650 ops/sec ±0.96% (81 runs sampled)
             */


            if (Array.isArray(obj) && (symbolToStringTagExists === false || !(Symbol.toStringTag in obj))) {
                return 'Array';
            } // Not caching existence of `window` and related properties due to potential
            // for `window` to be unset before tests in quasi-browser environments.


            if ((typeof window === "undefined" ? "undefined" : _typeof(window)) === 'object' && window !== null) {
                /* ! Spec Conformance
                 * (https://html.spec.whatwg.org/multipage/browsers.html#location)
                 * WhatWG HTML$7.7.3 - The `Location` interface
                 * Test: `Object.prototype.toString.call(window.location)``
                 *  - IE <=11 === "[object Object]"
                 *  - IE Edge <=13 === "[object Object]"
                 */
                if (_typeof(window.location) === 'object' && obj === window.location) {
                    return 'Location';
                }
                /* ! Spec Conformance
                 * (https://html.spec.whatwg.org/#document)
                 * WhatWG HTML$3.1.1 - The `Document` object
                 * Note: Most browsers currently adher to the W3C DOM Level 2 spec
                 *       (https://www.w3.org/TR/DOM-Level-2-HTML/html.html#ID-26809268)
                 *       which suggests that browsers should use HTMLTableCellElement for
                 *       both TD and TH elements. WhatWG separates these.
                 *       WhatWG HTML states:
                 *         > For historical reasons, Window objects must also have a
                 *         > writable, configurable, non-enumerable property named
                 *         > HTMLDocument whose value is the Document interface object.
                 * Test: `Object.prototype.toString.call(document)``
                 *  - Chrome === "[object HTMLDocument]"
                 *  - Firefox === "[object HTMLDocument]"
                 *  - Safari === "[object HTMLDocument]"
                 *  - IE <=10 === "[object Document]"
                 *  - IE 11 === "[object HTMLDocument]"
                 *  - IE Edge <=13 === "[object HTMLDocument]"
                 */


                if (_typeof(window.document) === 'object' && obj === window.document) {
                    return 'Document';
                }

                if (_typeof(window.navigator) === 'object') {
                    /* ! Spec Conformance
                     * (https://html.spec.whatwg.org/multipage/webappapis.html#mimetypearray)
                     * WhatWG HTML$8.6.1.5 - Plugins - Interface MimeTypeArray
                     * Test: `Object.prototype.toString.call(navigator.mimeTypes)``
                     *  - IE <=10 === "[object MSMimeTypesCollection]"
                     */
                    if (_typeof(window.navigator.mimeTypes) === 'object' && obj === window.navigator.mimeTypes) {
                        return 'MimeTypeArray';
                    }
                    /* ! Spec Conformance
                     * (https://html.spec.whatwg.org/multipage/webappapis.html#pluginarray)
                     * WhatWG HTML$8.6.1.5 - Plugins - Interface PluginArray
                     * Test: `Object.prototype.toString.call(navigator.plugins)``
                     *  - IE <=10 === "[object MSPluginsCollection]"
                     */


                    if (_typeof(window.navigator.plugins) === 'object' && obj === window.navigator.plugins) {
                        return 'PluginArray';
                    }
                }

                if ((typeof window.HTMLElement === 'function' || _typeof(window.HTMLElement) === 'object') && obj instanceof window.HTMLElement) {
                    /* ! Spec Conformance
                    * (https://html.spec.whatwg.org/multipage/webappapis.html#pluginarray)
                    * WhatWG HTML$4.4.4 - The `blockquote` element - Interface `HTMLQuoteElement`
                    * Test: `Object.prototype.toString.call(document.createElement('blockquote'))``
                    *  - IE <=10 === "[object HTMLBlockElement]"
                    */
                    if (obj.tagName === 'BLOCKQUOTE') {
                        return 'HTMLQuoteElement';
                    }
                    /* ! Spec Conformance
                     * (https://html.spec.whatwg.org/#htmltabledatacellelement)
                     * WhatWG HTML$4.9.9 - The `td` element - Interface `HTMLTableDataCellElement`
                     * Note: Most browsers currently adher to the W3C DOM Level 2 spec
                     *       (https://www.w3.org/TR/DOM-Level-2-HTML/html.html#ID-82915075)
                     *       which suggests that browsers should use HTMLTableCellElement for
                     *       both TD and TH elements. WhatWG separates these.
                     * Test: Object.prototype.toString.call(document.createElement('td'))
                     *  - Chrome === "[object HTMLTableCellElement]"
                     *  - Firefox === "[object HTMLTableCellElement]"
                     *  - Safari === "[object HTMLTableCellElement]"
                     */


                    if (obj.tagName === 'TD') {
                        return 'HTMLTableDataCellElement';
                    }
                    /* ! Spec Conformance
                     * (https://html.spec.whatwg.org/#htmltableheadercellelement)
                     * WhatWG HTML$4.9.9 - The `td` element - Interface `HTMLTableHeaderCellElement`
                     * Note: Most browsers currently adher to the W3C DOM Level 2 spec
                     *       (https://www.w3.org/TR/DOM-Level-2-HTML/html.html#ID-82915075)
                     *       which suggests that browsers should use HTMLTableCellElement for
                     *       both TD and TH elements. WhatWG separates these.
                     * Test: Object.prototype.toString.call(document.createElement('th'))
                     *  - Chrome === "[object HTMLTableCellElement]"
                     *  - Firefox === "[object HTMLTableCellElement]"
                     *  - Safari === "[object HTMLTableCellElement]"
                     */


                    if (obj.tagName === 'TH') {
                        return 'HTMLTableHeaderCellElement';
                    }
                }
            }
            /* ! Speed optimisation
            * Pre:
            *   Float64Array       x 625,644 ops/sec ±1.58% (80 runs sampled)
            *   Float32Array       x 1,279,852 ops/sec ±2.91% (77 runs sampled)
            *   Uint32Array        x 1,178,185 ops/sec ±1.95% (83 runs sampled)
            *   Uint16Array        x 1,008,380 ops/sec ±2.25% (80 runs sampled)
            *   Uint8Array         x 1,128,040 ops/sec ±2.11% (81 runs sampled)
            *   Int32Array         x 1,170,119 ops/sec ±2.88% (80 runs sampled)
            *   Int16Array         x 1,176,348 ops/sec ±5.79% (86 runs sampled)
            *   Int8Array          x 1,058,707 ops/sec ±4.94% (77 runs sampled)
            *   Uint8ClampedArray  x 1,110,633 ops/sec ±4.20% (80 runs sampled)
            * Post:
            *   Float64Array       x 7,105,671 ops/sec ±13.47% (64 runs sampled)
            *   Float32Array       x 5,887,912 ops/sec ±1.46% (82 runs sampled)
            *   Uint32Array        x 6,491,661 ops/sec ±1.76% (79 runs sampled)
            *   Uint16Array        x 6,559,795 ops/sec ±1.67% (82 runs sampled)
            *   Uint8Array         x 6,463,966 ops/sec ±1.43% (85 runs sampled)
            *   Int32Array         x 5,641,841 ops/sec ±3.49% (81 runs sampled)
            *   Int16Array         x 6,583,511 ops/sec ±1.98% (80 runs sampled)
            *   Int8Array          x 6,606,078 ops/sec ±1.74% (81 runs sampled)
            *   Uint8ClampedArray  x 6,602,224 ops/sec ±1.77% (83 runs sampled)
            */


            var stringTag = symbolToStringTagExists && obj[Symbol.toStringTag];

            if (typeof stringTag === 'string') {
                return stringTag;
            }

            var objPrototype = Object.getPrototypeOf(obj);
            /* ! Speed optimisation
            * Pre:
            *   regex literal      x 1,772,385 ops/sec ±1.85% (77 runs sampled)
            *   regex constructor  x 2,143,634 ops/sec ±2.46% (78 runs sampled)
            * Post:
            *   regex literal      x 3,928,009 ops/sec ±0.65% (78 runs sampled)
            *   regex constructor  x 3,931,108 ops/sec ±0.58% (84 runs sampled)
            */

            if (objPrototype === RegExp.prototype) {
                return 'RegExp';
            }
            /* ! Speed optimisation
            * Pre:
            *   date               x 2,130,074 ops/sec ±4.42% (68 runs sampled)
            * Post:
            *   date               x 3,953,779 ops/sec ±1.35% (77 runs sampled)
            */


            if (objPrototype === Date.prototype) {
                return 'Date';
            }
            /* ! Spec Conformance
             * (http://www.ecma-international.org/ecma-262/6.0/index.html#sec-promise.prototype-@@tostringtag)
             * ES6$25.4.5.4 - Promise.prototype[@@toStringTag] should be "Promise":
             * Test: `Object.prototype.toString.call(Promise.resolve())``
             *  - Chrome <=47 === "[object Object]"
             *  - Edge <=20 === "[object Object]"
             *  - Firefox 29-Latest === "[object Promise]"
             *  - Safari 7.1-Latest === "[object Promise]"
             */


            if (promiseExists && objPrototype === Promise.prototype) {
                return 'Promise';
            }
            /* ! Speed optimisation
            * Pre:
            *   set                x 2,222,186 ops/sec ±1.31% (82 runs sampled)
            * Post:
            *   set                x 4,545,879 ops/sec ±1.13% (83 runs sampled)
            */


            if (setExists && objPrototype === Set.prototype) {
                return 'Set';
            }
            /* ! Speed optimisation
            * Pre:
            *   map                x 2,396,842 ops/sec ±1.59% (81 runs sampled)
            * Post:
            *   map                x 4,183,945 ops/sec ±6.59% (82 runs sampled)
            */


            if (mapExists && objPrototype === Map.prototype) {
                return 'Map';
            }
            /* ! Speed optimisation
            * Pre:
            *   weakset            x 1,323,220 ops/sec ±2.17% (76 runs sampled)
            * Post:
            *   weakset            x 4,237,510 ops/sec ±2.01% (77 runs sampled)
            */


            if (weakSetExists && objPrototype === WeakSet.prototype) {
                return 'WeakSet';
            }
            /* ! Speed optimisation
            * Pre:
            *   weakmap            x 1,500,260 ops/sec ±2.02% (78 runs sampled)
            * Post:
            *   weakmap            x 3,881,384 ops/sec ±1.45% (82 runs sampled)
            */


            if (weakMapExists && objPrototype === WeakMap.prototype) {
                return 'WeakMap';
            }
            /* ! Spec Conformance
             * (http://www.ecma-international.org/ecma-262/6.0/index.html#sec-dataview.prototype-@@tostringtag)
             * ES6$24.2.4.21 - DataView.prototype[@@toStringTag] should be "DataView":
             * Test: `Object.prototype.toString.call(new DataView(new ArrayBuffer(1)))``
             *  - Edge <=13 === "[object Object]"
             */


            if (dataViewExists && objPrototype === DataView.prototype) {
                return 'DataView';
            }
            /* ! Spec Conformance
             * (http://www.ecma-international.org/ecma-262/6.0/index.html#sec-%mapiteratorprototype%-@@tostringtag)
             * ES6$23.1.5.2.2 - %MapIteratorPrototype%[@@toStringTag] should be "Map Iterator":
             * Test: `Object.prototype.toString.call(new Map().entries())``
             *  - Edge <=13 === "[object Object]"
             */


            if (mapExists && objPrototype === mapIteratorPrototype) {
                return 'Map Iterator';
            }
            /* ! Spec Conformance
             * (http://www.ecma-international.org/ecma-262/6.0/index.html#sec-%setiteratorprototype%-@@tostringtag)
             * ES6$23.2.5.2.2 - %SetIteratorPrototype%[@@toStringTag] should be "Set Iterator":
             * Test: `Object.prototype.toString.call(new Set().entries())``
             *  - Edge <=13 === "[object Object]"
             */


            if (setExists && objPrototype === setIteratorPrototype) {
                return 'Set Iterator';
            }
            /* ! Spec Conformance
             * (http://www.ecma-international.org/ecma-262/6.0/index.html#sec-%arrayiteratorprototype%-@@tostringtag)
             * ES6$22.1.5.2.2 - %ArrayIteratorPrototype%[@@toStringTag] should be "Array Iterator":
             * Test: `Object.prototype.toString.call([][Symbol.iterator]())``
             *  - Edge <=13 === "[object Object]"
             */


            if (arrayIteratorExists && objPrototype === arrayIteratorPrototype) {
                return 'Array Iterator';
            }
            /* ! Spec Conformance
             * (http://www.ecma-international.org/ecma-262/6.0/index.html#sec-%stringiteratorprototype%-@@tostringtag)
             * ES6$21.1.5.2.2 - %StringIteratorPrototype%[@@toStringTag] should be "String Iterator":
             * Test: `Object.prototype.toString.call(''[Symbol.iterator]())``
             *  - Edge <=13 === "[object Object]"
             */


            if (stringIteratorExists && objPrototype === stringIteratorPrototype) {
                return 'String Iterator';
            }
            /* ! Speed optimisation
            * Pre:
            *   object from null   x 2,424,320 ops/sec ±1.67% (76 runs sampled)
            * Post:
            *   object from null   x 5,838,000 ops/sec ±0.99% (84 runs sampled)
            */


            if (objPrototype === null) {
                return 'Object';
            }

            return Object.prototype.toString.call(obj).slice(toStringLeftSliceLength, toStringRightSliceLength);
        }

        return typeDetect;
    });
});

var isBufferExists = typeof Buffer !== 'undefined';
var isBufferFromExists = isBufferExists && typeof Buffer.from !== 'undefined';
var isBuffer = isBufferExists ?
/**
 * is value is Buffer?
 *
 * @param {*} value
 * @return {boolean}
 */
function isBuffer(value) {
    return Buffer.isBuffer(value);
} :
/**
 * return false
 *
 * NOTE: for Buffer unsupported
 *
 * @return {boolean}
 */
function isBuffer() {
    return false;
};
var copy = isBufferFromExists ?
/**
 * copy Buffer
 *
 * @param {Buffer} value
 * @return {Buffer}
 */
function copy(value) {
    return Buffer.from(value);
} : isBufferExists ?
/**
 * copy Buffer
 *
 * NOTE: for old node.js
 *
 * @param {Buffer} value
 * @return {Buffer}
 */
function copy(value) {
    return new Buffer(value);
} :
/**
 * shallow copy
 *
 * NOTE: for Buffer unsupported
 *
 * @param {*}
 * @return {*}
 */
function copy(value) {
    return value;
};

/**
 * detect type of value
 *
 * @param {*} value
 * @return {string}
 */

function detectType(value) {
    // NOTE: isBuffer must execute before type-detect,
    // because type-detect returns 'Uint8Array'.
    if (isBuffer(value)) {
        return 'Buffer';
    }

    return typeDetect(value);
}

/**
 * collection types
 */

var collectionTypeSet = new Set(['Arguments', 'Array', 'Map', 'Object', 'Set']);
/**
 * get value from collection
 *
 * @param {Array|Object|Map|Set} collection
 * @param {string|number|symbol} key
 * @param {string} [type=null]
 * @return {*}
 */

function get(collection, key) {
    var type = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : null;
    var valueType = type || detectType(collection);

    switch (valueType) {
        case 'Arguments':
        case 'Array':
        case 'Object':
            return collection[key];

        case 'Map':
            return collection.get(key);

        case 'Set':
            // NOTE: Set.prototype.keys is alias of Set.prototype.values
            // it means key is equals value
            return key;

        default:
    }
}
/**
 * check to type string is collection
 *
 * @param {string} type
 */

function isCollection(type) {
    return collectionTypeSet.has(type);
}
/**
 * set value to collection
 *
 * @param {Array|Object|Map|Set} collection
 * @param {string|number|symbol} key
 * @param {*} value
 * @param {string} [type=null]
 * @return {Array|Object|Map|Set}
 */

function set(collection, key, value) {
    var type = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : null;
    var valueType = type || detectType(collection);

    switch (valueType) {
        case 'Arguments':
        case 'Array':
        case 'Object':
            collection[key] = value;
            break;

        case 'Map':
            collection.set(key, value);
            break;

        case 'Set':
            collection.add(value);
            break;

        default:
    }

    return collection;
}

var freeGlobalThis = typeof globalThis !== 'undefined' && globalThis !== null && globalThis.Object === Object && globalThis;
var freeGlobal = typeof global !== 'undefined' && global !== null && global.Object === Object && global;
var freeSelf = typeof self !== 'undefined' && self !== null && self.Object === Object && self;
var globalObject = freeGlobalThis || freeGlobal || freeSelf || Function('return this')();

/**
 * copy ArrayBuffer
 *
 * @param {ArrayBuffer} value
 * @return {ArrayBuffer}
 */

function copyArrayBuffer(value) {
    return value.slice(0);
}
/**
 * copy Boolean
 *
 * @param {Boolean} value
 * @return {Boolean}
 */


function copyBoolean(value) {
    return new Boolean(value.valueOf());
}
/**
 * copy DataView
 *
 * @param {DataView} value
 * @return {DataView}
 */


function copyDataView(value) {
    // TODO: copy ArrayBuffer?
    return new DataView(value.buffer);
}
/**
 * copy Buffer
 *
 * @param {Buffer} value
 * @return {Buffer}
 */


function copyBuffer(value) {
    return copy(value);
}
/**
 * copy Date
 *
 * @param {Date} value
 * @return {Date}
 */


function copyDate(value) {
    return new Date(value.getTime());
}
/**
 * copy Number
 *
 * @param {Number} value
 * @return {Number}
 */


function copyNumber(value) {
    return new Number(value);
}
/**
 * copy RegExp
 *
 * @param {RegExp} value
 * @return {RegExp}
 */


function copyRegExp(value) {
    return new RegExp(value.source || '(?:)', value.flags);
}
/**
 * copy String
 *
 * @param {String} value
 * @return {String}
 */


function copyString(value) {
    return new String(value);
}
/**
 * copy TypedArray
 *
 * @param {*} value
 * @return {*}
 */


function copyTypedArray(value, type) {
    return globalObject[type].from(value);
}
/**
 * shallow copy
 *
 * @param {*} value
 * @return {*}
 */


function shallowCopy(value) {
    return value;
}
/**
 * get empty Array
 *
 * @return {Array}
 */


function getEmptyArray() {
    return [];
}
/**
 * get empty Map
 *
 * @return {Map}
 */


function getEmptyMap() {
    return new Map();
}
/**
 * get empty Object
 *
 * @return {Object}
 */


function getEmptyObject() {
    return {};
}
/**
 * get empty Set
 *
 * @return {Set}
 */


function getEmptySet() {
    return new Set();
}

var copyMap = new Map([// deep copy
['ArrayBuffer', copyArrayBuffer], ['Boolean', copyBoolean], ['Buffer', copyBuffer], ['DataView', copyDataView], ['Date', copyDate], ['Number', copyNumber], ['RegExp', copyRegExp], ['String', copyString], // typed arrays
// TODO: pass bound function
['Float32Array', copyTypedArray], ['Float64Array', copyTypedArray], ['Int16Array', copyTypedArray], ['Int32Array', copyTypedArray], ['Int8Array', copyTypedArray], ['Uint16Array', copyTypedArray], ['Uint32Array', copyTypedArray], ['Uint8Array', copyTypedArray], ['Uint8ClampedArray', copyTypedArray], // shallow copy
['Array Iterator', shallowCopy], ['Map Iterator', shallowCopy], ['Promise', shallowCopy], ['Set Iterator', shallowCopy], ['String Iterator', shallowCopy], ['function', shallowCopy], ['global', shallowCopy], // NOTE: WeakMap and WeakSet cannot get entries
['WeakMap', shallowCopy], ['WeakSet', shallowCopy], // primitives
['boolean', shallowCopy], ['null', shallowCopy], ['number', shallowCopy], ['string', shallowCopy], ['symbol', shallowCopy], ['undefined', shallowCopy], // collections
// NOTE: return empty value, because recursively copy later.
['Arguments', getEmptyArray], ['Array', getEmptyArray], ['Map', getEmptyMap], ['Object', getEmptyObject], ['Set', getEmptySet] // NOTE: type-detect returns following types
// 'Location'
// 'Document'
// 'MimeTypeArray'
// 'PluginArray'
// 'HTMLQuoteElement'
// 'HTMLTableDataCellElement'
// 'HTMLTableHeaderCellElement'
// TODO: is type-detect never return 'object'?
// 'object'
]);

/**
 * no operation
 */

function noop() {}
/**
 * copy value
 *
 * @param {*} value
 * @param {string} [type=null]
 * @param {Function} [customizer=noop]
 * @return {*}
 */


function copy$1(value) {
    var type = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
    var customizer = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : noop;

    if (arguments.length === 2 && typeof type === 'function') {
        customizer = type;
        type = null;
    }

    var valueType = type || detectType(value);
    var copyFunction = copyMap.get(valueType);

    if (valueType === 'Object') {
        var result = customizer(value, valueType);

        if (result !== undefined) {
            return result;
        }
    } // NOTE: TypedArray needs pass type to argument


    return copyFunction ? copyFunction(value, valueType) : value;
}

/**
 * deepcopy function
 *
 * @param {*} value
 * @param {Object|Function} [options]
 * @return {*}
 */

function deepcopy(value) {
    var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

    if (typeof options === 'function') {
        options = {
            customizer: options
        };
    }

    var _options = options,
        customizer = _options.customizer;
    var valueType = detectType(value);

    if (!isCollection(valueType)) {
        return recursiveCopy(value, null, null, null, customizer);
    }

    var copiedValue = copy$1(value, valueType, customizer);
    var references = new WeakMap([[value, copiedValue]]);
    var visited = new WeakSet([value]);
    return recursiveCopy(value, copiedValue, references, visited, customizer);
}
/**
 * recursively copy
 *
 * @param {*} value target value
 * @param {*} clone clone of value
 * @param {WeakMap} references visited references of clone
 * @param {WeakSet} visited visited references of value
 * @param {Function} customizer user customize function
 * @return {*}
 */

function recursiveCopy(value, clone, references, visited, customizer) {
    var _keys;

    var type = detectType(value);
    var copiedValue = copy$1(value, type); // return if not a collection value

    if (!isCollection(type)) {
        return copiedValue;
    }

    var keys;

    switch (type) {
        case 'Arguments':
        case 'Array':
            keys = Object.keys(value);
            break;

        case 'Object':
            keys = Object.keys(value);

            (_keys = keys).push.apply(_keys, _toConsumableArray(Object.getOwnPropertySymbols(value)));

            break;

        case 'Map':
        case 'Set':
            keys = value.keys();
            break;

        default:
    } // walk within collection with iterator


    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
        for (var _iterator = keys[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
            var collectionKey = _step.value;
            var collectionValue = get(value, collectionKey, type);

            if (visited.has(collectionValue)) {
                // for [Circular]
                set(clone, collectionKey, references.get(collectionValue), type);
            } else {
                var collectionValueType = detectType(collectionValue);
                var copiedCollectionValue = copy$1(collectionValue, collectionValueType); // save reference if value is collection

                if (isCollection(collectionValueType)) {
                    references.set(collectionValue, copiedCollectionValue);
                    visited.add(collectionValue);
                }

                set(clone, collectionKey, recursiveCopy(collectionValue, copiedCollectionValue, references, visited, customizer), type);
            }
        } // TODO: isSealed/isFrozen/isExtensible

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

    return clone;
}

function model(config) {
    return new Model(config);
}

var _orms = {};
var CREATE = 'CREATE',
    UPDATE = 'UPDATE',
    SUCCESS = 'SUCCESS',
    DELETE = 'DELETE',
    OVERWRITE = 'OVERWRITE';

var ORMWithReducer =
/*#__PURE__*/
function (_ORM) {
    _inherits(ORMWithReducer, _ORM);

    function ORMWithReducer(store) {
        var _this;

        _classCallCheck(this, ORMWithReducer);

        _this = _possibleConstructorReturn(this, _getPrototypeOf(ORMWithReducer).call(this));
        _this.store = store;
        return _this;
    }

    _createClass(ORMWithReducer, [{
        key: "getReverseRels",
        value: function getReverseRels(modelName) {
            var _this2 = this;

            if (!this._rrel) {
                this._rrel = {};
                var models = {};
                this.getModelClasses().forEach(function (cls) {
                    models[cls.modelName] = cls;
                });
                Object.values(models).forEach(function (cls) {
                    Object.entries(cls.fields).forEach(function (_ref) {
                        var _ref2 = _slicedToArray(_ref, 2),
                            name = _ref2[0],
                            field = _ref2[1];

                        if (!(field instanceof reduxOrm.ForeignKey)) {
                            return;
                        }

                        var to = field.toModelName,
                            toModel = models[to];

                        if (!toModel || !toModel.wqConfig) {
                            return;
                        }

                        var isNested = (toModel.wqConfig.form || []).filter(function (f) {
                            return f.type === 'repeat' && f.name === field.relatedName;
                        }).length > 0;

                        if (!_this2._rrel[to]) {
                            _this2._rrel[to] = [];
                        }

                        _this2._rrel[to].push({
                            model: cls.modelName,
                            fkName: name,
                            relatedName: field.relatedName,
                            nested: isNested
                        });
                    });
                });
            }

            return this._rrel[modelName] || [];
        }
    }, {
        key: "getNestedModels",
        value: function getNestedModels(modelName) {
            return this.getReverseRels(modelName).filter(function (rel) {
                return rel.nested;
            });
        }
    }, {
        key: "reducer",
        value: function reducer(state, action) {
            var _this3 = this;

            var session = this.session(state || this.getEmptyState()),
                match = action.type.match(/^([^_]+)_(.+)_([^_]+)$/);

            if (!match || match[1] !== this.prefix) {
                return session.state;
            }

            var modelName = match[2].toLowerCase(),
                actName = match[3],
                cls = session[modelName];

            if (!cls) {
                return session.state;
            }

            var currentCount = cls.count();
            var updateCount;

            switch (actName) {
                case CREATE:
                    {
                        this._nestedCreate(cls, action.payload);

                        updateCount = true;
                        break;
                    }

                case UPDATE:
                case SUCCESS:
                    {
                        var items = Array.isArray(action.payload) ? action.payload : [action.payload];

                        if (action.meta && action.meta.currentId && action.meta.currentId != items[0].id) {
                            this._updateID(cls, action.meta.currentId, items[0].id);
                        }

                        items.forEach(function (item) {
                            return _this3._nestedUpdate(cls, item);
                        });
                        updateCount = true;
                        break;
                    }

                case DELETE:
                    {
                        this._nestedDelete(cls.withId(action.payload));

                        updateCount = true;
                        break;
                    }

                case OVERWRITE:
                    {
                        var _action$payload = action.payload,
                            list = _action$payload.list,
                            info = _objectWithoutProperties(_action$payload, ["list"]);

                        this._removeObsolete(cls.all(), list, true);

                        list.forEach(function (item) {
                            return _this3._nestedUpdate(cls, item);
                        });

                        session._modelmeta.upsert(_objectSpread2({
                            id: cls.modelName
                        }, info));

                        break;
                    }
            }

            if (updateCount) {
                var meta = session._modelmeta.withId(cls.modelName);

                if (meta) {
                    // Use delta in case server count != local count.
                    var countChange = cls.count() - currentCount,
                        update = {
                        count: meta.count + countChange
                    };

                    if (meta.pages === 1 && meta.per_page === meta.count) {
                        update.per_page = update.count;
                    }

                    meta.update(update);
                } else {
                    session._modelmeta.create({
                        id: cls.modelName,
                        pages: 1,
                        count: cls.count(),
                        per_page: cls.count()
                    });
                } // FIXME: Update count for nested models

            }

            return session.state;
        }
    }, {
        key: "_setNested",
        value: function _setNested(cls, data) {
            var _this4 = this;

            var item = _objectSpread2({}, data),
                session = cls.session,
                nested = this.getNestedModels(cls.modelName);

            var exist = data.id ? cls.withId(data.id) : null; // Normalize nested records into their own models

            nested.forEach(function (_ref3) {
                var model = _ref3.model,
                    fkName = _ref3.fkName,
                    relatedName = _ref3.relatedName;

                if (!Array.isArray(item[relatedName])) {
                    return;
                }

                if (exist && exist[relatedName] && exist[relatedName].toRefArray) {
                    _this4._removeObsolete(exist[relatedName], item[relatedName]);
                }

                item[relatedName].forEach(function (row) {
                    session[model].upsert(_objectSpread2({}, row, _defineProperty({}, fkName, item.id)));
                });
                delete item[relatedName];
            });
            return item;
        }
    }, {
        key: "_removeObsolete",
        value: function _removeObsolete(qs, newItems, nested) {
            var _this5 = this;

            var idsToKeep = newItems.map(function (row) {
                return row.id;
            }).filter(function (id) {
                return !!id;
            }),
                obsolete = qs.filter(function (item) {
                return !idsToKeep.includes(item.id);
            });

            if (nested) {
                obsolete.toModelArray().forEach(function (item) {
                    return _this5._nestedDelete(item);
                });
            } else {
                obsolete.delete();
            }
        }
    }, {
        key: "_nestedCreate",
        value: function _nestedCreate(cls, data) {
            var item = this._setNested(cls, data);

            cls.create(item);
        }
    }, {
        key: "_nestedUpdate",
        value: function _nestedUpdate(cls, data) {
            var item = this._setNested(cls, data);

            cls.upsert(item);
        }
    }, {
        key: "_nestedDelete",
        value: function _nestedDelete(instance) {
            var nested = this.getNestedModels(instance.getClass().modelName);
            nested.forEach(function (_ref4) {
                var relatedName = _ref4.relatedName;
                instance[relatedName].delete();
            });
            instance.delete();
        }
    }, {
        key: "_updateID",
        value: function _updateID(cls, oldId, newId) {
            // New ID was assigned (i.e. by the server)
            var exist = cls.withId(oldId),
                rrel = this.getReverseRels(cls.modelName);

            if (!exist) {
                return;
            } // Update any existing FKs to point to the new ID
            // (including both nested and non-nested relationships)


            rrel.forEach(function (_ref5) {
                var fkName = _ref5.fkName,
                    relatedName = _ref5.relatedName;
                exist[relatedName].update(_defineProperty({}, fkName, newId));
            }); // Remove and replace (see redux-orm #176)

            cls.upsert(_objectSpread2({}, exist.ref, {
                id: newId
            }));
            exist.delete();
        }
    }, {
        key: "prefix",
        get: function get() {
            if (this.store.name === 'main') {
                return 'ORM';
            } else {
                return "".concat(this.store.name.toUpperCase(), "ORM");
            }
        }
    }]);

    return ORMWithReducer;
}(reduxOrm.ORM);

var ModelMeta =
/*#__PURE__*/
function (_ORMModel) {
    _inherits(ModelMeta, _ORMModel);

    function ModelMeta() {
        _classCallCheck(this, ModelMeta);

        return _possibleConstructorReturn(this, _getPrototypeOf(ModelMeta).apply(this, arguments));
    }

    return ModelMeta;
}(reduxOrm.Model);

ModelMeta.modelName = '_modelmeta';

function orm(store) {
    if (!_orms[store.name]) {
        var _orm = _orms[store.name] = new ORMWithReducer(store);

        store.addReducer('orm', function (state, action) {
            return _orm.reducer(state, action);
        }, true);

        _orm.register(ModelMeta);
    }

    return _orms[store.name];
}

model.cacheOpts = {
    // First page (e.g. 50 records) is stored locally; subsequent pages can be
    // loaded from server.
    first_page: {
        server: true,
        client: true,
        page: 1,
        reversed: true
    },
    // All data is prefetched and stored locally, no subsequent requests are
    // necessary.
    all: {
        server: false,
        client: true,
        page: 0,
        reversed: false
    },
    // "Important" data is cached; other data can be accessed via pagination.
    filter: {
        server: true,
        client: true,
        page: 0,
        reversed: true
    },
    // No data is cached locally; all data require a network request.
    none: {
        server: true,
        client: false,
        page: 0,
        reversed: false
    }
}; // Retrieve a stored list as an object with helper functions
//  - especially useful for server-paginated lists
//  - methods must be called asynchronously

var Model =
/*#__PURE__*/
function () {
    function Model(config) {
        _classCallCheck(this, Model);

        if (!config) {
            throw 'No configuration provided!';
        }

        if (typeof config == 'string') {
            config = {
                query: config,
                name: config
            };
        }

        if (!config.name) {
            throw new Error('Model name is now required.');
        }

        if (!config.cache) {
            config.cache = 'first_page';
        }

        this.config = config;
        this.name = config.name;
        this.idCol = config.idCol || 'id';
        this.opts = model.cacheOpts[config.cache];

        if (!this.opts) {
            throw 'Unknown cache option ' + config.cache;
        }

        ['max_local_pages', 'partial', 'reversed'].forEach(function (name) {
            if (name in config) {
                throw '"' + name + '" is deprecated in favor of "cache"';
            }
        }); // Default to main store, but allow overriding

        if (config.store) {
            if (config.store instanceof ds.constructor) {
                this.store = config.store;
            } else {
                this.store = ds.getStore(config.store);
            }
        } else {
            this.store = ds;
        }

        this.orm = orm(this.store);

        try {
            this._model = this.orm.get(this.name);
        } catch (e) {
            var idCol = this.idCol;

            var M =
            /*#__PURE__*/
            function (_ORMModel2) {
                _inherits(M, _ORMModel2);

                function M() {
                    _classCallCheck(this, M);

                    return _possibleConstructorReturn(this, _getPrototypeOf(M).apply(this, arguments));
                }

                _createClass(M, null, [{
                    key: "idAttribute",
                    get: function get() {
                        return idCol;
                    }
                }, {
                    key: "fields",
                    get: function get() {
                        var fields = {};
                        (config.form || []).forEach(function (field) {
                            if (field['wq:ForeignKey']) {
                                fields[field.name + '_id'] = reduxOrm.fk({
                                    to: field['wq:ForeignKey'],
                                    as: field.name,
                                    relatedName: field['wq:related_name'] || config.url || config.name + 's'
                                });
                            } else if (field.type !== 'repeat') {
                                fields[field.name] = reduxOrm.attr();
                            }
                        });
                        return fields;
                    }
                }, {
                    key: "wqConfig",
                    get: function get() {
                        return config;
                    }
                }]);

                return M;
            }(reduxOrm.Model);

            M.modelName = this.name;
            this.orm.register(M);
            this._model = M;
        }

        if (config.query) {
            this.query = this.store.normalizeQuery(config.query);
        } else if (config.url !== undefined) {
            this.query = {
                url: config.url
            };
        } // Configurable functions to e.g. filter data by


        this.functions = config.functions || {};
    }

    _createClass(Model, [{
        key: "expandActionType",
        value: function expandActionType(type) {
            return "".concat(this.orm.prefix, "_").concat(this.name.toUpperCase(), "_").concat(type);
        }
    }, {
        key: "dispatch",
        value: function dispatch(type, payload, meta) {
            var action = {
                type: this.expandActionType(type),
                payload: payload
            };

            if (meta) {
                action.meta = meta;
            }

            return this.store.dispatch(action);
        }
    }, {
        key: "getSession",
        value: function getSession() {
            return this.orm.session(this.store.getState().orm);
        }
    }, {
        key: "getSessionModel",
        value: function getSessionModel() {
            var model = this.getSession()[this.name];

            if (!model) {
                throw new Error('Could not find model in session');
            }

            return model;
        }
    }, {
        key: "getQuerySet",
        value: function getQuerySet() {
            var model = this.getSessionModel();
            return model.all().orderBy(this.idCol, this.opts.reversed ? 'desc' : 'asc');
        }
    }, {
        key: "getPage",
        value: function () {
            var _getPage = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee(page_num) {
                var query, result, data;
                return regenerator.wrap(function _callee$(_context) {
                    while (1) {
                        switch (_context.prev = _context.next) {
                            case 0:
                                query = _objectSpread2({}, this.query);

                                if (page_num !== null) {
                                    query.page = page_num;
                                }

                                _context.next = 4;
                                return this.store.fetch(query);

                            case 4:
                                result = _context.sent;
                                data = this._processData(result);

                                if (!data.page) {
                                    data.page = page_num;
                                }

                                return _context.abrupt("return", data);

                            case 8:
                            case "end":
                                return _context.stop();
                        }
                    }
                }, _callee, this);
            }));

            function getPage(_x) {
                return _getPage.apply(this, arguments);
            }

            return getPage;
        }()
    }, {
        key: "_processData",
        value: function _processData(data) {
            if (!data) {
                data = [];
            }

            if (Array.isArray(data)) {
                data = {
                    list: data
                };
            }

            if (!data.pages) {
                data.pages = 1;
            }

            if (!data.count) {
                data.count = data.list.length;
            }

            if (!data.per_page) {
                data.per_page = data.list.length;
            }

            return data;
        }
    }, {
        key: "_withNested",
        value: function _withNested(instance) {
            var data = deepcopy(instance.ref);
            var nested = this.orm.getNestedModels(instance.getClass().modelName);
            nested.forEach(function (_ref6) {
                var relatedName = _ref6.relatedName;
                data[relatedName] = instance[relatedName].toRefArray();
            });
            return data;
        }
    }, {
        key: "load",
        value: function () {
            var _load = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee2() {
                var _this6 = this;

                var info;
                return regenerator.wrap(function _callee2$(_context2) {
                    while (1) {
                        switch (_context2.prev = _context2.next) {
                            case 0:
                                _context2.next = 2;
                                return this.info();

                            case 2:
                                info = _context2.sent;
                                return _context2.abrupt("return", _objectSpread2({}, info, {
                                    list: this.getQuerySet().toModelArray().map(function (instance) {
                                        return _this6._withNested(instance);
                                    })
                                }));

                            case 4:
                            case "end":
                                return _context2.stop();
                        }
                    }
                }, _callee2, this);
            }));

            function load() {
                return _load.apply(this, arguments);
            }

            return load;
        }()
    }, {
        key: "info",
        value: function () {
            var _info = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee3() {
                var retry,
                    info,
                    _info$ref,
                    pages,
                    count,
                    per_page,
                    _args3 = arguments;

                return regenerator.wrap(function _callee3$(_context3) {
                    while (1) {
                        switch (_context3.prev = _context3.next) {
                            case 0:
                                retry = _args3.length > 0 && _args3[0] !== undefined ? _args3[0] : true;
                                info = this.getSession()._modelmeta.withId(this.name);

                                if (!info) {
                                    _context3.next = 7;
                                    break;
                                }

                                _info$ref = info.ref, pages = _info$ref.pages, count = _info$ref.count, per_page = _info$ref.per_page;
                                return _context3.abrupt("return", {
                                    pages: pages,
                                    count: count,
                                    per_page: per_page
                                });

                            case 7:
                                if (!(this.query && retry)) {
                                    _context3.next = 13;
                                    break;
                                }

                                _context3.next = 10;
                                return this.prefetch();

                            case 10:
                                return _context3.abrupt("return", this.info(false));

                            case 13:
                                return _context3.abrupt("return", {
                                    pages: 1,
                                    count: 0,
                                    per_page: 0
                                });

                            case 14:
                            case "end":
                                return _context3.stop();
                        }
                    }
                }, _callee3, this);
            }));

            function info() {
                return _info.apply(this, arguments);
            }

            return info;
        }()
    }, {
        key: "ensureLoaded",
        value: function () {
            var _ensureLoaded = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee4() {
                return regenerator.wrap(function _callee4$(_context4) {
                    while (1) {
                        switch (_context4.prev = _context4.next) {
                            case 0:
                                _context4.next = 2;
                                return this.info();

                            case 2:
                            case "end":
                                return _context4.stop();
                        }
                    }
                }, _callee4, this);
            }));

            function ensureLoaded() {
                return _ensureLoaded.apply(this, arguments);
            }

            return ensureLoaded;
        }() // Load data for the given page number

    }, {
        key: "page",
        value: function () {
            var _page = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee5(page_num) {
                return regenerator.wrap(function _callee5$(_context5) {
                    while (1) {
                        switch (_context5.prev = _context5.next) {
                            case 0:
                                if (this.config.url) {
                                    _context5.next = 3;
                                    break;
                                }

                                if (!(page_num > this.opts.page)) {
                                    _context5.next = 3;
                                    break;
                                }

                                throw new Error('No URL, cannot retrieve page ' + page_num);

                            case 3:
                                if (!(page_num <= this.opts.page)) {
                                    _context5.next = 7;
                                    break;
                                }

                                return _context5.abrupt("return", this.load());

                            case 7:
                                return _context5.abrupt("return", this.getPage(page_num));

                            case 8:
                            case "end":
                                return _context5.stop();
                        }
                    }
                }, _callee5, this);
            }));

            function page(_x2) {
                return _page.apply(this, arguments);
            }

            return page;
        }() // Iterate across stored data

    }, {
        key: "forEach",
        value: function () {
            var _forEach = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee6(cb, thisarg) {
                var data;
                return regenerator.wrap(function _callee6$(_context6) {
                    while (1) {
                        switch (_context6.prev = _context6.next) {
                            case 0:
                                _context6.next = 2;
                                return this.load();

                            case 2:
                                data = _context6.sent;
                                data.list.forEach(cb, thisarg);

                            case 4:
                            case "end":
                                return _context6.stop();
                        }
                    }
                }, _callee6, this);
            }));

            function forEach(_x3, _x4) {
                return _forEach.apply(this, arguments);
            }

            return forEach;
        }() // Find an object by id

    }, {
        key: "find",
        value: function () {
            var _find = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee7(value, localOnly) {
                var model, instance;
                return regenerator.wrap(function _callee7$(_context7) {
                    while (1) {
                        switch (_context7.prev = _context7.next) {
                            case 0:
                                if (!(localOnly && typeof localOnly !== 'boolean')) {
                                    _context7.next = 2;
                                    break;
                                }

                                throw new Error('Usage: find(value[, localOnly).  To customize id attr use config.idCol');

                            case 2:
                                _context7.next = 4;
                                return this.ensureLoaded();

                            case 4:
                                model = this.getSessionModel(), instance = model.withId(value);

                                if (!instance) {
                                    _context7.next = 9;
                                    break;
                                }

                                return _context7.abrupt("return", this._withNested(instance));

                            case 9:
                                if (!(value !== undefined && !localOnly && this.opts.server && this.config.url)) {
                                    _context7.next = 15;
                                    break;
                                }

                                _context7.next = 12;
                                return this.store.fetch('/' + this.config.url + '/' + value);

                            case 12:
                                return _context7.abrupt("return", _context7.sent);

                            case 15:
                                return _context7.abrupt("return", null);

                            case 16:
                            case "end":
                                return _context7.stop();
                        }
                    }
                }, _callee7, this);
            }));

            function find(_x5, _x6) {
                return _find.apply(this, arguments);
            }

            return find;
        }()
    }, {
        key: "filterFields",
        value: function filterFields() {
            var _this7 = this;

            var fields = [this.idCol];
            fields = fields.concat((this.config.form || []).map(function (field) {
                return field['wq:ForeignKey'] ? "".concat(field.name, "_id") : field.name;
            }));
            fields = fields.concat(Object.keys(this.functions));
            fields = fields.concat(this.config.filter_fields || []);

            if (this.config.filter_ignore) {
                fields = fields.filter(function (field) {
                    return !_this7.config.filter_ignore.includes(field);
                });
            }

            return fields;
        } // Filter an array of objects by one or more attributes

    }, {
        key: "filterPage",
        value: function () {
            var _filterPage = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee8(filter, any, localOnly) {
                var _this8 = this;

                var filterFields, result, qs, defaultFilter, customFilter, hasDefaultFilter, hasCustomFilter;
                return regenerator.wrap(function _callee8$(_context8) {
                    while (1) {
                        switch (_context8.prev = _context8.next) {
                            case 0:
                                // Ignore fields that are not explicitly registered
                                // (e.g. for use with list views that have custom URL params)
                                filterFields = this.filterFields();
                                Object.keys(filter).forEach(function (field) {
                                    if (!filterFields.includes(field)) {
                                        if (!(_this8.config.filter_ignore || []).includes(field)) {
                                            console.warn("Ignoring unrecognized field \"".concat(field, "\"") + " while filtering ".concat(_this8.name, " list.") + ' Add to form or filter_fields to enable filtering,' + ' or to filter_ignore to remove this warning.');
                                        }

                                        filter = _objectSpread2({}, filter);
                                        delete filter[field];
                                    }
                                }); // If partial list, we can never be 100% sure all filter matches are
                                // stored locally. In that case, run query on server.

                                if (!(!localOnly && this.opts.server && this.config.url)) {
                                    _context8.next = 7;
                                    break;
                                }

                                _context8.next = 5;
                                return this.store.fetch(_objectSpread2({
                                    url: this.config.url
                                }, filter));

                            case 5:
                                result = _context8.sent;
                                return _context8.abrupt("return", this._processData(result));

                            case 7:
                                if (!(!filter || !Object.keys(filter).length)) {
                                    _context8.next = 9;
                                    break;
                                }

                                return _context8.abrupt("return", this.load());

                            case 9:
                                _context8.next = 11;
                                return this.ensureLoaded();

                            case 11:
                                qs = this.getQuerySet();

                                if (any) {
                                    // any=true: Match on any of the provided filter attributes
                                    qs = qs.filter(function (item) {
                                        return Object.keys(filter).filter(function (attr) {
                                            return _this8.matches(item, attr, filter[attr]);
                                        }).length > 0;
                                    });
                                } else {
                                    // Default: require match on all filter attributes
                                    // Use object filter to take advantage of redux-orm indexes -
                                    // except for boolean/array/computed filters.
                                    defaultFilter = {}, customFilter = {}, hasDefaultFilter = false, hasCustomFilter = false;
                                    Object.keys(filter).forEach(function (attr) {
                                        var comp = filter[attr];

                                        if (_this8.isCustomFilter(attr, comp)) {
                                            customFilter[attr] = comp;
                                            hasCustomFilter = true;
                                        } else {
                                            defaultFilter[attr] = comp;
                                            hasDefaultFilter = true;
                                        }
                                    });

                                    if (hasDefaultFilter) {
                                        qs = qs.filter(defaultFilter);
                                    }

                                    if (hasCustomFilter) {
                                        qs = qs.filter(function (item) {
                                            var match = true;
                                            Object.keys(customFilter).forEach(function (attr) {
                                                if (!_this8.matches(item, attr, customFilter[attr])) {
                                                    match = false;
                                                }
                                            });
                                            return match;
                                        });
                                    }
                                }

                                return _context8.abrupt("return", this._processData(qs.toModelArray().map(function (instance) {
                                    return _this8._withNested(instance);
                                })));

                            case 14:
                            case "end":
                                return _context8.stop();
                        }
                    }
                }, _callee8, this);
            }));

            function filterPage(_x7, _x8, _x9) {
                return _filterPage.apply(this, arguments);
            }

            return filterPage;
        }() // Filter an array of objects by one or more attributes

    }, {
        key: "filter",
        value: function () {
            var _filter2 = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee9(_filter, any, localOnly) {
                var data;
                return regenerator.wrap(function _callee9$(_context9) {
                    while (1) {
                        switch (_context9.prev = _context9.next) {
                            case 0:
                                _context9.next = 2;
                                return this.filterPage(_filter, any, localOnly);

                            case 2:
                                data = _context9.sent;
                                return _context9.abrupt("return", data.list);

                            case 4:
                            case "end":
                                return _context9.stop();
                        }
                    }
                }, _callee9, this);
            }));

            function filter(_x10, _x11, _x12) {
                return _filter2.apply(this, arguments);
            }

            return filter;
        }() // Create new item

    }, {
        key: "create",
        value: function () {
            var _create = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee10(object, meta) {
                return regenerator.wrap(function _callee10$(_context10) {
                    while (1) {
                        switch (_context10.prev = _context10.next) {
                            case 0:
                                this.dispatch(CREATE, object, meta);

                            case 1:
                            case "end":
                                return _context10.stop();
                        }
                    }
                }, _callee10, this);
            }));

            function create(_x13, _x14) {
                return _create.apply(this, arguments);
            }

            return create;
        }() // Merge new/updated items into list

    }, {
        key: "update",
        value: function () {
            var _update2 = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee11(_update, meta) {
                return regenerator.wrap(function _callee11$(_context11) {
                    while (1) {
                        switch (_context11.prev = _context11.next) {
                            case 0:
                                if (!(meta && typeof meta === 'string')) {
                                    _context11.next = 2;
                                    break;
                                }

                                throw new Error('Usage: update(items[, meta]).  To customize id attr use config.idCol');

                            case 2:
                                return _context11.abrupt("return", this.dispatch(UPDATE, _update, meta));

                            case 3:
                            case "end":
                                return _context11.stop();
                        }
                    }
                }, _callee11, this);
            }));

            function update(_x15, _x16) {
                return _update2.apply(this, arguments);
            }

            return update;
        }()
    }, {
        key: "remove",
        value: function () {
            var _remove = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee12(id, meta) {
                return regenerator.wrap(function _callee12$(_context12) {
                    while (1) {
                        switch (_context12.prev = _context12.next) {
                            case 0:
                                if (!(meta && typeof meta === 'string')) {
                                    _context12.next = 2;
                                    break;
                                }

                                throw new Error('Usage: remove(id).  To customize id attr use config.idCol');

                            case 2:
                                return _context12.abrupt("return", this.dispatch(DELETE, id, meta));

                            case 3:
                            case "end":
                                return _context12.stop();
                        }
                    }
                }, _callee12, this);
            }));

            function remove(_x17, _x18) {
                return _remove.apply(this, arguments);
            }

            return remove;
        }() // Overwrite entire list

    }, {
        key: "overwrite",
        value: function () {
            var _overwrite = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee13(data, meta) {
                return regenerator.wrap(function _callee13$(_context13) {
                    while (1) {
                        switch (_context13.prev = _context13.next) {
                            case 0:
                                if (data.pages == 1 && data.list) {
                                    data.count = data.per_page = data.list.length;
                                } else {
                                    data = this._processData(data);
                                }

                                return _context13.abrupt("return", this.dispatch(OVERWRITE, data, meta));

                            case 2:
                            case "end":
                                return _context13.stop();
                        }
                    }
                }, _callee13, this);
            }));

            function overwrite(_x19, _x20) {
                return _overwrite.apply(this, arguments);
            }

            return overwrite;
        }() // Prefetch list

    }, {
        key: "prefetch",
        value: function () {
            var _prefetch = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee14() {
                var data;
                return regenerator.wrap(function _callee14$(_context14) {
                    while (1) {
                        switch (_context14.prev = _context14.next) {
                            case 0:
                                _context14.next = 2;
                                return this.getPage(null);

                            case 2:
                                data = _context14.sent;
                                return _context14.abrupt("return", this.overwrite(data));

                            case 4:
                            case "end":
                                return _context14.stop();
                        }
                    }
                }, _callee14, this);
            }));

            function prefetch() {
                return _prefetch.apply(this, arguments);
            }

            return prefetch;
        }() // Helper for partial list updates (useful for large lists)
        // Note: params should contain correct arguments to fetch only "recent"
        // items from server; idcol should be a unique identifier for the list

    }, {
        key: "fetchUpdate",
        value: function () {
            var _fetchUpdate = _asyncToGenerator(
            /*#__PURE__*/
            regenerator.mark(function _callee15(params, idCol) {
                var q, data;
                return regenerator.wrap(function _callee15$(_context15) {
                    while (1) {
                        switch (_context15.prev = _context15.next) {
                            case 0:
                                if (!idCol) {
                                    _context15.next = 2;
                                    break;
                                }

                                throw new Error('Usage: fetchUpdate(params).  To customize id attr use config.idCol');

                            case 2:
                                // Update local list with recent items from server
                                q = _objectSpread2({}, this.query, {}, params);
                                _context15.next = 5;
                                return this.store.fetch(q);

                            case 5:
                                data = _context15.sent;
                                return _context15.abrupt("return", this.update(data));

                            case 7:
                            case "end":
                                return _context15.stop();
                        }
                    }
                }, _callee15, this);
            }));

            function fetchUpdate(_x21, _x22) {
                return _fetchUpdate.apply(this, arguments);
            }

            return fetchUpdate;
        }() // Unsaved form items related to this list

    }, {
        key: "unsyncedItems",
        value: function unsyncedItems(withData) {
            // Note: wq/outbox needs to have already been loaded for this to work
            var outbox = this.store.outbox;

            if (!outbox) {
                return Promise.resolve([]);
            }

            return outbox.unsyncedItems(this.query, withData);
        } // Apply a predefined function to a retreived item

    }, {
        key: "compute",
        value: function compute(fn, item) {
            if (this.functions[fn]) {
                return this.functions[fn](item);
            } else {
                return null;
            }
        }
    }, {
        key: "isCustomFilter",
        value: function isCustomFilter(attr, comp) {
            return this.functions[attr] || isPotentialBoolean(comp) || Array.isArray(comp);
        }
    }, {
        key: "matches",
        value: function matches(item, attr, comp) {
            var value;

            if (this.functions[attr]) {
                value = this.compute(attr, item);
            } else {
                value = item[attr];
            }

            if (Array.isArray(comp)) {
                return comp.filter(function (c) {
                    return checkValue(value, c);
                }).length > 0;
            } else {
                return checkValue(value, comp);
            }

            function checkValue(value, comp) {
                if (isRawBoolean(value)) {
                    return value === toBoolean(comp);
                } else if (typeof value === 'number') {
                    return value === +comp;
                } else if (Array.isArray(value)) {
                    return value.filter(function (v) {
                        return checkValue(v, comp);
                    }).length > 0;
                } else {
                    return value === comp;
                }
            }
        }
    }, {
        key: "model",
        get: function get() {
            return this.getSessionModel();
        }
    }, {
        key: "objects",
        get: function get() {
            return this.getQuerySet();
        }
    }]);

    return Model;
}();

function isRawBoolean(value) {
    return [null, true, false].indexOf(value) > -1;
}

function toBoolean(value) {
    if ([true, 'true', 1, '1', 't', 'y'].indexOf(value) > -1) {
        return true;
    } else if ([false, 'false', 0, '0', 'f', 'n'].indexOf(value) > -1) {
        return false;
    } else if ([null, 'null'].indexOf(value) > -1) {
        return null;
    } else {
        return value;
    }
}

function isPotentialBoolean(value) {
    return isRawBoolean(toBoolean(value));
}

model.Model = Model;

exports.Model = Model;
exports.default = model;

Object.defineProperty(exports, '__esModule', { value: true });

});
//# sourceMappingURL=model.js.map
