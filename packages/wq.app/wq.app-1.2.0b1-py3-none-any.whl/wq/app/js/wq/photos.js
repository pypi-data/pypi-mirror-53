/*
 * wq.app v1.2.0b1 - @wq/app/photos 1.2.0-beta.1
 * Helpers for working with Cordova photo library
 * (c) 2012-2019, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['regenerator-runtime', 'localforage'], function (_regeneratorRuntime, localForage) { 'use strict';

_regeneratorRuntime = _regeneratorRuntime && _regeneratorRuntime.hasOwnProperty('default') ? _regeneratorRuntime['default'] : _regeneratorRuntime;
localForage = localForage && localForage.hasOwnProperty('default') ? localForage['default'] : localForage;

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

var LOCALFORAGE_PREFIX = '__lfsc__:blob~~local_forage_type~image/jpeg~';
var photos = {
    name: 'photos'
};
var _defaults = {
    quality: 75,
    destinationType: 0 //Camera.DestinationType.DATA_URL

};
var $, jqm, spin;

photos.init = function (config) {
    $ = config && config.jQuery || window.jQuery;
    spin = photos.app.spin;
};

photos.context = function () {
    return {
        image_url: function image_url() {
            try {
                return this.body && _getUrl(this.body);
            } catch (e) {// Image will be blank, but at least template won't crash
            }
        }
    };
};

photos.run = function ($page) {
    $page.on('change', 'input[type=file]', photos.preview);
    $page.on('click', 'button[data-wq-action=take]', photos.take);
    $page.on('click', 'button[data-wq-action=pick]', photos.pick);
};

photos.preview = function (imgid, file) {
    if (typeof imgid !== 'string' && !file) {
        imgid = $(this).data('wq-preview');

        if (!imgid) {
            return;
        }

        file = this.files[0];

        if (!file) {
            return;
        }
    }

    $('#' + imgid).attr('src', _getUrl(file));
};

function _getUrl(file) {
    var URL = window.URL || window.webkitURL;
    return URL && URL.createObjectURL(file);
}

photos.take = function (input, preview) {
    var options = $.extend({
        sourceType: Camera.PictureSourceType.CAMERA,
        correctOrientation: true,
        saveToPhotoAlbum: true
    }, _defaults);

    _start.call(this, options, input, preview);
};

photos.pick = function (input, preview) {
    var options = $.extend({
        sourceType: Camera.PictureSourceType.SAVEDPHOTOALBUM
    }, _defaults);

    _start.call(this, options, input, preview);
};

function _start(options, input, preview) {
    if (typeof input !== 'string' && !preview) {
        input = $(this).data('wq-input');

        if (!input) {
            return;
        }

        preview = jqm.activePage.find('#' + input).data('wq-preview');
    }

    navigator.camera.getPicture(function (data) {
        load(data, input, preview);
    }, function (msg) {
        error(msg);
    }, options);
}

photos.base64toBlob =
/*#__PURE__*/
function () {
    var _ref = _asyncToGenerator(
    /*#__PURE__*/
    _regeneratorRuntime.mark(function _callee(data) {
        var serializer;
        return _regeneratorRuntime.wrap(function _callee$(_context) {
            while (1) {
                switch (_context.prev = _context.next) {
                    case 0:
                        _context.next = 2;
                        return photos.app.store.ready;

                    case 2:
                        _context.next = 4;
                        return localForage.getSerializer();

                    case 4:
                        serializer = _context.sent;
                        return _context.abrupt("return", serializer.deserialize(LOCALFORAGE_PREFIX + data));

                    case 6:
                    case "end":
                        return _context.stop();
                }
            }
        }, _callee);
    }));

    return function (_x) {
        return _ref.apply(this, arguments);
    };
}();

photos._files = {};

photos.storeFile = function (name, type, blob, input) {
    // Save blob data for later retrieval
    var file = {
        name: name,
        type: type,
        body: blob
    };
    photos._files[name] = file;

    if (input) {
        $('#' + input).val(name);
    }
};

function load(data, input, preview) {
    spin.start('Loading image...');
    photos.base64toBlob(data).then(function (blob) {
        var number = Math.round(Math.random() * 1e10);
        var name = $('#' + input).val() || 'photo' + number + '.jpg';
        photos.storeFile(name, 'image/jpeg', blob, input);
        spin.stop();

        if (preview) {
            photos.preview(preview, blob);
        }
    });
}

function error(msg) {
    spin.start('Error Loading Image: ' + msg, 1.5, {
        theme: jqm.pageLoadErrorMessageTheme,
        textonly: true
    });
}

return photos;

});
//# sourceMappingURL=photos.js.map
