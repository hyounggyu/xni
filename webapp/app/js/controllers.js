var remote = require('remote');
var dialog = remote.require('dialog');
var xniApp = angular.module('xniApp', []);

xniApp.controller('ImageShiftCtrl', function ($scope) {
    $scope.sayHello = function() {
        $scope.greeting  = dialog.showOpenDialog({ properties: ['openFile', 'openDirectory', 'multiSelections']});
    };
});
