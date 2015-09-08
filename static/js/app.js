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

}());

'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
  'ngRoute',
  'myApp.overview'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/overview'});
}]);

angular.module('myApp').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('overview/overview.tpl.html',
    "<div ng-repeat=\"door in vm.doorList\">{{ door.id }}. Door name: {{ door.name }} <span ng-show=door.state>state: {{ door.state }}</span> <span ng-show=door.intent>intent: {{ door.intent }}</span> <a href=\"\" ng-click=vm.triggerDoor(door.id) class=button>Trigger</a></div>{{ vm.result }}"
  );

}]);

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
    }])
    .controller('OverviewCtrl', ['doorListService', 'doorService', '$log',
      function(doorListService, doorService, $log) {
      var vm = this;

      doorListService.getDoorList()
        .then(function (data){
          vm.doorList = data;
          $log.debug(JSON.stringify(vm.doorList));

          for (var i = 0; i < vm.doorList.length; i++) {
            doorService.getDoorState(i)
              .then(function (data) {
                for (var j = 0; j < vm.doorList.length; j++) {
                  if (vm.doorList[j].name = data.name) {
                    vm.doorList[j].state = data.state;
                    vm.doorList[j].intent = data.intent;
                  }
                }
                $log.debug(JSON.stringify(data));
              })
              .catch(function (status) {
                vm.doorList[i].state = null;
                $log.error('doorService.getDoorState returns status ' + status);
              })
          }
        })
        .catch(function (status) {
          vm.doorList = [];
          $log.error('doorListService returns status ' + status);
        });

        vm.triggerDoor = function triggerDoor(index) {
          doorService.triggerDoor(index - 1)
            .then(function () {
              vm.result = 'Door triggered';
            })
            .catch(function (status) {
              $log.error('doorService.triggerDoor returns status ' + status);
              vm.result = 'doorService.triggerDoor returns status ' + status;
            })
        }
    }]);
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
