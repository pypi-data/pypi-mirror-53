(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["report-report-module"],{

/***/ "./src/app/report/internal/img-classify/img-classify.component.css":
/*!*************************************************************************!*\
  !*** ./src/app/report/internal/img-classify/img-classify.component.css ***!
  \*************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "mat-button-toggle-group {\n    flex-wrap: wrap;\n}\n\nimg {\n    height: auto;\n    width: auto;\n}\n\n.section {\n    display: flex;\n    align-content: center;\n    align-items: center;\n    height: 12px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvcmVwb3J0L2ludGVybmFsL2ltZy1jbGFzc2lmeS9pbWctY2xhc3NpZnkuY29tcG9uZW50LmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtJQUNJLGVBQWU7QUFDbkI7O0FBRUE7SUFDSSxZQUFZO0lBQ1osV0FBVztBQUNmOztBQUVBO0lBQ0ksYUFBYTtJQUNiLHFCQUFxQjtJQUNyQixtQkFBbUI7SUFDbkIsWUFBWTtBQUNoQiIsImZpbGUiOiJzcmMvYXBwL3JlcG9ydC9pbnRlcm5hbC9pbWctY2xhc3NpZnkvaW1nLWNsYXNzaWZ5LmNvbXBvbmVudC5jc3MiLCJzb3VyY2VzQ29udGVudCI6WyJtYXQtYnV0dG9uLXRvZ2dsZS1ncm91cCB7XG4gICAgZmxleC13cmFwOiB3cmFwO1xufVxuXG5pbWcge1xuICAgIGhlaWdodDogYXV0bztcbiAgICB3aWR0aDogYXV0bztcbn1cblxuLnNlY3Rpb24ge1xuICAgIGRpc3BsYXk6IGZsZXg7XG4gICAgYWxpZ24tY29udGVudDogY2VudGVyO1xuICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gICAgaGVpZ2h0OiAxMnB4O1xufSJdfQ== */"

/***/ }),

/***/ "./src/app/report/internal/img-classify/img-classify.component.html":
/*!**************************************************************************!*\
  !*** ./src/app/report/internal/img-classify/img-classify.component.html ***!
  \**************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"mat-elevation-z8\" style=\"float: left\">\n    <table mat-table [dataSource]=\"dataSource\">\n\n        <ng-container matColumnDef=\"img\">\n            <th mat-header-cell *matHeaderCellDef>\n                <div>{{data.name}}</div>\n                <div [id]=\"'img_classify_'+data.name\"></div>\n\n                <mat-card class=\"result\">\n                    <mat-card-content>\n                        <div>\n                            <div>score min</div>\n                            <mat-slider\n                                    [max]=\"1\"\n                                    [min]=\"0\"\n                                    [step]=\"0.01\"\n                                    [thumbLabel]=\"true\"\n                                    (change)=\"change.emit()\"\n                                    [(ngModel)]=\"score_min\">\n\n                            </mat-slider>\n                        </div>\n\n                        <div>\n                            <div style=\"text-align: left\">score max</div>\n                            <mat-slider\n                                    [max]=\"1\"\n                                    [min]=\"0\"\n                                    [step]=\"0.01\"\n                                    [thumbLabel]=\"true\"\n                                    (change)=\"change.emit()\"\n                                    [(ngModel)]=\"score_max\">\n\n                            </mat-slider>\n                        </div>\n\n                    </mat-card-content>\n\n                    <mat-card-content *ngFor=\"let element of item.attrs\">\n\n                        <div *ngIf=\"element.type=='int'\">\n                            <mat-form-field>\n                                <mat-label>{{element.name}}</mat-label>\n\n                                <input\n                                        matInput\n                                        [(ngModel)]=\"element.equal\"\n                                        (change)=\"change.emit()\"\n                                        type=\"number\"/>\n\n                            </mat-form-field>\n                        </div>\n\n                        <div *ngIf=\"element.type=='greater'\">\n                            <mat-form-field>\n                                <mat-label>{{element.name}}_greater</mat-label>\n\n                                <input\n                                        matInput\n                                        [(ngModel)]=\"element.greater\"\n                                        (change)=\"change.emit()\"\n                                        type=\"number\"/>\n\n                            </mat-form-field>\n                        </div>\n\n                        <div *ngIf=\"element.type=='less'\">\n                            <mat-form-field>\n                                <mat-label>{{element.name}}_less</mat-label>\n\n                                <input\n                                        matInput\n                                        [(ngModel)]=\"element.less\"\n                                        (change)=\"change.emit()\"\n                                        type=\"number\"/>\n\n                            </mat-form-field>\n                        </div>\n\n                        <div *ngIf=\"element.type=='greater_less'\">\n                            <mat-form-field>\n                                <mat-label>{{element.name}}_less</mat-label>\n\n                                <input\n                                        matInput\n                                        (change)=\"change.emit()\"\n                                        [(ngModel)]=\"element.less\"\n                                        type=\"number\"/>\n\n                            </mat-form-field>\n\n                            <mat-form-field>\n                                <mat-label>{{element.name}}_greater</mat-label>\n\n                                <input\n                                        matInput\n                                        (change)=\"change.emit()\"\n                                        [(ngModel)]=\"element.greater\"\n                                        type=\"number\"/>\n\n                            </mat-form-field>\n                        </div>\n\n                        <div *ngIf=\"element.type=='str'\">\n                            <mat-form-field>\n                                <mat-label>{{element.name}}</mat-label>\n\n                                <input\n                                        matInput\n                                        (change)=\"change.emit()\"\n                                        [(ngModel)]=\"element.equal\"/>\n\n                            </mat-form-field>\n                        </div>\n\n\n                    </mat-card-content>\n\n                </mat-card>\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                <div>\n                    <span *ngIf=\"element.y!=null\">True:{{element.y}}\n                    </span>\n\n                    Pred:{{element.y_pred}} &nbsp;\n\n                    <span *ngIf=\"element.score!=null\">\n                        Score: {{element.score}}\n                    </span>\n\n                </div>\n\n                <img [attr.src]=\"'data:image/JPEG;base64,' + element.content\">\n            </td>\n        </ng-container>\n\n        <tr mat-header-row *matHeaderRowDef=\"displayed_columns\"></tr>\n        <tr mat-row *matRowDef=\"let row; columns: displayed_columns;\"></tr>\n    </table>\n\n    <mat-paginator\n            [pageSizeOptions]=\"[1 ,3, 5, 15, 30, 100]\"\n            [length]=\"total\"\n            [pageSize]=\"15\">\n\n    </mat-paginator>\n</div>"

/***/ }),

/***/ "./src/app/report/internal/img-classify/img-classify.component.ts":
/*!************************************************************************!*\
  !*** ./src/app/report/internal/img-classify/img-classify.component.ts ***!
  \************************************************************************/
/*! exports provided: ImgClassifyComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImgClassifyComponent", function() { return ImgClassifyComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _paginator__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../paginator */ "./src/app/paginator.ts");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../models */ "./src/app/models.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _img_classify_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./img-classify.service */ "./src/app/report/internal/img-classify/img-classify.service.ts");
/* harmony import */ var _dynamicresource_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../dynamicresource.service */ "./src/app/dynamicresource.service.ts");
/* harmony import */ var _layout_layout_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../layout/layout.service */ "./src/app/report/internal/layout/layout.service.ts");








var ImgClassifyComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImgClassifyComponent, _super);
    function ImgClassifyComponent(service, location, layout_service, resource_service) {
        var _this = _super.call(this, service, location, null, null, false) || this;
        _this.service = service;
        _this.location = location;
        _this.layout_service = layout_service;
        _this.resource_service = resource_service;
        _this.displayed_columns = ['img'];
        _this.loaded = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        _this.score_min = 0;
        _this.score_max = 1;
        return _this;
    }
    ImgClassifyComponent.prototype.subscribe_data_changed = function () {
        var _this = this;
        this.layout_service.data_updated.subscribe(function (event) {
            if (event.key != _this.item.source) {
                return;
            }
        });
    };
    ImgClassifyComponent.prototype._ngOnInit = function () {
        var self = this;
        this.subscribe_data_changed();
        this.data_updated.subscribe(function (res) {
            if (!res || !self.data.name) {
                return;
            }
            self.resource_service.load('plotly').
                then(function () {
                self.plot_confusion(res.confusion, self.data.name, res.class_names);
            });
        });
    };
    ImgClassifyComponent.prototype.plot_confusion = function (confusion, name, class_names) {
        if (!confusion || !confusion.data) {
            return;
        }
        var self = this;
        var colorscaleValue = [
            [0, '#3D9970'],
            [1, '#001f3f']
        ];
        var x = class_names.slice();
        var y = class_names.slice();
        var data = [{
                x: x,
                y: y,
                z: confusion.data,
                type: 'heatmap',
                colorscale: colorscaleValue,
                showscale: false
            }];
        var layout = {
            title: 'Confusion matrix',
            annotations: [],
            width: 300,
            height: 300,
            modebar: false,
            xaxis: {
                ticks: '',
                side: 'top'
            },
            yaxis: {
                ticks: '',
                ticksuffix: ' ',
                width: 700,
                height: 700,
                autosize: false,
                autorange: 'reversed'
            }
        };
        for (var i = 0; i < y.length; i++) {
            for (var j = 0; j < x.length; j++) {
                var currentValue = confusion.data[i][j];
                if (currentValue != 0.0) {
                    var textColor = 'white';
                }
                else {
                    var textColor = 'black';
                }
                var result = {
                    xref: 'x1',
                    yref: 'y1',
                    x: x[j],
                    y: y[i],
                    text: confusion.data[i][j],
                    font: {
                        family: 'Arial',
                        size: 12,
                        color: textColor
                    },
                    showarrow: false,
                };
                layout.annotations.push(result);
            }
        }
        var id = 'img_classify_' + name;
        window['Plotly'].newPlot(id, data, layout, { displayModeBar: false });
        var plot = document.getElementById(id);
        // @ts-ignore
        plot.on('plotly_click', function (data) {
            var pt = data.points[0];
            var y = class_names.indexOf(String(pt.y));
            var y_pred = class_names.indexOf(String(pt.x));
            if (y == self.y && y_pred == self.y_pred) {
                self.y = null;
                self.y_pred = null;
            }
            else {
                self.y = y;
                self.y_pred = y_pred;
            }
            self.change.emit();
        });
    };
    ImgClassifyComponent.prototype.get_filter = function () {
        if (!this.data) {
            return null;
        }
        var res = {};
        res['paginator'] = _super.prototype.get_filter.call(this);
        res['task'] = this.data.task;
        res['group'] = this.data.group;
        res['y'] = this.y;
        res['y_pred'] = this.y_pred;
        res['score_min'] = this.score_min;
        res['score_max'] = this.score_max;
        res['layout'] = this.item;
        return res;
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_3__["ReportItem"])
    ], ImgClassifyComponent.prototype, "item", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_3__["ImgClassify"])
    ], ImgClassifyComponent.prototype, "data", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], ImgClassifyComponent.prototype, "loaded", void 0);
    ImgClassifyComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-img-classify',
            template: __webpack_require__(/*! ./img-classify.component.html */ "./src/app/report/internal/img-classify/img-classify.component.html"),
            styles: [__webpack_require__(/*! ./img-classify.component.css */ "./src/app/report/internal/img-classify/img-classify.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_img_classify_service__WEBPACK_IMPORTED_MODULE_5__["ImgClassifyService"],
            _angular_common__WEBPACK_IMPORTED_MODULE_4__["Location"],
            _layout_layout_service__WEBPACK_IMPORTED_MODULE_7__["LayoutService"],
            _dynamicresource_service__WEBPACK_IMPORTED_MODULE_6__["DynamicresourceService"]])
    ], ImgClassifyComponent);
    return ImgClassifyComponent;
}(_paginator__WEBPACK_IMPORTED_MODULE_2__["Paginator"]));



/***/ }),

/***/ "./src/app/report/internal/img-classify/img-classify.service.ts":
/*!**********************************************************************!*\
  !*** ./src/app/report/internal/img-classify/img-classify.service.ts ***!
  \**********************************************************************/
/*! exports provided: ImgClassifyService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImgClassifyService", function() { return ImgClassifyService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _base_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../base.service */ "./src/app/base.service.ts");



var ImgClassifyService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImgClassifyService, _super);
    function ImgClassifyService() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.collection_part = 'img_classify';
        return _this;
    }
    ImgClassifyService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ImgClassifyService);
    return ImgClassifyService;
}(_base_service__WEBPACK_IMPORTED_MODULE_2__["BaseService"]));



/***/ }),

/***/ "./src/app/report/internal/img-segment/img-segment.component.css":
/*!***********************************************************************!*\
  !*** ./src/app/report/internal/img-segment/img-segment.component.css ***!
  \***********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "mat-button-toggle-group {\n    flex-wrap: wrap;\n}\n\nimg {\n    height: auto;\n    width: auto;\n}\n\n.section {\n    display: flex;\n    align-content: center;\n    align-items: center;\n    height: 12px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvcmVwb3J0L2ludGVybmFsL2ltZy1zZWdtZW50L2ltZy1zZWdtZW50LmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7SUFDSSxlQUFlO0FBQ25COztBQUVBO0lBQ0ksWUFBWTtJQUNaLFdBQVc7QUFDZjs7QUFFQTtJQUNJLGFBQWE7SUFDYixxQkFBcUI7SUFDckIsbUJBQW1CO0lBQ25CLFlBQVk7QUFDaEIiLCJmaWxlIjoic3JjL2FwcC9yZXBvcnQvaW50ZXJuYWwvaW1nLXNlZ21lbnQvaW1nLXNlZ21lbnQuY29tcG9uZW50LmNzcyIsInNvdXJjZXNDb250ZW50IjpbIm1hdC1idXR0b24tdG9nZ2xlLWdyb3VwIHtcbiAgICBmbGV4LXdyYXA6IHdyYXA7XG59XG5cbmltZyB7XG4gICAgaGVpZ2h0OiBhdXRvO1xuICAgIHdpZHRoOiBhdXRvO1xufVxuXG4uc2VjdGlvbiB7XG4gICAgZGlzcGxheTogZmxleDtcbiAgICBhbGlnbi1jb250ZW50OiBjZW50ZXI7XG4gICAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAgICBoZWlnaHQ6IDEycHg7XG59Il19 */"

/***/ }),

/***/ "./src/app/report/internal/img-segment/img-segment.component.html":
/*!************************************************************************!*\
  !*** ./src/app/report/internal/img-segment/img-segment.component.html ***!
  \************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"mat-elevation-z8\" style=\"float: left\">\n    <table mat-table [dataSource]=\"dataSource\">\n\n        <ng-container matColumnDef=\"img\">\n            <th mat-header-cell *matHeaderCellDef>\n                <div>{{data.name}}</div>\n\n                <mat-card class=\"result\">\n                    <mat-card-content>\n                        <div>\n                            <div>score min</div>\n                            <mat-slider\n                                    [max]=\"1\"\n                                    [min]=\"0\"\n                                    [step]=\"0.01\"\n                                    [thumbLabel]=\"true\"\n                                    (change)=\"change.emit()\"\n                                    [(ngModel)]=\"score_min\">\n\n                            </mat-slider>\n                        </div>\n\n                        <div>\n                            <div style=\"text-align: left\">score max</div>\n                            <mat-slider\n                                    [max]=\"1\"\n                                    [min]=\"0\"\n                                    [step]=\"0.01\"\n                                    [thumbLabel]=\"true\"\n                                    (change)=\"change.emit()\"\n                                    [(ngModel)]=\"score_max\">\n\n                            </mat-slider>\n                        </div>\n\n                    </mat-card-content>\n\n                    <mat-card-content *ngFor=\"let element of item.attrs\">\n\n                        <div *ngIf=\"element.type=='int'\">\n                            <mat-form-field>\n                                <mat-label>{{element.name}}</mat-label>\n\n                                <input\n                                        matInput\n                                        [(ngModel)]=\"element.equal\"\n                                        (change)=\"change.emit()\"\n                                        type=\"number\"/>\n\n                            </mat-form-field>\n                        </div>\n\n                        <div *ngIf=\"element.type=='greater'\">\n                            <mat-form-field>\n                                <mat-label>{{element.name}}_greater</mat-label>\n\n                                <input\n                                        matInput\n                                        [(ngModel)]=\"element.greater\"\n                                        (change)=\"change.emit()\"\n                                        type=\"number\"/>\n\n                            </mat-form-field>\n                        </div>\n\n                        <div *ngIf=\"element.type=='less'\">\n                            <mat-form-field>\n                                <mat-label>{{element.name}}_less</mat-label>\n\n                                <input\n                                        matInput\n                                        [(ngModel)]=\"element.less\"\n                                        (change)=\"change.emit()\"\n                                        type=\"number\"/>\n\n                            </mat-form-field>\n                        </div>\n\n                        <div *ngIf=\"element.type=='greater_less'\">\n                            <mat-form-field>\n                                <mat-label>{{element.name}}_less</mat-label>\n\n                                <input\n                                        matInput\n                                        (change)=\"change.emit()\"\n                                        [(ngModel)]=\"element.less\"\n                                        type=\"number\"/>\n\n                            </mat-form-field>\n\n                            <mat-form-field>\n                                <mat-label>{{element.name}}_greater</mat-label>\n\n                                <input\n                                        matInput\n                                        (change)=\"change.emit()\"\n                                        [(ngModel)]=\"element.greater\"\n                                        type=\"number\"/>\n\n                            </mat-form-field>\n                        </div>\n\n                        <div *ngIf=\"element.type=='str'\">\n                            <mat-form-field>\n                                <mat-label>{{element.name}}</mat-label>\n\n                                <input\n                                        matInput\n                                        (change)=\"change.emit()\"\n                                        [(ngModel)]=\"element.equal\"/>\n\n                            </mat-form-field>\n                        </div>\n\n\n                    </mat-card-content>\n\n                </mat-card>\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                <div>\n\n                    <span *ngIf=\"element.score!=null\">\n                        Score: {{element.score}}\n                    </span>\n\n                </div>\n\n                <img [attr.src]=\"'data:image/JPEG;base64,' + element.content\">\n            </td>\n        </ng-container>\n\n        <tr mat-header-row *matHeaderRowDef=\"displayed_columns\"></tr>\n        <tr mat-row *matRowDef=\"let row; columns: displayed_columns;\"></tr>\n    </table>\n\n    <mat-paginator\n            [pageSizeOptions]=\"[1 ,3, 5, 15, 30, 100]\"\n            [length]=\"total\"\n            [pageSize]=\"15\">\n\n    </mat-paginator>\n</div>"

/***/ }),

