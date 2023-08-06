(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("kepler.gl/actions"), require("kepler.gl/dist/middleware"), require("kepler.gl/processors"), require("kepler.gl/reducers"), require("kepler.gl/schemas"), require("redux"));
	else if(typeof define === 'function' && define.amd)
		define([, , , , , ], factory);
	else {
		var a = typeof exports === 'object' ? factory(require("kepler.gl/actions"), require("kepler.gl/dist/middleware"), require("kepler.gl/processors"), require("kepler.gl/reducers"), require("kepler.gl/schemas"), require("redux")) : factory(root["KeplerGl"], root["KeplerGl"], root["KeplerGl"], root["KeplerGl"], root["KeplerGl"], root["Redux"]);
		for(var i in a) (typeof exports === 'object' ? exports : root)[i] = a[i];
	}
})(window, function(__WEBPACK_EXTERNAL_MODULE_kepler_gl_actions__, __WEBPACK_EXTERNAL_MODULE_kepler_gl_dist_middleware__, __WEBPACK_EXTERNAL_MODULE_kepler_gl_processors__, __WEBPACK_EXTERNAL_MODULE_kepler_gl_reducers__, __WEBPACK_EXTERNAL_MODULE_kepler_gl_schemas__, __WEBPACK_EXTERNAL_MODULE_redux__) {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
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
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./lib/keplergl/main.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./lib/keplergl/components/root.js":
/*!*****************************************!*\
  !*** ./lib/keplergl/components/root.js ***!
  \*****************************************/
/*! exports provided: default */
/***/ (function(module, exports) {

eval("throw new Error(\"Module build failed (from ./node_modules/babel-loader/lib/index.js):\\nSyntaxError: /Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/lib/keplergl/components/root.js: Unexpected token (28:4)\\n\\n\\u001b[0m \\u001b[90m 26 | \\u001b[39m\\u001b[36mfunction\\u001b[39m renderRoot({id\\u001b[33m,\\u001b[39m store\\u001b[33m,\\u001b[39m ele}) {\\u001b[0m\\n\\u001b[0m \\u001b[90m 27 | \\u001b[39m  \\u001b[36mconst\\u001b[39m \\u001b[33mRoot\\u001b[39m \\u001b[33m=\\u001b[39m () \\u001b[33m=>\\u001b[39m (\\u001b[0m\\n\\u001b[0m\\u001b[31m\\u001b[1m>\\u001b[22m\\u001b[39m\\u001b[90m 28 | \\u001b[39m    \\u001b[33m<\\u001b[39m\\u001b[33mProvider\\u001b[39m store\\u001b[33m=\\u001b[39m{store}\\u001b[33m>\\u001b[39m\\u001b[0m\\n\\u001b[0m \\u001b[90m    | \\u001b[39m    \\u001b[31m\\u001b[1m^\\u001b[22m\\u001b[39m\\u001b[0m\\n\\u001b[0m \\u001b[90m 29 | \\u001b[39m      \\u001b[33m<\\u001b[39m\\u001b[33mApp\\u001b[39m \\u001b[33m/\\u001b[39m\\u001b[33m>\\u001b[39m\\u001b[0m\\n\\u001b[0m \\u001b[90m 30 | \\u001b[39m    \\u001b[33m<\\u001b[39m\\u001b[33m/\\u001b[39m\\u001b[33mProvider\\u001b[39m\\u001b[33m>\\u001b[39m\\u001b[0m\\n\\u001b[0m \\u001b[90m 31 | \\u001b[39m  )\\u001b[33m;\\u001b[39m\\u001b[0m\\n    at Parser.raise (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:6344:17)\\n    at Parser.unexpected (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:7659:16)\\n    at Parser.parseExprAtom (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8828:20)\\n    at Parser.parseExprSubscripts (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8413:23)\\n    at Parser.parseMaybeUnary (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8393:21)\\n    at Parser.parseExprOps (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8280:23)\\n    at Parser.parseMaybeConditional (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8253:23)\\n    at Parser.parseMaybeAssign (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8200:21)\\n    at Parser.parseParenAndDistinguishExpression (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8963:28)\\n    at Parser.parseExprAtom (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8760:21)\\n    at Parser.parseExprSubscripts (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8413:23)\\n    at Parser.parseMaybeUnary (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8393:21)\\n    at Parser.parseExprOps (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8280:23)\\n    at Parser.parseMaybeConditional (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8253:23)\\n    at Parser.parseMaybeAssign (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8200:21)\\n    at Parser.parseFunctionBody (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:9390:24)\\n    at Parser.parseArrowExpression (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:9349:10)\\n    at Parser.parseParenAndDistinguishExpression (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8986:12)\\n    at Parser.parseExprAtom (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8760:21)\\n    at Parser.parseExprSubscripts (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8413:23)\\n    at Parser.parseMaybeUnary (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8393:21)\\n    at Parser.parseExprOps (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8280:23)\\n    at Parser.parseMaybeConditional (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8253:23)\\n    at Parser.parseMaybeAssign (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:8200:21)\\n    at Parser.parseVar (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:10439:26)\\n    at Parser.parseVarStatement (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:10258:10)\\n    at Parser.parseStatementContent (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:9855:21)\\n    at Parser.parseStatement (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:9788:17)\\n    at Parser.parseBlockOrModuleBlockBody (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:10364:25)\\n    at Parser.parseBlockBody (/Users/shanhe/Uber/kepler.gl/bindings/kepler.gl-jupyter/js/node_modules/@babel/parser/lib/index.js:10351:10)\");\n\n//# sourceURL=webpack:///./lib/keplergl/components/root.js?");

/***/ }),

/***/ "./lib/keplergl/kepler.gl.js":
/*!***********************************!*\
  !*** ./lib/keplergl/kepler.gl.js ***!
  \***********************************/
/*! exports provided: addDataConfigToKeplerGl, dataToDatasets, default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"addDataConfigToKeplerGl\", function() { return addDataConfigToKeplerGl; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"dataToDatasets\", function() { return dataToDatasets; });\n/* harmony import */ var kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! kepler.gl/actions */ \"kepler.gl/actions\");\n/* harmony import */ var kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var kepler_gl_schemas__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! kepler.gl/schemas */ \"kepler.gl/schemas\");\n/* harmony import */ var kepler_gl_schemas__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_schemas__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var global_document__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! global/document */ \"./node_modules/global/document.js\");\n/* harmony import */ var global_document__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(global_document__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _components_root__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/root */ \"./lib/keplergl/components/root.js\");\n/* harmony import */ var _store__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./store */ \"./lib/keplergl/store.js\");\n/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./utils */ \"./lib/keplergl/utils.js\");\n/* harmony import */ var _log__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../log */ \"./lib/log.js\");\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n\n\n\n\n\n\n\n\nconst getData = that => that.model.get('data');\n\nconst getConfig = that => that.model.get('config');\n\nconst getHeight = that => that.model.get('height');\n\nconst DOM_EL_ID = 'keplergl';\nlet counter = 0;\nconst NONE_UPDATE_ACTIONS = [kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0__[\"ActionTypes\"].REGISTER_ENTRY, kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0__[\"ActionTypes\"].DELETE_ENTRY, kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0__[\"ActionTypes\"].RENAME_ENTRY, kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0__[\"ActionTypes\"].LOAD_MAP_STYLES, kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0__[\"ActionTypes\"].LAYER_HOVER];\n\nfunction getConfigInStore({\n  hash = true,\n  store\n} = {}) {\n  if (store) {\n    const currentState = store.getState().keplerGl.map;\n    const currentValue = kepler_gl_schemas__WEBPACK_IMPORTED_MODULE_1__[\"KeplerGlSchema\"].getConfigToSave(currentState);\n    return hash ? JSON.stringify(currentValue) : currentValue;\n  }\n\n  return {};\n}\n\nfunction getDatasetsInStore(store) {\n  if (store) {\n    return store.getState().keplerGl.map.visState.datasets;\n  }\n}\n\nclass KeplerGlJupyter {\n  constructor() {\n    this.id = `${DOM_EL_ID}-${counter}`;\n    counter++;\n    this.mapUpdateCounter = 0;\n  }\n\n  create(that) {\n    Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])('kepler.gl create');\n    let previousValue;\n\n    function handleStoreChange(action, nextStore) {\n      Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])(action);\n\n      if (!action || NONE_UPDATE_ACTIONS.includes(action.type)) {\n        return;\n      }\n\n      const saveState = getConfigInStore({\n        hash: false,\n        store: nextStore\n      });\n      const hash = JSON.stringify(saveState); // should not update model after first UPDATE_MAP action\n      // when component first mounted\n\n      if (previousValue !== hash && this.mapUpdateCounter > 2) {\n        // keplerGl State has changed\n        Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])('store state has changed, update model');\n        Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])(previousValue);\n        Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])(hash);\n        previousValue = hash;\n        that.model.set({\n          config: saveState\n        }); // that.model.save_changes();\n\n        that.touch();\n      }\n\n      if (action.type === kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0__[\"ActionTypes\"].UPDATE_MAP) {\n        this.mapUpdateCounter++;\n      }\n    }\n\n    this.store = Object(_store__WEBPACK_IMPORTED_MODULE_4__[\"default\"])(handleStoreChange.bind(this));\n    const height = getHeight(that);\n    that.el.classList.add('jupyter-widgets');\n    that.el.classList.add('keplergl-jupyter-widgets');\n    const divElmt = global_document__WEBPACK_IMPORTED_MODULE_2___default.a.createElement('div');\n    divElmt.setAttribute('id', this.id);\n    divElmt.classList.add('kepler-gl');\n    divElmt.setAttribute('style', ` width: 100%; height: ${height}px;`);\n    that.el.appendChild(divElmt);\n    Object(_components_root__WEBPACK_IMPORTED_MODULE_3__[\"default\"])({\n      id: this.id,\n      store: this.store,\n      ele: divElmt\n    });\n    const data = getData(that);\n    const config = getConfig(that);\n    Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])('<<<<<<<< render finished! >>>>>>>>>'); // After rendering the component,\n    // we add the data that's already in the model\n\n    const hasData = data && Object.keys(data).length;\n    const hasConfig = config && config.version;\n\n    if (hasData) {\n      Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])('data already in model');\n      addDataConfigToKeplerGl({\n        data,\n        config,\n        store: this.store\n      });\n    } else if (hasConfig) {\n      Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])('config already in model');\n      this.onConfigChange(that);\n    }\n  }\n\n  onDataChange(that) {\n    Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])('kepler.gl onDataChange');\n    const data = getData(that);\n    addDataConfigToKeplerGl({\n      data,\n      store: this.store\n    });\n  }\n\n  onConfigChange(that) {\n    Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])('kepler.gl onConfigChange');\n    const config = getConfig(that);\n    const currentValue = getConfigInStore({\n      hash: true,\n      store: this.store\n    });\n\n    if (currentValue === JSON.stringify(config)) {\n      // calling model.set('config') inside the js component will trigger another onConfigChange\n      Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])('onConfigChange: config is the same as saved in store');\n      return;\n    }\n\n    this.store.dispatch(Object(kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0__[\"addDataToMap\"])({\n      // reuse datasets in state\n      // a hack to apply config to existing data\n      datasets: Object.values(getDatasetsInStore(this.store)).map(d => ({\n        info: {\n          id: d.id,\n          label: d.label,\n          color: d.color\n        },\n        data: {\n          fields: d.fields,\n          rows: d.allData\n        }\n      })),\n      config,\n      options: {\n        centerMap: false\n      }\n    }));\n  }\n\n}\n\nfunction addDataConfigToKeplerGl({\n  data: inputData,\n  config,\n  options,\n  store\n}) {\n  const data = inputData ? dataToDatasets(inputData) : [];\n  Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])(data);\n  const results = Object(_utils__WEBPACK_IMPORTED_MODULE_5__[\"loadJupyterData\"])(data);\n  const succeeded = results.filter(r => r && r.data);\n  Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])('addDataConfigToKeplerGl');\n  Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])(succeeded);\n  Object(_log__WEBPACK_IMPORTED_MODULE_6__[\"default\"])(config);\n  store.dispatch(Object(kepler_gl_actions__WEBPACK_IMPORTED_MODULE_0__[\"addDataToMap\"])({\n    datasets: succeeded,\n    config,\n    options: options || {\n      centerMap: true\n    }\n  }));\n}\nfunction dataToDatasets(data) {\n  return Object.keys(data).map(key => ({\n    id: key,\n    data: data[key]\n  }));\n}\n/* harmony default export */ __webpack_exports__[\"default\"] = (KeplerGlJupyter);\n\n//# sourceURL=webpack:///./lib/keplergl/kepler.gl.js?");

/***/ }),

