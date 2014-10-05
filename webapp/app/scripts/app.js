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
    .factory('Dataset', function () {
        return {
            imfiles: null,
            destdir: null
        }
    })
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
