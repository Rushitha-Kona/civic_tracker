// 📍 Get GPS Location
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;

                document.getElementById("location").value = `${lat},${lon}`;
                document.getElementById("locStatus").innerText = "Location captured ✅";
            },
            () => {
                document.getElementById("locStatus").innerText = "Permission denied ❌";
            }
        );
    }
}

// 📩 Submit Complaint
async function submitComplaint() {
    const text = document.getElementById("text").value;
    const location = document.getElementById("location").value;

    const res = await fetch("/report", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text, location })
    });

    const data = await res.json();
    document.getElementById("result").innerText =
        `ID: ${data.complaint_id} | ${data.location}`;

    loadComplaints();
}

// 📋 Load complaints
async function loadComplaints() {
    const res = await fetch("/all");
    const data = await res.json();

    const table = document.getElementById("tableBody");
    table.innerHTML = "";

    data.forEach(c => {
        table.innerHTML += `
        <tr>
            <td>${c.complaint_id}</td>
            <td>${c.category}</td>
            <td>${c.status}</td>
            <td>${c.location}</td>
            <td>
        ${c.image_url ? `<a href="${c.image_url}" target="_blank">View</a>` : "No Image"}
    </td>
            <td>
                <button onclick="updateStatus('${c.complaint_id}','Resolved')">
                    Resolve
                </button>
            </td>
        </tr>`;
    });
}

// 🔄 Update status
async function updateStatus(id, status) {
    await fetch(`/update/${id}?status=${status}`, { method: "PUT" });
    loadComplaints();
}

// Auto refresh
setInterval(loadComplaints, 5000);
loadComplaints();