(function() {
  'use strict';

  angular
    .module('myApp.login')
    .config(['$routeProvider', function($routeProvider) {
      $routeProvider.when('/login', {
        templateUrl: 'login/login.tpl.html',
        controller: 'LoginCtrl',
        controllerAs: 'vm'
      });
    }]);

  angular
    .module('myApp.login')
    .controller('LoginCtrl', ['sessionService', '$log', '$timeout', '$q', LoginCtrl]);

  function LoginCtrl(sessionService, $log, $timeout, $q) {
    var vm = this;
    var hideMessageTimeout;

    vm.doLogin = doLogin;
    vm.doLogout = doLogout;
    vm.loggedIn = false;

    activate();

    // ------------------

    function clearMessages() {
      vm.errorText = '';
      vm.infoText = '';
    }

    function showMessage(messageText, messageType) {
      if (hideMessageTimeout) {
        $timeout.cancel(hideMessageTimeout);
      }

      if (messageType === 'info') {
        vm.infoText = messageText;
      }
      else if (messageType === 'error') {
        vm.errorText = messageText;
      }

      hideMessageTimeout = $timeout(clearMessages, 5000);
    }

    function getSessionState () {
      var deferred = $q.defer();

      sessionService.getLoginState()
        .then(function(data) {
          vm.loginState = data;
          vm.loggedIn = vm.loginState.loggedIn;
        })
        .catch(function(status) {
          vm.loginState = [];
          $log.error('doorListService returns status ' + status);
        })
        .finally(function () {
          deferred.resolve(vm.loggedIn);
        });

      return deferred.promise;
    }

    function activate() {
        getSessionState();
    }

    function doLogin() {
      sessionService.login(vm.username, vm.password)
        .then(function() {
          getSessionState()
            .then(function () {
              if (vm.loggedIn === true) {
                showMessage('LOGIN_SUCCESSFUL', 'info');
              } else {
                showMessage('LOGIN_FAILED', 'error');
              }
            });
        })
        .catch(function(status) {
          $log.error('sessionService.login returns status ' + status);
          vm.result = 'sessionService.login returns status ' + status;
        })
    }

    function doLogout() {
      sessionService.logout()
        .then(function() {
          getSessionState()
            .then(function () {
              if (vm.loggedIn === false) {
                showMessage('LOGOUT_SUCCESSFUL', 'info');
              } else {
                showMessage('LOGOUT_FAILED', 'error');
              }
            });
        })
        .catch(function(status) {
          $log.error('sessionService.logout returns status ' + status);
          vm.result = 'sessionService.logout returns status ' + status;
        })
    }
  }
})();
