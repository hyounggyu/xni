'use strict';

/**
 * @ngdoc function
 * @name xniApp.controller:AlignCtrl
 * @description
 * # AlignCtrl
 * Controller of the xniApp
 */
angular.module('xniApp')
    .controller('AlignCtrl', function ($scope, $http, $timeout) {
        $scope.awesomeThings = [
            'HTML5 Boilerplate',
            'AngularJS',
            'Karma'
        ];
        var updateStatus = function() {
            $http({method: 'GET', url: '/api/v1/tasks/status.json'}).
                success(function(data, status) {
                    $scope.response = data;
                }).
                error(function(data, status) {
                    $scope.response = data;
                });
            $timeout(updateStatus, 1000);
        };
        $scope.check_pattern = function() {
            $http({method: 'POST', url: '/api/v1/path/files/', params: {
                pattern: $scope.imfiles
            }}).
                success(function(data, status) {
                    $scope.num_files = data;
                }).
                error(function(data, status) {
                    $scope.num_files = data;
                })
        };
        $scope.check_directory = function() {
            $http({method: 'POST', url: '/api/v1/path/directory/', params: {
                directory: $scope.destdir
            }}).
                success(function(data, status) {
                    $scope.directory_status = data;
                }).
                error(function(data, status) {
                    $scope.directory_status = data;
                })
        };
        $scope.shift = function() {
            $http({method: 'POST', url: '/api/v1/tasks/shift/', params: {
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
            updateStatus();
        };
        $scope.correlation = function() {
            $http({method: 'POST', url: '/api/v1/tasks/correlation/', params: {
                imfiles: $scope.imfiles
            }}).
                success(function(data, status) {
                    $scope.response = data
                }).
                error(function(data, status) {
                    $scope.response = data
                });
            updateStatus();
        };
    });