/***/ "./lib/keplergl/main.js":
/*!******************************!*\
  !*** ./lib/keplergl/main.js ***!
  \******************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _store__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./store */ \"./lib/keplergl/store.js\");\n/* harmony import */ var _components_root__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/root */ \"./lib/keplergl/components/root.js\");\n/* harmony import */ var global_document__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! global/document */ \"./node_modules/global/document.js\");\n/* harmony import */ var global_document__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(global_document__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var global_window__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! global/window */ \"./node_modules/global/window.js\");\n/* harmony import */ var global_window__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(global_window__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _kepler_gl__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./kepler.gl */ \"./lib/keplergl/kepler.gl.js\");\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n// NOTE: this is only used for exporting html template\n\n\n\n\n\n\nconst map = function initKeplerGl() {\n  const id = 'keplergl-0';\n  const store = Object(_store__WEBPACK_IMPORTED_MODULE_0__[\"default\"])();\n  const divElmt = global_document__WEBPACK_IMPORTED_MODULE_2___default.a.createElement('div');\n  divElmt.setAttribute('style', 'width: 100vw; height: 100vh; position: absolute');\n  global_document__WEBPACK_IMPORTED_MODULE_2___default.a.body.appendChild(divElmt);\n  return {\n    render: () => {\n      Object(_components_root__WEBPACK_IMPORTED_MODULE_1__[\"default\"])({\n        id,\n        store,\n        ele: divElmt\n      });\n    },\n    store\n  };\n}();\n\nmap.render();\n\n(function loadDataConfig(keplerGlMap) {\n  const {\n    data,\n    config,\n    options\n  } = global_window__WEBPACK_IMPORTED_MODULE_3___default.a.__keplerglDataConfig || {};\n  Object(_kepler_gl__WEBPACK_IMPORTED_MODULE_4__[\"addDataConfigToKeplerGl\"])({\n    data,\n    config,\n    options,\n    store: keplerGlMap.store\n  });\n})(map);\n\n//# sourceURL=webpack:///./lib/keplergl/main.js?");