/***/ "./src/app/report/internal/img-segment/img-segment.component.ts":
/*!**********************************************************************!*\
  !*** ./src/app/report/internal/img-segment/img-segment.component.ts ***!
  \**********************************************************************/
/*! exports provided: ImgSegmentComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImgSegmentComponent", function() { return ImgSegmentComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _paginator__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../paginator */ "./src/app/paginator.ts");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../models */ "./src/app/models.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _img_segment_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./img-segment.service */ "./src/app/report/internal/img-segment/img-segment.service.ts");
/* harmony import */ var _dynamicresource_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../dynamicresource.service */ "./src/app/dynamicresource.service.ts");
/* harmony import */ var _layout_layout_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../layout/layout.service */ "./src/app/report/internal/layout/layout.service.ts");








var ImgSegmentComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImgSegmentComponent, _super);
    function ImgSegmentComponent(service, location, layout_service, resource_service) {
        var _this = _super.call(this, service, location, null, null, false) || this;
        _this.service = service;
        _this.location = location;
        _this.layout_service = layout_service;
        _this.resource_service = resource_service;
        _this.displayed_columns = ['img'];
        _this.loaded = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        _this.score_min = 0;
        _this.score_max = 1;
        return _this;
    }
    ImgSegmentComponent.prototype.subscribe_data_changed = function () {
        var _this = this;
        this.layout_service.data_updated.subscribe(function (event) {
            if (event.key != _this.item.source) {
                return;
            }
        });
    };
    ImgSegmentComponent.prototype._ngOnInit = function () {
        var self = this;
        this.subscribe_data_changed();
        this.data_updated.subscribe(function (res) {
            if (!res || !self.data.name) {
                return;
            }
        });
    };
    ImgSegmentComponent.prototype.get_filter = function () {
        if (!this.data) {
            return null;
        }
        var res = {};
        res['paginator'] = _super.prototype.get_filter.call(this);
        res['task'] = this.data.task;
        res['group'] = this.data.group;
        res['score_min'] = this.score_min;
        res['score_max'] = this.score_max;
        res['layout'] = this.item;
        return res;
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_3__["ReportItem"])
    ], ImgSegmentComponent.prototype, "item", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_3__["ImgClassify"])
    ], ImgSegmentComponent.prototype, "data", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], ImgSegmentComponent.prototype, "loaded", void 0);
    ImgSegmentComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-img-segment',
            template: __webpack_require__(/*! ./img-segment.component.html */ "./src/app/report/internal/img-segment/img-segment.component.html"),
            styles: [__webpack_require__(/*! ./img-segment.component.css */ "./src/app/report/internal/img-segment/img-segment.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_img_segment_service__WEBPACK_IMPORTED_MODULE_5__["ImgSegmentService"],
            _angular_common__WEBPACK_IMPORTED_MODULE_4__["Location"],
            _layout_layout_service__WEBPACK_IMPORTED_MODULE_7__["LayoutService"],
            _dynamicresource_service__WEBPACK_IMPORTED_MODULE_6__["DynamicresourceService"]])
    ], ImgSegmentComponent);
    return ImgSegmentComponent;
}(_paginator__WEBPACK_IMPORTED_MODULE_2__["Paginator"]));



/***/ }),

/***/ "./src/app/report/internal/img-segment/img-segment.service.ts":
/*!********************************************************************!*\
  !*** ./src/app/report/internal/img-segment/img-segment.service.ts ***!
  \********************************************************************/
/*! exports provided: ImgSegmentService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImgSegmentService", function() { return ImgSegmentService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _base_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../base.service */ "./src/app/base.service.ts");



var ImgSegmentService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImgSegmentService, _super);
    function ImgSegmentService() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.collection_part = 'img_segment';
        return _this;
    }
    ImgSegmentService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ImgSegmentService);
    return ImgSegmentService;
}(_base_service__WEBPACK_IMPORTED_MODULE_2__["BaseService"]));



/***/ }),

/***/ "./src/app/report/internal/img/img.component.css":
/*!*******************************************************!*\
  !*** ./src/app/report/internal/img/img.component.css ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3JlcG9ydC9pbnRlcm5hbC9pbWcvaW1nLmNvbXBvbmVudC5jc3MifQ== */"

/***/ }),

/***/ "./src/app/report/internal/img/img.component.html":
/*!********************************************************!*\
  !*** ./src/app/report/internal/img/img.component.html ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div style=\"text-align:center\">{{item.name}}</div>\n<img [attr.src]=\"'data:image/JPEG;base64,'+data.data\">"

/***/ }),

/***/ "./src/app/report/internal/img/img.component.ts":
/*!******************************************************!*\
  !*** ./src/app/report/internal/img/img.component.ts ***!
  \******************************************************/
/*! exports provided: ImgComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImgComponent", function() { return ImgComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../models */ "./src/app/models.ts");
/* harmony import */ var _layout_layout_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../layout/layout.service */ "./src/app/report/internal/layout/layout.service.ts");




var ImgComponent = /** @class */ (function () {
    function ImgComponent(layout_service) {
        this.layout_service = layout_service;
    }
    ImgComponent.prototype.ngOnInit = function () {
        this.subscribe_data_changed();
    };
    ImgComponent.prototype.subscribe_data_changed = function () {
        var _this = this;
        this.layout_service.data_updated.subscribe(function (event) {
            if (event.key != _this.item.source) {
                return;
            }
            _this.data = event.data[_this.item.index];
        });
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_2__["ReportItem"])
    ], ImgComponent.prototype, "item", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], ImgComponent.prototype, "data", void 0);
    ImgComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-img',
            template: __webpack_require__(/*! ./img.component.html */ "./src/app/report/internal/img/img.component.html"),
            styles: [__webpack_require__(/*! ./img.component.css */ "./src/app/report/internal/img/img.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_layout_layout_service__WEBPACK_IMPORTED_MODULE_3__["LayoutService"]])
    ], ImgComponent);
    return ImgComponent;
}());



/***/ }),

/***/ "./src/app/report/internal/layout/layout.component.css":
/*!*************************************************************!*\
  !*** ./src/app/report/internal/layout/layout.component.css ***!
  \*************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "app-layout{\n    width: 100%;\n    height: 100%;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvcmVwb3J0L2ludGVybmFsL2xheW91dC9sYXlvdXQuY29tcG9uZW50LmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtJQUNJLFdBQVc7SUFDWCxZQUFZO0FBQ2hCIiwiZmlsZSI6InNyYy9hcHAvcmVwb3J0L2ludGVybmFsL2xheW91dC9sYXlvdXQuY29tcG9uZW50LmNzcyIsInNvdXJjZXNDb250ZW50IjpbImFwcC1sYXlvdXR7XG4gICAgd2lkdGg6IDEwMCU7XG4gICAgaGVpZ2h0OiAxMDAlO1xufSJdfQ== */"

/***/ }),

/***/ "./src/app/report/internal/layout/layout.component.html":
/*!**************************************************************!*\
  !*** ./src/app/report/internal/layout/layout.component.html ***!
  \**************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div *ngIf=\"item && data\">\n    <div *ngIf=\"item.type=='root'\" style=\"margin-top: 10px\">\n        <app-layout\n                [data]=\"items_joined_data[i]\"\n                [item]=\"child\"\n                [metric]=\"metric\"\n                *ngFor=\"let child of items_joined; index as i\">\n\n        </app-layout>\n    </div>\n\n    <mat-expansion-panel\n            [expanded]=\"item.expanded!=null?item.expanded:true\"\n            *ngIf=\"item.type=='panel'\">\n        <mat-expansion-panel-header>\n            <mat-panel-title>\n                {{item.title}}\n            </mat-panel-title>\n        </mat-expansion-panel-header>\n\n        <div *ngIf=\"items_joined.length>0\">\n            <div *ngIf=\"item.parent_cols\">\n                <mat-grid-list\n                        cols=\"{{item.parent_cols}}\"\n                        rowHeight=\"{{item.row_height}}px\"\n                        *ngIf=\"!item.table\">\n\n                    <div *ngFor=\"let child of items_joined; index as i\">\n                        <mat-grid-tile\n                                [colspan]=\"child.cols!=null?child.cols:1\"\n                                [rowspan]=\"child.rows!=null?child.rows:1\">\n                            <app-layout\n                                    [item]=\"child\"\n                                    [metric]=\"metric\"\n                                    [data]=\"items_joined_data[i]\">\n\n                            </app-layout>\n\n                        </mat-grid-tile>\n                    </div>\n\n                </mat-grid-list>\n\n            </div>\n\n            <table *ngIf=\"item.table\" style=\"width: 100%;height: 100%\">\n                <td\n                        *ngFor=\"let child of items_joined; index as i\"\n                        [style.width]=\"td_width(child)\">\n                    <app-layout\n                            [item]=\"child\"\n                            [metric]=\"metric\"\n                            [data]=\"items_joined_data[i]\">\n\n                    </app-layout>\n                </td>\n            </table>\n\n            <div *ngIf=\"item.row_height==null&&!item.table\">\n                <app-layout [item]=\"child\"\n                            [data]=\"items_joined_data[i]\"\n                            [metric]=\"metric\"\n                            *ngFor=\"let child of items_joined; index as i\">\n\n                </app-layout>\n            </div>\n        </div>\n\n    </mat-expansion-panel>\n\n    <div *ngIf=\"item.type=='table'\">\n        <app-table\n                [item]=\"item\"\n                [data]=\"data\"\n                [metric]=\"metric\">\n\n        </app-table>\n    </div>\n\n    <div *ngIf=\"item.type=='series'\">\n        <app-series\n                [item]=\"item\"\n                [data]=\"data\">\n\n        </app-series>\n    </div>\n\n    <div *ngIf=\"item.type=='img'\">\n        <app-img\n                [item]=\"item\"\n                [data]=\"data\">\n\n        </app-img>\n    </div>\n\n    <div *ngIf=\"item.type=='img_classify'\">\n        <app-img-classify\n                [item]=\"item\"\n                [data]=\"data\">\n\n        </app-img-classify>\n    </div>\n\n    <div *ngIf=\"item.type=='img_segment'\">\n        <app-img-segment\n                [item]=\"item\"\n                [data]=\"data\">\n\n        </app-img-segment>\n    </div>\n\n\n</div>\n"

/***/ }),

