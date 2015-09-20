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
    "<div class=door><span class=door__name>{{ doorId }}. {{ 'DOOR_NAME' | translate }}: {{ doorName }}</span> <span ng-show=state>{{ 'STATE' | translate }}: {{ state }}</span> <span ng-show=intent>{{ 'INTENT' | translate }}: {{ intent }}</span><div class=open-intent ng-show=\"state !== 'OpenState'\"><two-stage-button inactive-class=\"button button__open\" active-class=\"button button__open\" click-action=setOpenIntent()>{{ 'BUTTON_OPEN_DOOR' | translate }}</two-stage-button></div><div class=close-intent ng-show=\"state !== 'ClosedState'\"><two-stage-button inactive-class=\"button button__close\" active-class=\"button button__close\" click-action=setCloseIntent()>{{ 'BUTTON_CLOSE_DOOR' | translate }}</two-stage-button></div><div class=idle-intent ng-show=\"intent !== 'IdleIntent'\"><two-stage-button inactive-class=\"button button__idle\" active-class=\"button button__idle\" click-action=setIdleIntent()>{{ 'BUTTON_IDLE_INTENT' | translate }}</two-stage-button></div><div class=trigger><two-stage-button inactive-class=\"button button__trigger\" active-class=\"button button__trigger\" click-action=triggerDoor()>{{ 'BUTTON_TRIGGER_DOOR' | translate }}</two-stage-button></div><div class=info-text ng-show=infoText>{{ infoText | translate }}</div><div class=error-text ng-show=errorText>{{ errorText | translate }}</div></div>"
  );


  $templateCache.put('log/log.tpl.html',
    "<pre>\n" +
    "{{ vm.log }}\n" +
    "</pre>"
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
        DOOR_NAME:            'Tor',
        STATE:                'Status',
        INTENT:               'Ziel',
        CLOSE_INTENT_SET:     'Ziel "Geschlossen" gesetzt',
        OPEN_INTENT_SET:      'Ziel "Offen" gesetzt',
        IDLE_INTENT_SET:      'Ziel "Leerlauf" gesetzt',
        DOOR_TRIGGERED:       'Tor angestoßen',
        BUTTON_OPEN_DOOR:     'Tor öffnen',
        BUTTON_CLOSE_DOOR:    'Tor schließen',
        BUTTON_IDLE_INTENT:   'Ziel stoppen',
        BUTTON_TRIGGER_DOOR:  'Taster'
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
        DOOR_NAME:            'Door name',
        STATE:                'state',
        INTENT:               'intent',
        CLOSE_INTENT_SET:     'Intent "close" set',
        OPEN_INTENT_SET:      'Intent "open" set',
        IDLE_INTENT_SET:      'Intent "idle" gesetzt',
        DOOR_TRIGGERED:       'Door triggered',
        BUTTON_OPEN_DOOR:     'Open door',
        BUTTON_CLOSE_DOOR:    'Close door',
        BUTTON_IDLE_INTENT:   'Stop intent',
        BUTTON_TRIGGER_DOOR:  'Trigger'
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
    .controller('OverviewCtrl', ['doorListService', 'doorService', '$log', OverviewCtrl]);

  function OverviewCtrl(doorListService, doorService, $log) {
    var vm = this;

    vm.triggerDoor = triggerDoor;

    activate();

    // ------------------

    function activate() {
      doorListService.getDoorList()
        .then(function(data) {
          vm.doorList = data;
          $log.debug(JSON.stringify(vm.doorList));
        })
        .catch(function(status) {
          vm.doorList = [];
          $log.error('doorListService returns status ' + status);
        });
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
