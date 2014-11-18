'use strict';

/**
 * @ngdoc service
 * @name xniApp.Dataset
 * @description
 * # Dataset
 * Factory in the xniApp.
 */
angular.module('xniApp')
  .factory('Dataset', function ($resource) {
    var server_url = 'http://127.0.0.1:8000';
    return $resource(server_url+'/api/v1/dataset/:datasetName', {datasetName: '@name'});
  });
