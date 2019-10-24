'use strict';
var canvas = document.getElementById("game_layer");
var context = canvas.getContext("2d");
var NATIVEWIDTH = 500;
var NATIVEHEIGHT = 500;
var mapOffset;
var chunkSize = 100;
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

//
// Game Entities
//

// Base Entity
function Entity(position, speed, direction) {
	this.position = position;
	this.speed = speed;
	this.direction = direction;
	this.time = 0;
	this.width = 5;
	this.height = 5;
	this.hp = 0;
}

Entity.prototype.update = function(tick) {
	this.time += tick;
};

Entity.prototype.collisionBox = function() {
	return new CollisionBox(
		this.position.x - this.width/2,
		this.position.y - this.height/2,
		this.width, this.height);
};

// Example: Moving Entities
function Worker(position, speed, direction, level) {
	Entity.call(this, position, speed, direction);
	this.width = 15;
	this.height = 15;
	this.level = level;
}
Worker.prototype = Object.create(Entity.prototype);

Worker.prototype.update = function(tick) {
	Entity.prototype.update.call(this, tick);
	if(this.collisionBox().top() <= 0 ||
		this.collisionBox().bottom() >=
		game.gameFieldBox().bottom()) {
			this.direction.y *= -1;
		}
	if(this.collisionBox().left() <= 0 ||
		this.collisionBox().right() >=
		game.gameFieldBox().right()) {
				this.direction.x *= -1;
	}
}

// Player Entity
function Player(position, speed, direction, level) {
	Entity.call(this, position, speed, direction);
	this.width = 10;
	this.height = 10;
	this.isMovingLeft = false;
	this.isMovingRight = false;
	this.isMovingUp = false;
	this.isMovingDown = false;
	this.level = level;
}
Player.prototype = Object.create(Entity.prototype);

Player.prototype.updateDirection = (function() {
	var direction = new Vector2d(0, 0);
	if(this.isMovingLeft) {
		direction = vectorAdd(direction, new Vector2d(1, 0));
	}
	if(this.isMovingRight) {
		direction = vectorAdd(direction, new Vector2d(-1, 0));
	}
	if(this.isMovingUp) {
		direction = vectorAdd(direction, new Vector2d(0, 1));
	}
	if(this.isMovingDown) {
		direction = vectorAdd(direction, new Vector2d(0, -1));
	}
	this.direction = direction;
});

Player.prototype.moveRight = (function(isActivated) {
	this.isMovingRight = isActivated;
	this.updateDirection();
});

Player.prototype.moveLeft = function(isActivated) {
	this.isMovingLeft = isActivated;
	this.updateDirection();
}

Player.prototype.moveUp = function(isActivated) {
	this.isMovingUp = isActivated;
	this.updateDirection();
}

Player.prototype.moveDown = function(isActivated) {
	this.isMovingDown = isActivated;
	this.updateDirection();
}

Player.prototype.attack = function() {
	console.log("Attack ability coming soon!");
}

//
// Graphics Renderer
//
var renderer=(function() {

	var _canvas = document.getElementById("game_layer"),
	_context = _canvas.getContext("2d");

	// Flexible screen size
	function _setCanvasSize() {

		var deviceWidth = window.innerWidth;
		var deviceHeight = window.innerHeight;

		let scalingFactor = Math.max(
			deviceWidth / NATIVEWIDTH,
			deviceHeight / NATIVEHEIGHT
		);
		canvas.width = Math.floor(deviceWidth / scalingFactor);;
		canvas.height = Math.floor(deviceWidth / scalingFactor);;
		canvas.style.width = '40%';
		canvas.style.height = '40%';
		if(scalingFactor < 1){
    	_context.imageSmoothingEnabled = true; // turn it on for low res screens
		} else {
			_context.imageSmoothingEnabled = false; // turn it off for high res screens.
		}
	}

  var _entityColors = [
    "rgb(71, 110, 74)", // Grass
    "rgb(159, 245, 166)", // Bush
    "rgb(5, 99, 13)", // Tree
    "rgb(68, 69, 68)" // Stone
  ]

	function _drawBox(color, entity) {
		_context.fillStyle = color;
    if(entity instanceof Player) {
      _context.fillRect(
        (entity.position.x - entity.width / 2) - mapOffset.x,
        (entity.position.y - entity.height / 2) - mapOffset.y,
  			entity.width,
  			entity.height
  		);
    } else {
      _context.fillRect(
        (entity.position.x - entity.width/2),
        (entity.position.y - entity.height / 2),
			  entity.width,
			  entity.height
		  );
    }
	}

  function _drawChunkBlock(block) {
    _context.fillStyle = _entityColors[block.entityID];
    _context.fillRect(
      block.xPos,
      block.yPos,
      block.size,
      block.size
    );
  }

	function _render(tick) {
		_setCanvasSize();
    _context.translate(mapOffset.x, mapOffset.y);
	  var i,
      x,
      z,
			entity,
			entities = game.entities();
    var chunks = game.chunks();
    for(x = 0; x < chunks.length; x++) {
      var chunk = chunks[x];
      for(z = 0; z < chunk.chunkGrid.length; z++) {
        var block = chunk.chunkGrid[z];
        _drawChunkBlock(block);
      }
    }
		for(i=entities.length-1; i >= 0; i--) {
			let entity = entities[i];
			if(entity instanceof Player) {
				_drawBox("rgb(255, 153, 0)", entity);
			}
		}
	}
	return {
		render: _render,
		setCanvasSize: _setCanvasSize
	}
})();

