(function() {
  'use strict';

  angular.module('myApp.en_US')
    .config(function ($translateProvider) {
      $translateProvider.translations('en_US', {
        DOOR_LIST:            'Doorlist',
        LOG:                  'Log',
        SESSION:              'Session',
        DOOR_NAME:            'Door name',
        STATE:                'state',
        INTENT:               'intent',
        CLOSE_INTENT_SET:     'Intent "close" set',
        OPEN_INTENT_SET:      'Intent "open" set',
        IDLE_INTENT_SET:      'Intent "idle" gesetzt',
        DOOR_TRIGGERED:       'Door triggered',
        LOGGED_IN:            'You are logged in',
        LOGIN_SUCCESSFUL:     'Login successful.',
        LOGIN_FAILED:         'Login failed!',
        LOGOUT_SUCCESSFUL:    'Logout successful.',
        LOGOUT_FAILED:        'Logout failed!',
        BUTTON_OPEN_DOOR:     'Open door',
        BUTTON_CLOSE_DOOR:    'Close door',
        BUTTON_IDLE_INTENT:   'Stop intent',
        BUTTON_TRIGGER_DOOR:  'Trigger',
        BUTTON_LOGIN:         'Login',
        BUTTON_LOGOUT:        'Logout'
      })
    });
}());
