(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~dag-dag-module~dag-detail-dag-detail-module"],{

/***/ "./src/app/dag/dag-detail/code/code.component.css":
/*!********************************************************!*\
  !*** ./src/app/dag/dag-detail/code/code.component.css ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".mat-tree-node { min-height: 20px }\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvZGFnL2RhZy1kZXRhaWwvY29kZS9jb2RlLmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUEsaUJBQWlCLGlCQUFpQiIsImZpbGUiOiJzcmMvYXBwL2RhZy9kYWctZGV0YWlsL2NvZGUvY29kZS5jb21wb25lbnQuY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLm1hdC10cmVlLW5vZGUgeyBtaW4taGVpZ2h0OiAyMHB4IH0iXX0= */"

/***/ }),

/***/ "./src/app/dag/dag-detail/code/code.component.html":
/*!*********************************************************!*\
  !*** ./src/app/dag/dag-detail/code/code.component.html ***!
  \*********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<link\n        href=\"https://fonts.googleapis.com/icon?family=Material+Icons\"\n        rel=\"stylesheet\">\n\n<table style=\"width: 70%;\">\n  <td class=\"mat-app-background basic-container\" style=\"width: 30%\">\n\n    <button mat-raised-button\n            style=\"margin-top: 15px;margin-bottom: 10px\"\n            (click)=\"download()\">\n        Download\n    </button>\n\n    <mat-tree [dataSource]=\"dataSource\" [treeControl]=\"treeControl\">\n      <!-- This is the tree node template for leaf nodes -->\n      <mat-tree-node *matTreeNodeDef=\"let node\" matTreeNodePadding>\n        <!-- use a disabled button to provide padding for tree leaf -->\n\n        <button mat-icon-button\n                mat-button\n                class=\"mat-icon-button\"\n                (click)=\"node_click(node)\">\n\n        </button>\n\n        {{node.name}}\n\n      </mat-tree-node>\n\n      <mat-tree-node\n              *matTreeNodeDef=\"let node;when: hasChild\"\n              matTreeNodePadding>\n        <button mat-icon-button matTreeNodeToggle\n                [attr.aria-label]=\"'toggle ' + node.name\"\n                class=\"mat-icon-button\">\n\n          <mat-icon class=\"mat-icon-rtl-mirror\">\n            {{treeControl.isExpanded(node) ? 'expand_more' : 'chevron_right'}}\n          </mat-icon>\n\n        </button>\n\n        {{node.name}}\n\n       </mat-tree-node>\n\n      </mat-tree>\n\n  </td>\n\n  <td style=\"width: 70%\">\n\n    <div id=\"codeholder\">\n\n    </div>\n\n  </td>\n</table>\n"

/***/ }),

/***/ "./src/app/dag/dag-detail/code/code.component.ts":
/*!*******************************************************!*\
  !*** ./src/app/dag/dag-detail/code/code.component.ts ***!
  \*******************************************************/
/*! exports provided: CodeComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CodeComponent", function() { return CodeComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_cdk_tree__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/cdk/tree */ "./node_modules/@angular/cdk/esm5/tree.es5.js");
/* harmony import */ var _angular_material_tree__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/tree */ "./node_modules/@angular/material/esm5/tree.es5.js");
/* harmony import */ var _dag_detail_dag_detail_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../dag-detail/dag-detail.service */ "./src/app/dag/dag-detail/dag-detail/dag-detail.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _message_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../message.service */ "./src/app/message.service.ts");
/* harmony import */ var _dynamicresource_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../dynamicresource.service */ "./src/app/dynamicresource.service.ts");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm5/platform-browser.js");









