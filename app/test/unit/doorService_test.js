(function() {
  'use strict';

  describe('door service', function () {
    var doorService, httpBackend;

    beforeEach(module('myApp.doorService'));

    beforeEach(inject(function (_doorService_, $httpBackend) {
      doorService = _doorService_;
      httpBackend = $httpBackend;
    }));

    afterEach(function() {
      httpBackend.verifyNoOutstandingExpectation();
      httpBackend.verifyNoOutstandingRequest();
    });

    it('should have an getDoorState function', function () {
      expect(angular.isFunction(doorService.getDoorState)).toBe(true);
    });

    it('should have an triggerDoor function', function () {
      expect(angular.isFunction(doorService.triggerDoor)).toBe(true);
    });

    it('should have an setIntent function', function () {
      expect(angular.isFunction(doorService.setIntent)).toBe(true);
    });

    it('should return a door state', function () {
      var aDoorState = {
          name: "Test Door 1",
          state: "IntermediateState",
          intent: "IdleIntent"
        };

      httpBackend
        .whenGET('/door/1')
        .respond(aDoorState);

      doorService.getDoorState(1)
        .then(function (data) {
          expect(data).toEqual(aDoorState);
        })
        .catch(function () {
          // this should be called
          expect(true).toBe(false);
        })

      httpBackend.flush();
    });

    it('should return an error on get door state', function () {
      httpBackend
        .whenGET('/door/2')
        .respond(500, '');

        doorService.getDoorState(2)
        .then(function (data) {
          // this should be called
          expect(true).toBe(false);
        })
        .catch(function (status) {
          expect(status).toEqual(500);
        });

      httpBackend.flush();
    });

    it('should send a door trigger', function () {
      httpBackend
        .expectPOST('/door/3', { trigger: true})
        .respond(200, '');

      doorService.triggerDoor(3)
        .then(function (data) {
          expect(true).toBe(true);
        })
        .catch(function () {
          // this should be called
          expect(true).toBe(false);
        })

      httpBackend.flush();
    });

    it('should return an error on post trigger', function () {
      httpBackend
        .expectPOST('/door/2', { trigger: true})
        .respond(500, '');

        doorService.triggerDoor(2)
        .then(function (data) {
          // this should be called
          expect(true).toBe(false);
        })
        .catch(function (status) {
          expect(status).toEqual(500);
        });

      httpBackend.flush();
    });

    it('should send an intent', function () {
      httpBackend
        .expectPOST('/door/4', { intent: 'idle'})
        .respond(200, '');

      doorService.setIntent(4, 'idle')
        .then(function (data) {
          expect(true).toBe(true);
        })
        .catch(function () {
          // this should be called
          expect(true).toBe(false);
        })

      httpBackend.flush();
    });


    it('should return an error on post intent', function () {
      httpBackend
        .expectPOST('/door/2', { intent: 'sleep'})
        .respond(500, '');

        doorService.setIntent(2, 'sleep')
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
