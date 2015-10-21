(function() {
  'use strict';

  angular.module('myApp.de_DE')
    .config(function ($translateProvider) {
      $translateProvider.translations('de_DE', {
        DOOR_LIST:            'Torliste',
        LOG:                  'Log',
        SESSION:              'Anmeldung',
        DOOR_NAME:            'Tor',
        STATE:                'Status',
        INTENT:               'Ziel',
        CLOSE_INTENT_SET:     'Ziel "Geschlossen" gesetzt',
        OPEN_INTENT_SET:      'Ziel "Offen" gesetzt',
        IDLE_INTENT_SET:      'Ziel "Leerlauf" gesetzt',
        DOOR_TRIGGERED:       'Tor angestoßen',
        LOGGED_IN:            'Du bist angemeldet',
        LOGIN_SUCCESSFUL:     'Login erfoglreich.',
        LOGIN_FAILED:         'Login fehlgeschlagen!',
        LOGOUT_SUCCESSFUL:    'Logout erfoglreich.',
        LOGOUT_FAILED:        'Logout fehlgeschlagen!',
        BUTTON_OPEN_DOOR:     'Tor öffnen',
        BUTTON_CLOSE_DOOR:    'Tor schließen',
        BUTTON_IDLE_INTENT:   'Ziel stoppen',
        BUTTON_TRIGGER_DOOR:  'Taster',
        BUTTON_LOGIN:         'Anmelden',
        BUTTON_LOGOUT:        'Abmelden'
      })
    });
}());
