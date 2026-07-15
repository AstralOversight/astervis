var mapMin = 0;

const params = new URLSearchParams(document.location.search);
const rawmap = {};

var summap = function(map, value) {
    if (map[parseInt(value) - mapMin]) map[parseInt(value) - mapMin] = map[parseInt(value) - mapMin]+1;
    else map[parseInt(value) - mapMin] = 1;
}

var callback = function() {
    const canvas = document.getElementById("obsspace");
    const ctx = canvas.getContext("2d");
    const dark_range = document.getElementById("dark");
    const light_range = document.getElementById("light");

    var header = this.getHeader();
    var data = this.getDataUnit();

    const width = header.get('NAXIS1'); // get image width
    const height = header.get('NAXIS2'); // get image height
    canvas.width = width;
    canvas.height = height;

    curObs = header.get('PRODUCT');

    //Draw the image
    const imgData = ctx.createImageData(width, height);
    data.getFrame(0, (pixels) => {
        //Due to the side full of black and white pixels, this is kinda broken
        // On further inspection, they're not actually fully black???
        var totminmax = FITS.ImageUtils.getExtent(pixels);
        mapMin = totminmax[0];
        dark_range.min = totminmax[0];
        dark_range.max = totminmax[1];
        light_range.min = totminmax[0];
        light_range.max = totminmax[1];

        const range = light_range.value - dark_range.value;

        // Paint the pixels.
        for (var i = 0; i < pixels.length; i++) {
            var value = ((pixels[i] - dark_range.value) / range) * 255;

            summap(rawmap, pixels[i]);//-totminmax[0]);//+header.get('BZERO'));???????? maybe?? idk,,,

            imgData.data[i*4 + 0] = value;
            imgData.data[i*4 + 1] = value;
            imgData.data[i*4 + 2] = value;
            imgData.data[i*4 + 3] = 255;
        };

        ctx.putImageData(imgData, 0, 0);

        graph()
    })

    const info_list = document.getElementById("info-list");
    Object.entries(header.cards).forEach(([key, value]) => {
        if (value.value || value.comment) {
            var item = document.createElement("li");
            var str = key + ": " + value.value;
            if (value.comment) str += " /" + value.comment;
            item.append(str);
            info_list.appendChild(item);
        }
    });
}

function graph() {
    const canvas = document.getElementById("light-graph");
    const ctx = canvas.getContext("2d");
    const values = Object.entries(rawmap);
    const dark_range = document.getElementById("dark");
    const light_range = document.getElementById("light");

    // Dimensions
    canvas.width = 1000;
    canvas.height = 350;
    const buffer = 20;

    // Maximum pixel count of light level.
    var max = 0;
    for (let i = 0; i < values.length; i++) {
        if (max < values[i][1]) max = values[i][1];
    }

    // Bar queue
    var queue = []
    
    // Trace graph
    var tickCount = 24;
    ctx.beginPath();
    ctx.moveTo(0, canvas.height-buffer);
    for (let i = 0; i < values.length; i++) {
        ctx.lineTo(i*canvas.width/values.length, canvas.height-(values[i][1]*(canvas.height-buffer)/max)-buffer);
        // Current level text & tick
        if (i % Math.floor(2*values.length/tickCount) == 0) ctx.fillText(parseInt(values[i][0])+mapMin, (i*canvas.width/values.length)+2, canvas.height-1)
        if (i % Math.floor(2*values.length/tickCount) == Math.floor(values.length/tickCount)) ctx.fillText(parseInt(values[i][0])+mapMin, (i*canvas.width/values.length)+2, canvas.height-11)
        if (i % Math.floor(values.length/tickCount) == 0) ctx.fillRect(i*canvas.width/values.length, canvas.height-buffer, 1, buffer);

        // Add to queue the bars for the dark & light zones.
        if (i+1 < values.length && ((parseInt(values[i][0]) <= dark_range.value-mapMin && parseInt(values[i+1][0]) > dark_range.value-mapMin)
                                || (parseInt(values[i][0]) <= light_range.value-mapMin && parseInt(values[i+1][0]) > light_range.value-mapMin))) {
            queue.push(i*canvas.width/values.length);
        }
    }
    ctx.closePath();
    ctx.fill();

    // Draw the queued bars
    ctx.fillStyle = "red";
    queue.forEach(pos => {
        ctx.fillRect(pos, 0, 1, canvas.height-buffer);
    })
}