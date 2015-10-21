(function() {
  'use strict';

  angular
    .module('myApp.doorDirective', ['myApp.doorService', 'pascalprecht.translate']);

  angular
    .module('myApp.twoStageButton', []);
}());

(function () {
  'use strict';

  angular
    .module('myApp.en_US', ['pascalprecht.translate']);

  angular
    .module('myApp.de_DE', ['pascalprecht.translate']);

})();

(function() {
  'use strict';

  angular
    .module('myApp.log', ['myApp.logService']);

}());

(function () {
  'use strict';

  angular
    .module('myApp.login', ['ngRoute', 'myApp.sessionService',
      'pascalprecht.translate']);

})();

(function () {
  'use strict';

  angular
    .module('myApp.overview', ['ngRoute', 'myApp.doorListService',
      'myApp.doorService', 'pascalprecht.translate']);

})();

(function() {
  'use strict';

  angular
    .module('myApp.doorListService', []);

  angular
    .module('myApp.doorService', []);

  angular
    .module('myApp.logService', []);

  angular
    .module('myApp.sessionService', []);

}());

(function() {
  'use strict';

  // Declare app level module which depends on views, and components
  angular.module('myApp', [
    'ngRoute',
    'pascalprecht.translate',
    'myApp.en_US',
    'myApp.de_DE',
    'myApp.overview',
    'myApp.login',
    'myApp.doorDirective',
    'myApp.twoStageButton',
    'myApp.log'
  ]).
  config(['$routeProvider', '$translateProvider', function($routeProvider, $translateProvider) {
    $translateProvider.determinePreferredLanguage();
    $translateProvider.useSanitizeValueStrategy('escapeParameters');

    $routeProvider.otherwise({redirectTo: '/overview'});

  }]);
}());

angular.module('myApp').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('directives/door.tpl.html',
    "<div class=door><span class=door__name>{{ doorId }}. {{ 'DOOR_NAME' | translate }}: {{ doorName }}</span> <span ng-show=state>{{ 'STATE' | translate }}: {{ state }}</span> <span ng-show=intent>{{ 'INTENT' | translate }}: {{ intent }}</span><div class=open-intent ng-show=\"state !== 'OpenState'\"><two-stage-button inactive-class=\"button button__open\" active-class=\"button button__open button__armed\" click-action=setOpenIntent()>{{ 'BUTTON_OPEN_DOOR' | translate }}</two-stage-button></div><div class=close-intent ng-show=\"state !== 'ClosedState'\"><two-stage-button inactive-class=\"button button__close\" active-class=\"button button__close button__armed\" click-action=setCloseIntent()>{{ 'BUTTON_CLOSE_DOOR' | translate }}</two-stage-button></div><div class=idle-intent ng-show=\"intent !== 'IdleIntent'\"><two-stage-button inactive-class=\"button button__idle\" active-class=\"button button__idle button__armed\" click-action=setIdleIntent()>{{ 'BUTTON_IDLE_INTENT' | translate }}</two-stage-button></div><div class=trigger><two-stage-button inactive-class=\"button button__trigger\" active-class=\"button button__trigger button__armed\" click-action=triggerDoor()>{{ 'BUTTON_TRIGGER_DOOR' | translate }}</two-stage-button></div><div class=info-text ng-show=infoText>{{ infoText | translate }}</div><div class=error-text ng-show=errorText>{{ errorText | translate }}</div></div>"
  );


  $templateCache.put('log/log.tpl.html',
    "<pre>\n" +
    "{{ vm.log }}\n" +
    "</pre>"
  );


  $templateCache.put('login/login.tpl.html',
    "<form ng-hide=vm.loggedIn ng-submit=vm.doLogin() id=login_form><label>Username <input name=username ng-model=vm.username></label><label>Password <input name=password type=password ng-model=vm.password></label><button type=submit class=button>{{ 'BUTTON_LOGIN' | translate }}</button></form><div ng-show=vm.loggedIn>{{ 'LOGGED_IN' | translate }}. <a href=\"\" ng-click=vm.doLogout() class=button>{{ 'BUTTON_LOGOUT' | translate }}</a></div><div class=info-text ng-show=vm.infoText>{{ vm.infoText | translate }}</div><div class=error-text ng-show=vm.errorText>{{ vm.errorText | translate }}</div>"
  );


  $templateCache.put('overview/overview.tpl.html',
    "<div class=door-list ng-repeat=\"door in vm.doorList\"><door door-id=door.id></door></div>"
  );

}]);

