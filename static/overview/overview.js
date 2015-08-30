(function() {
  'use strict';

  angular
    .module('myApp.overview', ['ngRoute', 'myApp.doorListService', 'myApp.doorService'])
    .config(['$routeProvider', function($routeProvider) {
      $routeProvider.when('/overview', {
        templateUrl: 'overview/overview.html',
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
    }]);

})();
