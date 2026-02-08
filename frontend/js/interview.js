// interview.js

const startBtn = document.getElementById("start-btn");
const nextBtn = document.getElementById("next-btn");
const finishBtn = document.getElementById("finish-btn");
const questionDiv = document.getElementById("question");
const answerInput = document.getElementById("answer");
const feedbackDiv = document.getElementById("feedback");

let currentQuestion = "";
let answers = [];

// Disable buttons initially
nextBtn.disabled = true;
finishBtn.disabled = true;

// --- Helper to send POST requests ---
async function postJSON(url, data) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Server error: ${response.status} - ${text}`);
    }

    return await response.json();
  } catch (err) {
    console.error("Error connecting to server:", err);
    alert("Error: Could not connect to server.");
  }
}

// --- Start Interview ---
startBtn.addEventListener("click", async () => {
  const role = document.getElementById("role").value || "Software Engineer";
  const data = await postJSON("/api/interview/start", { role });

  if (data?.question) {
    currentQuestion = data.question;
    questionDiv.innerText = currentQuestion;
    answerInput.value = "";
    feedbackDiv.innerText = "";
    answers = [];

    // Enable buttons
    nextBtn.disabled = false;
    finishBtn.disabled = false;
  }
});

// --- Submit Answer and Get Next Question ---
nextBtn.addEventListener("click", async () => {
  const answer = answerInput.value.trim();
  if (!answer) {
    alert("Please enter an answer.");
    return;
  }

  answers.push({ question: currentQuestion, answer });

  const data = await postJSON("/api/interview/answer", { answer });

  if (data?.question) {
    currentQuestion = data.question;
    questionDiv.innerText = currentQuestion;
    answerInput.value = "";
  } else {
    questionDiv.innerText = "Interview complete!";
    answerInput.value = "";
    nextBtn.disabled = true;
    finishBtn.disabled = true;
  }
});

// --- Finish Interview and Get Feedback ---
finishBtn.addEventListener("click", async () => {
  const answer = answerInput.value.trim();
  if (answer) {
    answers.push({ question: currentQuestion, answer });
  }

  const data = await postJSON("/api/interview/finish", { answers });

  if (data?.feedback) {
    feedbackDiv.innerText = data.feedback;
    questionDiv.innerText = "Interview complete!";
    answerInput.value = "";
    nextBtn.disabled = true;
    finishBtn.disabled = true;
  }
});