(function() {
  'use strict';

  angular
    .module('myApp.doorDirective')
    .directive('door', DoorDirective);

  function DoorDirective(doorService, $log, $interval, $timeout) {
    var doorId;
    var vm;
    var hideMessageTimeout;
    var updateInterval;

    return {
      restrict: 'E',
      templateUrl: 'directives/door.tpl.html',
      scope: {
        doorId: '=doorId'
      },
      link: function (scope, element, attrs) {
        doorId = scope.doorId;
        vm = scope;
        scope.triggerDoor = triggerDoor;
        scope.setOpenIntent = setOpenIntent;
        scope.setCloseIntent = setCloseIntent;
        scope.setIdleIntent = setIdleIntent;

        element.on('$destroy', function () {
          if (hideMessageTimeout) {
            $timeout.cancel(hideMessageTimeout);
          }

          if (angular.isDefined(updateInterval)) {
            $interval.cancel(updateInterval);
          }
        });

        updateDoorState();
        updateInterval = $interval(updateDoorState, 2000);
      }
    }

    function updateDoorState() {
      doorService.getDoorState(vm.doorId)
        .then(function(data) {
          vm.doorName = data.name;
          vm.state = data.state;
          vm.intent = data.intent;
        })
        .catch(function(status) {
          vm.doorName = null;
          vm.state = null;
          vm.intent = null;

          $log.error('doorService.getDoorState returns status ' + status);
          showMessage('doorService.getDoorState returns status ' + status, 'error');
        });
    }

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

    function triggerDoor() {
      doorService.triggerDoor(doorId)
        .then(function() {
          showMessage('DOOR_TRIGGERED', 'info');
        })
        .catch(function(status) {
          $log.error('doorService.triggerDoor returns status ' + status);
          showMessage('doorService.triggerDoor returns status ' + status, 'error');
        })
    }

    function setOpenIntent() {
      doorService.setIntent(doorId, 'open')
        .then(function() {
          showMessage('OPEN_INTENT_SET', 'info');
        })
        .catch(function(status) {
          $log.error('doorService.setOpenIntent returns status ' + status);
          showMessage('doorService.setOpenIntent returns status ' + status, 'error');
        })
    }

    function setCloseIntent() {
      doorService.setIntent(doorId, 'close')
        .then(function() {
          showMessage('CLOSE_INTENT_SET', 'info');
        })
        .catch(function(status) {
          $log.error('doorService.setCloseIntent returns status ' + status);
          showMessage('doorService.setCloseIntent returns status ' + status, 'error');
        })
    }

    function setIdleIntent() {
      doorService.setIntent(doorId, 'idle')
        .then(function() {
          showMessage('IDLE_INTENT_SET', 'info');
        })
        .catch(function(status) {
          $log.error('doorService.setIdleIntent returns status ' + status);
          showMessage('doorService.setIdleIntent returns status ' + status, 'error');
        })
    }
  }
}());

(function() {
  'use strict';

  angular
    .module('myApp.twoStageButton')
    .directive('twoStageButton', TwoStageButton);


  function TwoStageButton($log, $timeout) {
    return {
      restrict: 'E',
      template: '<a href="" ng-click="onButtonClick()">' +
        '<i ng-hide="active" class="fa fa-toggle-off"></i>' +
        '<i ng-show="active" class="fa fa-toggle-on"></i>&nbsp;' +
        '<span ng-transclude></span></a>',
      transclude: true,
      scope: {
        clickAction: '&',
        inactiveClass: '@',
        activeClass: '@'
      },
      link: function (scope, element, attrs) {
        scope.clickCount = 0;
        scope.active = false;

        scope.deactivate = function deactivate() {
          scope.clickCount = 0;
          if (scope.activeClass) {
            element.find('a').removeClass(scope.activeClass);
          }
          if (scope.inactiveClass) {
            element.find('a').addClass(scope.inactiveClass);
          }
          scope.active = false;
        }

        scope.activate = function activate() {
          if (scope.inactiveClass) {
            element.find('a').removeClass(scope.inactiveClass);
          }
          if (scope.activeClass) {
            element.find('a').addClass(scope.activeClass);
          }
          scope.active = true;
          $timeout(function () {
              scope.deactivate();
          }, 5000);
        }

        scope.deactivate();

        scope.onButtonClick = function () {
          scope.clickCount = scope.clickCount + 1;

          $log.debug('TwoStageButton: clickCount = ' + scope.clickCount);

          if (scope.clickCount > 0) {
            scope.activate();
          }

          if (scope.clickCount > 1) {
            scope.deactivate();

            if (scope.clickAction) {
              $log.debug('clickAction() fired.');
              scope.clickAction();
            }
            else {
              $log.error('No click-action defined in directive TwoStageButton!');
            }
          }
        }
      }
    }
  }

}());