var CodeComponent = /** @class */ (function () {
    function CodeComponent(service, route, message_service, resource_service, sanitizer) {
        this.service = service;
        this.route = route;
        this.message_service = message_service;
        this.resource_service = resource_service;
        this.sanitizer = sanitizer;
        this.transformer = function (node, level) {
            return {
                expandable: !!node.children && node.children.length > 0,
                name: node.name,
                level: level,
                content: node.content,
            };
        };
        this.treeControl = new _angular_cdk_tree__WEBPACK_IMPORTED_MODULE_2__["FlatTreeControl"](function (node) { return node.level; }, function (node) { return node.expandable; });
        this.treeFlattener = new _angular_material_tree__WEBPACK_IMPORTED_MODULE_3__["MatTreeFlattener"](this.transformer, function (node) { return node.level; }, function (node) { return node.expandable; }, function (node) { return node.children; });
        this.dataSource = new _angular_material_tree__WEBPACK_IMPORTED_MODULE_3__["MatTreeFlatDataSource"](this.treeControl, this.treeFlattener);
        this.hasChild = function (_, node) { return node.expandable; };
    }
    CodeComponent.prototype.ngAfterViewInit = function () {
        var self = this;
        this.service.get_code(this.dag).subscribe(function (res) {
            self.dataSource.data = res.items;
        });
        this.resource_service.load('prettify', 'prettify-yaml', 'prettify-css');
    };
    CodeComponent.prototype.prettify_lang = function (ext) {
        switch (ext) {
            case 'py':
                return 'lang-py';
            case 'yaml':
            case 'yml':
                return 'lang-yaml';
            case 'json':
                return 'lang-json';
            default:
                return '';
        }
    };
    CodeComponent.prototype.node_click = function (node) {
        var pre = document.createElement('pre');
        pre.textContent = node.content;
        var ext = node.name.indexOf('.') != -1 ?
            node.name.split('.')[1].toLowerCase() : '';
        pre.className = "prettyprint linenums " + this.prettify_lang(ext);
        var code_holder = document.getElementById('codeholder');
        code_holder.innerHTML = '';
        code_holder.appendChild(pre);
        window['PR'].prettyPrint();
    };
    CodeComponent.prototype.download = function () {
        var _this = this;
        this.service.code_download(this.dag).subscribe(function (x) {
            var url = window.URL.createObjectURL(x);
            var link = document.createElement('a');
            link.setAttribute('download', String(_this.dag));
            link.setAttribute('href', url);
            document.body.append(link);
            link.click();
            document.body.removeChild(link);
        });
    };
    CodeComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-code',
            template: __webpack_require__(/*! ./code.component.html */ "./src/app/dag/dag-detail/code/code.component.html"),
            styles: [__webpack_require__(/*! ./code.component.css */ "./src/app/dag/dag-detail/code/code.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_dag_detail_dag_detail_service__WEBPACK_IMPORTED_MODULE_4__["DagDetailService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_5__["ActivatedRoute"],
            _message_service__WEBPACK_IMPORTED_MODULE_6__["MessageService"],
            _dynamicresource_service__WEBPACK_IMPORTED_MODULE_7__["DynamicresourceService"],
            _angular_platform_browser__WEBPACK_IMPORTED_MODULE_8__["DomSanitizer"]])
    ], CodeComponent);
    return CodeComponent;
}());



/***/ }),

/***/ "./src/app/dag/dag-detail/config/config.component.css":
/*!************************************************************!*\
  !*** ./src/app/dag/dag-detail/config/config.component.css ***!
  \************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL2RhZy9kYWctZGV0YWlsL2NvbmZpZy9jb25maWcuY29tcG9uZW50LmNzcyJ9 */"

/***/ }),

/***/ "./src/app/dag/dag-detail/config/config.component.html":
/*!*************************************************************!*\
  !*** ./src/app/dag/dag-detail/config/config.component.html ***!
  \*************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div id=\"codeholder\">\n\n</div>\n"

/***/ }),

/***/ "./src/app/dag/dag-detail/config/config.component.ts":
/*!***********************************************************!*\
  !*** ./src/app/dag/dag-detail/config/config.component.ts ***!
  \***********************************************************/
/*! exports provided: ConfigComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigComponent", function() { return ConfigComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _message_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../message.service */ "./src/app/message.service.ts");
/* harmony import */ var _dag_detail_dag_detail_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../dag-detail/dag-detail.service */ "./src/app/dag/dag-detail/dag-detail/dag-detail.service.ts");
/* harmony import */ var _dynamicresource_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../dynamicresource.service */ "./src/app/dynamicresource.service.ts");





