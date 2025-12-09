async function runSimulation() {
    const program = document.getElementById("programInput").value;
    const memory = document.getElementById("memoryInput").value;

    // Run Python function
    const result = await pyscript.runtime.globals.get('simulate')(program, memory);

    // Display results
    document.getElementById("output").innerHTML = formatResult(result);
}

function formatResult(r) {

    if (r.error) {
        return `<p style="color:red">${r.error}</p>`;
    }

    let html = `
        <h3>Performance Metrics</h3>
        <p><b>Cycles:</b> ${r.cycles}</p>
        <p><b>IPC:</b> ${r.ipc}</p>
        <p><b>Branch Misprediction Rate:</b> ${r.branch_misprediction}</p>

        <h3>Instruction Timeline</h3>
        <table border="1" cellpadding="5">
        <tr>
            <th>Instruction</th>
            <th>Issue</th>
            <th>Exec Start</th>
            <th>Exec End</th>
            <th>Write</th>
            <th>Commit</th>
        </tr>
    `;

    r.timeline.forEach(row => {
        html += `
        <tr>
            <td>${row.text}</td>
            <td>${row.issue}</td>
            <td>${row.exec_start}</td>
            <td>${row.exec_end}</td>
            <td>${row.write}</td>
            <td>${row.commit}</td>
        </tr>`;
    });

    html += "</table>";
    return html;
}
