
document.getElementById("journalForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const age = document.getElementById("age").value;
  const gender = document.getElementById("gender").value;
  const journal = document.getElementById("journal").value;

  const resultCard = document.getElementById("resultCard");
  const stateEl = document.getElementById("state");
  const confidenceEl = document.getElementById("confidence");

  resultCard.classList.add("hidden");
  stateEl.innerText = "Analyzing...";
  confidenceEl.innerText = "...";

  try {
    
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ age, gender, journal })
    });

    const data = await response.json();

    stateEl.innerText = data.mental_state;
    confidenceEl.innerText = data.confidence;

    resultCard.classList.remove("hidden");

  } catch (error) {
    stateEl.innerText = "Error";
    confidenceEl.innerText = "Backend not reachable";
    resultCard.classList.remove("hidden");
  }
});
