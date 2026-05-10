// --- State Management ---
// Logic: Try to get data from localStorage; if it's empty, start with an empty array.
let tasks = JSON.parse(localStorage.getItem('myTasks')) || [];
const today = new Date().toISOString().split('T')[0];

// --- DOM Elements ---
const taskModal = document.getElementById('taskModal');
const taskForm = document.getElementById('taskForm');
const taskBody = document.getElementById('taskBody');
const modalTitle = document.getElementById('modalTitle');
const editIndexField = document.getElementById('editIndex');

// --- Initialization & Event Listeners ---
document.getElementById('addTaskBtn').onclick = () => openModal();
document.querySelector('.close-btn').onclick = () => closeModal();
document.getElementById('searchBox').oninput = () => renderTasks();
document.getElementById('sortOptions').onchange = () => renderTasks();

taskForm.onsubmit = (e) => {
    e.preventDefault();
    saveTask();
};

// --- Storage Helpers ---

/**
 * Persists the current 'tasks' array into the browser's localStorage.
 * We must use JSON.stringify because localStorage only stores strings.
 */
function syncLocalStorage() {
    localStorage.setItem('myTasks', JSON.stringify(tasks));
}

// --- CRUD Functions ---

function saveTask() {
    const index = parseInt(editIndexField.value);
    const taskData = {
        name: document.getElementById('taskName').value,
        priority: document.getElementById('priority').value,
        status: document.getElementById('status').value,
        deadline: document.getElementById('deadline').value
    };

    if (index === -1) {
        tasks.push(taskData);
    } else {
        tasks[index] = taskData;
    }

    syncLocalStorage(); // NEW: Save to storage after adding/editing
    closeModal();
    renderTasks();
}

function deleteTask(index) {
    if (confirm("Delete this task?")) {
        tasks.splice(index, 1);
        syncLocalStorage(); // NEW: Save to storage after deleting
        renderTasks();
    }
}

/**
 * READ (View Engine)
 */
function renderTasks() {
    const searchTerm = document.getElementById('searchBox').value.toLowerCase();
    const sortBy = document.getElementById('sortOptions').value;

    let displayList = tasks
        .map((task, index) => ({ ...task, originalIndex: index }))
        .filter(task => task.name.toLowerCase().includes(searchTerm));

    displayList = sortTasks(displayList, sortBy);

    taskBody.innerHTML = '';
    displayList.forEach(task => {
        const row = createTaskRow(task);
        taskBody.appendChild(row);
    });
}

// --- UI Helpers (Remains mostly the same) ---

function openModal(index = -1) {
    taskForm.reset();
    editIndexField.value = index;
    
    if (index === -1) {
        modalTitle.innerText = "Add New Task";
    } else {
        modalTitle.innerText = "Edit Task";
        const task = tasks[index];
        document.getElementById('taskName').value = task.name;
        document.getElementById('priority').value = task.priority;
        document.getElementById('status').value = task.status;
        document.getElementById('deadline').value = task.deadline;
    }
    taskModal.style.display = "block";
}

function closeModal() {
    taskModal.style.display = "none";
}

function sortTasks(list, criterion) {
    if (criterion === 'priority') {
        return list.sort((a, b) => b.priority - a.priority);
    } else if (criterion === 'date-asc') {
        return list.sort((a, b) => new Date(a.deadline) - new Date(b.deadline));
    } else if (criterion === 'date-desc') {
        return list.sort((a, b) => new Date(b.deadline) - new Date(a.deadline));
    }
    return list;
}

function createTaskRow(task) {
    const isExpired = task.deadline < today && task.status !== 'Completed';
    const tr = document.createElement('tr');
    if (isExpired) tr.classList.add('task-expired');

    tr.innerHTML = `
        <td>${task.name}</td>
        <td>${getPriorityLabel(task.priority)}</td>
        <td>${task.status}</td>
        <td>${task.deadline} ${isExpired ? '<br><small>(Expired)</small>' : ''}</td>
        <td>
            <button class="btn-edit" onclick="editTask(${task.originalIndex})">Edit</button>
            <button class="btn-delete" onclick="deleteTask(${task.originalIndex})">Delete</button>
        </td>
    `;
    return tr;
}

function getPriorityLabel(val) {
    const labels = { "1": "Low", "2": "Medium", "3": "High" };
    return labels[val] || "Low";
}

window.editTask = (index) => openModal(index);
window.deleteTask = (index) => deleteTask(index);

// Initial Render
renderTasks();
