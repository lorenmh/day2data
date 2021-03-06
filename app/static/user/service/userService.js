angular.module('user').factory('userService', ['$state', 'path', 'api',
  function($state, path, api) {
    var user = {};
    var logged_in = false;
    var login_observers = [];
    var logged_in_observers = [];
    var logout_observers = [];
    var error_observers = [];

    user.login_errors = null;
    user.id = null;

    user.observe_error = function(cb) {
      error_observers.push(cb);
    };

    user.observe_logged_in = function(cb) {
      logged_in_observers.push(cb);
    };

    user.observe_login = function(cb) {
      login_observers.push(cb);
    };

    user.observe_logout = function(cb) {
      logout_observers.push(cb);
    };

    var notify_login = function() {
      angular.forEach(login_observers, function(cb) {
        cb(user.id);
      });
    };

    var notify_logged_in = function() {
      angular.forEach(logged_in_observers, function(cb) {
        cb(logged_in);
      });
    };

    var notify_logout = function() {
      angular.forEach(logout_observers, function(cb) {
        cb();
      });
    };

    var notify_error = function() {
      angular.forEach(error_observers, function(cb) {
        cb(user.login_errors);
      });
    };

    var set_logged_in = function(bool) {
      logged_in = bool;
      notify_logged_in();
    };

    var set_id = function(id) {
      user.id = id;
      set_logged_in(true);
      notify_login();
    };

    var set_login_errors = function(errors) {
      user.login_errors = errors;
      notify_error();
    };

    user.logout = function() {
      api.logout()
        .success(function() {
          set_id(null);
          set_logged_in(false);
          notify_logout();
          $state.go(path.logout_redirect);
        });
    };

    user.login = function(id, password) {
      api.login(id, password)
        .success(function(d) {
          user.init(d.message);
        })
        .error(function(d) {
          set_login_errors(d.message);
        });
    };

    user.init = function(user) {
      if (user) {
        set_id(user.id);
        if ($state.current.name === 'root.home') {
          $state.go(path.login_redirect);
        }
      }
    };

    user.is_logged_in = function() {
      return logged_in;
    };

    return user;
}]);