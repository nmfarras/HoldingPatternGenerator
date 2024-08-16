function computeSemicircle(center, trackWidthDegLon, theta, vecIpTgtNorm) {
    // Create the semicircle points
    const semicircle = [
        center[0] + (trackWidthDegLon / 2) * Math.cos(theta),
        center[1] + (trackWidthDegLon / 2) * Math.sin(theta)
    ];

    // Define the transformation matrix
    const transformationMatrix = [
        [vecIpTgtNorm[0], vecIpTgtNorm[1]],
        [-vecIpTgtNorm[1], vecIpTgtNorm[0]]
    ];

    // Apply the transformation
    const semicircleTransformed = [
        (semicircle[0] - center[0]) * transformationMatrix[0][0] +
            (semicircle[1] - center[1]) * transformationMatrix[1][0] +
            center[0],
        (semicircle[0] - center[0]) * transformationMatrix[0][1] +
            (semicircle[1] - center[1]) * transformationMatrix[1][1] +
            center[1]
    ];

    return semicircleTransformed;
}

function calculateMidpoint(ip, tgt, distanceDegLon) {
    // Calculate the direction vector from TGT to IP
    const directionVector = [
        tgt[0] - ip[0],
        tgt[1] - ip[1]
    ];
	/* console.log(directionVector); */

    // Calculate the magnitude of the direction vector
    const norm = Math.sqrt(directionVector[0] ** 2 + directionVector[1] ** 2);
	
	/* console.log(norm); */

    // Normalize the direction vector
    directionVector[0] /= norm;
    directionVector[1] /= norm;
	
	/* console.log(directionVector); */

    // Calculate the midpoint
    const midpoint = [
        ip[0] - distanceDegLon * directionVector[0],
        ip[1] - distanceDegLon * directionVector[1]
    ];
	
	/* console.log(distanceDegLon); */

    return midpoint;
}



function generateRacetrack(ip, tgt, speed, timeMinutes, trackWidth, distanceToIp, holdType) {
    // Convert time from minutes to hours
    const timeHours = timeMinutes / 60;

    // Calculate leg length (distance covered in the given time)
    const legLength = speed * timeHours; // in nautical miles
	
	console.log(legLength);

    const legLengthDegLat = legLength / 60;
    const trackWidthDegLon = trackWidth / 60;
	
	/* console.log(distanceToIp); */
	
	// Distance to midpoint in degrees of longitude
    distanceDegLon = distanceToIp / 60.0;

    // Calculate the vector from IP to TGT
    const vecIpTgt = [tgt[0] - ip[0], tgt[1] - ip[1]];
    const vecIpTgtNorm = vecIpTgt.map((val) => val / Math.sqrt(vecIpTgt[0] ** 2 + vecIpTgt[1] ** 2));

    // Perpendicular vector to IP-TGT (rotate by 90 degrees)
    const perpVec = [-vecIpTgtNorm[1], vecIpTgtNorm[0]];

    // Calculate the midpoint between start_leg_1 and end_leg_1
    const midpoint = calculateMidpoint(ip, tgt, distanceDegLon);

    // Adjust the centers to ensure the distance between them is legLength
    const center1 = midpoint.map((val, idx) => val + (legLengthDegLat / 2) * perpVec[idx]);
    const center2 = midpoint.map((val, idx) => val - (legLengthDegLat / 2) * perpVec[idx]);

    const theta = Array.from({ length: 100 }, (_, i) => (i / 99) * Math.PI);

    // Compute semicircle_1
    const semicircle1 = theta.map((angle) =>
        computeSemicircle(center1, trackWidthDegLon, angle, vecIpTgtNorm)
    );

    // Compute semicircle_2
    const semicircle2 = theta.map((angle) =>
        computeSemicircle(center2, trackWidthDegLon, angle + Math.PI, vecIpTgtNorm)
    );
	
	console.log(holdType == "racetrack");
	
	var startLeg1 = [0, 0];
	var startLeg2 = [0, 0];
	var endLeg1 = [0, 0];
	var endLeg2 = [0, 0];

    if (holdType == "racetrack") {
		// Calculate the points for the straight legs
		startLeg1 = semicircle1[semicircle1.length - 1];
		endLeg1 = semicircle2[0];
		
		console.log(startLeg1)

		startLeg2 = semicircle2[semicircle2.length - 1];
		endLeg2 = semicircle1[0];
	}
	if (holdType == "eight-figure") {
		// Calculate the points for the straight legs
		startLeg1 = semicircle1[semicircle1.length - 1];
		endLeg1 = semicircle2[semicircle2.length - 1];

		startLeg2 = semicircle2[0];
		endLeg2 = semicircle1[0];
	}

    // Combine points into the racetrack
    const racetrackPoints = {
        leg1: [startLeg1, endLeg1],
        semicircle1,
        leg2: [startLeg2, endLeg2],
        semicircle2
    };

    return racetrackPoints;
}