var ConfigComponent = /** @class */ (function () {
    function ConfigComponent(message_service, service, resource_service) {
        this.message_service = message_service;
        this.service = service;
        this.resource_service = resource_service;
    }
    ConfigComponent.prototype.ngAfterViewInit = function () {
        var self = this;
        this.resource_service.load('prettify', 'prettify-yaml', 'prettify-css').then(function () {
            self.service.get_config(self.dag).subscribe(function (res) {
                var node = document.createElement('pre');
                node.textContent = res.data;
                node.className = "prettyprint linenums lang-yaml";
                var codeholder = document.getElementById('codeholder');
                codeholder.appendChild(node);
                window['PR'].prettyPrint();
            });
        });
    };
    ConfigComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-config',
            template: __webpack_require__(/*! ./config.component.html */ "./src/app/dag/dag-detail/config/config.component.html"),
            styles: [__webpack_require__(/*! ./config.component.css */ "./src/app/dag/dag-detail/config/config.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_message_service__WEBPACK_IMPORTED_MODULE_2__["MessageService"],
            _dag_detail_dag_detail_service__WEBPACK_IMPORTED_MODULE_3__["DagDetailService"],
            _dynamicresource_service__WEBPACK_IMPORTED_MODULE_4__["DynamicresourceService"]])
    ], ConfigComponent);
    return ConfigComponent;
}());



/***/ }),

/***/ "./src/app/dag/dag-detail/dag-detail-routing.module.ts":
/*!*************************************************************!*\
  !*** ./src/app/dag/dag-detail/dag-detail-routing.module.ts ***!
  \*************************************************************/
/*! exports provided: DagDetailRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DagDetailRoutingModule", function() { return DagDetailRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _code_code_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./code/code.component */ "./src/app/dag/dag-detail/code/code.component.ts");
/* harmony import */ var _config_config_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./config/config.component */ "./src/app/dag/dag-detail/config/config.component.ts");
/* harmony import */ var _graph_graph_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./graph/graph.component */ "./src/app/dag/dag-detail/graph/graph.component.ts");
/* harmony import */ var _dag_detail_dag_detail_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./dag-detail/dag-detail.component */ "./src/app/dag/dag-detail/dag-detail/dag-detail.component.ts");
/* harmony import */ var _task_tasks_tasks_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../task/tasks/tasks.component */ "./src/app/task/tasks/tasks.component.ts");








var routes = [
    {
        path: '',
        component: _dag_detail_dag_detail_component__WEBPACK_IMPORTED_MODULE_6__["DagDetailComponent"],
        children: [
            { path: 'code', component: _code_code_component__WEBPACK_IMPORTED_MODULE_3__["CodeComponent"] },
            { path: 'config', component: _config_config_component__WEBPACK_IMPORTED_MODULE_4__["ConfigComponent"] },
            { path: 'graph', component: _graph_graph_component__WEBPACK_IMPORTED_MODULE_5__["GraphComponent"] },
            { path: 'tasks', component: _task_tasks_tasks_component__WEBPACK_IMPORTED_MODULE_7__["TasksComponent"] }
        ]
    }
];
var DagDetailRoutingModule = /** @class */ (function () {
    function DagDetailRoutingModule() {
    }
    DagDetailRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)
            ],
            exports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]
            ]
        })
    ], DagDetailRoutingModule);
    return DagDetailRoutingModule;
}());



/***/ }),

/***/ "./src/app/dag/dag-detail/dag-detail.module.ts":
/*!*****************************************************!*\
  !*** ./src/app/dag/dag-detail/dag-detail.module.ts ***!
  \*****************************************************/
/*! exports provided: DagDetailModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DagDetailModule", function() { return DagDetailModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _code_code_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./code/code.component */ "./src/app/dag/dag-detail/code/code.component.ts");
/* harmony import */ var _config_config_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./config/config.component */ "./src/app/dag/dag-detail/config/config.component.ts");
/* harmony import */ var _graph_graph_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./graph/graph.component */ "./src/app/dag/dag-detail/graph/graph.component.ts");
/* harmony import */ var _dag_detail_routing_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./dag-detail-routing.module */ "./src/app/dag/dag-detail/dag-detail-routing.module.ts");
/* harmony import */ var _dag_detail_dag_detail_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./dag-detail/dag-detail.component */ "./src/app/dag/dag-detail/dag-detail/dag-detail.component.ts");
/* harmony import */ var _shared_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../shared.module */ "./src/app/shared.module.ts");








