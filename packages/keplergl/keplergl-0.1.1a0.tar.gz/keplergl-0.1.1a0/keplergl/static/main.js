(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("kepler.gl/actions"), require("kepler.gl/components"), require("kepler.gl/dist/middleware"), require("kepler.gl/processors"), require("kepler.gl/reducers"), require("kepler.gl/schemas"), require("react"), require("react-dom"), require("react-helmet"), require("react-redux"), require("redux"), require("styled-components"));
	else if(typeof define === 'function' && define.amd)
		define([, , , , , , , , , , , ], factory);
	else {
		var a = typeof exports === 'object' ? factory(require("kepler.gl/actions"), require("kepler.gl/components"), require("kepler.gl/dist/middleware"), require("kepler.gl/processors"), require("kepler.gl/reducers"), require("kepler.gl/schemas"), require("react"), require("react-dom"), require("react-helmet"), require("react-redux"), require("redux"), require("styled-components")) : factory(root["KeplerGl"], root["KeplerGl"], root["KeplerGl"], root["KeplerGl"], root["KeplerGl"], root["KeplerGl"], root["React"], root["ReactDOM"], root["Helmet"], root["ReactRedux"], root["Redux"], root["styled"]);
		for(var i in a) (typeof exports === 'object' ? exports : root)[i] = a[i];
	}
})(window, function(__WEBPACK_EXTERNAL_MODULE_kepler_gl_actions__, __WEBPACK_EXTERNAL_MODULE_kepler_gl_components__, __WEBPACK_EXTERNAL_MODULE_kepler_gl_dist_middleware__, __WEBPACK_EXTERNAL_MODULE_kepler_gl_processors__, __WEBPACK_EXTERNAL_MODULE_kepler_gl_reducers__, __WEBPACK_EXTERNAL_MODULE_kepler_gl_schemas__, __WEBPACK_EXTERNAL_MODULE_react__, __WEBPACK_EXTERNAL_MODULE_react_dom__, __WEBPACK_EXTERNAL_MODULE_react_helmet__, __WEBPACK_EXTERNAL_MODULE_react_redux__, __WEBPACK_EXTERNAL_MODULE_redux__, __WEBPACK_EXTERNAL_MODULE_styled_components__) {
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

/***/ "./lib/keplergl/components/app.js":
/*!****************************************!*\
  !*** ./lib/keplergl/components/app.js ***!
  \****************************************/
/*! exports provided: KEPLER_GL_JUPYTER_VERSION, default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"KEPLER_GL_JUPYTER_VERSION\", function() { return KEPLER_GL_JUPYTER_VERSION; });\n/* harmony import */ var _babel_runtime_helpers_objectSpread__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/helpers/objectSpread */ \"./node_modules/@babel/runtime/helpers/objectSpread.js\");\n/* harmony import */ var _babel_runtime_helpers_objectSpread__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_helpers_objectSpread__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _babel_runtime_helpers_slicedToArray__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @babel/runtime/helpers/slicedToArray */ \"./node_modules/@babel/runtime/helpers/slicedToArray.js\");\n/* harmony import */ var _babel_runtime_helpers_slicedToArray__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_helpers_slicedToArray__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var kepler_gl_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! kepler.gl/components */ \"kepler.gl/components\");\n/* harmony import */ var kepler_gl_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_components__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _panel_header__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./panel-header */ \"./lib/keplergl/components/panel-header.js\");\n/* harmony import */ var _side_bar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./side-bar */ \"./lib/keplergl/components/side-bar.js\");\n\n\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n\n\nvar ReactHelmet = __webpack_require__(/*! react-helmet */ \"react-helmet\");\n\nvar Helmet = ReactHelmet ? ReactHelmet.Helmet : null;\n\n\n\nvar KEPLER_GL_JUPYTER_VERSION = \"0.1.0\";\n\nvar CustomAddDataButtonFactory = function CustomAddDataButtonFactory() {\n  var CustomAddDataButton = function CustomAddDataButton() {\n    return react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(\"div\", null);\n  };\n\n  return CustomAddDataButton;\n};\n\nvar KeplerGl = Object(kepler_gl_components__WEBPACK_IMPORTED_MODULE_3__[\"injectComponents\"])([[kepler_gl_components__WEBPACK_IMPORTED_MODULE_3__[\"AddDataButtonFactory\"], CustomAddDataButtonFactory], [kepler_gl_components__WEBPACK_IMPORTED_MODULE_3__[\"SidebarFactory\"], _side_bar__WEBPACK_IMPORTED_MODULE_5__[\"default\"]], [kepler_gl_components__WEBPACK_IMPORTED_MODULE_3__[\"PanelHeaderFactory\"], _panel_header__WEBPACK_IMPORTED_MODULE_4__[\"default\"]]]);\nvar MAPBOX_TOKEN = \"pk.eyJ1IjoidWJlcmRhdGEiLCJhIjoiY2pza3FrOXh6MW05dTQzcWd1M3I3c2E0eCJ9.z0MFFrHYNbdK-QVHKrdepw\"; // eslint-disable-line\n\nfunction App() {\n  var rootElm = Object(react__WEBPACK_IMPORTED_MODULE_2__[\"useRef\"])(null);\n\n  var _useState = Object(react__WEBPACK_IMPORTED_MODULE_2__[\"useState\"])({}),\n      _useState2 = _babel_runtime_helpers_slicedToArray__WEBPACK_IMPORTED_MODULE_1___default()(_useState, 2),\n      windowDimension = _useState2[0],\n      setDimension = _useState2[1];\n\n  var handleResize = function handleResize() {\n    if (!rootElm.current) {\n      return;\n    }\n\n    var width = rootElm.current.offsetWidth;\n    var height = rootElm.current.offsetHeight;\n\n    var dimensionToSet = _babel_runtime_helpers_objectSpread__WEBPACK_IMPORTED_MODULE_0___default()({}, width && width !== windowDimension.width ? {\n      width: width\n    } : {}, height && height !== windowDimension.height ? {\n      height: height\n    } : {});\n\n    setDimension(dimensionToSet);\n  }; // in Jupyter Lab,  parent component has transition when window resize.\n  // need to delay call to get the final parent width,\n\n\n  var resizeDelay = function resizeDelay() {\n    return window.setTimeout(handleResize, 500);\n  };\n\n  Object(react__WEBPACK_IMPORTED_MODULE_2__[\"useEffect\"])(function () {\n    window.addEventListener('resize', resizeDelay);\n    return function () {\n      return window.removeEventListener('resize', resizeDelay);\n    };\n  }, []);\n  return react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(\"div\", {\n    style: {\n      width: '100%',\n      height: \"100%\"\n    },\n    ref: rootElm,\n    className: \"keplergl-widget-container\"\n  }, Helmet ? react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(Helmet, null, react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(\"meta\", {\n    charSet: \"utf-8\"\n  }), react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(\"title\", null, \"Kepler.gl Jupyter\"), react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(\"link\", {\n    rel: \"stylesheet\",\n    href: \"http://d1a3f4spazzrp4.cloudfront.net/kepler.gl/uber-fonts/4.0.0/superfine.css\"\n  }), react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(\"link\", {\n    rel: \"stylesheet\",\n    href: \"http://api.tiles.mapbox.com/mapbox-gl-js/v1.1.1/mapbox-gl.css\"\n  }), react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(\"style\", {\n    type: \"text/css\"\n  }, \"font-family: ff-clan-web-pro, 'Helvetica Neue', Helvetica, sans-serif;\\n                font-weight: 400;\\n                font-size: 0.875em;\\n                line-height: 1.71429;\\n\\n                *,\\n                *:before,\\n                *:after {\\n                  -webkit-box-sizing: border-box;\\n                  -moz-box-sizing: border-box;\\n                  box-sizing: border-box;\\n                }\\n                body {\\n                  margin: 0; padding: 0;\\n                }\\n                .kepler-gl .ReactModal__Overlay.ReactModal__Overlay--after-open {\\n                  position: absolute !important;\\n                }\\n\\n                .jupyter-widgets.keplergl-jupyter-widgets {\\n                  overflow: hidden;\\n                }\\n\\n                .p-Widget.p-Panel.jp-OutputArea-output.jupyter-widgets {\\n                  overflow: hidden\\n                }\\n                \"), react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(\"script\", {\n    async: true,\n    src: \"https://www.googletagmanager.com/gtag/js?id=UA-64694404-19\"\n  }), react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(\"script\", null, \"window.dataLayer=window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'UA-64694404-19', {page_path: '/keplergl-jupyter-widget'});\")) : null, react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement(KeplerGl, {\n    mapboxApiAccessToken: MAPBOX_TOKEN,\n    width: windowDimension.width || 800,\n    height: windowDimension.height || 400,\n    appName: \"Kepler.gl Jupyter\",\n    version: KEPLER_GL_JUPYTER_VERSION,\n    getMapboxRef: handleResize\n  }));\n}\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (App);\n\n//# sourceURL=webpack:///./lib/keplergl/components/app.js?");

/***/ }),

