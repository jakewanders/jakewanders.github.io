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


  $( "#contactButton" ).click(function() {
    $("#projects").hide( "slow", function() {
      $("#contact").slideDown("slow");
    });
  });

  $("#projectsButton").click(function() {
    $("#contact").slideUp("slow", function() {
      $("#projects").slideDown("slow");
    });
  });

var currentPage = Number(1);
var numPages = document.getElementsByClassName('projectRow');
console.log(numPages[0].id);
  $("#nextButton").click(function() {
      var curRow = "projectrow" + currentPage;
      var nextRow = (function() {
        if (currentPage == numPages.length) {
        return "projectrow1";
      }
      else return "projectrow" + Number(currentPage + 1);
    })();

      console.log(nextRow);
      console.log("curRow is " + curRow);
      $("#" + curRow).fadeOut("slow", function() {
        $("#" + nextRow).fadeIn("slow");
      });
      if (currentPage == 3) {
      currentPage = 1;
    } else {
      currentPage ++;
    }
  });

  $("#nextButton2").click(function() {
      var curRow = "projectrow" + currentPage;
      var nextRow = (function() {
        if (currentPage == numPages.length) {
        return "projectrow1";
      }
      else return "projectrow" + Number(currentPage + 1);
    })();

      console.log(nextRow);
      console.log("curRow is " + curRow);
      $("#" + curRow).fadeOut("slow", function() {
        $("#" + nextRow).fadeIn("slow");
      });
      if (currentPage == 3) {
      currentPage = 1;
    } else {
      currentPage ++;
    }
  });

});
