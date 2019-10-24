var ENTITYIDS = {
  0: "Grass",
  1: "BerryBush",
  2: "Tree",
  3: "Stone"
};

function randomInt(max) {
	return Math.floor(Math.random()*Math.floor(max));
}

function StationaryEntity(xPos, yPos) {
  this.chunkXPos = xPos;
  this.chunkYPos = yPos;
  this.width = 0;
  this.height = 0;
  this.hp = 0;
}

function ChunkBlock(xPos, yPos, entityID) {
  this.size = 20;
  this.xPos = xPos;
  this.yPos = yPos;
  this.entityID = entityID;
}

function Chunk(xPos, yPos, size) {
  this.size = size;
  this.mapXPos = xPos;
  this.mapYPos = yPos;
  this.chunkGrid = [];
}

Chunk.prototype.createBlock = function(blockNum, entityID) {

  var blockRow = parseInt((blockNum / 5));
  var blockCol = (blockNum % 5);
  var blockSize = 20;

  var blockX = this.mapXPos + (blockCol*blockSize);
  var blockY = this.mapYPos + (blockRow*blockSize);

  var newBlock = new ChunkBlock(blockX, blockY, entityID);
  this.chunkGrid.push(newBlock);
};

Chunk.prototype.genItems = function() {
  // Generate a random object ID greater than 0
  var gridEntityType = randomInt(3) + 1;
  var i = 0;
  for(i = 0; i < 25; i++) {
    var willGenEntity = (randomInt(5) < 1); // 20% chance to generate an object
    if(willGenEntity) {
      this.createBlock(i, gridEntityType);
    } else {
      this.createBlock(i, 0); // Push grass if no gen
    }
  }
};