/***/ "./lib/keplergl/components/panel-header.js":
/*!*************************************************!*\
  !*** ./lib/keplergl/components/panel-header.js ***!
  \*************************************************/
/*! exports provided: CustomPanelHeaderFactory, default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"CustomPanelHeaderFactory\", function() { return CustomPanelHeaderFactory; });\n/* harmony import */ var _babel_runtime_helpers_objectSpread__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/helpers/objectSpread */ \"./node_modules/@babel/runtime/helpers/objectSpread.js\");\n/* harmony import */ var _babel_runtime_helpers_objectSpread__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_helpers_objectSpread__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var kepler_gl_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! kepler.gl/components */ \"kepler.gl/components\");\n/* harmony import */ var kepler_gl_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_components__WEBPACK_IMPORTED_MODULE_1__);\n\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n // TODO: Move the doc to public repo\n\nvar KEPLER_DOC = 'https://github.com/keplergl/kepler.gl/blob/master/docs/keplergl-jupyter/user-guide.md';\nfunction CustomPanelHeaderFactory() {\n  var PanelHeader = Object(kepler_gl_components__WEBPACK_IMPORTED_MODULE_1__[\"PanelHeaderFactory\"])();\n  PanelHeader.defaultProps = _babel_runtime_helpers_objectSpread__WEBPACK_IMPORTED_MODULE_0___default()({}, PanelHeader.defaultProps, {\n    actionItems: [{\n      id: 'docs',\n      label: 'Docs',\n      iconComponent: kepler_gl_components__WEBPACK_IMPORTED_MODULE_1__[\"Icons\"].Docs,\n      href: KEPLER_DOC,\n      blank: true,\n      tooltip: 'Documentation',\n      onClick: function onClick() {}\n    }]\n  });\n  return PanelHeader;\n}\n/* harmony default export */ __webpack_exports__[\"default\"] = (CustomPanelHeaderFactory);\n\n//# sourceURL=webpack:///./lib/keplergl/components/panel-header.js?");

