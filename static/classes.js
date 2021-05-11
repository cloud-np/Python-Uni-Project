
class Net{
    constructor(id) {
        this.id = id * 1;
        this.arrCells = [];
        
        let a = Math.random();
        a <= 0.45 ? a += 0.45 : a; 
        //                                                         I only need the too digits after '.' e.x: 0.23
        let temp = [Utils.rndNum(255), Utils.rndNum(255), Utils.rndNum(255), Math.round(a * 100) / 100];
        this.color = `rgba(${temp[0]}, ${temp[1]}, ${temp[2]}, ${temp[3]})`;
    }

    getID(){
        return this.id;
    }

    getColor(){
        return this.color;
    }

    setCell(cell){
        this.arrCells.push(cell);
    }

    getArrCells(){
        return this.arrCells;
    }
}

class Cell{

    // The rect() functions draws the rectangular in the screen we are seeing.
    // It colors it based on the current stroke property value and the fill property.
    // I think there are more options but thats what I am using atm.

    // We * 1 to convent the possible strings into numbers.
    constructor(name, x, y, width, height, nets, isTerminal){
        this.name = name;
        this.x = x * 1;
        this.y = y * 1;
        this.width = width * 1;
        this.height = height * 1;
        this.shape = rect(x * 1, y * 1, width * 1, height * 1);  // Just to be sure to convert the possible string from json to a number
        this.nets = nets;
        this.isTerminal = isTerminal;
    }
    
    reColor(){
        // If its terminal we can't show/draw it since they don't have x or y
        if(!this.isTerminal) this.shape = rect(this.x, this.y, this.width, this.height);
    }

    setShape(x, y, width, height){
        this.shape = rect(x, y, width, height);
    }
    
    getName(){
        return this.name;
    }

    getX(){
        return this.x;
    }

    getY() {
        return this.y;
    }

    getWidth(){
        return this.width;
    }

    getHeight(){
        return this.height;
    }

    getNets(){
        return this.nets;
    }

    isTerminal(){
        return isTerminal;
    }

}
