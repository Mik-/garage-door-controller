(function() {
  'use strict';

  angular.module('myApp.en_US')
    .config(function ($translateProvider) {
      $translateProvider.translations('en_US', {
        DOOR_LIST:            'Doorlist',
        LOG:                  'Log',
        DOOR_NAME:            'Door name',
        STATE:                'state',
        INTENT:               'intent',
        CLOSE_INTENT_SET:     'Intent "close" set',
        OPEN_INTENT_SET:      'Intent "open" set',
        DOOR_TRIGGERED:       'Door triggered',
        BUTTON_OPEN_DOOR:     'Open door',
        BUTTON_CLOSE_DOOR:    'Close door',
        BUTTON_TRIGGER_DOOR:  'Trigger'
      })
    });
}());