/***/ }),

/***/ "./lib/keplergl/components/root.js":
/*!*****************************************!*\
  !*** ./lib/keplergl/components/root.js ***!
  \*****************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-dom */ \"react-dom\");\n/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var react_redux__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-redux */ \"react-redux\");\n/* harmony import */ var react_redux__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_redux__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _app__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app */ \"./lib/keplergl/components/app.js\");\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n\n\n\n\n\nfunction renderRoot(_ref) {\n  var id = _ref.id,\n      store = _ref.store,\n      ele = _ref.ele;\n\n  var Root = function Root() {\n    return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(react_redux__WEBPACK_IMPORTED_MODULE_2__[\"Provider\"], {\n      store: store\n    }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_app__WEBPACK_IMPORTED_MODULE_3__[\"default\"], null));\n  };\n\n  react_dom__WEBPACK_IMPORTED_MODULE_1___default.a.render(react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Root, null), ele);\n}\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (renderRoot);\n\n//# sourceURL=webpack:///./lib/keplergl/components/root.js?");

/***/ }),

/***/ "./lib/keplergl/components/side-bar.js":
/*!*********************************************!*\
  !*** ./lib/keplergl/components/side-bar.js ***!
  \*********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _babel_runtime_helpers_taggedTemplateLiteral__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/helpers/taggedTemplateLiteral */ \"./node_modules/@babel/runtime/helpers/taggedTemplateLiteral.js\");\n/* harmony import */ var _babel_runtime_helpers_taggedTemplateLiteral__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_helpers_taggedTemplateLiteral__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var kepler_gl_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! kepler.gl/components */ \"kepler.gl/components\");\n/* harmony import */ var kepler_gl_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_components__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! styled-components */ \"styled-components\");\n/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(styled_components__WEBPACK_IMPORTED_MODULE_3__);\n\n\nfunction _templateObject() {\n  var data = _babel_runtime_helpers_taggedTemplateLiteral__WEBPACK_IMPORTED_MODULE_0___default()([\"\\n  .side-panel--container {\\n    transform:scale(0.85);\\n    transform-origin: top left;\\n    height: 117.64%;\\n    padding-top: 0;\\n    padding-right: 0;\\n    padding-bottom: 0;\\n    padding-left: 0;\\n\\n    .side-bar {\\n      height: 100%;\\n    }\\n    .side-bar__close {\\n      right: -30px;\\n      top: 14px;\\n    }\\n  }\\n\"]);\n\n  _templateObject = function _templateObject() {\n    return data;\n  };\n\n  return data;\n}\n\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n\n\n\nvar StyledSideBarContainer = styled_components__WEBPACK_IMPORTED_MODULE_3___default.a.div(_templateObject()); // Custom sidebar will render kepler.gl default side bar\n// adding a wrapper component to edit its style\n\nfunction CustomSidebarFactory() {\n  var CloseButton = Object(kepler_gl_components__WEBPACK_IMPORTED_MODULE_2__[\"CollapseButtonFactory\"])();\n  var Sidebar = Object(kepler_gl_components__WEBPACK_IMPORTED_MODULE_2__[\"SidebarFactory\"])(CloseButton);\n\n  var CustomSidebar = function CustomSidebar(props) {\n    return react__WEBPACK_IMPORTED_MODULE_1___default.a.createElement(StyledSideBarContainer, null, react__WEBPACK_IMPORTED_MODULE_1___default.a.createElement(Sidebar, props));\n  };\n\n  return CustomSidebar;\n}\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (CustomSidebarFactory);\n\n//# sourceURL=webpack:///./lib/keplergl/components/side-bar.js?");

/***/ }),

/***/ "./lib/keplergl/kepler.gl.js":
/*!***********************************!*\
  !*** ./lib/keplergl/kepler.gl.js ***!
  \***********************************/