/***/ }),

/***/ "./lib/keplergl/store.js":
/*!*******************************!*\
  !*** ./lib/keplergl/store.js ***!
  \*******************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var redux__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! redux */ \"redux\");\n/* harmony import */ var redux__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(redux__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var kepler_gl_reducers__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! kepler.gl/reducers */ \"kepler.gl/reducers\");\n/* harmony import */ var kepler_gl_reducers__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_reducers__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var kepler_gl_dist_middleware__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! kepler.gl/dist/middleware */ \"kepler.gl/dist/middleware\");\n/* harmony import */ var kepler_gl_dist_middleware__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_dist_middleware__WEBPACK_IMPORTED_MODULE_2__);\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n\n\n // TODO: remove this after added middleware to files\n\n\nconst customizedKeplerGlReducer = kepler_gl_reducers__WEBPACK_IMPORTED_MODULE_1__[\"keplerGlReducer\"].initialState({\n  uiState: {\n    currentModal: null,\n    activeSidePanel: null\n  }\n});\nconst reducers = Object(redux__WEBPACK_IMPORTED_MODULE_0__[\"combineReducers\"])({\n  // mount keplerGl reducer\n  keplerGl: customizedKeplerGlReducer\n});\n\nconst createAppStore = onChangeHandler => {\n  const updatesMiddleware = store => next => action => {\n    // exclude some actions\n    // Call the next dispatch method in the middleware chain.\n\n    /* eslint-disable callback-return */\n    const returnValue = next(action);\n    /* eslint-enable callback-return */\n    // state after dispatch\n\n    if (typeof onChangeHandler === 'function') {\n      onChangeHandler(action, store);\n    } // This will likely be the action itself, unless\n    // a middleware further in chain changed it.\n\n\n    return returnValue;\n  };\n\n  const middlewares = Object(kepler_gl_dist_middleware__WEBPACK_IMPORTED_MODULE_2__[\"enhanceReduxMiddleware\"])([updatesMiddleware]);\n  const enhancers = [Object(redux__WEBPACK_IMPORTED_MODULE_0__[\"applyMiddleware\"])(...middlewares)];\n  const store = Object(redux__WEBPACK_IMPORTED_MODULE_0__[\"createStore\"])(reducers, {}, Object(redux__WEBPACK_IMPORTED_MODULE_0__[\"compose\"])(...enhancers));\n  return store;\n};\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (createAppStore);\n\n//# sourceURL=webpack:///./lib/keplergl/store.js?");

