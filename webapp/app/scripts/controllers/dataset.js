'use strict';

/**
 * @ngdoc function
 * @name xniApp.controller:DatasetCtrl
 * @description
 * # DatasetCtrl
 * Controller of the xniApp
 */
angular.module('xniApp')
    .controller('DatasetCtrl', function ($scope, $http) {
        $scope.awesomeThings = [
            'HTML5 Boilerplate',
            'AngularJS',
            'Karma'
        ];
        var server_url = 'http://127.0.0.1:8000';
        $scope.new_dataset = function() {
            $http({method: 'POST', url: server_url+'/api/v1/dataset/', params: {
                name: $scope.dataset_name,
                projections: $scope.destdir
            }}).
                success(function(data, status) {
                    $scope.response = data
                }).
                error(function(data, status) {
                    $scope.response = data
                });
        };
    });