/*! exports provided: addDataConfigToKeplerGl, dataToDatasets, default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"addDataConfigToKeplerGl\", function() { return addDataConfigToKeplerGl; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"dataToDatasets\", function() { return dataToDatasets; });\n/* harmony import */ var _babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/helpers/classCallCheck */ \"./node_modules/@babel/runtime/helpers/classCallCheck.js\");\n/* harmony import */ var _babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @babel/runtime/helpers/createClass */ \"./node_modules/@babel/runtime/helpers/createClass.js\");\n/* harmony import */ var _babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! kepler.gl/actions */ \"kepler.gl/actions\");\n/* harmony import */ var kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var kepler_gl_schemas__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! kepler.gl/schemas */ \"kepler.gl/schemas\");\n/* harmony import */ var kepler_gl_schemas__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_schemas__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var global_document__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! global/document */ \"./node_modules/global/document.js\");\n/* harmony import */ var global_document__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(global_document__WEBPACK_IMPORTED_MODULE_4__);\n/* harmony import */ var _components_root__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/root */ \"./lib/keplergl/components/root.js\");\n/* harmony import */ var _store__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./store */ \"./lib/keplergl/store.js\");\n/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./utils */ \"./lib/keplergl/utils.js\");\n/* harmony import */ var _log__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../log */ \"./lib/log.js\");\n\n\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n\n\n\n\n\n\n\n\nvar getData = function getData(that) {\n  return that.model.get('data');\n};\n\nvar getConfig = function getConfig(that) {\n  return that.model.get('config');\n};\n\nvar getHeight = function getHeight(that) {\n  return that.model.get('height');\n};\n\nvar DOM_EL_ID = 'keplergl';\nvar counter = 0;\nvar NONE_UPDATE_ACTIONS = [kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2__[\"ActionTypes\"].REGISTER_ENTRY, kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2__[\"ActionTypes\"].DELETE_ENTRY, kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2__[\"ActionTypes\"].RENAME_ENTRY, kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2__[\"ActionTypes\"].LOAD_MAP_STYLES, kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2__[\"ActionTypes\"].LAYER_HOVER];\n\nfunction getConfigInStore() {\n  var _ref = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {},\n      _ref$hash = _ref.hash,\n      hash = _ref$hash === void 0 ? true : _ref$hash,\n      store = _ref.store;\n\n  if (store) {\n    var currentState = store.getState().keplerGl.map;\n    var currentValue = kepler_gl_schemas__WEBPACK_IMPORTED_MODULE_3__[\"KeplerGlSchema\"].getConfigToSave(currentState);\n    return hash ? JSON.stringify(currentValue) : currentValue;\n  }\n\n  return {};\n}\n\nfunction getDatasetsInStore(store) {\n  if (store) {\n    return store.getState().keplerGl.map.visState.datasets;\n  }\n}\n\nvar KeplerGlJupyter =\n/*#__PURE__*/\nfunction () {\n  function KeplerGlJupyter() {\n    _babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_0___default()(this, KeplerGlJupyter);\n\n    this.id = \"\".concat(DOM_EL_ID, \"-\").concat(counter);\n    counter++;\n    this.mapUpdateCounter = 0;\n  }\n\n  _babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_1___default()(KeplerGlJupyter, [{\n    key: \"create\",\n    value: function create(that) {\n      Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])('kepler.gl create');\n      var previousValue;\n\n      function handleStoreChange(action, nextStore) {\n        Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])(action);\n\n        if (!action || NONE_UPDATE_ACTIONS.includes(action.type)) {\n          return;\n        }\n\n        var saveState = getConfigInStore({\n          hash: false,\n          store: nextStore\n        });\n        var hash = JSON.stringify(saveState); // should not update model after first UPDATE_MAP action\n        // when component first mounted\n\n        if (previousValue !== hash && this.mapUpdateCounter > 2) {\n          // keplerGl State has changed\n          Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])('store state has changed, update model');\n          Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])(previousValue);\n          Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])(hash);\n          previousValue = hash;\n          that.model.set({\n            config: saveState\n          }); // that.model.save_changes();\n\n          that.touch();\n        }\n\n        if (action.type === kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2__[\"ActionTypes\"].UPDATE_MAP) {\n          this.mapUpdateCounter++;\n        }\n      }\n\n      this.store = Object(_store__WEBPACK_IMPORTED_MODULE_6__[\"default\"])(handleStoreChange.bind(this));\n      var height = getHeight(that);\n      that.el.classList.add('jupyter-widgets');\n      that.el.classList.add('keplergl-jupyter-widgets');\n      var divElmt = global_document__WEBPACK_IMPORTED_MODULE_4___default.a.createElement('div');\n      divElmt.setAttribute('id', this.id);\n      divElmt.classList.add('kepler-gl');\n      divElmt.setAttribute('style', \" width: 100%; height: \".concat(height, \"px;\"));\n      that.el.appendChild(divElmt);\n      Object(_components_root__WEBPACK_IMPORTED_MODULE_5__[\"default\"])({\n        id: this.id,\n        store: this.store,\n        ele: divElmt\n      });\n      var data = getData(that);\n      var config = getConfig(that);\n      Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])('<<<<<<<< render finished! >>>>>>>>>'); // After rendering the component,\n      // we add the data that's already in the model\n\n      var hasData = data && Object.keys(data).length;\n      var hasConfig = config && config.version;\n\n      if (hasData) {\n        Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])('data already in model');\n        addDataConfigToKeplerGl({\n          data: data,\n          config: config,\n          store: this.store\n        });\n      } else if (hasConfig) {\n        Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])('config already in model');\n        this.onConfigChange(that);\n      }\n    }\n  }, {\n    key: \"onDataChange\",\n    value: function onDataChange(that) {\n      Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])('kepler.gl onDataChange');\n      var data = getData(that);\n      addDataConfigToKeplerGl({\n        data: data,\n        store: this.store\n      });\n    }\n  }, {\n    key: \"onConfigChange\",\n    value: function onConfigChange(that) {\n      Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])('kepler.gl onConfigChange');\n      var config = getConfig(that);\n      var currentValue = getConfigInStore({\n        hash: true,\n        store: this.store\n      });\n\n      if (currentValue === JSON.stringify(config)) {\n        // calling model.set('config') inside the js component will trigger another onConfigChange\n        Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])('onConfigChange: config is the same as saved in store');\n        return;\n      }\n\n      this.store.dispatch(Object(kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2__[\"addDataToMap\"])({\n        // reuse datasets in state\n        // a hack to apply config to existing data\n        datasets: Object.values(getDatasetsInStore(this.store)).map(function (d) {\n          return {\n            info: {\n              id: d.id,\n              label: d.label,\n              color: d.color\n            },\n            data: {\n              fields: d.fields,\n              rows: d.allData\n            }\n          };\n        }),\n        config: config,\n        options: {\n          centerMap: false\n        }\n      }));\n    }\n  }]);\n\n  return KeplerGlJupyter;\n}();\n\nfunction addDataConfigToKeplerGl(_ref2) {\n  var inputData = _ref2.data,\n      config = _ref2.config,\n      options = _ref2.options,\n      store = _ref2.store;\n  var data = inputData ? dataToDatasets(inputData) : [];\n  Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])(data);\n  var results = Object(_utils__WEBPACK_IMPORTED_MODULE_7__[\"loadJupyterData\"])(data);\n  var succeeded = results.filter(function (r) {\n    return r && r.data;\n  });\n  Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])('addDataConfigToKeplerGl');\n  Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])(succeeded);\n  Object(_log__WEBPACK_IMPORTED_MODULE_8__[\"default\"])(config);\n  store.dispatch(Object(kepler_gl_actions__WEBPACK_IMPORTED_MODULE_2__[\"addDataToMap\"])({\n    datasets: succeeded,\n    config: config,\n    options: options || {\n      centerMap: true\n    }\n  }));\n}\nfunction dataToDatasets(data) {\n  return Object.keys(data).map(function (key) {\n    return {\n      id: key,\n      data: data[key]\n    };\n  });\n}\n/* harmony default export */ __webpack_exports__[\"default\"] = (KeplerGlJupyter);\n\n//# sourceURL=webpack:///./lib/keplergl/kepler.gl.js?");

