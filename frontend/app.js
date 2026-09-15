const API_BASE = "http://127.0.0.1:8001";
let currentSyllabus = "";
let currentPlan = [];

async function sendRequest(endpoint, payload) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Backend error ${response.status}: ${errorText}`);
  }

  return await response.json();
}

document.getElementById("extractBtn").addEventListener("click", async () => {
  const syllabusText = document
    .getElementById("syllabusText")
    .value
    .trim();

  if (!syllabusText) {
    alert("Please paste your syllabus.");
    return;
  }

  const output = document.getElementById("topicsOutput");
  output.textContent = "Extracting topics...";

  try {
    currentSyllabus = syllabusText;

    const data = await sendRequest("/extract", {
      text: syllabusText
    });

    const topics = data.topics || [];

    if (topics.length === 0) {
      output.textContent = "No topics extracted.";
      return;
    }

    output.textContent =
      "Extracted topics:\n" +
      topics
        .map(topic => `- ${topic.topic} (weight: ${topic.weight})`)
        .join("\n");
  } catch (error) {
    console.error(error);
    output.textContent =
      "Could not extract topics. Check that the backend is running.";
  }
});

document.getElementById("planBtn").addEventListener("click", async () => {
  if (!currentSyllabus) {
    alert("Please extract topics first.");
    return;
  }

  const examDate = document.getElementById("examDate").value;
  const hoursPerDay = Number(
    document.getElementById("hoursPerDay").value || 3
  );

  if (!examDate) {
    alert("Please select an exam date.");
    return;
  }

  const output = document.getElementById("planOutput");
  output.textContent = "Generating plan...";

  try {
    const data = await sendRequest("/plan", {
      syllabus_text: currentSyllabus,
      exam_date: examDate,
      hours_per_day: hoursPerDay
    });

    currentPlan = data.plan || [];

    document.getElementById("planExplanation").textContent =
      data.explanation || "";

    renderTasks(currentPlan);
    output.textContent =
      "Plan generated. Mark completed tasks, then click Replan.";
  } catch (error) {
    console.error(error);
    output.textContent =
      "Could not generate the plan. Check the backend terminal.";
  }
});

document.getElementById("replanBtn").addEventListener("click", async () => {
  if (!currentSyllabus || currentPlan.length === 0) {
    alert("Generate a plan first.");
    return;
  }

  const examDate = document.getElementById("examDate").value;
  const hoursPerDay = Number(
    document.getElementById("hoursPerDay").value || 3
  );

  const completedTopics = [];
  const missedTopics = [];

  currentPlan.forEach((task, index) => {
    const checkbox = document.getElementById(`task-${index}`);

    if (checkbox && checkbox.checked) {
      completedTopics.push(task.topic);
    } else {
      missedTopics.push(task.topic);
    }
  });

  const output = document.getElementById("replanOutput");
  output.textContent = "Replanning...";

  try {
    const data = await sendRequest("/replan", {
      syllabus_text: currentSyllabus,
      exam_date: examDate,
      hours_per_day: hoursPerDay,
      completed_topics: completedTopics,
      missed_topics: missedTopics
    });

    currentPlan = data.plan || [];

    document.getElementById("replanExplanation").textContent =
      data.explanation || "";

    renderRevisedPlan(currentPlan);
  } catch (error) {
    console.error(error);
    output.textContent =
      "Could not replan. Check the backend terminal.";
  }
});

function renderTasks(plan) {
  const container = document.getElementById("tasksList");
  container.innerHTML = "";

  if (plan.length === 0) {
    container.textContent = "No tasks generated.";
    return;
  }

  plan.forEach((task, index) => {
    const row = document.createElement("div");
    row.className = "task-item";

    row.innerHTML = `
      <input type="checkbox" id="task-${index}" ${task.done ? "checked" : ""}>
      <label for="task-${index}">
        Day ${task.day}: ${task.topic}
      </label>
      <span class="task-meta">
        ${task.estimated_hours}h • Priority: ${task.priority}
      </span>
    `;

    container.appendChild(row);
  });
}

function renderRevisedPlan(plan) {
  const container = document.getElementById("replanOutput");

  if (plan.length === 0) {
    container.textContent = "No revised plan generated.";
    return;
  }

  container.textContent =
    "Revised plan:\n" +
    plan
      .map(
        task =>
          `Day ${task.day}: ${task.topic} ` +
          `(${task.estimated_hours}h, ${task.priority})` +
          `${task.done ? " [done]" : ""}`
      )
      .join("\n");
}