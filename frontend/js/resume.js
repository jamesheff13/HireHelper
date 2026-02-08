document.addEventListener("DOMContentLoaded", () => {
    const backBtn = document.getElementById("backToDashboard");
    const tipsSection = document.getElementById("tipsSection");

    // -----------------------------
    // Get resume text from sessionStorage
    // -----------------------------
    const resumeText = sessionStorage.getItem("resumeText");

    if (resumeText) {
        tipsSection.style.display = "grid";

        const previewEl = document.getElementById("resumePreview");
        previewEl.textContent = resumeText.slice(0, 300);

        // Call backend AI analyzer
        fetch("/api/resume/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ resume_text: resumeText })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }

            document.getElementById("overallScore").innerText = data.overall_score ?? "N/A";

            document.getElementById("headerTip").innerText = data.tips?.header?.tip ?? "N/A";
            document.getElementById("headerScore").innerText = data.tips?.header?.score ?? "N/A";

            document.getElementById("objectiveTip").innerText = data.tips?.objective?.tip ?? "N/A";
            document.getElementById("objectiveScore").innerText = data.tips?.objective?.score ?? "N/A";

            document.getElementById("experienceTip").innerText = data.tips?.experience?.tip ?? "N/A";
            document.getElementById("experienceScore").innerText = data.tips?.experience?.score ?? "N/A";

            document.getElementById("skillsTip").innerText = data.tips?.skills?.tip ?? "N/A";
            document.getElementById("skillsScore").innerText = data.tips?.skills?.score ?? "N/A";

            document.getElementById("educationTip").innerText = data.tips?.education?.tip ?? "N/A";
            document.getElementById("educationScore").innerText = data.tips?.education?.score ?? "N/A";

            document.getElementById("structureTip").innerText = data.tips?.structure?.tip ?? "N/A";
            document.getElementById("structureScore").innerText = data.tips?.structure?.score ?? "N/A";
        })

        .catch(err => {
            console.error("Resume analyze error:", err);

            // Fallback display
            document.getElementById("overallScore").innerText = "N/A";
        });
    }

    // -----------------------------
    // Back button
    // -----------------------------
    backBtn.addEventListener("click", () => {
        window.location.href = "dashboard.html";
    });
});

