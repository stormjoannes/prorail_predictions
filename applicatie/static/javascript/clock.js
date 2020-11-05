const deg= 6;
const hr = document.querySelector("#hr");
const mn = document.querySelector("#mn");
const tg = document.querySelector("#tg");
var durations = document.getElementsByClassName("duration");
var dates = document.getElementsByClassName("date");

// met behulp van de constante herhaling van de interval kunnen we de wijzers van de klok laten draaien
function createClock() {
    setInterval(() => {
        let day = new Date();
        let hh = day.getHours() * 30;
        let mm = day.getMinutes() * deg;
        hr.style.transform = `rotateZ(${hh+(mm/12)}deg)`;
        mn.style.transform = `rotateZ(${mm}deg)`;
    });
};

createClock();