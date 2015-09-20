(function() {
  'use strict';

  angular.module('myApp.de_DE')
    .config(function ($translateProvider) {
      $translateProvider.translations('de_DE', {
        DOOR_LIST:            'Torliste',
        LOG:                  'Log',
        DOOR_NAME:            'Tor',
        STATE:                'Status',
        INTENT:               'Ziel',
        CLOSE_INTENT_SET:     'Ziel "Geschlossen" gesetzt',
        OPEN_INTENT_SET:      'Ziel "Offen" gesetzt',
        IDLE_INTENT_SET:      'Ziel "Leerlauf" gesetzt',
        DOOR_TRIGGERED:       'Tor angestoßen',
        BUTTON_OPEN_DOOR:     'Tor öffnen',
        BUTTON_CLOSE_DOOR:    'Tor schließen',
        BUTTON_IDLE_INTENT:   'Ziel stoppen',
        BUTTON_TRIGGER_DOOR:  'Taster'
      })
    });
}());