// Example usage
const ip = [-108, 7.3]; // Initial point (longitude, latitude)
const tgt = [-108.5, 7.38]; // Target point (longitude, latitude)
const speed = 250; // Aircraft speed in knots
const timeMinutes = 2.5; // Time in minutes for the leg length
const trackWidth = 2; // Width of the racetrack in nautical miles
const distanceToIp = 2;  // Distance of the pattern to IP in nautical miles
/* const holdType = "eight-figure"  // Either "eight-figure" or "racetrack" */
const holdType = "racetrack";  // Either "eight-figure" or "racetrack"

const racetrack = generateRacetrack(ip, tgt, speed, timeMinutes, trackWidth, distanceToIp, holdType);
console.log(racetrack);

// Now you can use the racetrack points in your JSBSim simulation.


// app.js
const racetrackPoints = {
    leg1: {
        x: [...racetrack.leg1.map(point => point[0])],
        y: [...racetrack.leg1.map(point => point[1])],
    },
    semicircle1: {
        x: [...racetrack.semicircle1.map(point => point[0])],
        y: [...racetrack.semicircle1.map(point => point[1])],
    },
    leg2: {
        x: [...racetrack.leg2.map(point => point[0])],
        y: [...racetrack.leg2.map(point => point[1])],
    },
    semicircle2: {
        x: [...racetrack.semicircle2.map(point => point[0])],
        y: [...racetrack.semicircle2.map(point => point[1])],
    },
};

console.log(racetrackPoints.leg1);
console.log(racetrackPoints.semicircle1);

// Create a scatter plot
const trace1 = {
    x: racetrackPoints.leg1.x,
    y: racetrackPoints.leg1.y,
    mode: 'lines',
    line: { color: 'blue' },
    name: 'Leg 1',
};

const trace2 = {
    x: racetrackPoints.semicircle1.x,
    y: racetrackPoints.semicircle1.y,
    mode: 'lines',
    line: { color: 'red' },
    name: 'Semicircle 1',
};

const trace3 = {
    x: racetrackPoints.semicircle2.x,
    y: racetrackPoints.semicircle2.y,
    mode: 'lines',
    line: { color: 'red' },
    name: 'Semicircle 2',
};

const trace4 = {
    x: racetrackPoints.leg2.x,
    y: racetrackPoints.leg2.y,
    mode: 'lines',
    line: { color: 'blue' },
    name: 'Leg 2',
};

const trace5 = {
    x: [tgt[0]],
    y: [tgt[1]],
    mode: 'markers',
	type: 'scatter',
    marker: {
        size: 6,
		color: 'red',
		symbol: 'triangle-up',
    },
    name: 'TGT',
};

const trace6 = {
    x: [ip[0]],
    y: [ip[1]],
    mode: 'markers',
	type: 'scatter',
    marker: {
        size: 6,
		color: 'yellow',
		symbol: 'square',
    },
    name: 'IP',
};
// Repeat for other segments (leg2 and semicircle2)

const layout = {
    title: 'Aircraft Racetrack',
    xaxis: { title: 'X' },
    yaxis: { title: 'Y' },
	aspectmode: 'equal',
};

Plotly.newPlot('racetrack-plot', [trace5, trace6, trace1, trace2, trace3, trace4], layout);
