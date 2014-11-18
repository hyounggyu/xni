'use strict';

/**
 * @ngdoc function
 * @name xniApp.controller:DatasetCtrl
 * @description
 * # DatasetCtrl
 * Controller of the xniApp
 */
angular.module('xniApp')
  .controller('DatasetCtrl', function ($scope, $resource) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
    var server_url = 'http://127.0.0.1:8000';
    var dataset = $resource(server_url+'/api/v1/dataset/:datasetName', {datasetName: '@name'});
    dataset.query(function(data) {
      $scope.datasets = data;
    });
  });
