const deg= 6;
const hr = document.querySelector("#hr");
const mn = document.querySelector("#mn");
const tg = document.querySelector("#tg");
var list_int = []
var durations = document.getElementsByClassName("duration");


function listStringToInt(list) {
    for(i=0; i < list.length; i++) {
        console.log(list[i])
        num = parseInt(list[i]);
        list_int.push(num);
    }
}

listStringToInt(durations)

console.log(list_int);

setInterval(() => {
    let day = new Date();
    let hh = day.getHours() * 30;
    let mm = day.getMinutes() * deg;
    hr.style.transform = `rotateZ(${hh+(mm/12)}deg)`;
    mn.style.transform = `rotateZ(${mm}deg)`;
})