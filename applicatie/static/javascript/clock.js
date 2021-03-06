const deg= 6;
const hr = document.querySelector("#hr");
const mn = document.querySelector("#mn");
const th = document.querySelector("#th");
const tm = document.querySelector("#tm");

// met deze functie maken we een target door te kijken of de datum wel geldig is en door twee nieuwe wijzers te maken die de target tijd geeft
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
