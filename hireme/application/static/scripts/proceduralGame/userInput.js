//
// User Input
//

// Player Actions
var playerActions = (function () {
    var _currentActions = [];

    function _startAction(id, playerAction) {
        if( playerAction === undefined ) {
            return;
        }

        var action,
            acts = {"moveLeft":  function () {
							        if(game.player()) game.player().moveLeft(true); },
                    "moveRight": function () {
											if(game.player()) game.player().moveRight(true); },
										"moveUp": function () {
											if(game.player()) game.player().moveUp(true); },
										"moveDown": function () {
											if(game.player()) game.player().moveDown(true); },
                    "attack": function () {
											if(game.player()) game.player().attack(); }
										};

        if(action = acts[playerAction]) action();

        _currentActions.push( {identifier:id, playerAction:playerAction} );
    }

    function _endAction(id) {
        var action,
					acts = {"moveLeft":  function () {
										if(game.player()) game.player().moveLeft(false); },
									"moveRight": function () {
										if(game.player()) game.player().moveRight(false); },
									"moveUp": function () {
										if(game.player()) game.player().moveUp(false); },
									"moveDown": function () {
										if(game.player()) game.player().moveDown(false); },
									"attack": function () {
										if(game.player()) game.player().attack(); }
									};

        var idx = _currentActions.findIndex(function(a) { return a.identifier === id; });

        if (idx >= 0) {
            if(action = acts[_currentActions[idx].playerAction]) action();
            _currentActions.splice(idx, 1);  // remove action at idx
        }
    }

    return {
        startAction: _startAction,
        endAction: _endAction
    };
})();

// Key Listener ( w a s d )
var keybinds = { 87: "moveUp",
                 83: "moveDown",
                 65: "moveLeft",
				 			 	 68: "moveRight"};


function keyDown(e) {
    var x = e.which || e.keyCode;

    if( keybinds[x] !== undefined ) {
        e.preventDefault();
        playerActions.startAction(x, keybinds[x]);
    }
}


function keyUp(e) {
    var x = e.which || e.keyCode;

    if( keybinds[x] !== undefined ) {
        e.preventDefault();
        playerActions.endAction(x);
    }
}

document.body.addEventListener('keydown', keyDown);
document.body.addEventListener('keyup', keyUp);