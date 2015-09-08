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
