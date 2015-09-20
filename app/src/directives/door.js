(function() {
  'use strict';

  angular
    .module('myApp.doorDirective')
    .directive('door', DoorDirective);

  function DoorDirective(doorService, $log, $interval, $timeout) {
    var doorId;
    var vm;
    var hideMessageTimeout;
    var updateInterval;

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
        scope.setIdleIntent = setIdleIntent;

        element.on('$destroy', function () {
          if (hideMessageTimeout) {
            $timeout.cancel(hideMessageTimeout);
          }

          if (angular.isDefined(updateInterval)) {
            $interval.cancel(updateInterval);
          }
        });

        updateDoorState();
        updateInterval = $interval(updateDoorState, 2000);
      }
    }

    function updateDoorState() {
      doorService.getDoorState(vm.doorId)
        .then(function(data) {
          vm.doorName = data.name;
          vm.state = data.state;
          vm.intent = data.intent;
        })
        .catch(function(status) {
          vm.doorName = null;
          vm.state = null;
          vm.intent = null;

          $log.error('doorService.getDoorState returns status ' + status);
          showMessage('doorService.getDoorState returns status ' + status, 'error');
        });
    }

    function clearMessages() {
      vm.errorText = '';
      vm.infoText = '';
    }

    function showMessage(messageText, messageType) {
      if (hideMessageTimeout) {
        $timeout.cancel(hideMessageTimeout);
      }

      if (messageType === 'info') {
        vm.infoText = messageText;
      }
      else if (messageType === 'error') {
        vm.errorText = messageText;
      }

      hideMessageTimeout = $timeout(clearMessages, 5000);
    }

    function triggerDoor() {
      doorService.triggerDoor(doorId)
        .then(function() {
          showMessage('DOOR_TRIGGERED', 'info');
        })
        .catch(function(status) {
          $log.error('doorService.triggerDoor returns status ' + status);
          showMessage('doorService.triggerDoor returns status ' + status, 'error');
        })
    }

    function setOpenIntent() {
      doorService.setIntent(doorId, 'open')
        .then(function() {
          showMessage('OPEN_INTENT_SET', 'info');
        })
        .catch(function(status) {
          $log.error('doorService.setOpenIntent returns status ' + status);
          showMessage('doorService.setOpenIntent returns status ' + status, 'error');
        })
    }

    function setCloseIntent() {
      doorService.setIntent(doorId, 'close')
        .then(function() {
          showMessage('CLOSE_INTENT_SET', 'info');
        })
        .catch(function(status) {
          $log.error('doorService.setCloseIntent returns status ' + status);
          showMessage('doorService.setCloseIntent returns status ' + status, 'error');
        })
    }

    function setIdleIntent() {
      doorService.setIntent(doorId, 'idle')
        .then(function() {
          showMessage('IDLE_INTENT_SET', 'info');
        })
        .catch(function(status) {
          $log.error('doorService.setIdleIntent returns status ' + status);
          showMessage('doorService.setIdleIntent returns status ' + status, 'error');
        })
    }
  }
}());