/***/ }),

/***/ "./lib/keplergl/main.js":
/*!******************************!*\
  !*** ./lib/keplergl/main.js ***!
  \******************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _store__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./store */ \"./lib/keplergl/store.js\");\n/* harmony import */ var _components_root__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/root */ \"./lib/keplergl/components/root.js\");\n/* harmony import */ var global_document__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! global/document */ \"./node_modules/global/document.js\");\n/* harmony import */ var global_document__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(global_document__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var global_window__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! global/window */ \"./node_modules/global/window.js\");\n/* harmony import */ var global_window__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(global_window__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _kepler_gl__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./kepler.gl */ \"./lib/keplergl/kepler.gl.js\");\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n// NOTE: this is only used for exporting html template\n\n\n\n\n\n\nvar map = function initKeplerGl() {\n  var id = 'keplergl-0';\n  var store = Object(_store__WEBPACK_IMPORTED_MODULE_0__[\"default\"])();\n  var divElmt = global_document__WEBPACK_IMPORTED_MODULE_2___default.a.createElement('div');\n  divElmt.setAttribute('style', 'width: 100vw; height: 100vh; position: absolute');\n  global_document__WEBPACK_IMPORTED_MODULE_2___default.a.body.appendChild(divElmt);\n  return {\n    render: function render() {\n      Object(_components_root__WEBPACK_IMPORTED_MODULE_1__[\"default\"])({\n        id: id,\n        store: store,\n        ele: divElmt\n      });\n    },\n    store: store\n  };\n}();\n\nmap.render();\n\n(function loadDataConfig(keplerGlMap) {\n  var _ref = global_window__WEBPACK_IMPORTED_MODULE_3___default.a.__keplerglDataConfig || {},\n      data = _ref.data,\n      config = _ref.config,\n      options = _ref.options;\n\n  Object(_kepler_gl__WEBPACK_IMPORTED_MODULE_4__[\"addDataConfigToKeplerGl\"])({\n    data: data,\n    config: config,\n    options: options,\n    store: keplerGlMap.store\n  });\n})(map);\n\n//# sourceURL=webpack:///./lib/keplergl/main.js?");

/***/ }),

/***/ "./lib/keplergl/store.js":
/*!*******************************!*\
  !*** ./lib/keplergl/store.js ***!
  \*******************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/helpers/toConsumableArray */ \"./node_modules/@babel/runtime/helpers/toConsumableArray.js\");\n/* harmony import */ var _babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var redux__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! redux */ \"redux\");\n/* harmony import */ var redux__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(redux__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var kepler_gl_reducers__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! kepler.gl/reducers */ \"kepler.gl/reducers\");\n/* harmony import */ var kepler_gl_reducers__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_reducers__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var kepler_gl_dist_middleware__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! kepler.gl/dist/middleware */ \"kepler.gl/dist/middleware\");\n/* harmony import */ var kepler_gl_dist_middleware__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_dist_middleware__WEBPACK_IMPORTED_MODULE_3__);\n\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n\n\n // TODO: remove this after added middleware to files\n\n\nvar customizedKeplerGlReducer = kepler_gl_reducers__WEBPACK_IMPORTED_MODULE_2__[\"keplerGlReducer\"].initialState({\n  uiState: {\n    currentModal: null,\n    activeSidePanel: null\n  }\n});\nvar reducers = Object(redux__WEBPACK_IMPORTED_MODULE_1__[\"combineReducers\"])({\n  // mount keplerGl reducer\n  keplerGl: customizedKeplerGlReducer\n});\n\nvar createAppStore = function createAppStore(onChangeHandler) {\n  var updatesMiddleware = function updatesMiddleware(store) {\n    return function (next) {\n      return function (action) {\n        // exclude some actions\n        // Call the next dispatch method in the middleware chain.\n\n        /* eslint-disable callback-return */\n        var returnValue = next(action);\n        /* eslint-enable callback-return */\n        // state after dispatch\n\n        if (typeof onChangeHandler === 'function') {\n          onChangeHandler(action, store);\n        } // This will likely be the action itself, unless\n        // a middleware further in chain changed it.\n\n\n        return returnValue;\n      };\n    };\n  };\n\n  var middlewares = Object(kepler_gl_dist_middleware__WEBPACK_IMPORTED_MODULE_3__[\"enhanceReduxMiddleware\"])([updatesMiddleware]);\n  var enhancers = [redux__WEBPACK_IMPORTED_MODULE_1__[\"applyMiddleware\"].apply(void 0, _babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_0___default()(middlewares))];\n  var store = Object(redux__WEBPACK_IMPORTED_MODULE_1__[\"createStore\"])(reducers, {}, redux__WEBPACK_IMPORTED_MODULE_1__[\"compose\"].apply(void 0, enhancers));\n  return store;\n};\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (createAppStore);\n\n//# sourceURL=webpack:///./lib/keplergl/store.js?");

