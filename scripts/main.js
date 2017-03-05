$(document).ready(function() {
    $("#projectcontainer").hide();
    $("#contactcontainer").hide();

  $("#introNav").click(function() {
    $("#projectcontainer").hide( "slow", function() {$("#contactcontainer").hide( "slow", function() {$("#introcontainer").show("slow", function() {});});});


  });

    $("#portfolioNav").click(function() {
    $("#introcontainer").hide( "slow", function() {$("#contactcontainer").hide( "slow", function() {$("#projectcontainer").show("slow", function() {});});});

  });

    $("#contactNav").click(function() {
    $("#projectcontainer").hide( "slow", function() {$("#introcontainer").hide( "slow", function() {$("#contactcontainer").show("slow", function() {});});});

  });

  $("li").click(function() {
  $("li").each(function() {
      $(this).removeClass("active");
      $(this).removeClass("darkText");
    });
    $(this).addClass("active");
    $(this).addClass("darkText");
  });

  $( "#contactButton" ).click(function() {
    console.log("contactButton clicked");
    $("#projects").hide();
    $("#contact").show();
  });

  $("#projectsButton").click(function() {
    console.log("projectsButton clicked");
    $("#contact").hide();
    $("#projects").show();
  });

});
