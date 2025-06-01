async function solvePoW(challenge, difficulty) {
    console.log(`Challenge received with ID: ${POW_CHALLENGE_ID}`)
    console.log(`Solving challenge: ${challenge}, with difficulty: ${difficulty}`);
    let solution = 0;
    while (true) {
        const encoder = new TextEncoder();
        const guess = encoder.encode(challenge + solution);
        const hashBuffer = await crypto.subtle.digest("SHA-256", guess);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        if (hashHex.startsWith("0".repeat(difficulty))) {
            console.log(`Solved! Challenge ID: ${POW_CHALLENGE_ID}, Nonce: ${solution}, Hash: ${hashHex}`);
            return solution.toString();
        }
        solution++;
    }
}

document.getElementById("challengeIdDisplay").textContent = POW_CHALLENGE_ID;
document.getElementById("challengeDisplay").textContent = POW_CHALLENGE;
document.getElementById("difficultyDisplay").textContent = POW_DIFFICULTY;

solvePoW(POW_CHALLENGE, parseInt(POW_DIFFICULTY)).then(solution => {
    fetch("/pow", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            challenge_id: POW_CHALLENGE_ID,
            solution: solution,
            next: NEXT_URL
        })
    }).then(res => {
        if (res.ok) {
            window.location.href = NEXT_URL;
        } else {
            document.body.innerHTML = "<h2>Verification failed. Try refreshing.</h2>";
        }
    }).catch(error => {
        console.error("Error submitting PoW solution:", error);
        document.body.innerHTML = "<h2>Error submitting solution</h2>";
    });
}).catch(error => {
    console.error("Error solving PoW:", error);
    document.body.innerHTML = "<h2>Error solving PoW</h2>";
});