function shuffle() {
  var divs = [];
  var tmp = [];
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
  addTileEventlisteners();
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
  console.log("pos: "+ position + "\nstate: " + state+ "\ndim: " + dimension);

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

function validateState(state) {

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
}

function addTileEventlisteners() {
  $("#board > div").each(function(){
    $(this).on("click", function(){
      if(validateMove($(this).text(), getState())) {
        move($(this));
      }
    });
  })
}

$(function(){

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
  })

  // shuffles the board
  $("#reset").on("click", function(){
    shuffle();
  })

});