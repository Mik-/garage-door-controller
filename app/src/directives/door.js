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
