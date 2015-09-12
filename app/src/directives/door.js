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
