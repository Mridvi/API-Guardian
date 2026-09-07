async function loadStats() {
    try {
        const response = await fetch("/api/stats");

        if (!response.ok) {
            throw new Error("Failed to fetch statistics");
        }

        const stats = await response.json();

        document.getElementById("total-requests").textContent =
            stats.total_requests;

        document.getElementById("successful-requests").textContent =
            stats.successful_requests;

        document.getElementById("rate-limited-requests").textContent =
            stats.rate_limited_requests;

    } catch (error) {
        console.error("Error:", error);
    }
}



async function loadRecentRequests() {
    try {
        const response = await fetch("/api/recent-requests");

        if (!response.ok) {
            throw new Error("Failed to fetch recent requests");
        }

        const requests = await response.json();

        const requestList = document.getElementById("request-list");

        requestList.innerHTML = "";

        if (requests.length === 0) {
            requestList.innerHTML = `
                <tr>
                    <td colspan="4">No requests yet</td>
                </tr>
            `;
            return;
        }

        requests.slice().reverse().forEach(request => {
            const row = document.createElement("tr");

            const date = new Date(request.time * 1000);

            const time = date.toLocaleTimeString();

            const statusClass =
                request.status === 200
                    ? "status-success"
                    : "status-error";

            row.innerHTML = `
                <td>${time}</td>
                <td>${request.method}</td>
                <td>${request.endpoint}</td>
                <td class="${statusClass}">
                    ${request.status}
                </td>
            `;

            requestList.appendChild(row);
        });

    } catch (error) {
        console.error("Error loading recent requests:", error);
    }
}



loadStats();
loadRecentRequests();

setInterval(loadStats, 5000);
setInterval(loadRecentRequests, 5000);