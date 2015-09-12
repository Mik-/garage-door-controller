(function() {
  'use strict';

  angular
    .module('myApp.doorDirective')
    .directive('door', DoorDirective);

  function DoorDirective(doorService, $log) {
    var doorId;

    return {
      restrict: 'E',
      templateUrl: 'directives/door.tpl.html',
      scope: {
        doorId: '=doorId'
      },
      link: function (scope, element, attrs) {
        doorId = scope.doorId;

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
          result = 'Door triggered';
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
}());
