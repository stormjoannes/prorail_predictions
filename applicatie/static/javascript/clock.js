const deg= 6;
const hr = document.querySelector("#hr");
const mn = document.querySelector("#mn");
const tg = document.querySelector("#tg");
var durations = document.getElementsByClassName("duration");
var times = document.getElementsByClassName("time");

function getMinute(list, i) {
    var d = new Date(list[i].textContent);
    return d.getMinutes();
}

function createTargetDate() {
    var targets = []
    for(i=0; i < times.length; i++) {
        var target_date = new Date(times[i].textContent);
        target_date = target_date.setMinutes(target_date.getMinutes() + Number(durations[i].textContent));
        target_date = new Date(target_date);
        targets.push(target_date);
    }
    return targets;
};

function checkIfTargetValid() {
    let today = new Date();
    var targets = createTargetDate();
    var valid_dates = [];

    if(targets.length <= 0) {
        return [];
    }

    else {
        for(i=0; i < targets.length; i++) {
            if(targets[i] >= today) {
                valid_dates.push(targets[i]);
            }
        }

        return valid_dates;
    }
};

function getClosestTargets() {
    let today = new Date();
    var valid_targets = checkIfTargetValid();
    for(i=0; i < valid_targets.length; i++) {
        var difference = valid_targets[i] - today;
        difference = difference/1000;
        difference = difference/60;
        var difference_min = Math.floor(difference % 60);
        console.log(difference_min);
    }
}

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
getClosestTargets();