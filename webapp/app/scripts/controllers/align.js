'use strict';

/**
 * @ngdoc function
 * @name xniApp.controller:AlignCtrl
 * @description
 * # AlignCtrl
 * Controller of the xniApp
 */
angular.module('xniApp')
    .controller('AlignCtrl', function ($scope, $http, Dataset) {
        $scope.awesomeThings = [
            'HTML5 Boilerplate',
            'AngularJS',
            'Karma'
        ];
        $scope.shift = function() {
            $http({method: 'POST', url: '/api/v1/shift/', params: {
                imfiles: Dataset.imfiles,
                destdir: Dataset.destdir,
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
