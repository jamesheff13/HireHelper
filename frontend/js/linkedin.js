// console.log("linkedin.js is running");
// document.addEventListener("DOMContentLoaded", () => {
//     const uploadBtn = document.getElementById("uploadLinkedIn");
//     const backBtn = document.getElementById("backToDashboard");
//     const fileInput = document.getElementById("linkedinFile");

//     uploadBtn.addEventListener("click", async () => {
//         const file = fileInput.files[0];
//         if (!file) {
//             alert("Please upload your LinkedIn PDF first.");
//             return;
//         }

//         const formData = new FormData();
//         formData.append("file", file);

//         try {
//             const res = await fetch("http://127.0.0.1:5000/api/linkedin/upload", {
//                 method: "POST",
//                 body: formData
//             });

//             if (!res.ok) throw new Error("Upload failed");

//             const data = await res.json();

//             document.getElementById("connectBox").style.display = "none";
//             const tipsSection = document.getElementById("tipsSection");
//             tipsSection.style.display = "grid";

//             document.getElementById("headlineTip").innerText = data.recommendations.headline;
//             document.getElementById("aboutTip").innerText = data.recommendations.about;
//             document.getElementById("experienceTip").innerText = data.recommendations.experience;
//             document.getElementById("connectionTip").innerText = data.recommendations.connections;
//             document.getElementById("visualTip").innerText = data.recommendations.visual;

//         } catch (err) {
//             console.error(err);
//             alert("Failed to analyze LinkedIn PDF.");
//         }

//     });

//     backBtn.addEventListener("click", () => {
//         window.location.href = "dashboard.html";
//     });
// });

console.log("linkedin.js is running");

document.addEventListener("DOMContentLoaded", () => {
    const uploadBtn = document.getElementById("uploadLinkedIn");
    const backBtn = document.getElementById("backToDashboard");
    const fileInput = document.getElementById("linkedinFile");
    const connectBox = document.getElementById("connectBox");
    const tipsSection = document.getElementById("tipsSection");

    uploadBtn.addEventListener("click", async () => {
        console.log("Analyze Profile button clicked!"); // 🔹 confirm click

        const file = fileInput.files[0];
        if (!file) {
            alert("Please upload your LinkedIn PDF first.");
            return;
        }

        console.log("Sending PDF to backend:", file.name); // 🔹 confirm file

        // Show temporary analyzing message
        tipsSection.style.display = "grid";
        tipsSection.innerHTML = "<p>Analyzing your profile, please wait...</p>";

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch("http://127.0.0.1:5000/api/linkedin/upload", {
                method: "POST",
                body: formData
            });

            if (!res.ok) throw new Error("Upload failed");

            const data = await res.json();
            console.log("Backend response:", data); // 🔹 debug full response

            // Hide upload section
            connectBox.style.display = "none";

            // Restore tips section HTML with proper cards
            tipsSection.innerHTML = `
                <div class="tip-card"><h3>Profile Headline</h3><p id="headlineTip"></p></div>
                <div class="tip-card"><h3>About Section</h3><p id="aboutTip"></p></div>
                <div class="tip-card"><h3>Work Experience & Credibility</h3><p id="experienceTip"></p></div>
                <div class="tip-card"><h3>Connection Strategy</h3><p id="connectionTip"></p></div>
                <div class="tip-card"><h3>Visual Aesthetics</h3><p id="visualTip"></p></div>
            `;

            document.getElementById("headlineTip").innerText = data.recommendations.headline;
            document.getElementById("aboutTip").innerText = data.recommendations.about;
            document.getElementById("experienceTip").innerText = data.recommendations.experience;
            document.getElementById("connectionTip").innerText = data.recommendations.connections;
            document.getElementById("visualTip").innerText = data.recommendations.visual;

        } catch (err) {
            console.error(err);
            alert("Failed to analyze LinkedIn PDF.");
            // Hide tips section if error occurs
            tipsSection.style.display = "none";
        }
    });

    backBtn.addEventListener("click", () => {
        window.location.href = "dashboard.html";
    });
});

