const departmentId = 1;

async function loadQueue(){

    const response =
    await fetch(
        `http://127.0.0.1:8000/queue/${departmentId}`
    );

    const data =
    await response.json();

    let html = `
    <table>
        <tr>
            <th>Token</th>
            <th>Patient</th>
            <th>Status</th>
        </tr>
    `;

    data.forEach(token => {

        html += `
        <tr>
            <td>${token.token_number}</td>
            <td>${token.patient_name}</td>
            <td>${token.status}</td>
        </tr>
        `;

    });

    html += "</table>";

    document.getElementById("queue").innerHTML =
    html;
}

async function loadServing(){

    const response =
    await fetch(
        `http://127.0.0.1:8000/serving/${departmentId}`
    );

    const data =
    await response.json();

    document.getElementById("serving").innerHTML = `
        <div class="serving-token">
            ${data.token || "-"}
        </div>

        <div class="serving-patient">
            ${data.patient_name || data.patient || "No Patient"}
        </div>
    `;
}

async function loadStats(){

    const response =
    await fetch(
        `http://127.0.0.1:8000/department/${departmentId}/stats`
    );

    const data =
    await response.json();

    document.getElementById("stats").innerHTML = `

    <div class="stat-box">

        <div class="stat total">
            <div class="number">
                ${data.total_tokens}
            </div>
            <div class="label">
                Total
            </div>
        </div>

        <div class="stat waiting">
            <div class="number">
                ${data.waiting}
            </div>
            <div class="label">
                Waiting
            </div>
        </div>

    </div>

    <div class="stat-box">

        <div class="stat serving">
            <div class="number">
                ${data.serving}
            </div>
            <div class="label">
                Serving
            </div>
        </div>

        <div class="stat completed">
            <div class="number">
                ${data.completed}
            </div>
            <div class="label">
                Completed
            </div>
        </div>

    </div>
    `;
}

loadQueue();
loadServing();
loadStats();

setInterval(() => {
    loadQueue();
    loadServing();
    loadStats();
}, 5000);