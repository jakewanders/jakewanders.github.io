
    $("#projectcontainer").hide();
    $("#contactcontainer").hide();
  
  $("#introNav").click(function() {    
    $("#projectcontainer").hide( "fast", function() {$("#contactcontainer").hide( "fast", function() {$("#introcontainer").show("fast", function() {});});});
    
    
  });
  
    $("#portfolioNav").click(function() {
    $("#introcontainer").hide( "fast", function() {$("#contactcontainer").hide( "fast", function() {$("#projectcontainer").show("fast", function() {});});});

  });
  
    $("#contactNav").click(function() {
    $("#projectcontainer").hide( "fast", function() {$("#introcontainer").hide( "fast", function() {$("#contactcontainer").show("fast", function() {});});});
    
  });

  $("li").click(function() {
  $("li").each(function() {
      $(this).removeClass("active");
      $(this).removeClass("darkText");
    }); 
    $(this).addClass("active");
    $(this).addClass("darkText");
  });


