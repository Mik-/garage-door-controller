(function() {
  'use strict';

  // Declare app level module which depends on views, and components
  angular.module('myApp', [
    'ngRoute',
    'pascalprecht.translate',
    'myApp.en_US',
    'myApp.de_DE',
    'myApp.overview',
    'myApp.doorDirective',
    'myApp.log'
  ]).
  config(['$routeProvider', '$translateProvider', function($routeProvider, $translateProvider) {
    $translateProvider.determinePreferredLanguage();
    $translateProvider.useSanitizeValueStrategy('escapeParameters');

    $routeProvider.otherwise({redirectTo: '/overview'});

  }]);
}());
