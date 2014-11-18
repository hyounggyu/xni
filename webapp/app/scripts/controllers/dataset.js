'use strict';

/**
 * @ngdoc function
 * @name xniApp.controller:DatasetCtrl
 * @description
 * # DatasetCtrl
 * Controller of the xniApp
 */
angular.module('xniApp')
  .controller('DatasetCtrl', function ($scope, Dataset) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
    Dataset.query(function(data) {
      $scope.datasets = data;
    });
  });