var DagDetailModule = /** @class */ (function () {
    function DagDetailModule() {
    }
    DagDetailModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _dag_detail_routing_module__WEBPACK_IMPORTED_MODULE_5__["DagDetailRoutingModule"],
                _shared_module__WEBPACK_IMPORTED_MODULE_7__["SharedModule"]
            ],
            declarations: [
                _code_code_component__WEBPACK_IMPORTED_MODULE_2__["CodeComponent"],
                _config_config_component__WEBPACK_IMPORTED_MODULE_3__["ConfigComponent"],
                _graph_graph_component__WEBPACK_IMPORTED_MODULE_4__["GraphComponent"],
                _dag_detail_dag_detail_component__WEBPACK_IMPORTED_MODULE_6__["DagDetailComponent"]
            ]
        })
    ], DagDetailModule);
    return DagDetailModule;
}());



/***/ }),

/***/ "./src/app/dag/dag-detail/dag-detail/dag-detail.component.html":
/*!*********************************************************************!*\
  !*** ./src/app/dag/dag-detail/dag-detail/dag-detail.component.html ***!
  \*********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"mat-elevation-z8\">\n    <table mat-table [dataSource]=\"dataSource\" matSort>\n\n        <ng-container matColumnDef=\"project\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Project\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.name}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"id\">\n            <th\n                    mat-header-cell\n                    *matHeaderCellDef\n                    style=\"width: 18px\"\n                    mat-sort-header>\n                Id\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\" style=\"width: 18px\">\n                {{element.id}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"name\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Name</th>\n            <td mat-cell *matCellDef=\"let element\">\n                <a\n                        class=\"col-1-4\"\n                        routerLink=\"/dags/dag-detail/{{element.id}}/tasks\">\n                    {{element.name}}\n                </a>\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"task_count\">\n            <th\n                    mat-header-cell\n                    *matHeaderCellDef\n                    mat-sort-header\n                    style=\"width: 18px\">\n                Tasks\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\" style=\"width: 18px\">\n                {{element.task_count}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"created\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Created\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.created| date:\"MM.dd H:mm:ss\"}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"started\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Started\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.started| date:\"MM.dd H:mm:ss\"}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"last_activity\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Last activity\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.last_activity| date:\"MM.dd H:mm:ss\"}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"duration\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Duration\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.duration}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"img_size\">\n            <th mat-header-cell *matHeaderCellDef>\n                Image size\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\" style=\"min-width: 120px\">\n                <mat-icon\n                        svgIcon=\"remove\"\n                        matTooltip=\"Remove\"\n                        (click)=\"remove_imgs(element)\">\n                </mat-icon>\n\n                {{size(element.img_size)}}\n\n\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"file_size\">\n            <th mat-header-cell *matHeaderCellDef>\n                File size\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\" style=\"min-width: 120px\">\n                <mat-icon\n                        svgIcon=\"remove\"\n                        matTooltip=\"Remove\"\n                        (click)=\"remove_files(element)\"\n                        [class.transparent]=\"has_unfinished(element)\">\n                </mat-icon>\n\n                {{size(element.file_size)}}\n\n\n            </td>\n        </ng-container>\n\n\n        <ng-container matColumnDef=\"task_status\">\n            <th mat-header-cell *matHeaderCellDef style=\"text-align: center\">\n                Task status\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                <svg height=\"40\" width=\"220px\" style=\"display: block;\">\n                    <g matTooltip=\"{{status.name}}\"\n                       [attr.transform]=\"'translate('+\n                       (16+i*30).toString()+','+'20)'\"\n                       *ngFor=\"let status of element.task_statuses;\n                        let i = index\">\n\n                        <text\n                                fill=\"black\"\n                                text-anchor=\"middle\"\n                                vertical-align=\"middle\"\n                                font-size=\"10\" y=\"3\">{{status.count > 0 ?\n                            status.count : ''}}</text>\n\n                        <circle [attr.stroke-width]=\"status.count>0?2:1\"\n                                (click)=\"status_click(element, status)\"\n                                [attr.stroke]=\n                                        \"color_for_task_status(status.name,\n                                        status.count)\"\n                                fill-opacity=\"0\" r=\"12.5\"\n                                style=\"cursor: pointer; opacity: 1;\">\n                        </circle>\n\n                    </g>\n\n                </svg>\n\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"links\">\n            <th mat-header-cell *matHeaderCellDef\n                style=\"text-align: center; width: 14%;\"> Links\n            </th>\n            <td mat-cell *matCellDef=\"let element\"\n                style=\"padding-left: 1%;min-width: 120px\">\n                <mat-icon svgIcon=\"config\"\n                          matTooltip=\"Config\"\n                          routerLink=\"/dags/dag-detail/{{element.id}}/config\">\n\n                </mat-icon>\n\n                <mat-icon svgIcon=\"code\"\n                          matTooltip=\"Code\"\n                          routerLink=\"/dags/dag-detail/{{element.id}}/code\">\n\n                </mat-icon>\n\n                <mat-icon svgIcon=\"graph\"\n                          matTooltip=\"Graph\"\n                          routerLink=\"/dags/dag-detail/{{element.id}}/graph\">\n\n                </mat-icon>\n\n                <mat-icon svgIcon=\"start\"\n                          matTooltip=\"Start\"\n                          (click)=\"start(element)\"\n                          [class.transparent]=\n                                  \"!can_start(element)\">\n                </mat-icon>\n\n                <mat-icon svgIcon=\"stop\" matTooltip=\"Stop\"\n                          (click)=\"stop(element)\"\n                          [class.transparent]=\"!has_unfinished(element)\">\n                </mat-icon>\n\n                <mat-icon svgIcon=\"remove\" matTooltip=\"Remove\"\n                          (click)=\"remove(element)\">\n                </mat-icon>\n\n                <mat-icon svgIcon=\"report\"\n                          matTooltip=\"Report\"\n                          (click)=\"toogle_report(element)\"\n                          *ngIf=\"report\"\n                          [class.transparent]=\"!element.report_full\">\n                </mat-icon>\n\n            </td>\n        </ng-container>\n\n        <tr mat-header-row *matHeaderRowDef=\"displayed_columns\"></tr>\n        <tr mat-row *matRowDef=\"let row; columns: displayed_columns;\"></tr>\n    </table>\n\n\n</div>\n\n\n<nav>\n    <a routerLink=\"./tasks\" routerLinkActive=\"active\">Tasks</a>\n    <a routerLink=\"./config\" routerLinkActive=\"active\">Config</a>\n    <a routerLink=\"./code\" routerLinkActive=\"active\">Code</a>\n    <a routerLink=\"./graph\" routerLinkActive=\"active\">Graph</a>\n</nav>\n\n<router-outlet (activate)=\"onActivate($event)\"></router-outlet>"

/***/ }),

