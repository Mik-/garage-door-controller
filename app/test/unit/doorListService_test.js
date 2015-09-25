(function() {
  'use strict';

  describe('door list service', function () {
    var doorListService, httpBackend;

    beforeEach(module('myApp.doorListService'));

    beforeEach(inject(function (_doorListService_, $httpBackend) {
      doorListService = _doorListService_;
      httpBackend = $httpBackend;
    }));

    afterEach(function() {
      httpBackend.verifyNoOutstandingExpectation();
      httpBackend.verifyNoOutstandingRequest();
    });

    it('should have an getDoorList function', function () {
      expect(angular.isFunction(doorListService.getDoorList)).toBe(true);
    });

    it('should return a list of doors', function () {
      httpBackend
        .whenGET('/doors')
        .respond({
            doors: [
              {
                id: "1",
                name: "Test Door 1"
              }
            ]
          });

      doorListService.getDoorList()
        .then(function (data) {
          expect(data.length).toEqual(1);
          expect(data[0].id).toEqual('1');
          expect(data[0].name).toEqual('Test Door 1');
        })
        .catch(function () {
          // this should be called
          expect(true).toBe(false);
        })

      httpBackend.flush();
    });

    it('should return an error', function () {
      httpBackend
        .whenGET('/doors')
        .respond(500, '');

      doorListService.getDoorList()
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
