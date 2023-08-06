(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~task-detail-task-detail-module~task-task-module"],{

/***/ "./src/app/task/task-detail/step/step.component.css":
/*!**********************************************************!*\
  !*** ./src/app/task/task-detail/step/step.component.css ***!
  \**********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Rhc2svdGFzay1kZXRhaWwvc3RlcC9zdGVwLmNvbXBvbmVudC5jc3MifQ== */"

/***/ }),

/***/ "./src/app/task/task-detail/step/step.component.html":
/*!***********************************************************!*\
  !*** ./src/app/task/task-detail/step/step.component.html ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<mat-tree [dataSource]=\"dataSource\" [treeControl]=\"treeControl\">\n    <mat-tree-node *matTreeNodeDef=\"let node\" matTreeNodePadding>\n        <button\n                mat-icon-button\n                mat-button class=\"mat-icon-button\"\n                (click)=\"node_click(node)\">\n\n        </button>\n\n        <mat-accordion>\n            <mat-expansion-panel\n                    (opened)=\"node.opened = true\"\n                    (closed)=\"node.opened = false\">\n                <mat-expansion-panel-header>\n                    <mat-panel-title>\n                        <span [style.margin]=\"'auto'\">\n                            {{node.name}}\n                        </span>\n\n                    </mat-panel-title>\n                    <mat-panel-description>\n                        <span style=\"padding: 10px\">\n                            {{node.content.duration}}\n                        </span>\n\n                        <svg height=\"40\" width=\"220px\" style=\"display: block;\">\n                            <g matTooltip=\"{{status.name}}\"\n                               [attr.transform]=\"'translate('+\n                               (16+i*30).toString()+','+'20)'\"\n                               *ngFor=\"let status of\n                               node.content.log_statuses; let i = index\">\n\n                                <text\n                                        fill=\"black\"\n                                        text-anchor=\"middle\"\n                                        vertical-align=\"middle\"\n                                      font-size=\"10\" y=\"3\">\n                                    {{status.count > 0 ? status.count : ''}}\n                                </text>\n\n                                <circle [attr.stroke-width]=\n                                                \"status.count>0?2:1\"\n                                        (click)=\"status_click(node,\n                                        status.name)\"\n                                        [attr.stroke]=\"color_for_log_status(\n                                        status.name, status.count)\"\n                                        fill-opacity=\"0\" r=\"12.5\"\n                                        style=\"cursor: pointer; opacity: 1;\">\n\n                                </circle>\n                            </g>\n\n                        </svg>\n\n                    </mat-panel-description>\n                </mat-expansion-panel-header>\n\n                <app-log\n                        *ngIf=\"node.opened\"\n                        [step]=\"node.content.id\"\n                        [init_level]=\"node.content.init_level\">\n\n                </app-log>\n\n\n            </mat-expansion-panel>\n        </mat-accordion>\n\n\n    </mat-tree-node>\n\n    <mat-tree-node *matTreeNodeDef=\"let node;when: hasChild\"\n                   matTreeNodePadding>\n        <button mat-icon-button matTreeNodeToggle\n                [attr.aria-label]=\"'toggle ' + node.name\"\n                class=\"mat-icon-button\">\n\n            <mat-icon class=\"mat-icon-rtl-mirror\">\n\n            </mat-icon>\n        </button>\n\n            <mat-accordion>\n            <mat-expansion-panel\n                    (opened)=\"node.opened = true\"\n                    (closed)=\"node.opened = false\">\n                <mat-expansion-panel-header>\n                    <mat-panel-title>\n                        <span [style.margin]=\"'auto'\">\n                            {{node.name}}\n                        </span>\n\n                    </mat-panel-title>\n                    <mat-panel-description>\n                        <span style=\"padding: 10px\">\n                            {{node.content.duration}}\n                        </span>\n\n                        <svg height=\"40\" width=\"220px\" style=\"display: block;\">\n                            <g matTooltip=\"{{status.name}}\"\n                               [attr.transform]=\"'translate('+\n                               (16+i*30).toString()+','+'20)'\"\n                               *ngFor=\"let status of\n                               node.content.log_statuses; let i = index\">\n\n                                <text\n                                        fill=\"black\"\n                                        text-anchor=\"middle\"\n                                        vertical-align=\"middle\"\n                                      font-size=\"10\" y=\"3\">\n                                    {{status.count > 0 ? status.count : ''}}\n                                </text>\n\n                                <circle [attr.stroke-width]=\n                                                \"status.count>0?2:1\"\n                                        (click)=\"status_click(node,\n                                        status.name)\"\n                                        [attr.stroke]=\"color_for_log_status(\n                                        status.name, status.count)\"\n                                        fill-opacity=\"0\" r=\"12.5\"\n                                        style=\"cursor: pointer; opacity: 1;\">\n\n                                </circle>\n                            </g>\n\n                        </svg>\n\n                    </mat-panel-description>\n                </mat-expansion-panel-header>\n\n                <app-log\n                        *ngIf=\"node.opened\"\n                        [step]=\"node.content.id\"\n                        [init_level]=\"node.content.init_level\">\n\n                </app-log>\n\n            </mat-expansion-panel>\n        </mat-accordion>\n\n    </mat-tree-node>\n</mat-tree>"

/***/ }),

