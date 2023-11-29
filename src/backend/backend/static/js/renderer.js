// Copyright Lee Grey, 2014
// License: MIT

module lg.tileSystem {

	import Vector2D = lg.math.geometry.Vector2D;

	export class FieldInfo {

		distanceFromTarget: number = -1;

		flowDirection: Vector2D = new Vector2D;

		tile: Tile;

		// id of the current test, used for "visited" mark
		scanID: number = 0;

		// NOTE: diagonals are not actually used
		neighbourTop: FieldInfo = null;
		neighbourTopRight: FieldInfo = null;
		neighbourRight: FieldInfo = null;
		neighbourBottomRight: FieldInfo = null;
		neighbourBottom: FieldInfo = null;
		neighbourBottomLeft: FieldInfo = null;
		neighbourLeft: FieldInfo = null;
		neighbourTopLeft: FieldInfo = null;
	}


	////////////////////////////////////////////////////////////////////////////

	export class TileMapPathField {

		private map: TileMap = null;

		width: number = 0;
		height: number = 0;

		field: Array<FieldInfo> = [];
		scanIDCounter: number = 0;

		previousTestPosition: Vector2D = new Vector2D(-1, -1);

		// reusable array for path calculation (prevent gc by keeping it around)
		private tests: Array<FieldInfo> = [];
		private testNeighbours: Array<FieldInfo> = [];

		private totalTests: number = 0; // how many fieldInfos in the array
		private currentTest: number = 0; // index of the current info being tested

		static flowDirectionsByIndex: Array<Vector2D> = [
			new Vector2D(0, -1),
			new Vector2D(1, 0),
			new Vector2D(0, 1),
			new Vector2D(-1, 0)
		];

		constructor(map: TileMap = null, wrap: boolean = false) {
			if (map !== null) {
				this.initForMap(map, wrap);
			}
		}

