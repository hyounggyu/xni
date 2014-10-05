'use strict';

/**
 * @ngdoc overview
 * @name xniApp
 * @description
 * # xniApp
 *
 * Main module of the application.
 */
angular
  .module('xniApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/align', {
        templateUrl: 'views/align.html',
        controller: 'AlignCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
