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