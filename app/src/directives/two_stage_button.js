(function() {
  'use strict';

  angular
    .module('myApp.twoStageButton')
    .directive('twoStageButton', TwoStageButton);


  function TwoStageButton($log, $timeout) {
    return {
      restrict: 'E',
      template: '<a href="" ng-click="onButtonClick()">' +
        '<i ng-hide="active" class="fa fa-toggle-off"></i>' +
        '<i ng-show="active" class="fa fa-toggle-on"></i>&nbsp;' +
        '<span ng-transclude></span></a>',
      transclude: true,
      scope: {
        clickAction: '&',
        inactiveClass: '@',
        activeClass: '@'
      },
      link: function (scope, element, attrs) {
        scope.clickCount = 0;
        scope.active = false;

        scope.deactivate = function deactivate() {
          scope.clickCount = 0;
          if (scope.activeClass) {
            element.find('a').removeClass(scope.activeClass);
          }
          if (scope.inactiveClass) {
            element.find('a').addClass(scope.inactiveClass);
          }
          scope.active = false;
        }

        scope.activate = function activate() {
          if (scope.inactiveClass) {
            element.find('a').removeClass(scope.inactiveClass);
          }
          if (scope.activeClass) {
            element.find('a').addClass(scope.activeClass);
          }
          scope.active = true;
          $timeout(function () {
              scope.deactivate();
          }, 5000);
        }

        scope.deactivate();

        scope.onButtonClick = function () {
          scope.clickCount = scope.clickCount + 1;

          $log.debug('TwoStageButton: clickCount = ' + scope.clickCount);

          if (scope.clickCount > 0) {
            scope.activate();
          }

          if (scope.clickCount > 1) {
            scope.deactivate();

            if (scope.clickAction) {
              $log.debug('clickAction() fired.');
              scope.clickAction();
            }
            else {
              $log.error('No click-action defined in directive TwoStageButton!');
            }
          }
        }
      }
    }
  }

}());