/***/ "./src/app/report/internal/layout/layout.component.ts":
/*!************************************************************!*\
  !*** ./src/app/report/internal/layout/layout.component.ts ***!
  \************************************************************/
/*! exports provided: LayoutComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LayoutComponent", function() { return LayoutComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../models */ "./src/app/models.ts");
/* harmony import */ var _layout_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./layout.service */ "./src/app/report/internal/layout/layout.service.ts");
/* harmony import */ var _series_series_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../series/series.component */ "./src/app/report/internal/series/series.component.ts");
/* harmony import */ var _helpers__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../helpers */ "./src/app/helpers.ts");
/* harmony import */ var _report_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../report.service */ "./src/app/report/report.service.ts");







var LayoutComponent = /** @class */ (function () {
    function LayoutComponent(service, layout_service) {
        this.service = service;
        this.layout_service = layout_service;
        this.items_joined = [];
        this.items_joined_data = [];
    }
    LayoutComponent.prototype.ngOnInit = function () {
        this.form_items_joined();
        this.subscribe_report_changed();
    };
    Object.defineProperty(LayoutComponent.prototype, "item", {
        get: function () {
            return this._item;
        },
        set: function (item) {
            this._item = item;
            this.form_items_joined();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(LayoutComponent.prototype, "data", {
        get: function () {
            return this._data;
        },
        set: function (data) {
            this._data = data;
        },
        enumerable: true,
        configurable: true
    });
    LayoutComponent.prototype.form_items_joined = function () {
        this.items_joined = [];
        if (!this.item || !this.item.items) {
            return;
        }
        if (!this.data) {
            return;
        }
        for (var _i = 0, _a = this.item.items; _i < _a.length; _i++) {
            var child = _a[_i];
            if (child.type == 'series') {
                var subchildren = _series_series_component__WEBPACK_IMPORTED_MODULE_4__["SeriesComponent"].create(child, this.data[child.source]);
                for (var _b = 0, subchildren_1 = subchildren; _b < subchildren_1.length; _b++) {
                    var s = subchildren_1[_b];
                    this.items_joined.push(s[0]);
                    this.items_joined_data.push(s[1]);
                }
            }
            else {
                var single_elements = ['img_classify', 'img', 'img_segment'];
                if (single_elements.indexOf(child.type) != -1) {
                    if (!(child.source in this.data)) {
                        continue;
                    }
                    var i = 0;
                    for (var _c = 0, _d = this.data[child.source]; _c < _d.length; _c++) {
                        var d = _d[_c];
                        var child_clone = _helpers__WEBPACK_IMPORTED_MODULE_5__["Helpers"].clone(child);
                        child_clone.index = i;
                        this.items_joined.push(child_clone);
                        this.items_joined_data.push(d);
                        i++;
                    }
                }
                else if (child.type == 'table') {
                    this.items_joined.push(child);
                    this.items_joined_data.push(this.data);
                }
                else {
                    this.items_joined.push(child);
                    this.items_joined_data.push(this.data);
                }
            }
        }
    };
    LayoutComponent.prototype.td_width = function (child) {
        var total = 0;
        for (var _i = 0, _a = this.items_joined; _i < _a.length; _i++) {
            var c = _a[_i];
            total += c.cols ? c.cols : 1;
        }
        return (100 * (child.cols ? child.cols : 1) / total).toString() + '%';
    };
    LayoutComponent.prototype.subscribe_report_changed = function () {
        var _this = this;
        if (this.report_id != null) {
            this.interval = setInterval(function () {
                return _this.update();
            }, 5000);
            this.service.data_updated.subscribe(function (res) {
                _this.update(true);
            });
        }
    };
    LayoutComponent.prototype.update = function (hard) {
        var _this = this;
        if (hard === void 0) { hard = false; }
        this.service.get_obj(this.report_id).subscribe(function (data) {
            if (_this.item && !hard) {
                if (JSON.stringify(_this.item) !=
                    JSON.stringify(data.layout)) {
                    _this._data = data.data;
                    _this._item = data.layout;
                    _this.form_items_joined();
                }
                else {
                    for (var key in data.data) {
                        // noinspection JSUnfilteredForInLoop
                        if (JSON.stringify(_this.data[key]) !=
                            JSON.stringify(data.data[key])) {
                            if (data.data[key].length !=
                                _this.data[key].length) {
                                _this._data = data.data;
                                _this._item = data.layout;
                                _this.form_items_joined();
                                break;
                            }
                            else {
                                // noinspection JSUnfilteredForInLoop
                                var value = {
                                    'key': key,
                                    'data': data.data[key]
                                };
                                _this.layout_service.data_updated.emit(value);
                                // noinspection JSUnfilteredForInLoop
                                _this.data[key] = data.data[key];
                            }
                        }
                    }
                }
            }
            else {
                _this._data = data.data;
                _this._item = data.layout;
                _this.form_items_joined();
            }
            _this.layout_service.full_updated.emit(_this.data);
        });
    };
    LayoutComponent.prototype.ngOnDestroy = function () {
        if (this.interval) {
            clearInterval(this.interval);
        }
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Number)
    ], LayoutComponent.prototype, "report_id", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", String)
    ], LayoutComponent.prototype, "id", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_2__["Metric"])
    ], LayoutComponent.prototype, "metric", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_2__["ReportItem"]),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_models__WEBPACK_IMPORTED_MODULE_2__["ReportItem"]])
    ], LayoutComponent.prototype, "item", null);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [Object])
    ], LayoutComponent.prototype, "data", null);
    LayoutComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-layout',
            template: __webpack_require__(/*! ./layout.component.html */ "./src/app/report/internal/layout/layout.component.html"),
            styles: [__webpack_require__(/*! ./layout.component.css */ "./src/app/report/internal/layout/layout.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_report_service__WEBPACK_IMPORTED_MODULE_6__["ReportService"],
            _layout_service__WEBPACK_IMPORTED_MODULE_3__["LayoutService"]])
    ], LayoutComponent);
    return LayoutComponent;
}());



/***/ }),

/***/ "./src/app/report/internal/layout/layout.service.ts":
/*!**********************************************************!*\
  !*** ./src/app/report/internal/layout/layout.service.ts ***!
  \**********************************************************/
/*! exports provided: LayoutService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LayoutService", function() { return LayoutService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");


var LayoutService = /** @class */ (function () {
    function LayoutService() {
        this.data_updated = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.full_updated = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
    }
    LayoutService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], LayoutService);
    return LayoutService;
}());



/***/ }),

/***/ "./src/app/report/internal/series/series.component.css":
/*!*************************************************************!*\
  !*** ./src/app/report/internal/series/series.component.css ***!
  \*************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3JlcG9ydC9pbnRlcm5hbC9zZXJpZXMvc2VyaWVzLmNvbXBvbmVudC5jc3MifQ== */"

/***/ }),

/***/ "./src/app/report/internal/series/series.component.html":
/*!**************************************************************!*\
  !*** ./src/app/report/internal/series/series.component.html ***!
  \**************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div [attr.id]=\"id\"></div>"

/***/ }),

/***/ "./src/app/report/internal/series/series.component.ts":
/*!************************************************************!*\
  !*** ./src/app/report/internal/series/series.component.ts ***!
  \************************************************************/
/*! exports provided: SeriesComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SeriesComponent", function() { return SeriesComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../models */ "./src/app/models.ts");
/* harmony import */ var _helpers__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../helpers */ "./src/app/helpers.ts");
/* harmony import */ var _layout_layout_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../layout/layout.service */ "./src/app/report/internal/layout/layout.service.ts");





