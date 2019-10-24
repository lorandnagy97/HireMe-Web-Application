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

// Collision Detection
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