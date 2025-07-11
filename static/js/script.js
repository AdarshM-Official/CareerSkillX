document.getElementById("careerForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const field = this.field.value;
  const interests = this.interests.value;

  const response = await fetch("/recommend", {
    method: "POST",
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ field, interests })
  });

  const data = await response.json();
  document.getElementById("careerTitle").textContent = data.message;
  document.getElementById("results").classList.remove("hidden");

  const ctx = document.getElementById("careerChart").getContext("2d");
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: Object.keys(data.career_scores),
      datasets: [{
        data: Object.values(data.career_scores),
        backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#17a2b8']
      }]
    }
  });
});
