$(document).ready(function () {
    $("#projectcontainer").hide();
    $("#contactcontainer").hide();

    $("#introNav").click(function () {
        $("#projectcontainer").hide("slow", function () { $("#contactcontainer").hide("slow", function () { $("#introcontainer").show("slow", function () { }); }); });


    });

    $("#portfolioNav").click(function () {
        $("#introcontainer").hide("slow", function () { $("#contactcontainer").hide("slow", function () { $("#projectcontainer").show("slow", function () { }); }); });

    });

    $("#contactNav").click(function () {
        $("#projectcontainer").hide("slow", function () { $("#introcontainer").hide("slow", function () { $("#contactcontainer").show("slow", function () { }); }); });

    });


    $("#contactButton").click(function () {
        $("#cardContainer").hide("slow", function () {
            $("footer").hide();
            $("#contact").slideDown("slow");
        });
    });

    $("#projectsButton").click(function () {
        $("#contact").slideUp("slow", function () {
            $("#cardContainer").slideDown("slow");
            $("footer").slideDown("slow");
        });
    });


    // project info 
    var cardContainer = document.getElementById('cardContainer');
    var cardData = [
        {
            url: "https://codepen.io/JNelson180/full/mBemOG/",
            title: "Local Weather App",
            description: "A basic local weather app.",
            skills: "JavaScript/ES6, HTML, CSS"
        },
        // {
        //     url: "https://www.sunshinerising.net/",
        //     title: "Sunshine Rising Book Blog",
        //     description: "A WordPress based book blog with custom elements.",
        //     skills: "Wordpress, JavaScript, HTML, CSS, PHP"
        // },
        {
            url: "https://smurl-app.herokuapp.com/",
            title: "URL Shortener",
            description: "A URL shortener microservice used to return the client with an abbreviated URL from their input.",
            skills: "Javascript/ES6, Node.js, MongoDB, HTML, CSS"
        },
        {
            url: "http://codepen.io/JNelson180/full/gwaZKz",
            title: "Simon Says",
            description: "A Simon Says game mocked up in Javascript/HTML/CSS.",
            skills: "Javascript, jQuery, HTML, CSS"
        },
        {
            url: "http://codepen.io/JNelson180/full/zBaNqy",
            title: "Javascript Calculator",
            description: "A basic calculator app.",
            skills: "Javascript, HTML, CSS"
        },
        {
            url: "https://imglook.herokuapp.com/api/imagesearch/",
            title: "Image Search Metadata",
            description: "Provides JSON data of image search results.",
            skills: "Nodejs, Express, MongoDB, Javascript, HTML, CSS"
        },
        {
            url: "https://codepen.io/JNelson180/full/BpobRp/",
            title: "Javascript Piano",
            description: "Playable Javascript mini keyboard.",
            skills: "Javascript, HTML, CSS"
        },
        {
            url: "https://metafile-js.herokuapp.com/",
            title: "File metadata microservice",
            description: "Upload a file to view its metadata",
            skills: "Nodejs, Javascript, Express, Bootstrap"
        },
        {
            url: "https://codepen.io/JNelson180/full/JrbBWX/",
            title: "Flexbox Bookshelf",
            description: "Dynamically generated bookshelf based on Goodreads API data.",
            skills: "Nodejs, Express, Heroku, MongoDB, Javascript, HTML, CSS"
        },
        {
            url: "https://codepen.io/JNelson180/full/vKbrkv/",
            title: "Tic Tac Toe",
            description: "Javascript tic tac toe game.",
            skills: "Javascript, jQuery, HTML, CSS"
        },
        {
            url: "https://codepen.io/JNelson180/full/yOZJxQ/",
            title: "Motivational Quote Machine",
            description: "Motivational quote generator from external API.",
            skills: "Javascript, HTML, CSS"
        },
        {
            url: "https://codepen.io/JNelson180/full/Wxaybg/",
            title: "Pomodoro Clock",
            description: "Basic pomodoro clock app",
            skills: "Javascript, HTML, CSS"
        }
    ];

    var createCard = function createCard(url, title, description, skills) {
        return '<a href="' + url + '" target="_blank">' + '<div class="cardWrapper">' + '<iframe scrolling="no" src="' + url + '"></iframe>' + '<div class="cardText">' + '<h2>' + title + '</h2>' + '<div class="description">' + description + '</div>' + '<div class="skills">' + skills + '</div>' + '</div>' + '</div>' + '</a>';
    };

    var cards = cardData.map(function (c) {
        return createCard(c.url, c.title, c.description, c.skills);
    });

    var numPages = Math.round(cards.length / 3);

    var currentPage = 0;

    function renderCards() {
        var index = currentPage === 0 ? 0 : currentPage * 3;

        var cardsToRender = cards.slice(index, index + 3);

        let dex = 0;
        // render all the rows so they prefetch
        for (var i = 0; i < numPages; i++) {
            let newDiv = document.createElement("div");
            newDiv.id = "row" + i;
            newDiv.className = "cardContainer";
            newDiv.innerHTML = cards.slice(dex, dex + 3);
            dex = dex + 3;

            cardContainer.appendChild(newDiv);
        }

        hideInactivePages();
    }

    function hideInactivePages() {
        for (var i = 0; i < numPages; i++) {
            var currentRow = document.getElementById('row' + i);

            if (i !== currentPage) {
                currentRow.style.position = "absolute";
                currentRow.style.top = "-6000px";
                // currentRow.display = "none";
            } else {
                currentRow.style.position = "relative";
                currentRow.style.right = "0px"
                currentRow.style.left = "0px";
                currentRow.style.top = "0px";
                // currentRow.display = "flex";
                // currentRow.opacity = 1;
            }
        }
    }

    function incrementPages() {
        var currentRow = document.getElementById('row' + currentPage);
        currentRow.style.top = "-6000px";
        currentRow.style.position = "absolute";
        // increment the pages
        if (currentPage === numPages - 1) {
            currentPage = 0;
        } else {
            currentPage = currentPage + 1;
        }

        hideInactivePages();
    }

    document.getElementById('nextButton').onclick = function () {
        incrementPages();
    }

    renderCards();
});
