
class Vector2D {
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }

    set(x, y) {
        this.x = x;
        this.y = y;
    }

    normalise(length) {
        const magnitude = Math.sqrt(this.x * this.x + this.y * this.y);
        if (magnitude !== 0) {
            this.x *= length / magnitude;
            this.y *= length / magnitude;
        }
    }
}

lg.math.geometry.Vector2D = Vector2D;

class FieldInfo {
    constructor() {
        this.distanceFromTarget = -1;
        this.flowDirection = new Vector2D();
        this.tile = null;
        this.scanID = 0;
        this.neighbourTop = null;
        this.neighbourTopRight = null;
        this.neighbourRight = null;
        this.neighbourBottomRight = null;
        this.neighbourBottom = null;
        this.neighbourBottomLeft = null;
        this.neighbourLeft = null;
        this.neighbourTopLeft = null;
    }
}

class TileMapPathField {
    constructor(map = null, wrap = false) {
        this.map = null;
        this.width = 0;
        this.height = 0;
        this.field = [];
        this.scanIDCounter = 0;
        this.previousTestPosition = new Vector2D(-1, -1);
        this.tests = [];
        this.testNeighbours = [];
        this.totalTests = 0;
        this.currentTest = 0;

        if (map !== null) {
            this.initForMap(map, wrap);
        }
    }

    initForMap(map, wrap = false) {
        this.map = map;
        this.width = map.width;
        this.height = map.height;

        let fieldInfo;
        let i = 0;

        for (let iy = 0; iy < this.height; iy++) {
            for (let ix = 0; ix < this.width; ix++) {
                if (typeof this.field[i] !== "function") {
                    fieldInfo = new FieldInfo();
                } else {
                    console.log('recycling');
                }
                fieldInfo.tile = map.tileAt(ix, iy);
                this.field[i] = fieldInfo;
                i++;
            }
        }

        // truncate the array if necessary
        this.field.length = this.width * this.height;

        this.initNeighbours(wrap);
    }

    initNeighbours(wrap = false) {
        let fieldInfo;
        for (let iy = 0; iy < this.height; iy++) {
            for (let ix = 0; ix < this.width; ix++) {
                fieldInfo = this.fieldInfoAt(ix, iy);

                fieldInfo.neighbourTop = this.fieldInfoAt(ix, iy - 1, wrap);
                fieldInfo.neighbourTopRight = this.fieldInfoAt(ix + 1, iy - 1, wrap);
                fieldInfo.neighbourRight = this.fieldInfoAt(ix + 1, iy, wrap);
                fieldInfo.neighbourBottomRight = this.fieldInfoAt(ix + 1, iy + 1, wrap);
                fieldInfo.neighbourBottom = this.fieldInfoAt(ix, iy + 1, wrap);
                fieldInfo.neighbourBottomLeft = this.fieldInfoAt(ix - 1, iy + 1, wrap);
                fieldInfo.neighbourLeft = this.fieldInfoAt(ix - 1, iy, wrap);
                fieldInfo.neighbourTopLeft = this.fieldInfoAt(ix - 1, iy - 1, wrap);
            }
        }
    }

    calculateField(x, y) {
        if (this.calculateDistanceField(x, y)) {
            this.calculateFlowField();
            return true;
        }
        return false;
    }

    calculateDistanceField(x, y) {
        x = Math.floor(x);
        y = Math.floor(y);

        if (this.previousTestPosition.x === x && this.previousTestPosition.y === y) {
            return false;
        } else {
            this.previousTestPosition.set(x, y);
        }

        if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
            return false;
        }

        let i;

        this.currentTest = 0;
        this.totalTests = 1;

        this.scanIDCounter++;

        let neighbour;

        for (i = 0; i < this.field.length; i++) {
            this.field[i].distanceFromTarget = -1;
        }

        this.tests[0] = this.field[x + y * this.width];
        this.tests[0].distanceFromTarget = 0;
        this.tests[0].scanID = this.scanIDCounter;

        if (this.tests[0].tile.isSolid) {
            return false;
        }

        let currentFieldInfo;
        while (this.currentTest < this.totalTests) {
            currentFieldInfo = this.tests[this.currentTest];

            this.testNeighbours[0] = currentFieldInfo.neighbourTop;
            this.testNeighbours[1] = currentFieldInfo.neighbourRight;
            this.testNeighbours[2] = currentFieldInfo.neighbourBottom;
            this.testNeighbours[3] = currentFieldInfo.neighbourLeft;

            for (i = 0; i < 4; i++) {
                neighbour = this.testNeighbours[i];
                if (neighbour && neighbour.scanID !== this.scanIDCounter && !neighbour.tile.isSolid) {
                    this.tests[this.totalTests++] = neighbour;
                    neighbour.distanceFromTarget = currentFieldInfo.distanceFromTarget + 1;
                    neighbour.scanID = this.scanIDCounter;
                }
            }

            this.currentTest++;
        }

