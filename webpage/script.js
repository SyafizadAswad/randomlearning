// --- State Management ---
let tasks = [];
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

// --- CRUD Functions ---

/**
 * CREATE & UPDATE
 * Handles extracting data from the form and either pushing a new task 
 * or updating an existing one based on the hidden index field.
 */
function saveTask() {
    const index = parseInt(editIndexField.value);
    const taskData = {
        name: document.getElementById('taskName').value,
        priority: document.getElementById('priority').value,
        status: document.getElementById('status').value,
        deadline: document.getElementById('deadline').value
    };

    if (index === -1) {
        // Create
        tasks.push(taskData);
    } else {
        // Update
        tasks[index] = taskData;
    }

    closeModal();
    renderTasks();
}

/**
 * READ
 * The "View Engine". Filters, sorts, and transforms the array into HTML.
 */
function renderTasks() {
    const searchTerm = document.getElementById('searchBox').value.toLowerCase();
    const sortBy = document.getElementById('sortOptions').value;

    // Map to keep track of original indices, then filter by search
    let displayList = tasks
        .map((task, index) => ({ ...task, originalIndex: index }))
        .filter(task => task.name.toLowerCase().includes(searchTerm));

    // Apply Sorting
    displayList = sortTasks(displayList, sortBy);

    // Clear and Build Table
    taskBody.innerHTML = '';
    displayList.forEach(task => {
        const row = createTaskRow(task);
        taskBody.appendChild(row);
    });
}

/**
 * DELETE
 * Removes an item from the main array.
 */
function deleteTask(index) {
    if (confirm("Delete this task?")) {
        tasks.splice(index, 1);
        renderTasks();
    }
}

// --- Helper Functions (Cleaning up the logic) ---

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

// Global exposure for inline HTML onclicks
window.editTask = (index) => openModal(index);
window.deleteTask = (index) => deleteTask(index);

// Initial Render
renderTasks();