/***/ }),

/***/ "./lib/keplergl/utils.js":
/*!*******************************!*\
  !*** ./lib/keplergl/utils.js ***!
  \*******************************/
/*! exports provided: loadJupyterData */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"loadJupyterData\", function() { return loadJupyterData; });\n/* harmony import */ var kepler_gl_processors__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! kepler.gl/processors */ \"kepler.gl/processors\");\n/* harmony import */ var kepler_gl_processors__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_processors__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _log__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../log */ \"./lib/log.js\");\n/* harmony import */ var global_console__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! global/console */ \"./node_modules/global/console.js\");\n/* harmony import */ var global_console__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(global_console__WEBPACK_IMPORTED_MODULE_2__);\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n\n\n\n\nfunction handleJuptyerDataFormat(dataEntry) {\n  // This makes passing data between Jupyter the iframe easier\n  // detect data type here\n  Object(_log__WEBPACK_IMPORTED_MODULE_1__[\"default\"])('handleJuptyerDataFormat');\n  const {\n    data,\n    id\n  } = dataEntry;\n  let parsed = data;\n  let type = 'csv';\n\n  if (typeof data === 'object') {\n    if (data.columns && data.data && data.index) {\n      // Data is parsed as a Dataframe\n      Object(_log__WEBPACK_IMPORTED_MODULE_1__[\"default\"])('data is a dataframe');\n      type = 'df'; // parsed = {fields: data.columns, data: data.data};\n    } else {\n      // assume is geojson\n      type = 'json';\n    }\n  } else if (typeof data === 'string') {\n    try {\n      parsed = JSON.parse(data);\n      type = 'json';\n    } catch (e) {// assume it is csv\n    }\n  }\n\n  return {\n    data: parsed,\n    type,\n    id\n  };\n}\n\nfunction processReceivedData({\n  data,\n  info\n}) {\n  // assume there is only 1 file\n  Object(_log__WEBPACK_IMPORTED_MODULE_1__[\"default\"])('processReceivedData');\n  let processed;\n\n  try {\n    processed = info.queryType === 'csv' ? Object(kepler_gl_processors__WEBPACK_IMPORTED_MODULE_0__[\"processCsvData\"])(data) : info.queryType === 'json' ? Object(kepler_gl_processors__WEBPACK_IMPORTED_MODULE_0__[\"processGeojson\"])(data) : info.queryType === 'df' ? processDataFrame(data) : null;\n  } catch (e) {\n    global_console__WEBPACK_IMPORTED_MODULE_2___default.a.log(`Kepler.gl fails to parse data, detected data\n    format is ${info.queryType}`, e);\n  }\n\n  return {\n    data: processed,\n    info\n  };\n}\n\nfunction processDataFrame(data) {\n  const fields = data.columns.map(name => ({\n    name\n  }));\n  const rows = data.data; // kepler.gl will detect field types\n\n  return {\n    fields,\n    rows\n  };\n}\n\nfunction loadJupyterData(rawData) {\n  const dataToLoad = rawData.map(handleJuptyerDataFormat).map(rd => ({\n    data: rd.data,\n    info: {\n      id: rd.id,\n      label: rd.id,\n      queryType: rd.type,\n      queryOption: 'jupyter'\n    }\n  }));\n  return dataToLoad.map(processReceivedData);\n}\n\n//# sourceURL=webpack:///./lib/keplergl/utils.js?");