var SeriesComponent = /** @class */ (function () {
    function SeriesComponent(layout_service) {
        this.layout_service = layout_service;
        this.id = 'series_' + Math.random().toString();
    }
    SeriesComponent.prototype.ngOnInit = function () {
        this.display();
        this.subscribe_data_changed();
    };
    SeriesComponent.prototype.display = function () {
        var _this = this;
        setTimeout(function () {
            if (document.getElementById(_this.id)) {
                var layout = {
                    'title': _this.data.name,
                    'height': 300,
                    'width': 600,
                    'margin': { 'b': 40, 't': 40 },
                    'shapes': [],
                    'annotations': []
                };
                for (var row_idx = 0; row_idx < _this.data.series.length; row_idx++) {
                    var row = _this.data.series[row_idx];
                    var text = [];
                    var last_stage = '';
                    for (var i = 0; i < row.time.length; i++) {
                        var t = new Date(Date.parse(row.time[i]));
                        text.push(_helpers__WEBPACK_IMPORTED_MODULE_3__["Helpers"].format_date_time(t));
                        if (row_idx == 0 &&
                            last_stage &&
                            last_stage != row.stage[i]) {
                            layout.shapes.push({
                                type: 'line',
                                color: 'green',
                                yref: 'paper',
                                x0: row.x[i] - 1,
                                y0: 0,
                                x1: row.x[i] - 1,
                                y1: 1,
                                text: 'text',
                                line: {
                                    color: 'green',
                                    width: 1.5
                                }
                            });
                            layout.annotations.push({
                                x: row.x[i] - 1,
                                y: 0,
                                showarrow: false,
                                yref: "paper",
                                text: row.stage[i],
                            });
                        }
                        last_stage = row.stage[i];
                    }
                    row.text = text;
                }
                if (_this.data.layout && JSON.stringify(_this.data.layout) !=
                    JSON.stringify(layout)) {
                    for (var _i = 0, _a = _this.data.series; _i < _a.length; _i++) {
                        var s = _a[_i];
                        s.plotted = 0;
                    }
                }
                _this.data.layout = layout;
                if (_this.data.series.length > 0) {
                    if (_this.data.series.map(function (x) { return x.plotted; }).reduce(function (s, c) { return s + c; }, 0) > 0) {
                        var keys = Array(_this.data.series.length).keys();
                        var indices = Array.from(keys);
                        var y = { 'y': [], 'text': [] };
                        for (var s_idx = 0; s_idx < _this.data.series.length; s_idx++) {
                            var s = _this.data.series[s_idx];
                            y['y'].push(s.y.slice(s.plotted));
                            var text = s.text.slice(s.plotted);
                            y['text'].push(text);
                            s.plotted += text.length;
                        }
                        window['Plotly'].extendTraces(_this.id, y, indices);
                    }
                    else {
                        window['Plotly'].newPlot(_this.id, _this.data.series, layout);
                        for (var _b = 0, _c = _this.data.series; _b < _c.length; _b++) {
                            var s = _c[_b];
                            s.plotted = s.x.length;
                        }
                    }
                }
            }
        }, 100);
    };
    SeriesComponent.prototype.subscribe_data_changed = function () {
        var _this = this;
        this.layout_service.data_updated.subscribe(function (event) {
            if (event.key != _this.item.source) {
                return;
            }
            var was_change = false;
            for (var i = 0; i < _this.data.series.length; i++) {
                var d = _this.data.series[i];
                for (var _i = 0, _a = event.data; _i < _a.length; _i++) {
                    var series = _a[_i];
                    if (series.task_id == d.task_id &&
                        series.group == d.group && series.source == d.source) {
                        if (series.x.length > _this.data.series[i].x.length) {
                            _this.data.series[i].x = series.x;
                            _this.data.series[i].y = series.y;
                            _this.data.series[i].time = series.time;
                            _this.data.series[i].stage = series.stage;
                            was_change = true;
                            break;
                        }
                    }
                }
            }
            if (was_change) {
                _this.display();
            }
        });
    };
    SeriesComponent.create_single_task = function (data) {
        var first = data[0];
        var plot = {
            'name': first.source +
                ' - ' + first.task_name,
            'series': [],
            'layout': null
        };
        for (var _i = 0, data_1 = data; _i < data_1.length; _i++) {
            var d = data_1[_i];
            d = _helpers__WEBPACK_IMPORTED_MODULE_3__["Helpers"].clone(d);
            d.plotted = 0;
            d.name = d.group;
            plot.series.push(d);
        }
        return [plot];
    };
    SeriesComponent.create_multi_key = function (data, key) {
        var by_key = {};
        for (var _i = 0, data_2 = data; _i < data_2.length; _i++) {
            var d = data_2[_i];
            d = _helpers__WEBPACK_IMPORTED_MODULE_3__["Helpers"].clone(d);
            if (!(d[key] in by_key)) {
                by_key[d[key]] = {
                    'name': d.source + ' - ' +
                        (key == 'group' ?
                            d[key] :
                            d['task_name']), 'series': []
                };
            }
            d.name = key == 'task_id' ? d.group : d.task_name;
            d.plotted = 0;
            by_key[d[key]].series.push(d);
        }
        var res = [];
        for (var k in by_key) {
            res.push(by_key[k]);
        }
        return res;
    };
    SeriesComponent.create = function (item, data) {
        if (!data || data.length == 0) {
            return [];
        }
        var tasks = _helpers__WEBPACK_IMPORTED_MODULE_3__["Helpers"].unique(data, 'task_id');
        if (tasks.length == 0) {
            return [];
        }
        data = data.filter(function (d) { return !item.group ||
            item.part.indexOf(d.group) != -1; });
        var plots = [];
        if (tasks.length == 1) {
            plots = this.create_single_task(data);
        }
        else if (item.multi) {
            plots = this.create_multi_key(data, 'task_id');
        }
        else {
            plots = this.create_multi_key(data, 'group');
        }
        var items = [];
        for (var _i = 0, plots_1 = plots; _i < plots_1.length; _i++) {
            var p = plots_1[_i];
            var resitem = _helpers__WEBPACK_IMPORTED_MODULE_3__["Helpers"].clone(item);
            items.push([resitem, p]);
        }
        return items;
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_2__["ReportItem"])
    ], SeriesComponent.prototype, "item", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_2__["SeriesItem"])
    ], SeriesComponent.prototype, "data", void 0);
    SeriesComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-series',
            template: __webpack_require__(/*! ./series.component.html */ "./src/app/report/internal/series/series.component.html"),
            styles: [__webpack_require__(/*! ./series.component.css */ "./src/app/report/internal/series/series.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_layout_layout_service__WEBPACK_IMPORTED_MODULE_4__["LayoutService"]])
    ], SeriesComponent);
    return SeriesComponent;
}());



/***/ }),

/***/ "./src/app/report/internal/table/table.component.css":
/*!***********************************************************!*\
  !*** ./src/app/report/internal/table/table.component.css ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "table {\n    border-collapse: collapse;\n    margin-left: auto;\n    margin-right: auto;\n}\n\ntable, th, td {\n    border: 1px solid black;\n}\n\nth, td{\n    padding: 5px;\n}\n\nth.up:after{\n    padding-left: 5px;\n    content: \"\\25B4\";\n}\n\nth.down:after{\n    padding-left: 5px;\n    content: \"\\25BE\";\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvcmVwb3J0L2ludGVybmFsL3RhYmxlL3RhYmxlLmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7SUFDSSx5QkFBeUI7SUFDekIsaUJBQWlCO0lBQ2pCLGtCQUFrQjtBQUN0Qjs7QUFFQTtJQUNJLHVCQUF1QjtBQUMzQjs7QUFFQTtJQUNJLFlBQVk7QUFDaEI7O0FBRUE7SUFDSSxpQkFBaUI7SUFDakIsZ0JBQWdCO0FBQ3BCOztBQUVBO0lBQ0ksaUJBQWlCO0lBQ2pCLGdCQUFnQjtBQUNwQiIsImZpbGUiOiJzcmMvYXBwL3JlcG9ydC9pbnRlcm5hbC90YWJsZS90YWJsZS5jb21wb25lbnQuY3NzIiwic291cmNlc0NvbnRlbnQiOlsidGFibGUge1xuICAgIGJvcmRlci1jb2xsYXBzZTogY29sbGFwc2U7XG4gICAgbWFyZ2luLWxlZnQ6IGF1dG87XG4gICAgbWFyZ2luLXJpZ2h0OiBhdXRvO1xufVxuXG50YWJsZSwgdGgsIHRkIHtcbiAgICBib3JkZXI6IDFweCBzb2xpZCBibGFjaztcbn1cblxudGgsIHRke1xuICAgIHBhZGRpbmc6IDVweDtcbn1cblxudGgudXA6YWZ0ZXJ7XG4gICAgcGFkZGluZy1sZWZ0OiA1cHg7XG4gICAgY29udGVudDogXCJcXDI1QjRcIjtcbn1cblxudGguZG93bjphZnRlcntcbiAgICBwYWRkaW5nLWxlZnQ6IDVweDtcbiAgICBjb250ZW50OiBcIlxcMjVCRVwiO1xufSJdfQ== */"

/***/ }),

