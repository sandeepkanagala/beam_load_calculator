// Toggle visibility of load-specific input fields
function showFields() {
  const type = document.getElementById("loadType")?.value;
  const sections = ["point_center", "point_anywhere", "udl", "uvl", "moment"];

  sections.forEach(id => {
    const section = document.getElementById(id);
    if (section) {
      section.style.display = (type === id) ? "block" : "none";
    }
  });
}

// Initialize page functionality on load
document.addEventListener("DOMContentLoaded", () => {
  // Load type handler
  showFields();
  const loadType = document.getElementById("loadType");
  if (loadType) {
    loadType.addEventListener("change", showFields);
  }

  // Dark mode toggle handler
  const toggleSwitch = document.getElementById("modeSwitch");
  const body = document.body;

  if (toggleSwitch) {
    const isDark = localStorage.getItem("dark-mode") === "enabled";
    if (isDark) {
      body.classList.add("dark-mode");
      toggleSwitch.checked = true;
    }

    toggleSwitch.addEventListener("change", () => {
      const enabled = toggleSwitch.checked;
      body.classList.toggle("dark-mode", enabled);
      localStorage.setItem("dark-mode", enabled ? "enabled" : "disabled");
    });
  }
});

// GPT-powered Structural Assistant
async function askAssistant() {
  const inputField = document.getElementById("chatInput");
  const responseBox = document.getElementById("chatResponse");

  const input = inputField?.value.trim();
  if (!input) {
    responseBox.innerText = "⚠️ Please enter a question.";
    return;
  }

  responseBox.innerText = "🧠 Thinking...";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });

    const data = await response.json();
    responseBox.innerText = data?.response
      ? `💡 ${data.response}`
      : "❌ No response from assistant.";
  } catch (error) {
    console.error("Assistant error:", error);
    responseBox.innerText = "❌ Assistant error. Please try again.";
  }
}