/***/ "./src/app/task/task-detail/step/step.component.ts":
/*!*********************************************************!*\
  !*** ./src/app/task/task-detail/step/step.component.ts ***!
  \*********************************************************/
/*! exports provided: StepComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StepComponent", function() { return StepComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_material__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material */ "./node_modules/@angular/material/esm5/material.es5.js");
/* harmony import */ var _angular_cdk_tree__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/cdk/tree */ "./node_modules/@angular/cdk/esm5/tree.es5.js");
/* harmony import */ var _app_settings__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../app-settings */ "./src/app/app-settings.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _task_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../task.service */ "./src/app/task/task.service.ts");








var StepComponent = /** @class */ (function () {
    function StepComponent(service, location) {
        var _this = this;
        this.service = service;
        this.location = location;
        this.flat_node_map = new Map();
        this.transformer = function (node, level) {
            var res = {
                expandable: !!node.children && node.children.length > 0,
                name: node.name,
                level: level,
                content: node
            };
            if (node.id in _this.flat_node_map) {
                var node_flat = _this.flat_node_map[node.id];
                for (var k in res) {
                    if (res[k] != node_flat[k]) {
                        Object.defineProperty(node_flat, k, { 'value': res[k] });
                    }
                }
                return node_flat;
            }
            _this.flat_node_map[node.id] = res;
            return res;
        };
        this.get_children = function (node) { return Object(rxjs__WEBPACK_IMPORTED_MODULE_6__["of"])(node.children); };
        this.treeControl = new _angular_cdk_tree__WEBPACK_IMPORTED_MODULE_4__["FlatTreeControl"](function (node) { return node.level; }, function (node) { return node.expandable; });
        this.treeFlattener = new _angular_material__WEBPACK_IMPORTED_MODULE_3__["MatTreeFlattener"](this.transformer, function (node) { return node.level; }, function (node) { return node.expandable; }, this.get_children);
        this.dataSource = new _angular_material__WEBPACK_IMPORTED_MODULE_3__["MatTreeFlatDataSource"](this.treeControl, this.treeFlattener);
        this.hasChild = function (_, node) { return node.expandable; };
    }
    StepComponent.prototype.load = function () {
        var self = this;
        this.service.steps(this.task).subscribe(function (res) {
            if (!res || !res.data) {
                return;
            }
            self.dataSource.data = res.data;
            self.treeControl.expandAll();
        });
    };
    StepComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.load();
        this.interval = setInterval(function () { return _this.load(); }, 3000);
    };
    StepComponent.prototype.node_click = function (node) {
    };
    StepComponent.prototype.color_for_log_status = function (name, count) {
        return count > 0 ? _app_settings__WEBPACK_IMPORTED_MODULE_5__["AppSettings"].log_colors[name] : 'gainsboro';
    };
    StepComponent.prototype.status_click = function (node, status) {
        node.content.init_level = status;
    };
    StepComponent.prototype.ngOnDestroy = function () {
        clearInterval(this.interval);
    };
    StepComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-step',
            template: __webpack_require__(/*! ./step.component.html */ "./src/app/task/task-detail/step/step.component.html"),
            styles: [__webpack_require__(/*! ./step.component.css */ "./src/app/task/task-detail/step/step.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_task_service__WEBPACK_IMPORTED_MODULE_7__["TaskService"],
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["Location"]])
    ], StepComponent);
    return StepComponent;
}());



