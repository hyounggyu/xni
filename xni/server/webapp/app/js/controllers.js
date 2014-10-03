'use strict';

var xniApp = angular.module('xniApp', []);

xniApp.controller('XNICtrl', function ($scope, $http) {
    $scope.imfiles_change = function() {
        $http({method: 'POST', url: '/api/v1/path/', params: {
            path: $scope.imfiles
        }}).
            success(function(data, status){
                $scope.imfiles_status = data;
            }).
            error(function(data, status){
                $scope.imfiles_status = data;
            });
    };
    $scope.destdir_change = function() {
        $http({method: 'POST', url: '/api/v1/path/', params: {
            path: $scope.destdir
        }}).
            success(function(data, status){
                $scope.destdir_status = data;
            }).
            error(function(data, status){
                $scope.destdir_status = data;
            });
    };
    $scope.shift = function() {
        $http({method: 'POST', url: '/api/v1/shift/', params: {
            imfiles: $scope.imfiles,
            destdir: $scope.destdir,
            posdata: $scope.posdata
        }}).
            success(function(data, status) {
                $scope.response = data
            }).
            error(function(data, status) {
                $scope.response = data
            });
    };
});
