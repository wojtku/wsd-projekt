const leftStart = 0;
const topStart = 0;
const leftEnd = 904;
const topEnd = 492;
const pointSize = 11;
let wolves = [];

const canvas = document.getElementById("myCanvas");
let context = canvas.getContext("2d");

/* default wolf type is alfa */
class Wolf {
    constructor(x, y, type = "ALFA") {
        this.x = x;
        this.y = y;
        this.type = type;
    }
}

const drawWolf = ({x,y, type}) => {
    context.beginPath();

    if(type == "ALPHA") {
        context.fillStyle="#FFFFFF";
    } else if (type == "BETA") {
        context.fillStyle="pink"
    } else if (type == "DELTA") {
        context.fillStyle="violet"
    } else {
        context.fillStyle="yellow";
    }


    console.log('Pozycja x: ' + x);
    console.log('Pozycja y: ' + y);
    context.arc(scaleXPosition(x), scaleYPosition(y), pointSize, 0, Math.PI*2, true);
    context.closePath();
    context.fill();
};

const clearMap = () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
};

const getWolvesLocation = () => {
    const wolf1 = new Wolf(getRandomX(), getRandomY());
    const wolf2 = new Wolf(getRandomX(), getRandomY());
    const wolf3 = new Wolf(getRandomX(), getRandomY());
    const wolf4 = new Wolf(getRandomX(), getRandomY());
    const wolf5 = new Wolf(getRandomX(), getRandomY());
    return [wolf1, wolf2, wolf3, wolf4, wolf5];
};


const fetchMap = (successCallback, errorCallback) => {
    $.ajax({
       url: "/api/map",
       success: function(data) {
           console.log("success fetching map");
           successCallback(data);
       },
        error: function() {
           console.error("Erorr while fetching map");
            errorCallback();
        }
    });
};

const fetchWolvesLocation = (successCallback, errorCallback) => {
    // api
    $.ajax({
        url: "http://localhost:8080/api/wolf",
        success: function(data) {
            console.log("success fetching wolves");
            successCallback(data);
        },
        error: function() {
            console.error("Erorr fetching wolves");
            errorCallback();
        }
    });

};

const getRandomX = () => {
    //return Math.floor(Math.random() * leftEnd) + leftStart;
    return -10;
};

const getRandomY = () => {
    //return Math.floor(Math.random() * topEnd) + topStart;
    return 5;
};

const updatePosition = () => {
    if(false) {
        const wolves = getWolvesLocation();
    clearMap();
        wolves.forEach(function(wolf) {
            drawWolf(wolf);
        });
    } else {
        fetchWolvesLocation((wolves)=>{
        clearMap();
        wolves.forEach(function(wolf) {
            drawWolf(wolf);
        });
    }, () => {
        console.error("Cant get wolves");
    });
    }
};

const scaleXPosition = (x) => (30.2*x + leftEnd/2);
const scaleYPosition = (y) => (-16.4*y + topEnd/2);

/* updatePosition every 2 seconds */
window.setInterval(function(){
    updatePosition()
}, 1200);
