(function () {
  'use strict';

  angular
    .module('myApp.doorService')
    .factory('doorService', doorService);

  function doorService($http, $rootScope, $log, $q) {
    var service = {
      getDoorState: getDoorState,
      triggerDoor: triggerDoor,
      setIntent: setIntent
    }

    return service;

    function getDoorState(index) {
      var deferred = $q.defer();

      $http.get('/door/' + index)
        .success(function (doorState) {
          deferred.resolve(doorState);
        })
        .error(function (data, status) {
          deferred.reject(status);
        });

      return deferred.promise;
    }

    function triggerDoor(index) {
      var deferred = $q.defer();

      $http.post('/door/' + index, '{ "trigger": true }')
        .success(function (doorState) {
          deferred.resolve();
        })
        .error(function (data, status) {
          deferred.reject(status);
        });

      return deferred.promise;
    }

    function setIntent(index, intent) {
      var deferred = $q.defer();

      $http.post('/door/' + index, '{ "intent": "' + intent + '" }')
        .success(function (doorState) {
          deferred.resolve();
        })
        .error(function (data, status) {
          deferred.reject(status);
        });

      return deferred.promise;
    }
  }
})();
