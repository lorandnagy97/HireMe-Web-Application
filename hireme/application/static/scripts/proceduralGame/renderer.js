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