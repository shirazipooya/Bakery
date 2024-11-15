// Table and Search and Sort Start
let currentPage = 1;
let currentSortBy = "id";
let currentSortOrder = "asc";
let totalCountPage = 1;

function loadBakeriesTable() {
    const search = $("#search").val();
    $.get(
        "/api/database/table",
        {
            search: search,
            sort_by: currentSortBy,
            sort_order: currentSortOrder,
            page: currentPage,
        },
        function (response) {
            const { data, total_count, per_page, page } = response;           
            totalCountPage = Math.ceil(total_count / per_page);
            const tableBody = $("#bakeries-table-body");
            document.getElementById("total").innerHTML = total_count;
            tableBody.empty();

            data.forEach((bakery) => {
                tableBody.append(`
                    <tr>
                        <td>
                        <div class="dropdown">
                            <button type="button" class="btn p-0 dropdown-toggle hide-arrow" data-bs-toggle="dropdown">
                                <i class="bx bx-dots-vertical-rounded"></i>
                            </button>
                            <div class="dropdown-menu">
                                <button class="dropdown-item" onclick="showEditModal(${bakery.id})">
                                    <i class="bx bx-edit-alt me-1"></i>ویرایش
                                </button>
                                <button class="dropdown-item" onclick="showDeleteModal(${bakery.id})">
                                    <i class="bx bx-trash me-1"></i>حذف
                                </button>
                            </div>
                        </div>
                        </td>
                        <td>${bakery.id}</td>
                        <td>${bakery.first_name}</td>
                        <td>${bakery.last_name}</td>
                        <td>${bakery.nid}</td>
                        <td>${bakery.phone}</td>
                        <td>${bakery.bakery_id}</td>
                        <td>${bakery.ownership_status}</td>
                        <td>${bakery.number_violations}</td>
                        <td>${bakery.second_fuel}</td>
                        <td>${bakery.household_risk}</td>
                        <td>${bakery.bakers_risk}</td>
                        <td>${bakery.flour_types}</td>
                        <td>${bakery.bread_types}</td>
                        <td>${bakery.bread_rations}</td>
                        <td>${bakery.ostan}</td>
                        <td>${bakery.shahrestan}</td>
                        <td>${bakery.bakhsh}</td>
                        <td>${bakery.shahr}</td>
                        <td>${bakery.region}</td>
                        <td>${bakery.district}</td>
                        <td>${bakery.lat.toFixed(2)}</td>
                        <td>${bakery.lon.toFixed(2)}</td>
                    </tr>
                `);
            });

            $("#page-info").text(`صفحه ${page} از ${totalCountPage}`);
        }
    );
};

function showDeleteTableModal() {
    $("#deleteTableModal").modal("show");
};



$("#confirmTableDelete").on("click", function () {
    if (true) {
        $.ajax({
            url: `/api/database/delete/`,
            type: "DELETE",
            success: function () {
                $("#deleteTableModal").modal("hide");
                loadBakeriesTable();
            },
        });
    }
});


function showDeleteModal(id) {
    deleteID = id;
    $("#deleteModal").modal("show");
};



$("#confirmDelete").on("click", function () {
    if (deleteID) {
        $.ajax({
            url: `/api/database/delete/${deleteID}`,
            type: "DELETE",
            success: function () {
                $("#deleteModal").modal("hide");
                loadBakeriesTable();
            },
        });
    }
});

function showEditModal(id) {
    const search = $("#search").val();
    $.get(`/api/database/table`, { search: search, page: currentPage }, function(response) {
        const bakery = response.data.find(b => b.id === id);
        $('#editID').val(bakery.id);
        $('#editFirstName').val(bakery.first_name);
        $('#editLastName').val(bakery.last_name);
        $('#editNID').val(bakery.nid);
        $('#editPhone').val(bakery.phone);
        $('#editBakeryID').val(bakery.bakery_id);
        $('#editOwnershipStatus').val(bakery.ownership_status).change();
        $('#editNumberViolations').val(bakery.number_violations);
        $('#editSecondFuel').val(bakery.second_fuel).change();
        $('#editCity').val(bakery.city).change();
        $('#editRegion').val(bakery.region).change();
        $('#editDistrict').val(bakery.district).change();
        $('#editLat').val(bakery.lat);
        $('#editLon').val(bakery.lon);
        $('#editHouseholdRisk').val(bakery.household_risk).change();
        $('#editBakersRisk').val(bakery.bakers_risk).change();
        $('#editTypeFlour').val(bakery.flour_types).change();
        $('#editTypeBread').val(bakery.bread_types).change();
        $('#editBreadRations').val(bakery.bread_rations);
        $('#editModal').modal('show');
    });
};

$('#editForm').on('submit', function(event) {
    event.preventDefault();
    const id = $('#editID').val();
    const updatedData = {
        first_name: $('#editFirstName').val(),
        last_name: $('#editLastName').val(),
        nid: $('#editNID').val(),
        phone: $('#editPhone').val(),
        bakery_id: $('#editBakeryID').val(),
        ownership_status: $('#editOwnershipStatus').val(),
        number_violations: $('#editNumberViolations').val(),
        second_fuel: $('#editSecondFuel').val(),
        city: $('#editCity').val(),
        region: $('#editRegion').val(),
        district: $('#editDistrict').val(),
        lat: $('#editLat').val(),
        lon: $('#editLon').val(),
        household_risk: $('#editHouseholdRisk').val(),
        bakers_risk: $('#editBakersRisk').val(),
        flour_types: $('#editTypeFlour').val(),
        bread_types: $('#editTypeBread').val(),
        bread_rations: $('#editBreadRations').val(),
    };

    $.ajax({
        url: `/api/database/update/${id}`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(updatedData),
        success: function() {
            $('#editModal').modal('hide');
            loadBakeriesTable();
        }
    });
});

function sortTable(column) {
    currentSortBy = column;
    currentSortOrder = currentSortOrder === "asc" ? "desc" : "asc";
    loadBakeriesTable();
};

$(document).ready(function () {
    loadBakeriesTable();

    $("#search").on("input", function () {
        currentPage = 1;
        loadBakeriesTable();
    });
    
    $("#prev-page").on("click", function () {
        if (currentPage > 1) {
            currentPage--;
            loadBakeriesTable();
        }
    });
    
    $("#next-page").on("click", function () {
        if (currentPage < totalCountPage) {
            currentPage++;
            loadBakeriesTable();
        }
    });


});
// Table and Search and Sort End


document.getElementById('fileInput').addEventListener('change', function() {
    const fileName = this.files[0] ? this.files[0].name : 'هیچ فایلی انتخاب نشده';
    document.getElementById('fileName').value = fileName;
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

async function addCategory() {
    const column = document.getElementById('columnSelect').value;
    const newCategory = document.getElementById('newCategory').value;

    if (!column || !newCategory) return;
    
    const response = await fetch('/api/database/add_category', {
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

    const response = await fetch('/api/database/all_items', {
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

const socket = io();

socket.on('validation_message', function(message) {
    const textarea = document.getElementById('element-Status');
    textarea.value += message + "\n";
    textarea.scrollTop = textarea.scrollHeight;  // Auto-scroll to the bottom
});