const modal = document.getElementById('taskModal');
const openModalBtn = document.getElementById('openModalBtn');
const closeModalBtn = document.getElementById('closeModalBtn');
const taskForm = document.getElementById('taskForm');
const taskList = document.getElementById('taskList');

// Modal Logic
openModalBtn.onclick = () => modal.style.display = 'flex';
closeModalBtn.onclick = () => modal.style.display = 'none';

// Close modal if clicking outside the box
window.onclick = (event) => {
    if (event.target == modal) modal.style.display = 'none';
}

// Add Task Logic
taskForm.addEventListener('submit', function(e) {
    e.preventDefault();

    // Get values from form
    const name = document.getElementById('taskName').value;
    const status = document.getElementById('taskStatus').value;
    const priority = document.getElementById('taskPriority').value;
    const deadline = document.getElementById('taskDeadline').value;
    const memo = document.getElementById('taskMemo').value;

    // Create the row element
    const row = document.createElement('div');
    row.className = 'table-row';

    row.innerHTML = `
        <div class="col-check"><input type="checkbox"></div>
        <div class="col-name"><strong>${name}</strong></div>
        <div class="col-status">
            <select class="row-select">
                <option ${status === 'To Do' ? 'selected' : ''}>To Do</option>
                <option ${status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                <option ${status === 'Review' ? 'selected' : ''}>Review</option>
                <option ${status === 'Done' ? 'selected' : ''}>Done</option>
            </select>
        </div>
        <div class="col-priority">
            <select class="row-select">
                <option ${priority === 'Low' ? 'selected' : ''}>Low</option>
                <option ${priority === 'Medium' ? 'selected' : ''}>Medium</option>
                <option ${priority === 'High' ? 'selected' : ''}>High</option>
                <option ${priority === 'Urgent' ? 'selected' : ''}>Urgent</option>
            </select>
        </div>
        <div class="col-date">${deadline}</div>
        <div class="col-memo" title="${memo}">${memo}</div>
        <div class="col-actions">
            <select class="row-options" onchange="handleAction(this)">
                <option value="" disabled selected>•••</option>
                <option value="edit">Edit</option>
                <option value="delete">Delete</option>
                <option value="view">View</option>
                <option value="complete">Mark as Complete</option>
            </select>
        </div>
    `;

    // Append to list
    taskList.appendChild(row);

    // Reset and close
    taskForm.reset();
    modal.style.display = 'none';
});

// Simple action handler for the "..." menu
function handleAction(selectElement) {
    const action = selectElement.value;
    const row = selectElement.closest('.table-row');
    
    if (action === 'delete') {
        row.remove();
    } else if (action === 'complete') {
        row.style.opacity = '0.5';
        row.style.textDecoration = 'line-through';
    } else {
        alert("Action: " + action);
    }
    selectElement.value = ""; // Reset dropdown
}