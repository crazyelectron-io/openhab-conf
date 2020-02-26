(
    function(i) {
        var dimmervalue = parseFloat(i);
    
        var minmired = 2000.0/13.0 // 6500°K
        var maxmired = 500.0  // 2000°K
    
        colortemp = Math.round(100000000/(dimmervalue*maxmired-dimmervalue*minmired+100*minmired))
    
        return colortemp + "K"
    }
)(input)
