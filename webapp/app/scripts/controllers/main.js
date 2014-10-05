'use strict';

/**
 * @ngdoc function
 * @name xniApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the xniApp
 */
angular.module('xniApp')
  .controller('MainCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
