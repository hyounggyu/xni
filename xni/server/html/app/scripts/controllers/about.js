'use strict';

/**
 * @ngdoc function
 * @name xniApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the xniApp
 */
angular.module('xniApp')
  .controller('AboutCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
