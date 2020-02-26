angular.module("floor", []).filter("floor", function() {
  return function(input) {
    if (input < 0) {
      result = -(Math.floor(Math.abs(input)));
      if (input < 0 && result == 0)
        return "-0";
      else
        return "" + result;
    }
    else
      return "" + Math.floor(input);
  };
});