/***/ }),

/***/ "./src/app/task/task-detail/task-detail-routing.module.ts":
/*!****************************************************************!*\
  !*** ./src/app/task/task-detail/task-detail-routing.module.ts ***!
  \****************************************************************/
/*! exports provided: TaskDetailRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TaskDetailRoutingModule", function() { return TaskDetailRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _task_detail_task_detail_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./task-detail/task-detail.component */ "./src/app/task/task-detail/task-detail/task-detail.component.ts");
/* harmony import */ var _log_log_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../log/log.component */ "./src/app/log/log.component.ts");
/* harmony import */ var _report_reports_reports_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../report/reports/reports.component */ "./src/app/report/reports/reports.component.ts");
/* harmony import */ var _step_step_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./step/step.component */ "./src/app/task/task-detail/step/step.component.ts");







var routes = [
    {
        path: '',
        component: _task_detail_task_detail_component__WEBPACK_IMPORTED_MODULE_3__["TaskDetailComponent"],
        children: [
            { path: 'report', component: _report_reports_reports_component__WEBPACK_IMPORTED_MODULE_5__["ReportsComponent"] },
            { path: 'step', component: _step_step_component__WEBPACK_IMPORTED_MODULE_6__["StepComponent"] },
            { path: 'logs', component: _log_log_component__WEBPACK_IMPORTED_MODULE_4__["LogComponent"] }
        ]
    }
];
var TaskDetailRoutingModule = /** @class */ (function () {
    function TaskDetailRoutingModule() {
    }
    TaskDetailRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)
            ],
            exports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]
            ]
        })
    ], TaskDetailRoutingModule);
    return TaskDetailRoutingModule;
}());



/***/ }),

/***/ "./src/app/task/task-detail/task-detail.module.ts":
/*!********************************************************!*\
  !*** ./src/app/task/task-detail/task-detail.module.ts ***!
  \********************************************************/
/*! exports provided: TaskDetailModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TaskDetailModule", function() { return TaskDetailModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _task_detail_routing_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./task-detail-routing.module */ "./src/app/task/task-detail/task-detail-routing.module.ts");
/* harmony import */ var _shared_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../shared.module */ "./src/app/shared.module.ts");
/* harmony import */ var _task_detail_task_detail_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./task-detail/task-detail.component */ "./src/app/task/task-detail/task-detail/task-detail.component.ts");
/* harmony import */ var _step_step_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./step/step.component */ "./src/app/task/task-detail/step/step.component.ts");






var TaskDetailModule = /** @class */ (function () {
    function TaskDetailModule() {
    }
    TaskDetailModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _task_detail_routing_module__WEBPACK_IMPORTED_MODULE_2__["TaskDetailRoutingModule"],
                _shared_module__WEBPACK_IMPORTED_MODULE_3__["SharedModule"]
            ],
            declarations: [
                _task_detail_task_detail_component__WEBPACK_IMPORTED_MODULE_4__["TaskDetailComponent"],
                _step_step_component__WEBPACK_IMPORTED_MODULE_5__["StepComponent"]
            ]
        })
    ], TaskDetailModule);
    return TaskDetailModule;
}());



/***/ }),

