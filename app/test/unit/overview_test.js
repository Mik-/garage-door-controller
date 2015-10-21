'use strict';

describe('myApp.overview module', function() {

  // beforeEach(module('myApp.doorDirective'));
  // beforeEach(module('myApp.doorService'));
  // beforeEach(module('pascalprecht.translate'));
  beforeEach(module('myApp.overview'));
  beforeEach(module('myApp.sessionService'));

  describe('overview controller', function(){

    it('should ....', inject(function($controller) {
      //spec body
      var overviewCtrl = $controller('OverviewCtrl');
      expect(overviewCtrl).toBeDefined();
    }));

  });
});
