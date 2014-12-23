angular.module('user').factory('userService', ['$state', 'path', 'api',
  function($state, path, api) {
    var user = {};
    var logged_in = false;
    var login_observers = [];
    var logout_observers = [];
    var error_observers = [];

    user.login_errors = null;
    user.id = null;

    user.observe_error = function(cb) {
      error_observers.push(cb);
    };

    user.observe_login = function(cb) {
      login_observers.push(cb);
    };

    user.observe_logout = function(cb) {
      logout_observers.push(cb);
    };

    var notify_login = function() {
      angular.forEach(login_observers, function(cb) {
        cb();
      });
    };

    var notify_logout = function() {
      angular.forEach(logout_observers, function(cb) {
        cb();
      });
    };

    var notify_error = function() {
      angular.forEach(error_observers, function(cb) {
        cb();
      });
    };

    var set_id = function(id) {
      user.id = id;
      logged_in = true;
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
          logged_in = false;
          notify_logout();
          $state.go(path.logout_redirect);
        });
    };

    user.login = function(id, password) {
      api.login(id, password)
        .success(function(d) {
          user.init(d.message);
          $state.go(path.login_redirect);
        })
        .error(function(d) {
          set_login_errors(d.message);
        });
    };

    user.init = function(user) {
      if (user) {
        set_id(user.id);
      }
    };

    user.is_logged_in = function() {
      return logged_in;
    };

    return user;
}]);