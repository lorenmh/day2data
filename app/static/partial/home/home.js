angular.module('app').controller('HomeCtrl', [
          '$scope', 'api', 'path',
  function($scope, api, path){
    $scope.test = "World";
    api.get(path.api.build({ user: 'foo', record: 1, set: 1})).success(function(d) {
      console.log(d);
      $scope.test = d;
    });

  var line_animation = function(dur, step) {
      return function(selector) {
      var path, length, map;
      
      path = document.querySelector(selector);
      
      length = (function(p) {
        var dx, dy;
        dx = + p.getAttribute('x1') - p.getAttribute('x2');
        dy = + p.getAttribute('y1') - p.getAttribute('y2');
        return Math.sqrt( (dx * dx) + (dy * dy) );
      })(path);
 
      map = {};
 
      map.then = function(next) {
        map.next = next.anim;
        return next;
      };
 
      map.anim = function() {
        
        var init_t, called_next;
 
        init_t = Date.now();
 
        // initialize
        path.style.strokeDashoffset = length;
        path.style.strokeDasharray = length + ' ' + length;
 
 
        (function draw() {
        var progress = ( Date.now() - init_t ) / dur;
        if (progress < 1) {
          path.style.strokeDashoffset = Math.floor( length * progress );
          setTimeout(draw, step);
        } else if (!called_next) {
          path.style.strokeDashoffset = length;
          called_next = true;
          if (map.next) {
            map.next();
          }
        }
        })();
      };
 
      return map;
 
      };
 
    };
 
    var circle_animation = function(dur, step, final_r) {
      return function(selector) {
      var  path, map;
 
      path = document.querySelector(selector);
 
      map = {};
 
      map.then = function(next) {
        map.next = next.anim;
        return next;
      };
 
      map.anim = function() {
        
        var init_t, called_next;
 
        init_t = Date.now();
 
        // initialize
        path.setAttribute('r', 0);
 
 
        (function draw() {
        var progress = ( Date.now() - init_t ) / dur;
        console.log(progress);
        if (progress < 1) {
          path.setAttribute('r', final_r * progress );
          setTimeout(draw, step);
        } else if (!called_next) {
          path.setAttribute('r', final_r);
          
          called_next = true;
          if (map.next) {
          map.next();
          }
        }
        })();
      };
 
      return map;
 
      };
    };
 
    var text_animation = function(dur, step, dist) {
      return function(selector) {
      var  el, map;
 
      el = document.querySelector(selector);
 
      map = {};
 
      map.then = function(next) {
        map.next = next.anim;
        return next;
      };
 
      map.anim = function() {
        
        var init_t, called_next;
 
        init_t = Date.now();
 
        // initialize
        el.style.top = '0px';
 
        (function draw() {
          var progress = ( Date.now() - init_t ) / dur;
          if (progress < 0.5) {
            el.style.top = ((progress * -2) * dist) + 'px';
            setTimeout(draw, step);
          } else if (progress < 1) {
            el.style.top =  (((progress - 0.5) * 2 * dist) - dist) + 'px';
            setTimeout(draw, step);
          } else if (!called_next) {
            el.style.top = '0px';
            
            called_next = true;
            if (map.next) {
              map.next();
            }
          }
        })();
      };
 
      return map;
 
      };
    };
 
    var step, circle_dur, line_dur, text_dur, dist, final_r, c_a, l_a, t_a;
    var a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14;
 
    step = 20;
    circle_dur = 100;
    final_r = 10;
    line_dur = 200;
    text_dur = 250;
    dist = 10;
 
    c_a = circle_animation(circle_dur, step, final_r);
    l_a = line_animation(line_dur, step);
    t_a = text_animation(text_dur, step, dist);
 
    a1 = c_a('.anim-1');
    a2 = l_a('.anim-2');
    a3 = c_a('.anim-3');
    a4 = l_a('.anim-4');
    a5 = c_a('.anim-5');
    a6 = l_a('.anim-6');
    a7 = c_a('.anim-7');
    a8 = l_a('.anim-8');
    a9 = c_a('.anim-9');
    a10 = l_a('.anim-10');
    a11 = c_a('.anim-11');
    a12 = t_a('#d2d-title-day')
    a13 = t_a('#d2d-title-2')
    a14 = t_a('#d2d-title-data')
 
    a1.then(a2).then(a3).then(a4).then(a5).then(a6).then(a7).then(a8).then(a9).then(a10).then(a11)
    .then(a12).then(a13).then(a14);
    a1.anim();


}]);