"use strict";angular.module("xniApp",["ngAnimate","ngCookies","ngResource","ngRoute","ngSanitize","ngTouch"]).config(["$routeProvider",function(a){a.when("/",{templateUrl:"views/main.html",controller:"MainCtrl"}).when("/align",{templateUrl:"views/align.html",controller:"AlignCtrl"}).otherwise({redirectTo:"/"})}]),angular.module("xniApp").controller("MainCtrl",["$scope",function(a){a.awesomeThings=["HTML5 Boilerplate","AngularJS","Karma"]}]),angular.module("xniApp").controller("AlignCtrl",["$scope","$http","$timeout",function(a,b,c){a.awesomeThings=["HTML5 Boilerplate","AngularJS","Karma"];var d=function(){b({method:"GET",url:"/api/v1/tasks/status.json"}).success(function(b){a.response=b}).error(function(b){a.response=b}),c(d,1e3)};a.check_pattern=function(){b({method:"POST",url:"/api/v1/path/files/",params:{pattern:a.imfiles}}).success(function(b){a.num_files=b}).error(function(b){a.num_files=b})},a.check_directory=function(){b({method:"POST",url:"/api/v1/path/directory/",params:{directory:a.destdir}}).success(function(b){a.directory_status=b}).error(function(b){a.directory_status=b})},a.shift=function(){b({method:"POST",url:"/api/v1/tasks/shift/",params:{imfiles:a.imfiles,destdir:a.destdir,posdata:a.posdata}}).success(function(b){a.response=b}).error(function(b){a.response=b}),d()}}]);