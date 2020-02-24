angular.module("floor", []).filter("floor", function() {
  return function(input) {
    return  Math.floor(input);
  };
});
