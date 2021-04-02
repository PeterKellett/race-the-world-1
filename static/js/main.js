$(document).ready(function () {
      console.log("main.js Document ready!");
      setGridSize();
      $(window).resize(setGridSize);

      function setGridSize() {
          var windowWidth = window.innerWidth-50;
          var windowHeight = window.innerHeight;
          var gameBoardWidth = windowHeight-50;
          console.log("windowWidth = ", windowWidth);
          console.log("windowHeight = ", windowHeight);
          $('.zoom-window').height(gameBoardWidth).width((windowWidth-gameBoardWidth)/2);
          $('.game-board').height(gameBoardWidth).width(gameBoardWidth);
          $('.game-controls').height(gameBoardWidth).width((windowWidth-gameBoardWidth)/2);
      }
    });