"use strict";angular.module("xniApp",["ngAnimate","ngCookies","ngResource","ngRoute","ngSanitize","ngTouch"]).config(["$routeProvider",function(a){a.when("/",{templateUrl:"views/main.html",controller:"MainCtrl"}).when("/align",{templateUrl:"views/align.html",controller:"AlignCtrl"}).otherwise({redirectTo:"/"})}]),angular.module("xniApp").controller("MainCtrl",["$scope",function(a){a.awesomeThings=["HTML5 Boilerplate","AngularJS","Karma"]}]),angular.module("xniApp").controller("AlignCtrl",["$scope","$http",function(a,b){a.awesomeThings=["HTML5 Boilerplate","AngularJS","Karma"],a.imfiles_change=function(){b({method:"POST",url:"/api/v1/path/",params:{path:a.imfiles}}).success(function(b){a.imfiles_status=b}).error(function(b){a.imfiles_status=b})},a.destdir_change=function(){b({method:"POST",url:"/api/v1/path/",params:{path:a.destdir}}).success(function(b){a.destdir_status=b}).error(function(b){a.destdir_status=b})},a.shift=function(){b({method:"POST",url:"/api/v1/shift/",params:{imfiles:a.imfiles,destdir:a.destdir,posdata:a.posdata}}).success(function(b){a.response=b}).error(function(b){a.response=b})}}]);