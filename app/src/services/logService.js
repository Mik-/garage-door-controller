(function() {
  'use strict';

  angular
    .module('myApp.logService')
    .factory('logService', logService);

  function logService($http, $rootScope, $log, $q) {
    var service = {
      getLog: getLog
    }

    return service;

    function getLog() {
      var deferred = $q.defer();

      $http.get('/log')
        .success(function(log) {
          deferred.resolve(log);
        })
        .error(function(data, status) {
          deferred.reject(status);
        });

      return deferred.promise;
    }
  }
})();
