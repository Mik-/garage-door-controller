(function() {
  'use strict';

  describe('session service', function () {
    var sessionService, httpBackend;

    beforeEach(module('myApp.sessionService'));

    beforeEach(inject(function (_sessionService_, $httpBackend) {
      sessionService = _sessionService_;
      httpBackend = $httpBackend;
    }));

    afterEach(function() {
      httpBackend.verifyNoOutstandingExpectation();
      httpBackend.verifyNoOutstandingRequest();
    });

    it('should have an getLoginState function', function () {
      expect(angular.isFunction(sessionService.getLoginState)).toBe(true);
    });

    it('should have an login function', function () {
      expect(angular.isFunction(sessionService.login)).toBe(true);
    });

    it('should have an logut function', function () {
      expect(angular.isFunction(sessionService.logout)).toBe(true);
    });

    it('should return a login state', function () {
      var aLoginState = {
          loggedIn: false
        };

      httpBackend
        .whenGET('/session')
        .respond(aLoginState);

      sessionService.getLoginState()
        .then(function (data) {
          expect(data).toEqual(aLoginState);
        })
        .catch(function () {
          // this should be called
          expect(true).toBe(false);
        })

      httpBackend.flush();
    });

    it('should return an error on get login state', function () {
      httpBackend
        .whenGET('/session')
        .respond(500, '');

        sessionService.getLoginState()
        .then(function (data) {
          // this should not be called
          expect(true).toBe(false);
        })
        .catch(function (status) {
          expect(status).toEqual(500);
        });

      httpBackend.flush();
    });

    it('should send a correct login', function () {
      httpBackend
        .expectPOST('/session', { username: 'Test', password: 'test1'})
        .respond(200, '{ "loggedIn": true }');

      sessionService.login('Test', 'test1')
        .then(function (data) {
          expect(data.loggedIn).toBe(true);
        })
        .catch(function () {
          // this should not be called
          expect(true).toBe(false);
        })

      httpBackend.flush();
    });

    it('should send a wrong login', function () {
      httpBackend
        .expectPOST('/session', { username: 'Test', password: 'test1'})
        .respond(200, '{ "loggedIn": false }');

        sessionService.login('Test', 'test1')
        .then(function (data) {
          expect(data.loggedIn).toBe(false);
        })
        .catch(function (status) {
          // this should not be called
          expect(true).toBe(false);
        });

      httpBackend.flush();
    });

    it('should send a logout', function () {
      httpBackend
        .expectPOST('/session', { logout: true })
        .respond(200, '{ "loggedIn": false }');

        sessionService.logout()
        .then(function (data) {
          expect(data.loggedIn).toBe(false);
        })
        .catch(function (status) {
          // this should not be called
          expect(true).toBe(false);
        });

      httpBackend.flush();
    });
  });
}());
