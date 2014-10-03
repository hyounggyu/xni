'use strict';

var remote = require('remote');
var dialog = remote.require('dialog');
var xniApp = angular.module('xniApp', []);

var config = {};

xniApp.controller('ImageShiftCtrl', function ($scope, $http) {
    $scope.selectImageFiles = function() {
        config.image_files = dialog.showOpenDialog({ properties: ['openFile', 'multiSelections'] });
        $scope.image_files = config.image_files.length + ' files selected.';
    };
    $scope.selectPositionFile = function() {
        config.position_file = dialog.showOpenDialog({ properties: ['openFile'] });
        $scope.position_file = config.position_file;
    };
    $scope.selectDestDirectory = function() {
        config.dest_directory = dialog.showOpenDialog({ properties: ['openDirectory'] });
        $scope.dest_directory = config.dest_directory;
    };
    $scope.selectBackgroundFiles = function() {
        config.background_files = dialog.showOpenDialog({ properties: ['openFile', 'multiSelections'] });
        $scope.background_files = config.background_files;
    };
    $scope.selectDarkFiles = function() {
        config.dark_files = dialog.showOpenDialog({ properties: ['openFile', 'multiSelections'] });
        $scope.dark_files = config.dark_files;
    };
    $scope.run = function() {
        $http({method: 'POST', url: 'http://127.0.0.1:8000/shift/', params: { config: config }}).
            success(function(data, status) {
                $scope.response = data
            }).
            error(function(data, status) {
                $scope.response = data
            });
    };
});