        return true;
    }

    calculateFlowField() {
        let fieldInfo;
        let left, right, top, bottom;
        const zeroVector = new Vector2D();

        for (let i = 0; i < this.field.length; i++) {
            fieldInfo = this.field[i];

            if (fieldInfo.neighbourLeft && !(fieldInfo.neighbourLeft.distanceFromTarget < 0)) {
                left = fieldInfo.neighbourLeft.distanceFromTarget;
            } else {
                left = fieldInfo.distanceFromTarget;
            }

            if (fieldInfo.neighbourRight && !(fieldInfo.neighbourRight.distanceFromTarget < 0)) {
                right = fieldInfo.neighbourRight.distanceFromTarget;
            } else {
                right = fieldInfo.distanceFromTarget;
            }

            if (fieldInfo.neighbourTop && !(fieldInfo.neighbourTop.distanceFromTarget < 0)) {
                top = fieldInfo.neighbourTop.distanceFromTarget;
            } else {
                top = fieldInfo.distanceFromTarget;
            }

            if (fieldInfo.neighbourBottom && !(fieldInfo.neighbourBottom.distanceFromTarget < 0)) {
                bottom = fieldInfo.neighbourBottom.distanceFromTarget;
            } else {
                bottom = fieldInfo.distanceFromTarget;
            }

            fieldInfo.flowDirection.x = left - right;
            fieldInfo.flowDirection.y = top - bottom;

            fieldInfo.flowDirection.normalise(1.0);
        }
    }

    getDirectionVectorField(resultObject, x, y, hint = 0) {
        x = Math.floor(x);
        y = Math.floor(y);

        if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
            resultObject.x = 0;
            resultObject.y = 0;
            return;
        }

        const fieldInfo = this.field[x + y * this.width];

        if (fieldInfo.distanceFromTarget < 0) {
            resultObject.x = resultObject.y = 0;
            return;
        }

        if (fieldInfo.flowDirection.x === 0 && fieldInfo.flowDirection.y === 0) {
            this.getDirectionCardinal(resultObject, x, y, hint);
            return;
        }

        resultObject.x = fieldInfo.flowDirection.x;
        resultObject.y = fieldInfo.flowDirection.y;
    }

    getDirectionCardinal(resultObject, x, y, hint = 0) {
        x = Math.floor(x);
        y = Math.floor(y);

        if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
            resultObject.x = 0;
            resultObject.y = 0;
            return;
        }

        const fieldInfo = this.field[x + y * this.width];

        if (fieldInfo.distanceFromTarget < 0) {
            resultObject.x = resultObject.y = 0;
            return;
        }

        this.testNeighbours[0] = fieldInfo.neighbourTop;
        this.testNeighbours[1] = fieldInfo.neighbourRight;
        this.testNeighbours[2] = fieldInfo.neighbourBottom;
        this.testNeighbours[3] = fieldInfo.neighbourLeft;

        const hintValue = Math.floor(hint * 4) % 4;

        let closestIndex = hintValue;
        let closestDistance = 999999999999999;

        let testFieldInfo;
        let testIndex = 0;

        for (let i = 0; i < 4; i++) {
            testIndex = (i + hintValue) % 4;
            testFieldInfo = this.testNeighbours[testIndex];
            if (testFieldInfo) {
                if (
                    testFieldInfo.distanceFromTarget >= 0 &&
                    testFieldInfo.distanceFromTarget < closestDistance
                ) {
                    closestIndex = testIndex;
                    closestDistance = testFieldInfo.distanceFromTarget;
                }
            }
        }

        const actualDirection = TileMapPathField.flowDirectionsByIndex[closestIndex];

        resultObject.x = actualDirection.x;
        resultObject.y = actualDirection.y;
    }

    fieldInfoAt(x, y, wrap = false) {
        if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
            if (wrap) {
                x = x % this.width;
                y = y % this.width;
                if (x < 0) x += this.width;
                if (y < 0) y += this.height;
            } else {
                return null;
            }
        }

        return this.field[x + y * this.width];
    }

    fieldInfoAtWorldSpace(x, y) {
        x = Math.floor(x / Tile.TILE_SIZE);
        y = Math.floor(y / Tile.TILE_SIZE);

        if (x < 0 || x >= this.width || y < 0 || x >= this.height) {
            return null;
        }

        return this.field[x + y * this.width];
    }

    describe() {
        let lineString = '';
        for (let iy = 0; iy < this.height; iy++) {
            for (let ix = 0; ix < this.width; ix++) {
                lineString += this.fieldInfoAt(ix, iy).distanceFromTarget + "    ";
            }
            console.log(lineString);
            lineString = '';
        }
    }
}

TileMapPathField.flowDirectionsByIndex = [
    new Vector2D(0, -1),
    new Vector2D(1, 0),
    new Vector2D(0, 1),
    new Vector2D(-1, 0)
];

lg.tileSystem = { TileMapPathField, FieldInfo };

// Usage Example:
const map = new lg.tileSystem.TileMap();
const pathField = new lg.tileSystem.TileMapPathField(map, true);
pathField.calculateField(0, 0);
pathField.describe();
