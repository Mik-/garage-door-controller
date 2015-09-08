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
