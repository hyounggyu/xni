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
        var server_url = 'http://127.0.0.1:8000';
        $scope.alert_message = true;
        var updateResponse = function(data, status) {
            $scope.alert_message = false;
            console.log(data);
            $scope.response = data;
            $timeout(function () { $scope.alert_message = true }, 3000)
        };
        $scope.shift = function() {
            $http({method: 'POST', url: server_url+'/api/v1/tasks/shift/', params: {
                imfiles: $scope.imfiles,
                destdir: $scope.destdir,
                posdata: $scope.posdata
            }}).success(updateResponse).error(updateResponse);
        };
        $scope.correlation = function() {
            $http({method: 'POST', url: server_url+'/api/v1/tasks/correlation/', params: {
                imfiles: $scope.imfiles
            }}).success(updateResponse).error(updateResponse);
        };
    });
