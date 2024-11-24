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
        li.className = "list-group-item list-group-timeline-primary d-flex align-items-center"
        
        const deleteButton = document.createElement('button');
        deleteButton.className = "btn px-0 pe-1";
        deleteButton.innerHTML = '<i class="bx bx-x bx-xs text-danger"></i>';
        // deleteButton.id = "confirm-text"
        deleteButton.addEventListener('click', () => showDeleteItemModal(column, item));
        li.appendChild(deleteButton);
        
        const textNode = document.createTextNode(item);
        li.appendChild(textNode);
        
        itemsList.appendChild(li);
    });
}

// -----------------------------------------------------------------------------
// Delete Record
// -----------------------------------------------------------------------------
function showDeleteItemModal(column, item) {
    columnValue = column;
    itemValue = item;
    $("#deleteItemModal").modal("show");
};


$("#confirmDeleteItem").on("click", function () {
    console.log("Deleted!");
    
    if (columnValue && itemValue) {
        $.ajax({
            url: `/api/settings/delete/${columnValue}/${itemValue}`,
            type: "DELETE",
            success: function (result) {
                $("#deleteItemModal").modal("hide");
                fetchCategories();
                showAlert(result.message, result.type);
            },
            error: function (result) {
                $("#deleteItemModal").modal("hide");
                showAlert(result.message, result.type);
            },
        });
    }
});




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