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