(function() {
  'use strict';

  angular.module('myApp.de_DE')
    .config(function ($translateProvider) {
      $translateProvider.translations('de_DE', {
        DOOR_LIST:            'Torliste',
        LOG:                  'Log',
        SESSION:              'Anmeldung',
        DOOR_NAME:            'Tor',
        STATE:                'Status',
        INTENT:               'Ziel',
        CLOSE_INTENT_SET:     'Ziel "Geschlossen" gesetzt',
        OPEN_INTENT_SET:      'Ziel "Offen" gesetzt',
        IDLE_INTENT_SET:      'Ziel "Leerlauf" gesetzt',
        DOOR_TRIGGERED:       'Tor angestoßen',
        LOGGED_IN:            'Du bist angemeldet',
        LOGIN_SUCCESSFUL:     'Login erfoglreich.',
        LOGIN_FAILED:         'Login fehlgeschlagen!',
        LOGOUT_SUCCESSFUL:    'Logout erfoglreich.',
        LOGOUT_FAILED:        'Logout fehlgeschlagen!',
        BUTTON_OPEN_DOOR:     'Tor öffnen',
        BUTTON_CLOSE_DOOR:    'Tor schließen',
        BUTTON_IDLE_INTENT:   'Ziel stoppen',
        BUTTON_TRIGGER_DOOR:  'Taster',
        BUTTON_LOGIN:         'Anmelden',
        BUTTON_LOGOUT:        'Abmelden'
      })
    });
}());

(function() {
  'use strict';

  angular.module('myApp.en_US')
    .config(function ($translateProvider) {
      $translateProvider.translations('en_US', {
        DOOR_LIST:            'Doorlist',
        LOG:                  'Log',
        SESSION:              'Session',
        DOOR_NAME:            'Door name',
        STATE:                'state',
        INTENT:               'intent',
        CLOSE_INTENT_SET:     'Intent "close" set',
        OPEN_INTENT_SET:      'Intent "open" set',
        IDLE_INTENT_SET:      'Intent "idle" gesetzt',
        DOOR_TRIGGERED:       'Door triggered',
        LOGGED_IN:            'You are logged in',
        LOGIN_SUCCESSFUL:     'Login successful.',
        LOGIN_FAILED:         'Login failed!',
        LOGOUT_SUCCESSFUL:    'Logout successful.',
        LOGOUT_FAILED:        'Logout failed!',
        BUTTON_OPEN_DOOR:     'Open door',
        BUTTON_CLOSE_DOOR:    'Close door',
        BUTTON_IDLE_INTENT:   'Stop intent',
        BUTTON_TRIGGER_DOOR:  'Trigger',
        BUTTON_LOGIN:         'Login',
        BUTTON_LOGOUT:        'Logout'
      })
    });
}());

(function() {
  'use strict';

  angular
    .module('myApp.log')
    .config(['$routeProvider', function($routeProvider) {
      $routeProvider.when('/log', {
        templateUrl: 'log/log.tpl.html',
        controller: 'LogCtrl',
        controllerAs: 'vm'
      });
    }]);

  angular
    .module('myApp.log')
    .controller('LogCtrl', ['logService', '$log', LogCtrl]);

  function LogCtrl(logService, $log) {
    var vm = this;

    activate();

    // --------

    function activate() {
      logService.getLog()
        .then(function(data) {
          vm.log = data;
        })
        .catch(function(status) {
          $log.error('doorListService returns status ' + status);
          vm.log = 'logService returns status ' + status;
        });
    }
  }
})();

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

(function() {
  'use strict';

  angular
    .module('myApp.overview')
    .config(['$routeProvider', function($routeProvider) {
      $routeProvider.when('/overview', {
        templateUrl: 'overview/overview.tpl.html',
        controller: 'OverviewCtrl',
        controllerAs: 'vm'
      });
    }]);

  angular
    .module('myApp.overview')
    .controller('OverviewCtrl', ['doorListService', 'doorService',
      'sessionService', '$location', '$log', OverviewCtrl]);

  function OverviewCtrl(doorListService, doorService, sessionService, $location, $log) {
    var vm = this;

    vm.triggerDoor = triggerDoor;

    activate();

    // ------------------

    function activate() {
      sessionService.getLoginState()
        .then(function (data) {
          if (data.loggedIn == true) {
            doorListService.getDoorList()
              .then(function(data) {
                vm.doorList = data;
                $log.debug(JSON.stringify(vm.doorList));
              })
              .catch(function(status) {
                vm.doorList = [];
                $log.error('doorListService returns status ' + status);
              });
          } else {
            // Not logged in. Redirect to login page
            $location.path('/login');
          }
        })
        .catch(function (status) {
          vm.doorList = [];
        })
    }

    function triggerDoor(index) {
      doorService.triggerDoor(index - 1)
        .then(function() {
          vm.result = 'Door triggered';
          setTimeout(function(vm) {
            vm.result = '';
          }, 5000, vm);
        })
        .catch(function(status) {
          $log.error('doorService.triggerDoor returns status ' + status);
          vm.result = 'doorService.triggerDoor returns status ' + status;
        })
    }
  }
})();

(function () {
  'use strict';

  angular
    .module('myApp.doorListService')
    .factory('doorListService', doorListService);

  function doorListService($http, $rootScope, $log, $q) {
    var service = {
      getDoorList: getDoorList
    }

    return service;

    function getDoorList() {
      var deferred = $q.defer();

      $http.get('/doors')
        .success(function (doorList) {
          $log.debug(JSON.stringify(doorList));
          deferred.resolve(doorList.doors);
        })
        .error(function (data, status) {
          deferred.reject(status);
        });

      return deferred.promise;
    }
  }
})();

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
