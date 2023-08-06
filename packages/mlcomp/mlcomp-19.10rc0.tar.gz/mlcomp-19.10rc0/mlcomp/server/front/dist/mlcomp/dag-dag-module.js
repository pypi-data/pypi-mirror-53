(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["dag-dag-module"],{

/***/ "./src/app/dag/dag-routing.module.ts":
/*!*******************************************!*\
  !*** ./src/app/dag/dag-routing.module.ts ***!
  \*******************************************/
/*! exports provided: DagRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DagRoutingModule", function() { return DagRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _dags_dags_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./dags/dags.component */ "./src/app/dag/dags/dags.component.ts");
/* harmony import */ var _dag_dag_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./dag/dag.component */ "./src/app/dag/dag/dag.component.ts");





var routes = [
    {
        path: '',
        component: _dag_dag_component__WEBPACK_IMPORTED_MODULE_4__["DagComponent"],
        children: [
            {
                path: 'dag-detail/:id',
                loadChildren: './dag-detail/dag-detail.module#DagDetailModule'
            },
            { path: '', component: _dags_dags_component__WEBPACK_IMPORTED_MODULE_3__["DagsComponent"] }
        ]
    }
];
var DagRoutingModule = /** @class */ (function () {
    function DagRoutingModule() {
    }
    DagRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)
            ],
            exports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]
            ]
        })
    ], DagRoutingModule);
    return DagRoutingModule;
}());

/*
Copyright Google LLC. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 


/***/ }),

/***/ "./src/app/dag/dag.module.ts":
/*!***********************************!*\
  !*** ./src/app/dag/dag.module.ts ***!
  \***********************************/
/*! exports provided: DagModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DagModule", function() { return DagModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _dag_detail_dag_detail_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./dag-detail/dag-detail.module */ "./src/app/dag/dag-detail/dag-detail.module.ts");
/* harmony import */ var _dag_dag_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./dag/dag.component */ "./src/app/dag/dag/dag.component.ts");
/* harmony import */ var _dag_routing_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./dag-routing.module */ "./src/app/dag/dag-routing.module.ts");
/* harmony import */ var _shared_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../shared.module */ "./src/app/shared.module.ts");






var DagModule = /** @class */ (function () {
    function DagModule() {
    }
    DagModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _dag_routing_module__WEBPACK_IMPORTED_MODULE_4__["DagRoutingModule"],
                _dag_detail_dag_detail_module__WEBPACK_IMPORTED_MODULE_2__["DagDetailModule"],
                _shared_module__WEBPACK_IMPORTED_MODULE_5__["SharedModule"]
            ],
            declarations: [
                _dag_dag_component__WEBPACK_IMPORTED_MODULE_3__["DagComponent"]
            ]
        })
    ], DagModule);
    return DagModule;
}());



/***/ }),

/***/ "./src/app/dag/dag/dag.component.css":
/*!*******************************************!*\
  !*** ./src/app/dag/dag/dag.component.css ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL2RhZy9kYWcvZGFnLmNvbXBvbmVudC5jc3MifQ== */"

/***/ }),

/***/ "./src/app/dag/dag/dag.component.html":
/*!********************************************!*\
  !*** ./src/app/dag/dag/dag.component.html ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<router-outlet></router-outlet>"

/***/ }),

/***/ "./src/app/dag/dag/dag.component.ts":
/*!******************************************!*\
  !*** ./src/app/dag/dag/dag.component.ts ***!
  \******************************************/
/*! exports provided: DagComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DagComponent", function() { return DagComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");


var DagComponent = /** @class */ (function () {
    function DagComponent() {
    }
    DagComponent.prototype.ngOnInit = function () {
    };
    DagComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-dag',
            template: __webpack_require__(/*! ./dag.component.html */ "./src/app/dag/dag/dag.component.html"),
            styles: [__webpack_require__(/*! ./dag.component.css */ "./src/app/dag/dag/dag.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [])
    ], DagComponent);
    return DagComponent;
}());



/***/ })

}]);
//# sourceMappingURL=dag-dag-module.js.map