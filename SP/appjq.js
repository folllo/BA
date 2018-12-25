function shuffle(timerId, moveCnt) {
  var divs = [];
  var tmp = [];
  $("#action-message").text("Make your move");
  $('#movecounter').text("Moves: 0");
  $('#timer').text("00:00");
  $("#board > div").each(function(){
    divs.push($(this));
  });
  while(divs.length) {
    tmp.push(divs.splice(Math.floor(Math.random() * divs.length),1)[0]);
  }
  $("#board").html("");
  for (var j = 0; j < tmp.length; j++) {
    $("#board").append(tmp[j]);
  }
  addTileEventlisteners(timerId, moveCnt);
}

function fillBoard(dimension){
  $("#board").html("");
  n = dimension*dimension;
  for (var i = 0; i < n; i++) {
    $("#board").append(buildTile(i));
    if(i == 0){
      $("#t"+i).addClass("empty-tile-"+dimension+"x"+dimension);
    }else {
      $("#t"+i).addClass("tile-"+dimension+"x"+dimension);
    }
  }
}

function buildTile(i) {
  return '<div id="t'+i+'"><span class="label">'+i+'</span></div>';
}

function getState() {
  var state = [];
  $("#board > div > span").each(function(){
    state.push($(this).text());
  })
  return state;
}

function validateMove(tileId, state) {
  var position = -1;
  var dimension = Math.sqrt(state.length);
  for (var i = 0; i < state.length; i++) {
    if(parseInt(state[i]) == parseInt(tileId)){
      position = i;
    }
  }
  if (parseInt(state[position+dimension]) == 0){
    return true;
  } else if (parseInt(state[position+1]) == 0 && position%dimension != (dimension-1)) {
    return true;
  } else if (parseInt(state[position-1]) == 0 && position%dimension != 0) {
    return true;
  } else if (parseInt(state[position-dimension]) == 0){
    return true;
  }
  return false;
}

function validateState() {
  var state = getState();
  var intState = [];
  var x = 0;
  // convert state to array of integers
  for (var i = 0; i < state.length; i++) {
    intState.push(parseInt(state[i]));
  }

  var dim = Math.sqrt(state.length);
	var numberOfInversions = calcInversions(state);

  //console.log(intState);
  //console.log(numberOfInversions);
  //console.log(parseInt(intState.indexOf(0)/4)%2);

  //True if the dimension of the puzzle is odd and the number of inversions is even.
	if (dim%2 == 1){
		if (numberOfInversions%2==0) {
			return true;
		} else {
			return false;
    }
	//True if dimension of the puzzle is even, the blank tile is on an odd row counted from the bottom and the number of inversions is even.
  } else {
    if ((parseInt(intState.indexOf(0)/4)%2)==1) {
  			if (numberOfInversions%2==0) {
  				return true;
  			} else {
  				return false;
        }

  		//True if dimension of the puzzle is even, the blank tile is on an even row counted from the bottom and the number of inversions is odd.
        } else {
    			if (numberOfInversions%2==1) {
    				return true;
    			} else {
    				return false;
          }
        }
  }
}

function calcInversions(state){
	var invCount = 0;
	var arrLen = state.length;
  var intState = [];
  // convert state to array of integers
  for (var i = 0; i < state.length; i++) {
    intState.push(parseInt(state[i]));
  }

  for (var i = 0; i < arrLen; i++) {
    for (var j = i+1; j < arrLen; j++) {
      if (intState[i] != 0 && intState[j] != 0 && intState[i]>intState[j]) {
        invCount += 1;
      }
    }
  }

  return invCount;
}

function move(element) {
  var emptyTile = $("#t0");
  var currentTile = element;
  var dimension = Math.sqrt(getState().length);
  emptyTile.removeClass("empty-tile-" + dimension + "x" + dimension);
  emptyTile.addClass("tile-" + dimension + "x" + dimension);
  emptyTile.attr("id", currentTile.attr("id"));
  emptyTile.html(currentTile.html());
  currentTile.removeClass("tile-" + dimension + "x" + dimension);
  currentTile.addClass("empty-tile-" + dimension + "x" + dimension);
  currentTile.attr("id", "t0");
  currentTile.html('<span class="label">0</span>');
  //check if new stat == final state
  //console.log(getState());
  //console.log("Inversions: " + calcInversions(getState()));
}

function addTileEventlisteners(timerId, moveCnt) {
  $("#board > div").each(function(){
    $(this).on("click", function(){
      if(validateMove($(this).text(), getState())) {
        move($(this));
        moveCnt += 1;
        $('#movecounter').text("Moves: " + moveCnt);
      }
      if(calcInversions(getState()) == 0 && getState().indexOf("0") == getState().length-1) {
        removeTileEventlisteners();
        $("#action-message").text("YOU WON!");
        stopTimer(timerId);
      }
    });
  })
}

function removeTileEventlisteners() {
  $("#board > div").each(function(){
    $(this).off("click");
  })
}

function formatTime(n) {
  return n > 9 ? n : "0" + n;
}

function startTimer(sec) {
  var timerId = setInterval(function(){
    sec += 1;
    var timeString;
    var minStr = formatTime(Math.floor(sec/60));
    var secStr = formatTime(sec%60);
    timeString = minStr + ":" + secStr;
    //console.log("TIMER: " + timeString);
    $('#timer').text(timeString);
  },1000);

  return timerId;
}

function stopTimer(timerId) {
  clearInterval(timerId);
}

$(function(){

  var sec = 0;
  var timer;
  var moveCnt = 0;

  // Changes the text of the size button and fills the board with dim*dim tiles
  $("#puzzlesize").on("click", function(){
    if($(this).text() == "3x3"){
      $(this).text("4x4");
      fillBoard(4);
    }else if ($(this).text() == "4x4") {
      $(this).text("5x5");
      fillBoard(5);
    }else {
      $(this).text("3x3");
      fillBoard(3);
    }
  })

  //changes the text of the difficulty button TODO: implement difficulties
  $("#difficulty").on("click", function(){
    if($(this).text() == "Easy"){
      $(this).text("Medium");
      //setDifficulty(2);
    }else if ($(this).text() == "Medium") {
      $(this).text("Hard");
      //setDifficulty(3);
    }else {
      $(this).text("Easy");
      //setDifficulty(1);
    }
    stopTimer(timer);
  })

  // shuffles the board TODO: fix bug with timer when shuffling multiple times
  $("#reset").on("click", function(){
    timer = startTimer(sec);
    shuffle(timer, moveCnt);
    while(!validateState()){
      shuffle(timer, moveCnt);
    }

  })

});