/***/ "./src/app/report/internal/table/table.component.html":
/*!************************************************************!*\
  !*** ./src/app/report/internal/table/table.component.html ***!
  \************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<table>\n    <thead>\n    <th\n            [class.up]=\"sort_desc\"\n            [class.down]=\"!sort_desc\"\n            (click)=\"sort_desc=!sort_desc;sort_column=h;sort()\"\n            *ngFor=\"let h of header\">\n        <span style=\"display: inline-block\">{{h}}</span>\n    </th>\n\n    </thead>\n\n    <tbody>\n    <tr *ngFor=\"let r of rows\">\n        <td *ngFor=\"let c of r\" align=\"center\">\n                <span *ngIf=\"is_number(c)\">\n                     {{c| number: '.0-4'}}\n                </span>\n            <span *ngIf=\"!is_number(c)\">\n                   {{c}}\n               </span>\n        </td>\n    </tr>\n    </tbody>\n\n</table>"

/***/ }),

/***/ "./src/app/report/internal/table/table.component.ts":
/*!**********************************************************!*\
  !*** ./src/app/report/internal/table/table.component.ts ***!
  \**********************************************************/
/*! exports provided: TableComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TableComponent", function() { return TableComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../models */ "./src/app/models.ts");
/* harmony import */ var _layout_layout_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../layout/layout.service */ "./src/app/report/internal/layout/layout.service.ts");




var TableComponent = /** @class */ (function () {
    function TableComponent(layout_service) {
        this.layout_service = layout_service;
    }
    TableComponent.prototype.ngOnInit = function () {
        this.update();
        this.subscribe_data_changed();
    };
    TableComponent.prototype._best_epoch = function (items) {
        var best_epoch = null;
        var best_score = this.metric.minimize ? Math.pow(10, 6) : -(Math.pow(10, 6));
        for (var _i = 0, items_1 = items; _i < items_1.length; _i++) {
            var item = items_1[_i];
            if (item.group == 'valid' && item.name == this.metric.name) {
                for (var epoch = 0; epoch < item.y.length; epoch++) {
                    var is_best = false;
                    var v = item.y[epoch];
                    if (v > best_score && !this.metric.minimize) {
                        is_best = true;
                    }
                    else if (v < best_score && this.metric.minimize) {
                        is_best = true;
                    }
                    if (is_best) {
                        best_score = v;
                        best_epoch = epoch;
                    }
                }
                break;
            }
        }
        return best_epoch;
    };
    TableComponent.prototype.subscribe_data_changed = function () {
        var _this = this;
        this.layout_service.full_updated.subscribe(function (event) {
            _this.update();
        });
    };
    TableComponent.prototype.update = function () {
        var data = [];
        for (var k in this.data) {
            if (this.item.source.indexOf(k) != -1 || k == this.metric.name) {
                for (var _i = 0, _a = this.data[k]; _i < _a.length; _i++) {
                    var s = _a[_i];
                    data.push(s);
                }
            }
        }
        var task_group = data.reduce(function (g, s) {
            g[s.task_id] = g[s.task_id] || [];
            g[s.task_id].push(s);
            return g;
        }, {});
        var header = [];
        var rows = [];
        for (var task_id in task_group) {
            var items = task_group[task_id];
            var best_epoch = this._best_epoch(items);
            if (best_epoch == null) {
                continue;
            }
            var task_name = items[0].task_name;
            if (header.length == 0) {
                header.push('model');
                header.push('epoch');
            }
            var row = [task_name, best_epoch];
            for (var i = row.length; i < header.length; i++) {
                row.push(null);
            }
            var name_group = items.reduce(function (g, s) {
                g[s.name] = g[s.name] || [];
                g[s.name].push(s);
                return g;
            }, {});
            for (var name_1 in name_group) {
                if (this.item.source.indexOf(name_1) == -1) {
                    continue;
                }
                var group = name_group[name_1].reduce(function (g, s) {
                    g[s.group] = g[s.group] || [];
                    g[s.group].push(s);
                    return g;
                }, {});
                for (var group_name in group) {
                    var s = group[group_name][0];
                    var h = name_1 + '_' + group_name;
                    var idx = header.indexOf(h);
                    if (idx == -1) {
                        header.push(h);
                        row.push(s.y[best_epoch]);
                    }
                    else {
                        row[idx] = s.y[best_epoch];
                    }
                }
            }
            rows.push(row);
        }
        this.header = header;
        this.rows = rows;
        if (this.sort_desc == null) {
            this.sort_desc = this.metric.minimize;
        }
        this.sort();
    };
    TableComponent.prototype.sort = function () {
        var self = this;
        var column = this.sort_column ?
            this.sort_column :
            this.metric.name + '_' + 'valid';
        var key_idx = this.header.indexOf(column);
        function sort_row(a, b) {
            if (self.sort_desc) {
                return a[key_idx] < b[key_idx] ? -1 : 1;
            }
            return a[key_idx] > b[key_idx] ? -1 : 1;
        }
        this.rows.sort(sort_row);
    };
    TableComponent.prototype.is_number = function (n) {
        return !isNaN(parseFloat(n)) && isFinite(n);
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_2__["ReportItem"])
    ], TableComponent.prototype, "item", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], TableComponent.prototype, "data", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _models__WEBPACK_IMPORTED_MODULE_2__["Metric"])
    ], TableComponent.prototype, "metric", void 0);
    TableComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-table',
            template: __webpack_require__(/*! ./table.component.html */ "./src/app/report/internal/table/table.component.html"),
            styles: [__webpack_require__(/*! ./table.component.css */ "./src/app/report/internal/table/table.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_layout_layout_service__WEBPACK_IMPORTED_MODULE_3__["LayoutService"]])
    ], TableComponent);
    return TableComponent;
}());



/***/ }),

/***/ "./src/app/report/layouts/layouts.component.css":
/*!******************************************************!*\
  !*** ./src/app/report/layouts/layouts.component.css ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".mat-form-field {\n  font-size: 14px;\n  width: 100%;\n}\n\nmat-icon{\n  cursor: pointer;\n}\n\n::ng-deep .mat-sort-header-container{\n  display:flex;\n  justify-content:center;\n  text-align: center;\n  margin-left: 12px !important;\n}\n\n.mat-header-cell{\n  text-align: center !important;\n}\n\ntd{\n  text-align: center;\n}\n\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvcmVwb3J0L2xheW91dHMvbGF5b3V0cy5jb21wb25lbnQuY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsZUFBZTtFQUNmLFdBQVc7QUFDYjs7QUFFQTtFQUNFLGVBQWU7QUFDakI7O0FBRUE7RUFDRSxZQUFZO0VBQ1osc0JBQXNCO0VBQ3RCLGtCQUFrQjtFQUNsQiw0QkFBNEI7QUFDOUI7O0FBRUE7RUFDRSw2QkFBNkI7QUFDL0I7O0FBRUE7RUFDRSxrQkFBa0I7QUFDcEIiLCJmaWxlIjoic3JjL2FwcC9yZXBvcnQvbGF5b3V0cy9sYXlvdXRzLmNvbXBvbmVudC5jc3MiLCJzb3VyY2VzQ29udGVudCI6WyIubWF0LWZvcm0tZmllbGQge1xuICBmb250LXNpemU6IDE0cHg7XG4gIHdpZHRoOiAxMDAlO1xufVxuXG5tYXQtaWNvbntcbiAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG46Om5nLWRlZXAgLm1hdC1zb3J0LWhlYWRlci1jb250YWluZXJ7XG4gIGRpc3BsYXk6ZmxleDtcbiAganVzdGlmeS1jb250ZW50OmNlbnRlcjtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBtYXJnaW4tbGVmdDogMTJweCAhaW1wb3J0YW50O1xufVxuXG4ubWF0LWhlYWRlci1jZWxse1xuICB0ZXh0LWFsaWduOiBjZW50ZXIgIWltcG9ydGFudDtcbn1cblxudGR7XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbn1cbiJdfQ== */"

/***/ }),