/***/ "./src/app/dag/dag-detail/dag-detail/dag-detail.component.ts":
/*!*******************************************************************!*\
  !*** ./src/app/dag/dag-detail/dag-detail/dag-detail.component.ts ***!
  \*******************************************************************/
/*! exports provided: DagDetailComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DagDetailComponent", function() { return DagDetailComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _dags_dags_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../dags/dags.component */ "./src/app/dag/dags/dags.component.ts");



var DagDetailComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](DagDetailComponent, _super);
    function DagDetailComponent() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DagDetailComponent.prototype.get_filter = function () {
        var res = _super.prototype.get_filter.call(this);
        res.id = parseInt(this.route.snapshot.paramMap.get('id'));
        return res;
    };
    DagDetailComponent.prototype.onActivate = function (component) {
        component.dag = parseInt(this.route.snapshot.paramMap.get('id'));
    };
    DagDetailComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-dag-detail',
            template: __webpack_require__(/*! ./dag-detail.component.html */ "./src/app/dag/dag-detail/dag-detail/dag-detail.component.html"),
            styles: [__webpack_require__(/*! ../../dags/dags.component.css */ "./src/app/dag/dags/dags.component.css")]
        })
    ], DagDetailComponent);
    return DagDetailComponent;
}(_dags_dags_component__WEBPACK_IMPORTED_MODULE_2__["DagsComponent"]));



