document.getElementById("journalForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const age = document.getElementById("age").value;
  const gender = document.getElementById("gender").value;
  const journal = document.getElementById("journal").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ age, gender, journal })
    });

    const data = await response.json();

    document.getElementById("result").innerHTML = `
      <b>Mental State:</b> ${data.mental_state}<br>
      <b>Confidence:</b> ${data.confidence}%<br>
    `;
  } catch (error) {
    document.getElementById("result").innerHTML =
      "❌ Backend not reachable. Is FastAPI running?";
  }
});
