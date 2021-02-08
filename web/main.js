const hint = document.getElementById("hint");
const error = document.getElementById("canvas-error");
const spinner = document.getElementById("spinner");
const shadow = document.getElementById("shadow");
const description = document.getElementById("description-input");
const draw = document.getElementById("draw");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const advanced = document.getElementById("advanced");
const settings = document.getElementById("settings");
const caret = document.getElementById("caret");
const speed = document.getElementById("drawing-speed");
const clear = document.getElementById("clear");
const useML = document.getElementById("use-ml");
const useRelSizes = document.getElementById("use-rel-sizes");

var textureImg = new Image();
textureImg.src = 'resources/texture32.png'
var texture;
textureImg.onload = function() {
	texture = ctx.createPattern(textureImg, "repeat");
}

advanced.addEventListener("click", function () {
    if (settings.getAttribute("aria-hidden") !== "true") {
        caret.style.transform = "rotate(0deg)";
    } else {
        caret.style.transform = "rotate(90deg)";
    }
    settings.setAttribute("aria-hidden", settings.getAttribute("aria-hidden") !== "true");
});

function downloadImage(data, filename) {
    var a = document.createElement("a");
    a.href = data;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
}

description.addEventListener("keydown", function (e) {
    let code;
    if (e.key !== undefined) {
        code = e.key;
    } else if (e.keyIdentifier !== undefined) {
        code = e.keyIdentifier;
    } else if (e.keyCode !== undefined) {
        code = e.keyCode;
    }

    if (code === "Enter" || code === 13) {
        e.preventDefault();
        draw.click();
    }
});

function resizeTextarea() {
    window.setTimeout(() => {
        description.style.height = "auto";
        description.style.height = description.scrollHeight - 10 + "px";
    }, 0);
}
description.addEventListener("keydown", resizeTextarea);
window.addEventListener("resize", resizeTextarea);
window.addEventListener("load", resizeTextarea);

function apiCall() {
    shadow.setAttribute("aria-hidden", false);
    hint.setAttribute("aria-hidden", true);
    error.setAttribute("aria-hidden", true);
    spinner.setAttribute("aria-hidden", false);

    desc = description.value;

    axios
        .post("http://127.0.0.1:5000/drawtomat", {
            description: desc,
            options: {
                use_machine_learning: useML.checked,
                use_relative_sizes: useRelSizes.checked,
            },
        })
        .then(function (res) {
            spinner.setAttribute("aria-hidden", true);
            shadow.setAttribute("aria-hidden", true);
            drawPicture(res.data);
        })
        .catch(function (err) {
            spinner.setAttribute("aria-hidden", true);
            error.setAttribute("aria-hidden", false);
            console.error(err.response)
        });
}


clear.addEventListener("click", clearCanvas); 

var intervalId = null;

function clearCanvas() {
    clearInterval(intervalId)
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function drawPicture(data) {
    clearCanvas();

    let width = data.bounds.right - data.bounds.left;
    let height = data.bounds.top - data.bounds.bottom;
    let padding = 20;

    let offx = (data.bounds.right + data.bounds.left) / 2;
    let offy = (data.bounds.top + data.bounds.bottom) / 2;

    let cx = canvas.width / 2;
    let cy = canvas.height / 2;
    let scale = 2 * Math.min(cx / (width + padding), cy / (height + padding));

    ctx.clearRect(0, 0, canvas.width, canvas.height);

	ctx.strokeStyle = texture;
	ctx.lineWidth = 2;
	ctx.lineCap = "round";

    let objIdx = 0;
    let stkIdx = 0;
    let idx = 0;
    let duration = speed.value;
    let stroke = data.drawing[objIdx][stkIdx];
    let t0 = Math.min(...stroke[2]);
    let t1 = Math.max(...stroke[2]);
    let t = 0;
    let timeScale = duration < t1 - t0 ? duration / (t1 - t0) : 1;
    let step = 10;
    intervalId = setInterval(function () {
        t += step;

        if (t > duration) {
            ++stkIdx;
            idx = 0;

            if (stkIdx >= data.drawing[objIdx].length) {
                ++objIdx;
                stkIdx = 0;
            }
            if (objIdx >= data.drawing.length) {
                clearInterval(intervalId);
                return;
            }

            stroke = data.drawing[objIdx][stkIdx];
            t0 = Math.min(...stroke[2]);
            t1 = Math.max(...stroke[2]);
            timeScale = duration < t1 - t0 ? duration / (t1 - t0) : 1;
            t = 0;
        }

        while (t > (stroke[2][idx] - t0) * timeScale) {
            ++idx;
            ctx.beginPath();
            ctx.moveTo(cx + scale * (stroke[0][idx] - offx), cy + scale * (stroke[1][idx] - offy));
            ctx.lineTo(cx + scale * (stroke[0][idx + 1] - offx), cy + scale * (stroke[1][idx + 1] - offy));
            ctx.stroke();
        }
    }, step);
}