//
// Physics Logic
//
var physicsEngine = (function() {
	function _update(tick) {
		var i,
			entity,
			velocity,
			entities = game.entities();
		for(i=entities.length-1; i >= 0; i--) {
			entity = entities[i];
      if(entity instanceof Player) {
        velocity = vectorScalarMultiply(
          entity.direction,
          entity.speed
        );
        mapOffset = vectorAdd(
          mapOffset,
          vectorScalarMultiply(velocity, tick)
        );
        continue
      }
			velocity = vectorScalarMultiply(
				entity.direction,
				entity.speed
			);
			entity.position =
				vectorAdd(
					entity.position,
					vectorScalarMultiply(velocity, tick)
				);
		}
	}
	return {
		update: _update
	};
})();

// Vector object and functions
function Vector2d(x, y) {
	this.x = parseInt(x);
	this.y = parseInt(y);
}

function vectorAdd(v1, v2) {
	return new Vector2d(v1.x+v2.x, v1.y+v2.y);
}

function vectorSubtract(v1, v2) {
	return new Vector2d(v1.x-v2.x, v1.y-v2.y);
}

function vectorScalarMultiply(v1, s) {
	return new Vector2d(v1.x*s, v1.y*s);
}

function vectorLength(v) {
	return Math.sqrt(v.x*v.x + v.y*v.y);
}

function vectorNormalize(v) {
	var reciprocal = 1.0 /
		(vectorLength(v) + 1.0e-037);
	return vectorScalarMultiply(v, reciprocal);
}

//
// Collision Detection
//
function CollisionBox(x, y, width, height) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
}

CollisionBox.prototype.left = function() {
	return this.x;
}

CollisionBox.prototype.right = function() {
	return this.x + this.width;
}

CollisionBox.prototype.top = function() {
	return this.y;
}

CollisionBox.prototype.bottom = function() {
	return this.y + this.height;
}

CollisionBox.prototype.intersects = function(colBox2) {
	return this.right() >= colBox2.left() &&
		this.left() <= colBox2.right() &&
		this.top() <= colBox2.bottom() &&
		this.bottom() >= colBox2.top();
};

function CollisionBoxUnion(colBox1, colBox2) {
	var x, y, width, height;

	if(colBox1 === undefined) {
		return colBox2;
	}
	if(colBox2 === undefined) {
		return colBox1;
	}

	x = Math.min(colBox1.x, colBox2.x);
	y = Math.min(colBox1.y, colBox2.y);
	width =
		Math.max(colBox1.right(), colBox2.right()) -
		Math.min(colBox1.left(), colBox2.left()
	);
	height =
		Math.max(colBox1.bottom(), colBox2.bottom()) -
		Math.min(colBox1.top(), colBox2.top()
	);

	return new CollisionBox(x, y, width, height);
}


function randomInt(max) {
	return Math.floor(Math.random()*Math.floor(max));
}

//
// Main Game Engine
//
var game = (function() {
	renderer.setCanvasSize();
	var _entities,
		_workers,
    _chunks,
		_player,
		_gameFieldBox,
    _previousTick,
    _playerStartPos,
    _playerWalkSpeed,
    _playerStartLevel,
    _workerWalkSpeed,
    _workerWorkSpeed,
		_started = false;

  function _genChunks() {
    var startingChunks = 625;
    for(var i = 0; i < startingChunks; i++) {
      var chunkRow = parseInt((i / 25));
      var chunkCol = (i % 25);
      var chunkX = chunkCol * chunkSize;
      var chunkY = chunkRow * chunkSize;
      var chunk = new Chunk(chunkX, chunkY, chunkSize);
      _chunks.push(chunk);
    }
  }

  function _populateChunks() {
    for(var i = 0; i < _chunks.length; i++) {
      var chunk = _chunks[i];
      chunk.genItems();
    }
  }

	function _start() {
		_entities = [];
    _chunks = [];
		_previousTick = 0;
		_gameFieldBox = new CollisionBox(0, 0, canvas.width, canvas.height);
		_playerStartPos = new Vector2d(_gameFieldBox.width / 2, _gameFieldBox.height / 2);
		_playerWalkSpeed = 45;
		_playerStartLevel = 1;
		_addEntity(
			new Player(_playerStartPos, _playerWalkSpeed, new Vector2d(0, 0), _playerStartLevel)
		);
		_genChunks();
    _populateChunks();
    mapOffset = new Vector2d(-1250, -1250);
		if(!_started) {
			window.requestAnimationFrame(this.update.bind(this));
			_started = true;
		}
	}

	function _addEntity(entity) {
		_entities.push(entity);
		if(entity instanceof Player) {
			_player = entity;
		}
	}

	function _removeEntities(entities) {
		if(!entities) return;

		function isNotInEntities(entity) {
			return !entities.includes(entity);
		}
		_entities = _entities.filter(isNotInEntities);
		_workers = _workers.filter(isNotInEntities);

		if(entities.includes(_player)) {
			_player = undefined;
		}
	}

	function _update(tick) {
		var tick = Math.min((tick - _previousTick) / 1000, 3/60); // ~60 FPS
		physicsEngine.update(tick);
		var i;
		for(i=_entities.length-1; i >= 0; i--) {
			_entities[i].update(tick);
		}
		// Update game field box in case screen is resized
		renderer.setCanvasSize();
		_gameFieldBox = new CollisionBox(0, 0, canvas.width, canvas.height);
		renderer.render();
		window.requestAnimationFrame(this.update.bind(this));
	}

	return {
		start: _start,
		update: _update,
    chunks: function() { return _chunks; },
		entities: function() { return _entities; },
		workers: function() { return _workers; },
		player: function() { return _player; },
		gameFieldBox: function () { return _gameFieldBox; }
	};
})();

document.addEventListener("DOMContentLoaded", function(event){
  game.start();
});
