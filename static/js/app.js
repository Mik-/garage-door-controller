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
    'myApp.log'
  ]).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.otherwise({redirectTo: '/overview'});
  }]);
}());

angular.module('myApp').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('log/log.tpl.html',
    "<pre>\n" +
    "{{ vm.log }}\n" +
    "</pre>"
  );


  $templateCache.put('overview/overview.tpl.html',
    "<div ng-repeat=\"door in vm.doorList\"><span class=door__name>{{ door.id }}. Door name: {{ door.name }}</span> <span ng-show=door.state>state: {{ door.state }}</span> <span ng-show=door.intent>intent: {{ door.intent }}</span> <a href=\"\" ng-click=vm.triggerDoor(door.id) class=button>Trigger</a></div>{{ vm.result }}"
  );

}]);

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

          for (var i = 0; i < vm.doorList.length; i++) {
            doorService.getDoorState(i)
              .then(function(data) {
                for (var j = 0; j < vm.doorList.length; j++) {
                  if (vm.doorList[j].name = data.name) {
                    vm.doorList[j].state = data.state;
                    vm.doorList[j].intent = data.intent;
                  }
                }
                $log.debug(JSON.stringify(data));
              })
              .catch(function(status) {
                vm.doorList[i].state = null;
                $log.error('doorService.getDoorState returns status ' + status);
              })
          }
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
      triggerDoor: triggerDoor
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