/***/ "./src/app/task/task-detail/task-detail/task-detail.component.html":
/*!*************************************************************************!*\
  !*** ./src/app/task/task-detail/task-detail/task-detail.component.html ***!
  \*************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<h4>Task detail</h4>\n\n<app-task-table\n        [paginator]=\"this\"\n        [report]=\"report\"\n        [projects]=\"projects\">\n\n</app-task-table>\n\n<div *ngIf=\"child_paginator.total==null||child_paginator.total>0\">\n    <h4>Child tasks</h4>\n\n    <app-task-table\n            [paginator]=\"child_paginator\"\n            [show_links]=\"false\">\n    </app-task-table>\n</div>\n\n\n<nav>\n    <a routerLink=\"./logs\" routerLinkActive=\"active\"\n       [routerLinkActiveOptions]=\"{ exact: true }\">Logs</a>\n    <a routerLink=\"./step\" routerLinkActive=\"active\">Steps</a>\n    <a routerLink=\"./report\" routerLinkActive=\"active\">Reports</a>\n</nav>\n\n<router-outlet (activate)=\"onActivate($event)\"></router-outlet>"

/***/ }),

/***/ "./src/app/task/task-detail/task-detail/task-detail.component.ts":
/*!***********************************************************************!*\
  !*** ./src/app/task/task-detail/task-detail/task-detail.component.ts ***!
  \***********************************************************************/
/*! exports provided: TaskDetailComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TaskDetailComponent", function() { return TaskDetailComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _tasks_tasks_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../tasks/tasks.component */ "./src/app/task/tasks/tasks.component.ts");
/* harmony import */ var _paginator__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../paginator */ "./src/app/paginator.ts");




var TaskDetailComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](TaskDetailComponent, _super);
    function TaskDetailComponent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.components = [];
        return _this;
    }
    TaskDetailComponent.prototype.get_filter = function () {
        var res = _super.prototype.get_filter.call(this);
        res.id = this.id;
        res.type = ['User', 'Train', 'Service'];
        return res;
    };
    Object.defineProperty(TaskDetailComponent.prototype, "id", {
        get: function () {
            return parseInt(this.route.snapshot.paramMap.get('id'));
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(TaskDetailComponent.prototype, "filter_params_get", {
        get: function () {
            var self = this;
            function filter_params_get_int() {
                return {
                    parent: self.id,
                    type: ['Service']
                };
            }
            return filter_params_get_int;
        },
        enumerable: true,
        configurable: true
    });
    TaskDetailComponent.prototype.ngOnInit = function () {
        var _this = this;
        _super.prototype.ngOnInit.call(this);
        this.child_paginator = new _paginator__WEBPACK_IMPORTED_MODULE_3__["Paginator"](this.service, this.location, this.filter_params_get, 'paginator', true, false);
        this.child_paginator.ngOnInit();
        this.child_paginator.change.subscribe(function (x) {
            for (var _i = 0, _a = _this.components; _i < _a.length; _i++) {
                var c = _a[_i];
                c.task = _this.id;
            }
        });
        this.child_paginator.change.emit();
    };
    TaskDetailComponent.prototype.ngOnDestroy = function () {
        _super.prototype.ngOnDestroy.call(this);
        this.child_paginator.ngOnDestroy();
    };
    TaskDetailComponent.prototype.onActivate = function (component) {
        component.task = this.id;
        this.components.push(component);
    };
    TaskDetailComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-task-detail',
            template: __webpack_require__(/*! ./task-detail.component.html */ "./src/app/task/task-detail/task-detail/task-detail.component.html"),
            styles: [__webpack_require__(/*! ../../tasks/tasks.component.css */ "./src/app/task/tasks/tasks.component.css")]
        })
    ], TaskDetailComponent);
    return TaskDetailComponent;
}(_tasks_tasks_component__WEBPACK_IMPORTED_MODULE_2__["TasksComponent"]));



/***/ })

}]);
//# sourceMappingURL=default~task-detail-task-detail-module~task-task-module.js.map