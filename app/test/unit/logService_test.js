(function() {
  'use strict';

  describe('log service', function () {
    var logService, httpBackend;

    beforeEach(module('myApp.logService'));

    beforeEach(inject(function (_logService_, $httpBackend) {
      logService = _logService_;
      httpBackend = $httpBackend;
    }));

    afterEach(function() {
      httpBackend.verifyNoOutstandingExpectation();
      httpBackend.verifyNoOutstandingRequest();
    });

    it('should have an getLog function', function () {
      expect(angular.isFunction(logService.getLog)).toBe(true);
    });

    it('should return log data', function () {
      var someLogData = 'This is an log entry.';

      httpBackend
        .whenGET('/log')
        .respond(someLogData);

      logService.getLog()
        .then(function (data) {
          expect(data).toEqual(someLogData);
        })
        .catch(function () {
          // this should be called
          expect(true).toBe(false);
        })

      httpBackend.flush();
    });

    it('should return an error', function () {
      httpBackend
        .whenGET('/log')
        .respond(500, '');

      logService.getLog()
        .then(function (data) {
          // this should be called
          expect(true).toBe(false);
        })
        .catch(function (status) {
          expect(status).toEqual(500);
        });

      httpBackend.flush();
    });

  });

}());
