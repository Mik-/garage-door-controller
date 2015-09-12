(function() {
  'use strict';

  angular
    .module('myApp.doorDirective', ['myApp.doorService']);
}());

(function() {
  'use strict';

  angular
    .module('myApp.log', ['myApp.logService']);

}());

(function () {
  'use strict';

  angular
    .module('myApp.overview', ['ngRoute', 'myApp.doorListService',
    'myApp.doorService']);

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
    'myApp.overview',
    'myApp.doorDirective',
    'myApp.log'
  ]).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.otherwise({redirectTo: '/overview'});
  }]);
}());

angular.module('myApp').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('directives/door.tpl.html',
    "<div class=door><span class=door__name>{{ doorId }}. Door name: {{ doorName }}</span> <span ng-show=state>state: {{ state }}</span> <span ng-show=intent>intent: {{ intent }}</span> <a class=button href=\"\" ng-click=triggerDoor()>Trigger</a><div ng-show=\"state !== 'OpenState'\" class=open-intent><a href=\"\" ng-click=setOpenIntent() class=button>Open intent</a></div><div ng-show=\"state !== 'ClosedState'\" class=close-intent><a href=\"\" ng-click=setCloseIntent() class=button>Close intent</a></div><div ng-show=infoText class=info-text>{{ infoText }}</div><div ng-show=errorText class=error-text>{{ errorText }}</div></div>"
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

  function DoorDirective(doorService, $log) {
    var doorId;
    var vm;

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

    function triggerDoor() {
      doorService.triggerDoor(doorId)
        .then(function() {
          vm.infoText = 'Door triggered';
          setTimeout(function() {
            vm.infoText = '';
          }, 5000);
        })
        .catch(function(status) {
          $log.error('doorService.triggerDoor returns status ' + status);
          vm.errorText = 'doorService.triggerDoor returns status ' + status;
        })
    }

    function setOpenIntent() {
      doorService.setOpenIntent(doorId)
        .then(function() {
          vm.infoText = 'Intent "open" set';
          setTimeout(function() {
            vm.infoText = '';
          }, 5000);
        })
        .catch(function(status) {
          $log.error('doorService.setOpenIntent returns status ' + status);
          vm.errorText = 'doorService.setOpenIntent returns status ' + status;
        })
    }

    function setCloseIntent() {
      doorService.setCloseIntent(doorId)
        .then(function() {
          vm.infoText = 'Intent "close" set';
          setTimeout(function() {
            vm.infoText = '';
          }, 5000);
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
