(function () {
  'use strict';

  angular
    .module('myApp.sessionService')
    .factory('sessionService', sessionService);

  function sessionService($http, $rootScope, $log, $q) {
    var service = {
      getLoginState: getLoginState,
      login: login,
      logout: logout
    }

    return service;

    function getLoginState() {
      var deferred = $q.defer();

      $http.get('/session')
        .success(function (loginState) {
          deferred.resolve(loginState);
        })
        .error(function (data, status) {
          deferred.reject(status);
        });

      return deferred.promise;
    }

    function login(username, password) {
      var deferred = $q.defer();

      $http.post('/session', '{ "username": "' + username + '", "password": "' + password + '" }')
        .success(function (loginState) {
          deferred.resolve(loginState);
        })
        .error(function (data, status) {
          deferred.reject(status);
        });

      return deferred.promise;
    }

    function logout() {
      var deferred = $q.defer();

      $http.post('/session', '{ "logout": true }')
        .success(function (loginState) {
          deferred.resolve(loginState);
        })
        .error(function (data, status) {
          deferred.reject(status);
        });

      return deferred.promise;
    }
  }
})();