/***/ }),

/***/ "./lib/keplergl/utils.js":
/*!*******************************!*\
  !*** ./lib/keplergl/utils.js ***!
  \*******************************/
/*! exports provided: loadJupyterData */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"loadJupyterData\", function() { return loadJupyterData; });\n/* harmony import */ var _babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/helpers/typeof */ \"./node_modules/@babel/runtime/helpers/typeof.js\");\n/* harmony import */ var _babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var kepler_gl_processors__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! kepler.gl/processors */ \"kepler.gl/processors\");\n/* harmony import */ var kepler_gl_processors__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(kepler_gl_processors__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _log__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../log */ \"./lib/log.js\");\n/* harmony import */ var global_console__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! global/console */ \"./node_modules/global/console.js\");\n/* harmony import */ var global_console__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(global_console__WEBPACK_IMPORTED_MODULE_3__);\n\n// Copyright (c) 2019 Uber Technologies, Inc.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a copy\n// of this software and associated documentation files (the \"Software\"), to deal\n// in the Software without restriction, including without limitation the rights\n// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n// copies of the Software, and to permit persons to whom the Software is\n// furnished to do so, subject to the following conditions:\n//\n// The above copyright notice and this permission notice shall be included in\n// all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n// THE SOFTWARE.\n\n\n\n\nfunction handleJuptyerDataFormat(dataEntry) {\n  // This makes passing data between Jupyter the iframe easier\n  // detect data type here\n  Object(_log__WEBPACK_IMPORTED_MODULE_2__[\"default\"])('handleJuptyerDataFormat');\n  var data = dataEntry.data,\n      id = dataEntry.id;\n  var parsed = data;\n  var type = 'csv';\n\n  if (_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_0___default()(data) === 'object') {\n    if (data.columns && data.data && data.index) {\n      // Data is parsed as a Dataframe\n      Object(_log__WEBPACK_IMPORTED_MODULE_2__[\"default\"])('data is a dataframe');\n      type = 'df'; // parsed = {fields: data.columns, data: data.data};\n    } else {\n      // assume is geojson\n      type = 'json';\n    }\n  } else if (typeof data === 'string') {\n    try {\n      parsed = JSON.parse(data);\n      type = 'json';\n    } catch (e) {// assume it is csv\n    }\n  }\n\n  return {\n    data: parsed,\n    type: type,\n    id: id\n  };\n}\n\nfunction processReceivedData(_ref) {\n  var data = _ref.data,\n      info = _ref.info;\n  // assume there is only 1 file\n  Object(_log__WEBPACK_IMPORTED_MODULE_2__[\"default\"])('processReceivedData');\n  var processed;\n\n  try {\n    processed = info.queryType === 'csv' ? Object(kepler_gl_processors__WEBPACK_IMPORTED_MODULE_1__[\"processCsvData\"])(data) : info.queryType === 'json' ? Object(kepler_gl_processors__WEBPACK_IMPORTED_MODULE_1__[\"processGeojson\"])(data) : info.queryType === 'df' ? processDataFrame(data) : null;\n  } catch (e) {\n    global_console__WEBPACK_IMPORTED_MODULE_3___default.a.log(\"Kepler.gl fails to parse data, detected data\\n    format is \".concat(info.queryType), e);\n  }\n\n  return {\n    data: processed,\n    info: info\n  };\n}\n\nfunction processDataFrame(data) {\n  var fields = data.columns.map(function (name) {\n    return {\n      name: name\n    };\n  });\n  var rows = data.data; // kepler.gl will detect field types\n\n  return {\n    fields: fields,\n    rows: rows\n  };\n}\n\nfunction loadJupyterData(rawData) {\n  var dataToLoad = rawData.map(handleJuptyerDataFormat).map(function (rd) {\n    return {\n      data: rd.data,\n      info: {\n        id: rd.id,\n        label: rd.id,\n        queryType: rd.type,\n        queryOption: 'jupyter'\n      }\n    };\n  });\n  return dataToLoad.map(processReceivedData);\n}\n\n//# sourceURL=webpack:///./lib/keplergl/utils.js?");

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