/***/ }),

/***/ "./lib/log.js":
/*!********************!*\
  !*** ./lib/log.js ***!
  \********************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var global_console__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! global/console */ \"./node_modules/global/console.js\");\n/* harmony import */ var global_console__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(global_console__WEBPACK_IMPORTED_MODULE_0__);\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n\n\n\nfunction log(...args) {\n  if (true) {\n    global_console__WEBPACK_IMPORTED_MODULE_0___default.a.log(...args);\n  }\n}\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (log);\n\n\n//# sourceURL=webpack:///./lib/log.js?");

/***/ }),

/***/ "./node_modules/global/console.js":
/*!****************************************!*\
  !*** ./node_modules/global/console.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = console;\n\n\n//# sourceURL=webpack:///./node_modules/global/console.js?");

/***/ }),

/***/ "./node_modules/global/document.js":
/*!*****************************************!*\
  !*** ./node_modules/global/document.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function(global) {var topLevel = typeof global !== 'undefined' ? global :\n    typeof window !== 'undefined' ? window : {}\nvar minDoc = __webpack_require__(/*! min-document */ 0);\n\nvar doccy;\n\nif (typeof document !== 'undefined') {\n    doccy = document;\n} else {\n    doccy = topLevel['__GLOBAL_DOCUMENT_CACHE@4'];\n\n    if (!doccy) {\n        doccy = topLevel['__GLOBAL_DOCUMENT_CACHE@4'] = minDoc;\n    }\n}\n\nmodule.exports = doccy;\n\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../webpack/buildin/global.js */ \"./node_modules/webpack/buildin/global.js\")))\n\n//# sourceURL=webpack:///./node_modules/global/document.js?");