/***/ "./src/app/report/layouts/layouts.component.html":
/*!*******************************************************!*\
  !*** ./src/app/report/layouts/layouts.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<button mat-raised-button style=\"margin-top: 15px\"\n        (click)=\"add()\">\n    Add\n</button>\n\n<button mat-raised-button\n        style=\"margin-top: 15px\"\n        [disabled]=\"selected==null\"\n        (click)=\"edit_name()\">\n    Edit name\n</button>\n\n<button mat-raised-button\n        style=\"margin-top: 15px\"\n        [disabled]=\"selected==null\"\n        (click)=\"remove()\">\n    Remove\n</button>\n\n<table style=\"width: 100%;\">\n    <td style=\"width: 30%\" valign=\"top\">\n        <table mat-table [dataSource]=\"dataSource\" matSort>\n\n            <ng-container matColumnDef=\"name\">\n                <th mat-header-cell\n                    *matHeaderCellDef\n                    mat-sort-header\n                    style=\"width: 20%\">\n                    Name\n                </th>\n\n                <td mat-cell *matCellDef=\"let element\">\n                    {{element.name}}\n                </td>\n            </ng-container>\n\n            <ng-container matColumnDef=\"last_modified\">\n                <th mat-header-cell\n                    *matHeaderCellDef\n                    mat-sort-header\n                    style=\"width: 15%\">\n                    Last modified\n                </th>\n\n                <td mat-cell *matCellDef=\"let element\">\n                    {{element.last_modified| date:\"MM.dd H:mm:ss\"}}\n                </td>\n            </ng-container>\n\n            <tr mat-header-row *matHeaderRowDef=\"displayed_columns\"></tr>\n            <tr\n                    mat-row\n                    (click)=\"row_select(row)\"\n                    [style.background]=\"selected==row ? 'lightblue' : ''\"\n                    *matRowDef=\"let row; columns: displayed_columns;\">\n\n            </tr>\n\n        </table>\n\n        <mat-paginator [pageSizeOptions]=\"[15, 30, 100]\"\n                       [length]=\"total\"\n                       [pageSize]=\"15\">\n\n        </mat-paginator>\n\n    </td>\n\n    <td style=\"width: 30%\" valign=\"top\">\n\n        <div [style.visibility]=\"selected?'visible': 'hidden'\">\n\n            <mat-form-field>\n                <mat-label>Content</mat-label>\n\n                <textarea\n                        #textarea\n                        style=\"height:600px;text-align: left\"\n                        matInput\n                        (keyup)=\"key_up($event)\"\n                        (keydown)=\"key_down($event)\">\n\n                </textarea>\n\n            </mat-form-field>\n\n            <button mat-raised-button (click)=\"save()\">Save</button>\n\n        </div>\n\n    </td>\n\n    <td style=\"width: 30%\" valign=\"top\">\n        <pre style=\"color: red\" *ngIf=\"error\">\n                {{error}}\n        </pre>\n    </td>\n\n</table>"

/***/ }),

/***/ "./src/app/report/layouts/layouts.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/report/layouts/layouts.component.ts ***!
  \*****************************************************/
/*! exports provided: LayoutsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LayoutsComponent", function() { return LayoutsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _paginator__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../paginator */ "./src/app/paginator.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _layouts_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./layouts.service */ "./src/app/report/layouts/layouts.service.ts");
/* harmony import */ var _angular_material__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material */ "./node_modules/@angular/material/esm5/material.es5.js");
/* harmony import */ var _layout_add_dialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./layout-add-dialog */ "./src/app/report/layouts/layout-add-dialog.ts");
/* harmony import */ var _helpers__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../helpers */ "./src/app/helpers.ts");








var LayoutsComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](LayoutsComponent, _super);
    function LayoutsComponent(service, location, dialog) {
        var _this = _super.call(this, service, location, null, null, false) || this;
        _this.service = service;
        _this.location = location;
        _this.dialog = dialog;
        _this.displayed_columns = [
            'name',
            'last_modified'
        ];
        _this.id_column = 'name';
        return _this;
    }
    LayoutsComponent.prototype.row_select = function (element) {
        this.selected = element;
        this.textarea.nativeElement.value = element.content;
    };
    ;
    LayoutsComponent.prototype.get_filter = function () {
        var res = {};
        res['paginator'] = _super.prototype.get_filter.call(this);
        res['paginator']['sort_column'] = 'last_modified';
        return res;
    };
    LayoutsComponent.prototype.add = function () {
        var _this = this;
        var dialogRef = this.dialog.open(_layout_add_dialog__WEBPACK_IMPORTED_MODULE_6__["LayoutAddDialogComponent"], {
            width: '400px', height: '200px',
            data: {}
        });
        dialogRef.afterClosed().subscribe(function (result) {
            if (result) {
                _this.service.add(result).subscribe(function (res) {
                    _this.change.emit();
                    _this.error = res.error;
                });
            }
        });
    };
    LayoutsComponent.prototype.edit_name = function () {
        var _this = this;
        var name = this.selected.name;
        var dialogRef = this.dialog.open(_layout_add_dialog__WEBPACK_IMPORTED_MODULE_6__["LayoutAddDialogComponent"], {
            width: '400px', height: '200px',
            data: { 'name': name }
        });
        dialogRef.afterClosed().subscribe(function (result) {
            if (result) {
                _this.service.edit(name, null, result.name).subscribe(function (res) {
                    _this.change.emit();
                    _this.error = res.error;
                });
            }
        });
    };
    LayoutsComponent.prototype.remove = function () {
        var _this = this;
        this.service.remove(this.selected.name)
            .subscribe(function (res) {
            if (res.success) {
                _this.change.emit();
                _this.selected = null;
            }
            _this.error = res.error;
        });
    };
    LayoutsComponent.prototype.save = function () {
        var _this = this;
        this.service.edit(this.selected.name, this.selected.content)
            .subscribe(function (res) {
            if (res.success) {
                _this.change.emit();
            }
            _this.error = res.error;
        });
    };
    LayoutsComponent.prototype.key_down = function (event) {
        if (!this.selected) {
            return;
        }
        var content = _helpers__WEBPACK_IMPORTED_MODULE_7__["Helpers"].handle_textarea_down_key(event, this.textarea.nativeElement);
        if (content) {
            this.selected.content = content;
        }
    };
    LayoutsComponent.prototype.key_up = function (event) {
        if (!this.selected) {
            return;
        }
        this.selected.content = event.target.value;
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('textarea'),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], LayoutsComponent.prototype, "textarea", void 0);
    LayoutsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-layouts',
            template: __webpack_require__(/*! ./layouts.component.html */ "./src/app/report/layouts/layouts.component.html"),
            styles: [__webpack_require__(/*! ./layouts.component.css */ "./src/app/report/layouts/layouts.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_layouts_service__WEBPACK_IMPORTED_MODULE_4__["LayoutsService"],
            _angular_common__WEBPACK_IMPORTED_MODULE_3__["Location"],
            _angular_material__WEBPACK_IMPORTED_MODULE_5__["MatDialog"]])
    ], LayoutsComponent);
    return LayoutsComponent;
}(_paginator__WEBPACK_IMPORTED_MODULE_2__["Paginator"]));



/***/ }),

/***/ "./src/app/report/layouts/layouts.service.ts":
/*!***************************************************!*\
  !*** ./src/app/report/layouts/layouts.service.ts ***!
  \***************************************************/
/*! exports provided: LayoutsService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LayoutsService", function() { return LayoutsService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _base_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../base.service */ "./src/app/base.service.ts");
/* harmony import */ var _app_settings__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../app-settings */ "./src/app/app-settings.ts");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../models */ "./src/app/models.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");






var LayoutsService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](LayoutsService, _super);
    function LayoutsService() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.collection_part = 'layouts';
        _this.single_part = 'layout';
        return _this;
    }
    LayoutsService.prototype.add = function (data) {
        var message = this.constructor.name + ".add";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_3__["AppSettings"].API_ENDPOINT + this.single_part + '/add';
        return this.http.post(url, data).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_4__["BaseResult"]())));
    };
    LayoutsService.prototype.edit = function (name, content, new_name) {
        if (content === void 0) { content = null; }
        if (new_name === void 0) { new_name = null; }
        var message = this.constructor.name + ".edit";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_3__["AppSettings"].API_ENDPOINT + this.single_part + '/edit';
        var params = { 'name': name, 'content': content, 'new_name': new_name };
        return this.http.post(url, params).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_4__["BaseResult"]())));
    };
    LayoutsService.prototype.remove = function (name) {
        var message = this.constructor.name + ".remove";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_3__["AppSettings"].API_ENDPOINT + this.single_part + '/remove';
        var params = { 'name': name };
        return this.http.post(url, params).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_4__["BaseResult"]())));
    };
    LayoutsService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], LayoutsService);
    return LayoutsService;
}(_base_service__WEBPACK_IMPORTED_MODULE_2__["BaseService"]));



/***/ }),

/***/ "./src/app/report/report-detail/report-detail.component.css":
/*!******************************************************************!*\
  !*** ./src/app/report/report-detail/report-detail.component.css ***!
  \******************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3JlcG9ydC9yZXBvcnQtZGV0YWlsL3JlcG9ydC1kZXRhaWwuY29tcG9uZW50LmNzcyJ9 */"

/***/ }),

/***/ "./src/app/report/report-detail/report-detail.component.html":
/*!*******************************************************************!*\
  !*** ./src/app/report/report-detail/report-detail.component.html ***!
  \*******************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<button mat-raised-button\n        style=\"margin-top: 15px\"\n        (click)=\"update_layout()\">\n    Update layout\n</button>\n\n<mat-accordion>\n    <mat-expansion-panel (opened)=\"dag_panel_open = true\"\n                         (closed)=\"dag_panel_open = false\">\n        <mat-expansion-panel-header>\n            <mat-panel-title>\n                Dags\n            </mat-panel-title>\n            <mat-panel-description>\n                Dags to add/remove\n            </mat-panel-description>\n        </mat-expansion-panel-header>\n\n        <app-dags *ngIf=\"dag_panel_open\" [report]=\"id\"></app-dags>\n    </mat-expansion-panel>\n\n    <mat-expansion-panel (opened)=\"task_panel_open = true\"\n                         (closed)=\"task_panel_open = false\">\n        <mat-expansion-panel-header>\n            <mat-panel-title>\n                Tasks\n            </mat-panel-title>\n            <mat-panel-description>\n                Tasks to add/remove\n            </mat-panel-description>\n        </mat-expansion-panel-header>\n\n        <app-tasks *ngIf=\"task_panel_open\" [report]=\"id\"></app-tasks>\n    </mat-expansion-panel>\n\n</mat-accordion>\n\n<app-layout\n        [item]=\"report.layout\"\n        [data]=\"report.data\"\n        [metric]=\"report.metric\"\n        [report_id]=\"id\"\n        *ngIf=\"report\">\n\n</app-layout>\n\n\n\n"

/***/ }),