/***/ }),

/***/ "./src/app/dag/dag-detail/dag-detail/dag-detail.service.ts":
/*!*****************************************************************!*\
  !*** ./src/app/dag/dag-detail/dag-detail/dag-detail.service.ts ***!
  \*****************************************************************/
/*! exports provided: DagDetailService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DagDetailService", function() { return DagDetailService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _app_settings__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../app-settings */ "./src/app/app-settings.ts");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../models */ "./src/app/models.ts");
/* harmony import */ var _base_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../base.service */ "./src/app/base.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");







var DagDetailService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](DagDetailService, _super);
    function DagDetailService() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.url = "" + _app_settings__WEBPACK_IMPORTED_MODULE_3__["AppSettings"].API_ENDPOINT;
        return _this;
    }
    DagDetailService.prototype.get_config = function (dag_id) {
        var _this = this;
        return this.http.post(this.url + "config", dag_id)
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["tap"])(function (_) { return _this.log('fetched config'); }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["catchError"])(this.handleError('config', new _models__WEBPACK_IMPORTED_MODULE_4__["Data"]())));
    };
    DagDetailService.prototype.get_code = function (dag_id) {
        var _this = this;
        return this.http.post(this.url + "code", dag_id)
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["tap"])(function (_) { return _this.log('fetched code'); }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["catchError"])(this.handleError('config', { 'items': [] })));
    };
    DagDetailService.prototype.get_graph = function (dag_id) {
        var _this = this;
        return this.http.post(this.url + "graph", dag_id)
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["tap"])(function (_) { return _this.log('fetched graph'); }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["catchError"])(this.handleError('graph', new _models__WEBPACK_IMPORTED_MODULE_4__["Graph"]())));
    };
    DagDetailService.prototype.code_download = function (dag_id) {
        var _this = this;
        var url = this.url + "code_download";
        var params = new _angular_common_http__WEBPACK_IMPORTED_MODULE_6__["HttpParams"]().set('id', String(dag_id));
        return this.http.get(url, { params: params, responseType: 'blob' })
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["tap"])(function (_) { return _this.log('fetched archive'); }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["catchError"])(this.handleError()));
    };
    DagDetailService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({ providedIn: 'root' })
    ], DagDetailService);
    return DagDetailService;
}(_base_service__WEBPACK_IMPORTED_MODULE_5__["BaseService"]));



/***/ }),

/***/ "./src/app/dag/dag-detail/graph/graph.component.css":
/*!**********************************************************!*\
  !*** ./src/app/dag/dag-detail/graph/graph.component.css ***!
  \**********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "#mynetwork {\n    border: 1px solid black;\n    background: white;\n    display: inline-block;\n    width: 100%;\n    height: 800px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvZGFnL2RhZy1kZXRhaWwvZ3JhcGgvZ3JhcGguY29tcG9uZW50LmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtJQUNJLHVCQUF1QjtJQUN2QixpQkFBaUI7SUFDakIscUJBQXFCO0lBQ3JCLFdBQVc7SUFDWCxhQUFhO0FBQ2pCIiwiZmlsZSI6InNyYy9hcHAvZGFnL2RhZy1kZXRhaWwvZ3JhcGgvZ3JhcGguY29tcG9uZW50LmNzcyIsInNvdXJjZXNDb250ZW50IjpbIiNteW5ldHdvcmsge1xuICAgIGJvcmRlcjogMXB4IHNvbGlkIGJsYWNrO1xuICAgIGJhY2tncm91bmQ6IHdoaXRlO1xuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgICB3aWR0aDogMTAwJTtcbiAgICBoZWlnaHQ6IDgwMHB4O1xufSJdfQ== */"

/***/ }),