/***/ }),

/***/ "./node_modules/global/window.js":
/*!***************************************!*\
  !*** ./node_modules/global/window.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function(global) {var win;\n\nif (typeof window !== \"undefined\") {\n    win = window;\n} else if (typeof global !== \"undefined\") {\n    win = global;\n} else if (typeof self !== \"undefined\"){\n    win = self;\n} else {\n    win = {};\n}\n\nmodule.exports = win;\n\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../webpack/buildin/global.js */ \"./node_modules/webpack/buildin/global.js\")))\n\n//# sourceURL=webpack:///./node_modules/global/window.js?");

/***/ }),

/***/ "./node_modules/webpack/buildin/global.js":
/*!***********************************!*\
  !*** (webpack)/buildin/global.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("var g;\n\n// This works in non-strict mode\ng = (function() {\n\treturn this;\n})();\n\ntry {\n\t// This works if eval is allowed (see CSP)\n\tg = g || new Function(\"return this\")();\n} catch (e) {\n\t// This works if the window reference is available\n\tif (typeof window === \"object\") g = window;\n}\n\n// g can still be undefined, but nothing to do about it...\n// We return undefined, instead of nothing here, so it's\n// easier to handle this case. if(!global) { ...}\n\nmodule.exports = g;\n\n\n//# sourceURL=webpack:///(webpack)/buildin/global.js?");

/***/ }),

/***/ 0:
/*!******************************!*\
  !*** min-document (ignored) ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("/* (ignored) */\n\n//# sourceURL=webpack:///min-document_(ignored)?");

/***/ }),

/***/ "kepler.gl/actions":
/*!***************************************************************************************************!*\
  !*** external {"root":"KeplerGl","commonjs2":"kepler.gl/actions","commonjs":"kepler.gl/actions"} ***!
  \***************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_kepler_gl_actions__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22KeplerGl%22,%22commonjs2%22:%22kepler.gl/actions%22,%22commonjs%22:%22kepler.gl/actions%22%7D?");

/***/ }),

/***/ "kepler.gl/dist/middleware":
/*!*******************************************************************************************************************!*\
  !*** external {"root":"KeplerGl","commonjs2":"kepler.gl/dist/middleware","commonjs":"kepler.gl/dist/middleware"} ***!
  \*******************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_kepler_gl_dist_middleware__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22KeplerGl%22,%22commonjs2%22:%22kepler.gl/dist/middleware%22,%22commonjs%22:%22kepler.gl/dist/middleware%22%7D?");

/***/ }),

/***/ "kepler.gl/processors":
/*!*********************************************************************************************************!*\
  !*** external {"root":"KeplerGl","commonjs2":"kepler.gl/processors","commonjs":"kepler.gl/processors"} ***!
  \*********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_kepler_gl_processors__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22KeplerGl%22,%22commonjs2%22:%22kepler.gl/processors%22,%22commonjs%22:%22kepler.gl/processors%22%7D?");

/***/ }),

/***/ "kepler.gl/reducers":
/*!*****************************************************************************************************!*\
  !*** external {"root":"KeplerGl","commonjs2":"kepler.gl/reducers","commonjs":"kepler.gl/reducers"} ***!
  \*****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_kepler_gl_reducers__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22KeplerGl%22,%22commonjs2%22:%22kepler.gl/reducers%22,%22commonjs%22:%22kepler.gl/reducers%22%7D?");

/***/ }),

/***/ "kepler.gl/schemas":
/*!***************************************************************************************************!*\
  !*** external {"root":"KeplerGl","commonjs2":"kepler.gl/schemas","commonjs":"kepler.gl/schemas"} ***!
  \***************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_kepler_gl_schemas__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22KeplerGl%22,%22commonjs2%22:%22kepler.gl/schemas%22,%22commonjs%22:%22kepler.gl/schemas%22%7D?");

/***/ }),

/***/ "redux":
/*!************************************************************************!*\
  !*** external {"root":"Redux","commonjs2":"redux","commonjs":"redux"} ***!
  \************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_redux__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22Redux%22,%22commonjs2%22:%22redux%22,%22commonjs%22:%22redux%22%7D?");

/***/ })

/******/ });
});