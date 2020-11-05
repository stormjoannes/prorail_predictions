const deg= 6;
const hr = document.querySelector("#hr");
const mn = document.querySelector("#mn");
const th = document.querySelector("#th");
const tm = document.querySelector("#tm");

function create_target(date) {
    var today = new Date();
    var target_date = new Date(date.textContent);
    if(target_date >= today) {
        if(target_date.getMonth() == today.getMonth()) {
            if(target_date.getDate() == today.getDate()) {
                let thh = target_date.getHours() * 30;
                let tmm = target_date.getMinutes() * deg;
                th.style.transform = `rotateZ(${thh+(tmm/12)}deg)`;
                th.style.display = "flex";
                tm.style.transform = `rotateZ(${tmm}deg)`;
                tm.style.display = "flex";
            }
            else {
                window.alert("De dag is of te ver of de voorspelling gaat te ver (voorbij 00.00)")
            }
        }

        else {
            window.alert("De maand is te ver")
        }
    }
    else {
        window.alert("Geen datums in het verleden")
    }
}
// de target date is de datum die je was meegegeven plus de duur die het model heeft gegeven
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
        }
        return valid_dates;
    }
};

// kijk of een target 5 minuten ervan af is zo ja dan maak toon je de target op de clock
function getClosestTargets() {
    let today = new Date();
    var valid_targets = checkIfTargetValid();

    var closest_target = [];

    for(i=0; i < valid_targets.length; i++) {
        var difference = valid_targets[i] - today;
        // zo bereken je het verschil...blijkbaar
        difference = difference/1000;
        difference = difference/60;
        var difference_min = Math.floor(difference % 60);
        if(difference_min <= 5) {
            closest_target.push(valid_targets[i]);
        }
        else {
            console.log('none');
        }
    }
    console.log(closest_target);
    return closest_target;
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