/***/ "./node_modules/@babel/runtime/helpers/arrayWithHoles.js":
/*!***************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/arrayWithHoles.js ***!
  \***************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _arrayWithHoles(arr) {\n  if (Array.isArray(arr)) return arr;\n}\n\nmodule.exports = _arrayWithHoles;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/arrayWithHoles.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/arrayWithoutHoles.js":
/*!******************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/arrayWithoutHoles.js ***!
  \******************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _arrayWithoutHoles(arr) {\n  if (Array.isArray(arr)) {\n    for (var i = 0, arr2 = new Array(arr.length); i < arr.length; i++) {\n      arr2[i] = arr[i];\n    }\n\n    return arr2;\n  }\n}\n\nmodule.exports = _arrayWithoutHoles;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/arrayWithoutHoles.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/classCallCheck.js":
/*!***************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/classCallCheck.js ***!
  \***************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _classCallCheck(instance, Constructor) {\n  if (!(instance instanceof Constructor)) {\n    throw new TypeError(\"Cannot call a class as a function\");\n  }\n}\n\nmodule.exports = _classCallCheck;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/classCallCheck.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/createClass.js":
/*!************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/createClass.js ***!
  \************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _defineProperties(target, props) {\n  for (var i = 0; i < props.length; i++) {\n    var descriptor = props[i];\n    descriptor.enumerable = descriptor.enumerable || false;\n    descriptor.configurable = true;\n    if (\"value\" in descriptor) descriptor.writable = true;\n    Object.defineProperty(target, descriptor.key, descriptor);\n  }\n}\n\nfunction _createClass(Constructor, protoProps, staticProps) {\n  if (protoProps) _defineProperties(Constructor.prototype, protoProps);\n  if (staticProps) _defineProperties(Constructor, staticProps);\n  return Constructor;\n}\n\nmodule.exports = _createClass;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/createClass.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/defineProperty.js":
/*!***************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/defineProperty.js ***!
  \***************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _defineProperty(obj, key, value) {\n  if (key in obj) {\n    Object.defineProperty(obj, key, {\n      value: value,\n      enumerable: true,\n      configurable: true,\n      writable: true\n    });\n  } else {\n    obj[key] = value;\n  }\n\n  return obj;\n}\n\nmodule.exports = _defineProperty;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/defineProperty.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/iterableToArray.js":
/*!****************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/iterableToArray.js ***!
  \****************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _iterableToArray(iter) {\n  if (Symbol.iterator in Object(iter) || Object.prototype.toString.call(iter) === \"[object Arguments]\") return Array.from(iter);\n}\n\nmodule.exports = _iterableToArray;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/iterableToArray.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/iterableToArrayLimit.js":
/*!*********************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/iterableToArrayLimit.js ***!
  \*********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _iterableToArrayLimit(arr, i) {\n  var _arr = [];\n  var _n = true;\n  var _d = false;\n  var _e = undefined;\n\n  try {\n    for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) {\n      _arr.push(_s.value);\n\n      if (i && _arr.length === i) break;\n    }\n  } catch (err) {\n    _d = true;\n    _e = err;\n  } finally {\n    try {\n      if (!_n && _i[\"return\"] != null) _i[\"return\"]();\n    } finally {\n      if (_d) throw _e;\n    }\n  }\n\n  return _arr;\n}\n\nmodule.exports = _iterableToArrayLimit;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/iterableToArrayLimit.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/nonIterableRest.js":
/*!****************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/nonIterableRest.js ***!
  \****************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _nonIterableRest() {\n  throw new TypeError(\"Invalid attempt to destructure non-iterable instance\");\n}\n\nmodule.exports = _nonIterableRest;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/nonIterableRest.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/nonIterableSpread.js":
/*!******************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/nonIterableSpread.js ***!
  \******************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _nonIterableSpread() {\n  throw new TypeError(\"Invalid attempt to spread non-iterable instance\");\n}\n\nmodule.exports = _nonIterableSpread;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/nonIterableSpread.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/objectSpread.js":
/*!*************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/objectSpread.js ***!
  \*************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("var defineProperty = __webpack_require__(/*! ./defineProperty */ \"./node_modules/@babel/runtime/helpers/defineProperty.js\");\n\nfunction _objectSpread(target) {\n  for (var i = 1; i < arguments.length; i++) {\n    var source = arguments[i] != null ? arguments[i] : {};\n    var ownKeys = Object.keys(source);\n\n    if (typeof Object.getOwnPropertySymbols === 'function') {\n      ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) {\n        return Object.getOwnPropertyDescriptor(source, sym).enumerable;\n      }));\n    }\n\n    ownKeys.forEach(function (key) {\n      defineProperty(target, key, source[key]);\n    });\n  }\n\n  return target;\n}\n\nmodule.exports = _objectSpread;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/objectSpread.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/slicedToArray.js":
/*!**************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/slicedToArray.js ***!
  \**************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("var arrayWithHoles = __webpack_require__(/*! ./arrayWithHoles */ \"./node_modules/@babel/runtime/helpers/arrayWithHoles.js\");\n\nvar iterableToArrayLimit = __webpack_require__(/*! ./iterableToArrayLimit */ \"./node_modules/@babel/runtime/helpers/iterableToArrayLimit.js\");\n\nvar nonIterableRest = __webpack_require__(/*! ./nonIterableRest */ \"./node_modules/@babel/runtime/helpers/nonIterableRest.js\");\n\nfunction _slicedToArray(arr, i) {\n  return arrayWithHoles(arr) || iterableToArrayLimit(arr, i) || nonIterableRest();\n}\n\nmodule.exports = _slicedToArray;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/slicedToArray.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/taggedTemplateLiteral.js":
