'use strict';

/**
 * @ngdoc function
 * @name xniApp.controller:StatusCtrl
 * @description
 * # StatusCtrl
 * Controller of the xniApp
 */
angular.module('xniApp')
    .controller('StatusCtrl', function ($scope, $http, $timeout) {
        $scope.awesomeThings = [
            'HTML5 Boilerplate',
            'AngularJS',
            'Karma'
        ];
        var server_url = 'http://127.0.0.1:8000';
        var updateStatus = function() {
            $http({method: 'GET', url: server_url+'/api/v1/status/'}).
                success(function (data, status) {
                    $scope.response = data;
                }).
                error(function (data, status) {
                    $scope.response = data;
                });
        };
        $scope.update = updateStatus;
    });
