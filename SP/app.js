let cnt = 1;
const difficulty_div = document.getElementById("difficulty");
const size_div = document.getElementById("puzzlesize");
const reset_div = document.getElementById("reset");
const board_div = document.getElementById("board");

function changeDifficulty() {
	if(difficulty_div.innerHTML == "Easy") {
		difficulty_div.innerHTML = "Medium";
	} else if(difficulty_div.innerHTML == "Medium") {
		difficulty_div.innerHTML = "Hard";
	} else {
		difficulty_div.innerHTML = "Easy";
	}	
}

function changeSize() {
	if(size_div.innerHTML == "3x3") {
		size_div.innerHTML = "4x4";
		fillBoard(4);
	} else if(size_div.innerHTML == "4x4") {
		size_div.innerHTML = "5x5";
		fillBoard(5);
	} else {
		size_div.innerHTML = "3x3";
		fillBoard(3);
	}

}

function fillBoard(dimension) {
	board_div.innerHTML = "";
	n = dimension*dimension;
	for(i = 0; i<n; i++) {
		newTile = buildTile(i);
		board_div.innerHTML += newTile;
		if(i == 0) {
			document.getElementById("t"+i).classList.add('empty-tile-'+dimension+'x'+dimension);;
		}else {
			document.getElementById("t"+i).classList.add('tile-'+dimension+'x'+dimension);;
		}	
	}
}

function buildTile() {
	return '<div id="t'+i+'"><span class="label">'+i+'</span></div>';
}

function resetGame() {

}

function main() {
	difficulty_div.addEventListener('click', () => changeDifficulty());
	size_div.addEventListener('click', () => changeSize());
	reset_div.addEventListener('click', () => resetGame());		
}

main();