/*!**********************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/taggedTemplateLiteral.js ***!
  \**********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _taggedTemplateLiteral(strings, raw) {\n  if (!raw) {\n    raw = strings.slice(0);\n  }\n\n  return Object.freeze(Object.defineProperties(strings, {\n    raw: {\n      value: Object.freeze(raw)\n    }\n  }));\n}\n\nmodule.exports = _taggedTemplateLiteral;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/taggedTemplateLiteral.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/toConsumableArray.js":
/*!******************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/toConsumableArray.js ***!
  \******************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("var arrayWithoutHoles = __webpack_require__(/*! ./arrayWithoutHoles */ \"./node_modules/@babel/runtime/helpers/arrayWithoutHoles.js\");\n\nvar iterableToArray = __webpack_require__(/*! ./iterableToArray */ \"./node_modules/@babel/runtime/helpers/iterableToArray.js\");\n\nvar nonIterableSpread = __webpack_require__(/*! ./nonIterableSpread */ \"./node_modules/@babel/runtime/helpers/nonIterableSpread.js\");\n\nfunction _toConsumableArray(arr) {\n  return arrayWithoutHoles(arr) || iterableToArray(arr) || nonIterableSpread();\n}\n\nmodule.exports = _toConsumableArray;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/toConsumableArray.js?");

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/typeof.js":
/*!*******************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/typeof.js ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function _typeof2(obj) { if (typeof Symbol === \"function\" && typeof Symbol.iterator === \"symbol\") { _typeof2 = function _typeof2(obj) { return typeof obj; }; } else { _typeof2 = function _typeof2(obj) { return obj && typeof Symbol === \"function\" && obj.constructor === Symbol && obj !== Symbol.prototype ? \"symbol\" : typeof obj; }; } return _typeof2(obj); }\n\nfunction _typeof(obj) {\n  if (typeof Symbol === \"function\" && _typeof2(Symbol.iterator) === \"symbol\") {\n    module.exports = _typeof = function _typeof(obj) {\n      return _typeof2(obj);\n    };\n  } else {\n    module.exports = _typeof = function _typeof(obj) {\n      return obj && typeof Symbol === \"function\" && obj.constructor === Symbol && obj !== Symbol.prototype ? \"symbol\" : _typeof2(obj);\n    };\n  }\n\n  return _typeof(obj);\n}\n\nmodule.exports = _typeof;\n\n//# sourceURL=webpack:///./node_modules/@babel/runtime/helpers/typeof.js?");

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

/***/ "kepler.gl/components":
/*!*********************************************************************************************************!*\
  !*** external {"root":"KeplerGl","commonjs2":"kepler.gl/components","commonjs":"kepler.gl/components"} ***!
  \*********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_kepler_gl_components__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22KeplerGl%22,%22commonjs2%22:%22kepler.gl/components%22,%22commonjs%22:%22kepler.gl/components%22%7D?");

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

/***/ "react":
/*!************************************************************************!*\
  !*** external {"root":"React","commonjs2":"react","commonjs":"react"} ***!
  \************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_react__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22React%22,%22commonjs2%22:%22react%22,%22commonjs%22:%22react%22%7D?");

/***/ }),

/***/ "react-dom":
/*!***********************************************************************************!*\
  !*** external {"root":"ReactDOM","commonjs2":"react-dom","commonjs":"react-dom"} ***!
  \***********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_react_dom__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22ReactDOM%22,%22commonjs2%22:%22react-dom%22,%22commonjs%22:%22react-dom%22%7D?");

/***/ }),

/***/ "react-helmet":
/*!***************************************************************************************!*\
  !*** external {"root":"Helmet","commonjs2":"react-helmet","commonjs":"react-helmet"} ***!
  \***************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_react_helmet__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22Helmet%22,%22commonjs2%22:%22react-helmet%22,%22commonjs%22:%22react-helmet%22%7D?");

/***/ }),

/***/ "react-redux":
/*!*****************************************************************************************!*\
  !*** external {"root":"ReactRedux","commonjs2":"react-redux","commonjs":"react-redux"} ***!
  \*****************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_react_redux__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22ReactRedux%22,%22commonjs2%22:%22react-redux%22,%22commonjs%22:%22react-redux%22%7D?");

/***/ }),

/***/ "redux":
/*!************************************************************************!*\
  !*** external {"root":"Redux","commonjs2":"redux","commonjs":"redux"} ***!
  \************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_redux__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22Redux%22,%22commonjs2%22:%22redux%22,%22commonjs%22:%22redux%22%7D?");

/***/ }),

/***/ "styled-components":
/*!*************************************************************************************************!*\
  !*** external {"root":"styled","commonjs2":"styled-components","commonjs":"styled-components"} ***!
  \*************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE_styled_components__;\n\n//# sourceURL=webpack:///external_%7B%22root%22:%22styled%22,%22commonjs2%22:%22styled-components%22,%22commonjs%22:%22styled-components%22%7D?");

/***/ })

/******/ });
});