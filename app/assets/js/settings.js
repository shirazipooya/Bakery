async function addCategory() {
    const column = document.getElementById('columnSelect').value;
    const newCategory = document.getElementById('newCategory').value;

    if (!column || !newCategory) return;
    
    const response = await fetch('/api/settings/add_category', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ column: column, new_category: newCategory })
    });

    const result = await response.json();

    if (response.ok) {
        document.getElementById('newCategory').value = '';
        showAlert(result.message, result.type);
        fetchCategories();
    } else {
        showAlert(result.message, result.type);
    }
}


document.getElementById('columnSelect').addEventListener('change', fetchCategories);

async function fetchCategories() {
    const column = document.getElementById('columnSelect').value;
    if (!column) return;

    const response = await fetch('/api/settings/all_items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ column: column })
    });

    const items = await response.json();
    const itemsList = document.getElementById('itemsList');
    itemsList.innerHTML = '';
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        li.className = "list-group-item list-group-timeline-primary"
        itemsList.appendChild(li);
    });
}



function showAlert(message, type) {
    const alertBox = document.getElementById('alertBox');
    alertBox.textContent = message;
    alertBox.style.display = 'flex';
    alertBox.className = `alert alert-${type} mt-3 `;
    setTimeout(closeAlert, 5000);
}

function closeAlert() {
    const alertBox = document.getElementById('alertBox');
    alertBox.style.display = 'none';
}