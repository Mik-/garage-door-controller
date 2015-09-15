(function() {
  'use strict';

  angular
    .module('myApp.doorDirective', ['myApp.doorService', 'pascalprecht.translate']);
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
    "<div class=door><span class=door__name>{{ doorId }}. {{ 'DOOR_NAME' | translate }}: {{ doorName }}</span> <span ng-show=state>{{ 'STATE' | translate }}: {{ state }}</span> <span ng-show=intent>{{ 'INTENT' | translate }}: {{ intent }}</span><div class=open-intent ng-show=\"state !== 'OpenState'\"><a class=\"button button__open\" href=\"\" ng-click=setOpenIntent()>{{ 'BUTTON_OPEN_DOOR' | translate }}</a></div><div class=close-intent ng-show=\"state !== 'ClosedState'\"><a class=\"button button__close\" href=\"\" ng-click=setCloseIntent()>{{ 'BUTTON_CLOSE_DOOR' | translate }}</a></div><div class=trigger><a class=\"button button__trigger\" href=\"\" ng-click=triggerDoor()>{{ 'BUTTON_TRIGGER_DOOR' | translate }}</a></div><div class=info-text ng-show=infoText>{{ infoText | translate }}</div><div class=error-text ng-show=errorText>{{ errorText | translate }}</div></div>"
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

  function DoorDirective(doorService, $log, $interval) {
    var doorId;
    var vm;
    var hideTextInterval;

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

        element.on('$destroy', function () {
          if (angular.isDefined(hideTextInterval)) {
            $interval.cancel(hideTextInterval);
            hideTextInterval = undefined;
          }
        })

        doorService.getDoorState(doorId)
          .then(function(data) {
            $log.debug('doorDirective: ' + JSON.stringify(data));
            scope.doorName = data.name;
            scope.state = data.state;
            scope.intent = data.intent;

            $log.debug(JSON.stringify(data));
          })
          .catch(function(status) {
            scope.doorName = null;
            scope.state = null;
            scope.intent = null;

            $log.error('doorService.getDoorState returns status ' + status);
          });
      }
    }

    function clearMessages() {
      $interval.cancel(hideTextInterval);
      hideTextInterval = undefined;

      vm.errorText = '';
      vm.infoText = '';
    }

    function triggerDoor() {
      doorService.triggerDoor(doorId)
        .then(function() {
          clearMessages();
          vm.infoText = 'DOOR_TRIGGERED';

          hideTextInterval = $interval(clearMessages, 5000);
        })
        .catch(function(status) {
          $log.error('doorService.triggerDoor returns status ' + status);
          vm.errorText = 'doorService.triggerDoor returns status ' + status;
        })
    }

    function setOpenIntent() {
      doorService.setOpenIntent(doorId)
        .then(function() {
          clearMessages();
          vm.infoText = 'OPEN_INTENT_SET';

          hideTextInterval = $interval(clearMessages, 5000);
        })
        .catch(function(status) {
          $log.error('doorService.setOpenIntent returns status ' + status);
          vm.errorText = 'doorService.setOpenIntent returns status ' + status;
        })
    }

    function setCloseIntent() {
      doorService.setCloseIntent(doorId)
        .then(function() {
          clearMessages();
          vm.infoText = 'CLOSE_INTENT_SET';

          hideTextInterval = $interval(clearMessages, 5000);
        })
        .catch(function(status) {
          $log.error('doorService.setCloseIntent returns status ' + status);
          vm.errorText = 'doorService.setCloseIntent returns status ' + status;
        })
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
        DOOR_TRIGGERED:       'Tor angestoßen',
        BUTTON_OPEN_DOOR:     'Tor öffnen',
        BUTTON_CLOSE_DOOR:    'Tor schließen',
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
        DOOR_TRIGGERED:       'Door triggered',
        BUTTON_OPEN_DOOR:     'Open door',
        BUTTON_CLOSE_DOOR:    'Close door',
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
      setOpenIntent: setOpenIntent,
      setCloseIntent: setCloseIntent
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

    function setOpenIntent(index) {
      var deferred = $q.defer();

      $http.post('/door/' + index, '{ "intent": "open" }')
        .success(function (doorState) {
          deferred.resolve();
        })
        .error(function (data, status) {
          deferred.reject(status);
        });

      return deferred.promise;
    }

    function setCloseIntent(index) {
      var deferred = $q.defer();

      $http.post('/door/' + index, '{ "intent": "close" }')
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