/***/ "./src/app/dag/dag-detail/graph/graph.component.html":
/*!***********************************************************!*\
  !*** ./src/app/dag/dag-detail/graph/graph.component.html ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div id=\"mynetwork\"></div>"

/***/ }),

/***/ "./src/app/dag/dag-detail/graph/graph.component.ts":
/*!*********************************************************!*\
  !*** ./src/app/dag/dag-detail/graph/graph.component.ts ***!
  \*********************************************************/
/*! exports provided: GraphComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "GraphComponent", function() { return GraphComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _message_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../message.service */ "./src/app/message.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _dag_detail_dag_detail_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../dag-detail/dag-detail.service */ "./src/app/dag/dag-detail/dag-detail/dag-detail.service.ts");
/* harmony import */ var _dynamicresource_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../dynamicresource.service */ "./src/app/dynamicresource.service.ts");
/* harmony import */ var _app_settings__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../app-settings */ "./src/app/app-settings.ts");







var GraphComponent = /** @class */ (function () {
    function GraphComponent(message_service, route, service, resource_service, router) {
        this.message_service = message_service;
        this.route = route;
        this.service = service;
        this.resource_service = resource_service;
        this.router = router;
    }
    GraphComponent.prototype.ngAfterViewInit = function () {
        var _this = this;
        this.load_network();
        this.interval = setInterval(function () {
            return _this.load_network();
        }, 3000);
    };
    GraphComponent.prototype.load_network = function () {
        var _this = this;
        var self = this;
        this.resource_service.load('vis.min.js', 'vis.min.css').
            then(function (res) {
            _this.service.get_graph(_this.dag).subscribe(function (res) {
                res.nodes.forEach(function (obj) {
                    return obj.color = _app_settings__WEBPACK_IMPORTED_MODULE_6__["AppSettings"].status_colors[obj.status];
                });
                res.edges.forEach(function (obj) {
                    return obj.color = _app_settings__WEBPACK_IMPORTED_MODULE_6__["AppSettings"].status_colors[obj.status];
                });
                var vis = window['vis'];
                var nodes = new vis.DataSet(res.nodes);
                // create an array with edges
                var edges = new vis.DataSet(res.edges);
                // create a network
                var container = document.getElementById('mynetwork');
                if (!_this.data) {
                    _this.data = {
                        nodes: nodes,
                        edges: edges
                    };
                    var options = {
                        layout: {
                            hierarchical: {
                                direction: 'LR',
                                "sortMethod": "directed",
                            },
                        },
                        edges: {
                            arrows: 'to'
                        }
                    };
                    var network = new vis.Network(container, _this.data, options);
                    network.on('doubleClick', function (properties) {
                        var ids = properties.nodes;
                        var clickedNodes = nodes.get(ids);
                        self.router.navigate(['/tasks/task-detail/' +
                                clickedNodes[0].id +
                                '/logs']);
                    });
                    return;
                }
                for (var _i = 0, _a = res.nodes; _i < _a.length; _i++) {
                    var item = _a[_i];
                    _this.data.nodes.update(item);
                }
                for (var _b = 0, _c = res.edges; _b < _c.length; _b++) {
                    var item = _c[_b];
                    _this.data.edges.update(item);
                }
            });
        }).catch(function (err) { return _this.message_service.add(err); });
    };
    GraphComponent.prototype.ngOnDestroy = function () {
        clearInterval(this.interval);
    };
    GraphComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-graph',
            template: __webpack_require__(/*! ./graph.component.html */ "./src/app/dag/dag-detail/graph/graph.component.html"),
            styles: [__webpack_require__(/*! ./graph.component.css */ "./src/app/dag/dag-detail/graph/graph.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_message_service__WEBPACK_IMPORTED_MODULE_2__["MessageService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"],
            _dag_detail_dag_detail_service__WEBPACK_IMPORTED_MODULE_4__["DagDetailService"],
            _dynamicresource_service__WEBPACK_IMPORTED_MODULE_5__["DynamicresourceService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"]])
    ], GraphComponent);
    return GraphComponent;
}());



/***/ })

}]);
//# sourceMappingURL=default~dag-dag-module~dag-detail-dag-detail-module.js.map