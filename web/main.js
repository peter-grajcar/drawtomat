const hint = document.getElementById("hint");
const error = document.getElementById("canvas-error");
const spinner = document.getElementById("spinner");
const shadow = document.getElementById("shadow");
const description = document.getElementById("description-input");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

function resizeTextarea() {
    window.setTimeout(() => {
        description.style.height = "auto";
        description.style.height = description.scrollHeight - 10 + "px";
    }, 0);
}

window.addEventListener("resize", resizeTextarea);
window.addEventListener("load", resizeTextarea);

function apiCall() {
    hint.setAttribute("aria-hidden", true);
    error.setAttribute("aria-hidden", true);
    spinner.setAttribute("aria-hidden", false);

    desc = description.value;

    axios
        .post("http://127.0.0.1:5000/drawtomat", {
            description: desc,
        })
        .then(function (res) {
            spinner.setAttribute("aria-hidden", true);
            shadow.setAttribute("aria-hidden", true);
            console.log(res.data);
            drawPicture(res.data);
        })
        .catch(function (err) {
            spinner.setAttribute("aria-hidden", true);
            error.setAttribute("aria-hidden", false);
        });
}

function drawPicture(data) {
    let width = data.bounds.right - data.bounds.left;
    let height = data.bounds.top - data.bounds.bottom;
    let padding = 50;

    let scale = Math.min(canvas.width / (width + padding), canvas.height / (height + padding));
    let cx = canvas.width / 2;
    let cy = canvas.height / 2;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let obj = 0; obj < data.drawing.length; ++obj)
        for (let s = 0; s < data.drawing[obj].length; ++s) drawStroke(ctx, data.drawing[obj][s], cx, cy, scale);
}

function drawStroke(ctx, stroke, cx, cy, scale) {
    let t0 = Math.min(...stroke[2]);
    let t1 = Math.max(...stroke[2]);
    let duration = 1000;
    let timeScale = duration / (t1 - t0);
    let t = 0;
    let idx = 0;

    let step = 10;
    let interval = setInterval(function () {
        t += step;
        if (t > duration) clearInterval(interval);
        while (t > (stroke[2][idx] - t0) * timeScale) {
            ++idx;
            ctx.beginPath();
            ctx.moveTo(cx + scale * stroke[0][idx], cy + scale * stroke[1][idx]);
            ctx.lineTo(cx + scale * stroke[0][idx + 1], cy + scale * stroke[1][idx + 1]);
            ctx.stroke();
        }
    }, step);
}
