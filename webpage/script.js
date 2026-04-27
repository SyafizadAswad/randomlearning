let tasks = [];
const taskModal = document.getElementById('taskModal');
const taskForm = document.getElementById('taskForm');
const taskBody = document.getElementById('taskBody');
const modalTitle = document.getElementById('modalTitle');

// Open modal for Create
document.getElementById('addTaskBtn').onclick = () => {
    taskForm.reset();
    document.getElementById('editIndex').value = "-1";
    modalTitle.innerText = "Add New Task";
    taskModal.style.display = "block";
};

// Close modal
document.querySelector('.close-btn').onclick = () => taskModal.style.display = "none";

// Handle Form Submission (Create and Update)
taskForm.onsubmit = (e) => {
    e.preventDefault();
    const index = document.getElementById('editIndex').value;
    const taskData = {
        name: document.getElementById('taskName').value,
        priority: document.getElementById('priority').value,
        status: document.getElementById('status').value,
        deadline: document.getElementById('deadline').value
    };

    if (index === "-1") {
        tasks.push(taskData);
    } else {
        tasks[index] = taskData;
    }

    taskModal.style.display = "none";
    renderTasks();
};

// Render Table
function renderTasks() {
    const searchTerm = document.getElementById('searchBox').value.toLowerCase();
    const sortBy = document.getElementById('sortOptions').value;
    
    // Get today's date in YYYY-MM-DD format for comparison
    const today = new Date().toISOString().split('T')[0];

    let filteredTasks = tasks.map((task, index) => ({ ...task, originalIndex: index }))
        .filter(task => task.name.toLowerCase().includes(searchTerm));

    // Sort Logic (remains the same)
    if (sortBy === 'priority') {
        filteredTasks.sort((a, b) => b.priority - a.priority);
    } else if (sortBy === 'date-asc') {
        filteredTasks.sort((a, b) => new Date(a.deadline) - new Date(b.deadline));
    } else if (sortBy === 'date-desc') {
        filteredTasks.sort((a, b) => new Date(b.deadline) - new Date(a.deadline));
    }

    taskBody.innerHTML = '';

    filteredTasks.forEach((task) => {
        // Logic: Is the deadline before today AND is it not already completed?
        const isExpired = task.deadline < today && task.status !== 'Completed';
        
        const row = document.createElement('tr');
        
        // Apply the grayed-out class if expired
        if (isExpired) {
            row.classList.add('task-expired');
        }

        row.innerHTML = `
            <td>${task.name}</td>
            <td>${getPriorityLabel(task.priority)}</td>
            <td>${task.status}</td>
            <td>
                ${task.deadline} 
                ${isExpired ? '<br><span class="status-expired">(Expired)</span>' : ''}
            </td>
            <td>
                <button class="btn-edit" onclick="editTask(${task.originalIndex})">Edit</button>
                <button class="btn-delete" onclick="deleteTask(${task.originalIndex})">Delete</button>
            </td>
        `;
        taskBody.appendChild(row);
    });
}

function getPriorityLabel(val) {
    return val == "3" ? "High" : val == "2" ? "Medium" : "Low";
}

// Edit Action
window.editTask = (index) => {
    const task = tasks[index];
    document.getElementById('taskName').value = task.name;
    document.getElementById('priority').value = task.priority;
    document.getElementById('status').value = task.status;
    document.getElementById('deadline').value = task.deadline;
    document.getElementById('editIndex').value = index;
    modalTitle.innerText = "Edit Task";
    taskModal.style.display = "block";
};

// Delete Action
window.deleteTask = (index) => {
    if (confirm("Are you sure you want to delete this task?")) {
        tasks.splice(index, 1);
        renderTasks();
    }
};

// Listeners for Search and Sort
document.getElementById('searchBox').oninput = renderTasks;
document.getElementById('sortOptions').onchange = renderTasks;

// Initial render
renderTasks();