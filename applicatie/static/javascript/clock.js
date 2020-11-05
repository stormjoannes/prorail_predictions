const deg= 6;
const hr = document.querySelector("#hr");
const mn = document.querySelector("#mn");
const tg = document.querySelector("#tg");
var durations = document.getElementsByClassName("duration");
var dates = document.getElementsByClassName("date");

// de target date is de datum die je was meegegeven plus de duur die het model heeft gegeven
function createTargetDate() {
    var targets = []
    for(i=0; i < dates.length; i++) {
        var target_date = new Date(dates[i].textContent);
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

    // een target moet dezelfde yaar, maand en dezelfde dag hebben om het voor de clock "valid" te noemen
    else {
        for(i=0; i < targets.length; i++) {
            let day = targets[i].getDate();
            let month = targets[i].getMonth();
            if(targets[i] >= today) {
                if(month == today.getMonth()) {
                    if(day == today.getDate()) {
                        valid_dates.push(targets[i]);
                    }
                }
            }
        }
        return valid_dates;
    }
};

// kijk of een target 5 minuten ervan af is zo ja dan maak toon je de target op de clock
function getClosestTargets() {
    let today = new Date();
    var valid_targets = checkIfTargetValid();
    for(i=0; i < valid_targets.length; i++) {
        console.log('valid ' + valid_targets);
        var difference = valid_targets[i] - today;
        difference = difference/1000;
        difference = difference/60;
        var difference_min = Math.floor(difference % 60);
    }
}

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
getClosestTargets();