/***/ "./src/app/report/report-detail/report-detail.component.ts":
/*!*****************************************************************!*\
  !*** ./src/app/report/report-detail/report-detail.component.ts ***!
  \*****************************************************************/
/*! exports provided: ReportDetailComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ReportDetailComponent", function() { return ReportDetailComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _dynamicresource_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../dynamicresource.service */ "./src/app/dynamicresource.service.ts");
/* harmony import */ var _report_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../report.service */ "./src/app/report/report.service.ts");
/* harmony import */ var _angular_material__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material */ "./node_modules/@angular/material/esm5/material.es5.js");
/* harmony import */ var _report_update_dialog_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./report-update-dialog.component */ "./src/app/report/report-detail/report-update-dialog.component.ts");








var ReportDetailComponent = /** @class */ (function () {
    function ReportDetailComponent(service, location, router, route, resource_service, update_dialog) {
        this.service = service;
        this.location = location;
        this.router = router;
        this.route = route;
        this.resource_service = resource_service;
        this.update_dialog = update_dialog;
        this.dag_panel_open = false;
        this.task_panel_open = false;
    }
    ReportDetailComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.id = parseInt(this.route.snapshot.paramMap.get('id'));
        this.resource_service.load('plotly').then(function () {
            _this.service.get_obj(_this.id).subscribe(function (data) {
                _this.report = data;
            });
        });
    };
    ReportDetailComponent.prototype.update_layout = function () {
        var _this = this;
        this.service.update_layout_start(this.id).subscribe(function (data) {
            var config = {
                width: '250px', height: '180px',
                data: data
            };
            var dialog = _this.update_dialog.open(_report_update_dialog_component__WEBPACK_IMPORTED_MODULE_7__["ReportUpdateDialogComponent"], config);
            dialog.afterClosed().subscribe(function (res) {
                if (!res || !res.id) {
                    return;
                }
                _this.service.update_layout_end(res.id, res.layout).
                    subscribe(function (res) {
                    _this.report = res;
                });
            });
        });
    };
    ReportDetailComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-report-detail',
            template: __webpack_require__(/*! ./report-detail.component.html */ "./src/app/report/report-detail/report-detail.component.html"),
            styles: [__webpack_require__(/*! ./report-detail.component.css */ "./src/app/report/report-detail/report-detail.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_report_service__WEBPACK_IMPORTED_MODULE_5__["ReportService"],
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["Location"],
            _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"],
            _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"],
            _dynamicresource_service__WEBPACK_IMPORTED_MODULE_4__["DynamicresourceService"],
            _angular_material__WEBPACK_IMPORTED_MODULE_6__["MatDialog"]])
    ], ReportDetailComponent);
    return ReportDetailComponent;
}());



/***/ }),

/***/ "./src/app/report/report-routing.module.ts":
/*!*************************************************!*\
  !*** ./src/app/report/report-routing.module.ts ***!
  \*************************************************/
/*! exports provided: ReportRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ReportRoutingModule", function() { return ReportRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _report_report_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./report/report.component */ "./src/app/report/report/report.component.ts");
/* harmony import */ var _reports_reports_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./reports/reports.component */ "./src/app/report/reports/reports.component.ts");
/* harmony import */ var _report_detail_report_detail_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./report-detail/report-detail.component */ "./src/app/report/report-detail/report-detail.component.ts");
/* harmony import */ var _layouts_layouts_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./layouts/layouts.component */ "./src/app/report/layouts/layouts.component.ts");







var routes = [
    {
        path: '',
        component: _report_report_component__WEBPACK_IMPORTED_MODULE_3__["ReportComponent"],
        children: [
            { path: 'list', component: _reports_reports_component__WEBPACK_IMPORTED_MODULE_4__["ReportsComponent"] },
            { path: 'layouts', component: _layouts_layouts_component__WEBPACK_IMPORTED_MODULE_6__["LayoutsComponent"] },
            { path: 'report-detail/:id', component: _report_detail_report_detail_component__WEBPACK_IMPORTED_MODULE_5__["ReportDetailComponent"] },
        ]
    }
];
var ReportRoutingModule = /** @class */ (function () {
    function ReportRoutingModule() {
    }
    ReportRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)
            ],
            exports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]
            ]
        })
    ], ReportRoutingModule);
    return ReportRoutingModule;
}());



/***/ }),

/***/ "./src/app/report/report.module.ts":
/*!*****************************************!*\
  !*** ./src/app/report/report.module.ts ***!
  \*****************************************/
/*! exports provided: ReportModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ReportModule", function() { return ReportModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _report_routing_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./report-routing.module */ "./src/app/report/report-routing.module.ts");
/* harmony import */ var _shared_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../shared.module */ "./src/app/shared.module.ts");
/* harmony import */ var _internal_series_series_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./internal/series/series.component */ "./src/app/report/internal/series/series.component.ts");
/* harmony import */ var _internal_img_img_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./internal/img/img.component */ "./src/app/report/internal/img/img.component.ts");
/* harmony import */ var _internal_img_classify_img_classify_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./internal/img-classify/img-classify.component */ "./src/app/report/internal/img-classify/img-classify.component.ts");
/* harmony import */ var _report_report_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./report/report.component */ "./src/app/report/report/report.component.ts");
/* harmony import */ var _internal_layout_layout_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./internal/layout/layout.component */ "./src/app/report/internal/layout/layout.component.ts");
/* harmony import */ var _report_detail_report_detail_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./report-detail/report-detail.component */ "./src/app/report/report-detail/report-detail.component.ts");
/* harmony import */ var _layouts_layouts_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./layouts/layouts.component */ "./src/app/report/layouts/layouts.component.ts");
/* harmony import */ var _internal_table_table_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./internal/table/table.component */ "./src/app/report/internal/table/table.component.ts");
/* harmony import */ var _internal_img_segment_img_segment_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./internal/img-segment/img-segment.component */ "./src/app/report/internal/img-segment/img-segment.component.ts");













var ReportModule = /** @class */ (function () {
    function ReportModule() {
    }
    ReportModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _report_routing_module__WEBPACK_IMPORTED_MODULE_2__["ReportRoutingModule"],
                _shared_module__WEBPACK_IMPORTED_MODULE_3__["SharedModule"]
            ],
            declarations: [
                _internal_series_series_component__WEBPACK_IMPORTED_MODULE_4__["SeriesComponent"],
                _internal_img_img_component__WEBPACK_IMPORTED_MODULE_5__["ImgComponent"],
                _internal_img_classify_img_classify_component__WEBPACK_IMPORTED_MODULE_6__["ImgClassifyComponent"],
                _internal_img_segment_img_segment_component__WEBPACK_IMPORTED_MODULE_12__["ImgSegmentComponent"],
                _report_report_component__WEBPACK_IMPORTED_MODULE_7__["ReportComponent"],
                _internal_layout_layout_component__WEBPACK_IMPORTED_MODULE_8__["LayoutComponent"],
                _report_detail_report_detail_component__WEBPACK_IMPORTED_MODULE_9__["ReportDetailComponent"],
                _layouts_layouts_component__WEBPACK_IMPORTED_MODULE_10__["LayoutsComponent"],
                _internal_table_table_component__WEBPACK_IMPORTED_MODULE_11__["TableComponent"]
            ]
        })
    ], ReportModule);
    return ReportModule;
}());



/***/ }),

/***/ "./src/app/report/report/report.component.css":
/*!****************************************************!*\
  !*** ./src/app/report/report/report.component.css ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3JlcG9ydC9yZXBvcnQvcmVwb3J0LmNvbXBvbmVudC5jc3MifQ== */"

/***/ }),

/***/ "./src/app/report/report/report.component.html":
/*!*****************************************************!*\
  !*** ./src/app/report/report/report.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<nav>\n  <a routerLink=\"./list\" routerLinkActive=\"active\">List</a>\n  <a routerLink=\"./layouts\" routerLinkActive=\"active\">Layouts</a>\n</nav>\n\n<router-outlet></router-outlet>"

/***/ }),

/***/ "./src/app/report/report/report.component.ts":
/*!***************************************************!*\
  !*** ./src/app/report/report/report.component.ts ***!
  \***************************************************/
/*! exports provided: ReportComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ReportComponent", function() { return ReportComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");


var ReportComponent = /** @class */ (function () {
    function ReportComponent() {
    }
    ReportComponent.prototype.ngOnInit = function () {
    };
    ReportComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-reports',
            template: __webpack_require__(/*! ./report.component.html */ "./src/app/report/report/report.component.html"),
            styles: [__webpack_require__(/*! ./report.component.css */ "./src/app/report/report/report.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [])
    ], ReportComponent);
    return ReportComponent;
}());



/***/ })

}]);
//# sourceMappingURL=report-report-module.js.map