		initForMap(map: TileMap, wrap: boolean = false): void {

			this.map = map;
			this.width = map.width;
			this.height = map.height;

			var fieldInfo: FieldInfo;

			var i: number = 0;
			for (var iy = 0; iy < this.height; iy++) {
				for (var ix = 0; ix < this.width; ix++) {
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


		private initNeighbours(wrap: boolean = false): void {
			var fieldInfo: FieldInfo;
			for (var iy: number = 0; iy < this.height; iy++) {
				for (var ix: number = 0; ix < this.width; ix++) {

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

		calculateField(x: number, y: number): boolean {

			if (this.calculateDistanceField(x, y)) {
				this.calculateFlowField();
				return true;
			}
			return false;
		}

		calculateDistanceField(x: number, y: number): boolean {

			x = Math.floor(x);
			y = Math.floor(y);

			// don't recalculate if it hasn't changed
			if (this.previousTestPosition.x === x && this.previousTestPosition.y === y) {
				return false;
			} else {
				this.previousTestPosition.set(x, y);
			}

			if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
				return false;
			}

			var i: number;

			this.currentTest = 0;
			this.totalTests = 1;

			// scanID is used to prevent the test from being performed more than once
			// on the same tile. (ie to mark it as "visited") A counter is used
			// so they don't need to be reset.
			this.scanIDCounter++;

			var neighbour: FieldInfo;

			// get the first FieldInfo

			//  reset distances to -1
			for (i = 0; i < this.field.length; i++) {
				this.field[i].distanceFromTarget = -1;
			}

			this.tests[0] = this.field[x + y * this.width];
			this.tests[0].distanceFromTarget = 0;
			this.tests[0].scanID = this.scanIDCounter;

			// if the test tile is solid, just return as there is no path to
			// that location
			if (this.tests[0].tile.isSolid) {
				return false;
			}

			var currentFieldInfo: FieldInfo;
			while (this.currentTest < this.totalTests) {

				currentFieldInfo = this.tests[this.currentTest];

				this.testNeighbours[0] = currentFieldInfo.neighbourTop;
				this.testNeighbours[1] = currentFieldInfo.neighbourRight;
				this.testNeighbours[2] = currentFieldInfo.neighbourBottom;
				this.testNeighbours[3] = currentFieldInfo.neighbourLeft;

				// TODO: for optimal efficiency, inline this loop
				// and don't use the above array
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

			// return true to indicate that the data was updated
			return true;
		}

		calculateFlowField(): void {

			var fieldInfo: FieldInfo;

			var left: number;
			var right: number;
			var top: number;
			var bottom: number;
			var zeroVector: Vector2D = new Vector2D();

			for (var i = 0; i < this.field.length; i++) {

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

		getDirectionVectorField(
			resultObject: { x: number; y: number },
			x: number,
			y: number,
			hint: number = 0 // NOTE: hint must be a value from zero to one
			): void {

			x = Math.floor(x);
			y = Math.floor(y);

			// bounds test
			if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
				resultObject.x = 0;
				resultObject.y = 0;
				return;
			}

			var fieldInfo: FieldInfo = this.field[x + y * this.width];

			if (fieldInfo.distanceFromTarget < 0) {
				resultObject.x = resultObject.y = 0;
				return;
			}

			// fall back on cardinal calculation when stuck in an equilibrium
			if (fieldInfo.flowDirection.x == 0 && fieldInfo.flowDirection.y == 0) {
				this.getDirectionCardinal(resultObject, x, y, hint);
				return;
			}

			resultObject.x = fieldInfo.flowDirection.x;
			resultObject.y = fieldInfo.flowDirection.y;
		}pre

		// getDirectionCardinal always returns a cardinal direction

		// TODO: implement caching for results, use the scanID here as well
		getDirectionCardinal(
			resultObject: { x: number; y: number },
			x: number,
			y: number,
			hint: number = 0 // NOTE: hint must be a value from zero to one
			): void {

			x = Math.floor(x);
			y = Math.floor(y);

			// bounds test
			if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
				resultObject.x = 0;
				resultObject.y = 0;
				return;
			}

			//shortestDirectionFlags

			// always look for the closest one by looping through the four,
			// but use the hint to selecting a location in the array
			// to start checking. (This way each entity will get a different result
			// that will also be consistent on a per-entity basis.)

			var fieldInfo: FieldInfo = this.field[x + y * this.width];

			if (fieldInfo.distanceFromTarget < 0) {
				resultObject.x = resultObject.y = 0;
				return;
			}

			this.testNeighbours[0] = fieldInfo.neighbourTop;
			this.testNeighbours[1] = fieldInfo.neighbourRight;
			this.testNeighbours[2] = fieldInfo.neighbourBottom;
			this.testNeighbours[3] = fieldInfo.neighbourLeft;

			// get a hint that ranges from 0 - 3 (assuming hint is from 0 - 1)
			var hint = Math.floor(hint * 4) % 4;

			var closestIndex: number = hint;
			var closestDistance: number = 999999999999999;

			var testFieldInfo: FieldInfo;
			var testIndex: number = 0;

			for (var i = 0; i < 4; i++) {

				testIndex = (i + hint) % 4;
				testFieldInfo = this.testNeighbours[testIndex];
				if (testFieldInfo) {
					if (
						// must not be -1 (solid or inacessable)
						testFieldInfo.distanceFromTarget >= 0
						// if it is closer
						&& testFieldInfo.distanceFromTarget < closestDistance
						) {
						closestIndex = testIndex;
						closestDistance = testFieldInfo.distanceFromTarget;
					}
				}
			}

			var actualDirection: Vector2D = TileMapPathField.flowDirectionsByIndex[closestIndex];

			resultObject.x = actualDirection.x;
			resultObject.y = actualDirection.y;
		}

		fieldInfoAt(x: number, y: number, wrap: boolean = false): FieldInfo {

			// clamp and return null
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

		fieldInfoAtWorldSpace(x: number, y: number): FieldInfo {

			x = Math.floor(x / Tile.TILE_SIZE);
			y = Math.floor(y / Tile.TILE_SIZE);

			// just return null if the coordinates are outside the range
			if (x < 0 || x >= this.width || y < 0 || x >= this.height) {
				return null;
			}

			return this.field[x + y * this.width];
		}

		// DEBUG Visualisation:
		describe() {

			var lineString: string = '';
			for (var iy = 0; iy < this.height; iy++) {
				for (var ix = 0; ix < this.width; ix++) {
					lineString += this.fieldInfoAt(ix, iy).distanceFromTarget + "	";
				}
				console.log(lineString);
				lineString = '';
			}
		}

	} // class TileMapPathField

} // module


