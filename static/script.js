function fetchTasks() {
  fetch("/tasks")
    .then((response) => response.json())
    .then((data) => {
      const taskList = document.getElementById("task-list");
      taskList.innerHTML = "";
      data.forEach((task) => {
        const li = document.createElement("li");
        li.textContent = task.title + " - " + task.status;
        const completeButton = document.createElement("button");
        completeButton.textContent = "Marcar como completa";
        completeButton.onclick = () => updateTaskStatus(task.id, "complete");
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Excluir";
        deleteButton.onclick = () => deleteTask(task.id);
        li.append(completeButton, deleteButton);
        taskList.appendChild(li);
      });
    });
}
document
  .getElementById("task-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const title = document.getElementById("task-title").value;

    fetch("/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title }),
    })
      .then((response) => response.json())
      .then((data) => {
        fetchTasks();
      });
  });

function updateTaskStatus(taskId, status) {
  fetch(`/tasks/${taskId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ status }),
  })
    .then((response) => response.json())
    .then((data) => {
      fetchTasks();
    });
}

function deleteTask(taskId) {
  fetch(`/tasks/${taskId}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      fetchTasks();
    });
}

window.onload = fetchTasks;
