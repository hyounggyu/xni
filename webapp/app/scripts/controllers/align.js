'use strict';

/**
 * @ngdoc function
 * @name xniApp.controller:AlignCtrl
 * @description
 * # AlignCtrl
 * Controller of the xniApp
 */
angular.module('xniApp')
  .controller('AlignCtrl', function ($scope, Dataset) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
    Dataset.query(function(data) {
      $scope.datasets = data;
    });
  });
