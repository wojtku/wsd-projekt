const leftStart = 0;
const topStart = 0;
const leftEnd = 631;
const topEnd = 404;
const pointSize = 5;
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

const drawWolf = ({x,y}) => {
    context.beginPath();
    context.arc(x, y, pointSize, 0, Math.PI*2, true);
    context.closePath();
    context.fill();
};

const clearMap = () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
};

const getWolvesLocation = () => {
    /* Tu b�dzie pobieranie danych o lokalizacji z serwera
     * zamiast randoma */

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
        url: "/api/wolf",
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
    return Math.floor(Math.random() * leftEnd) + leftStart;
};

const getRandomY = () => {
    return Math.floor(Math.random() * topEnd) + topStart
};

const updatePosition = () => {

    // wolves = getWolvesLocation();

    fetchWolvesLocation((wolves)=>{
        clearMap();
        wolves.forEach(function(wolf) {
            drawWolf(wolf);
        });
    }, () => {
        console.error("Cant get wolves");
    });

};

/* updatePosition every 2 seconds */
window.setInterval(function(){
    updatePosition()
}, 1000);
