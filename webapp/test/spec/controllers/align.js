'use strict';

describe('Controller: AlignCtrl', function () {

  // load the controller's module
  beforeEach(module('xniApp'));

  var AlignCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    AlignCtrl = $controller('AlignCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
