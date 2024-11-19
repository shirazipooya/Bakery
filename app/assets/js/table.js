// =============================================================================
// Utils
// =============================================================================
let currentPage = 1;
let currentSortBy = "id";
let currentSortOrder = "asc";
let totalCountPage = 1;



// =============================================================================
// API
// =============================================================================
async function get_table_headers() {
    try {
        const response = await fetch("/api/table/headers");
        if (!response.ok) {
            throw new Error("Failed to fetch headers");
        }
        const headers = await response.json();
        const thead = $("table thead tr");
        thead.empty();
        thead.append("<th></th>");
        headers.forEach(header => {
            const excludedFields = ["city", "created_at", "updated_at"];
            if (excludedFields.includes(header.field)) return;
            thead.append(`<th class="clickable-header" onclick="sortTable('${header.field}')">${header.label}</th>`);
        });
    } catch (error) {
        console.error("Error fetching table headers:", error);        
    }
}


async function get_table_data() {
    try {
        const search = $("#search").val();
        const selected_column_search = $("#table_column").val();     

        // Fetch table data
        const dataResponse = await fetch(`/api/table/data?column=${selected_column_search}&search=${search}&sort_by=${currentSortBy}&sort_order=${currentSortOrder}&page=${currentPage}`);
        if (!dataResponse.ok) {
            throw new Error("Failed to fetch table data");
        }
        const { data, total_count, per_page, page } = await dataResponse.json();
        totalCountPage = Math.ceil(total_count / per_page);
        const tableBody = $("#bakeries-table-body");
        document.getElementById("total").innerHTML = total_count;
        tableBody.empty();
        // Fetch headers dynamically to ensure alignment
        const headersResponse = await fetch("/api/table/headers");
        if (!headersResponse.ok) {
            throw new Error("Failed to fetch headers");
        }
        const headers = await headersResponse.json();

        // Clear existing rows and generate dynamically
        data.forEach((bakery) => {
            const row = $("<tr></tr>");

            // Add action column
            row.append(`
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
            `);

            // Add columns dynamically based on header fields
            headers.forEach(header => {
                const excludedFields = ["city", "created_at", "updated_at"];
                if (excludedFields.includes(header.field)) return;
                const value = bakery[header.field] || "-"; // Use the field key
                row.append(`<td>${value}</td>`);
            });

            tableBody.append(row);
        });

        // Update page info
        $("#page-info").text(`صفحه ${page} از ${totalCountPage}`);
        
    } catch (error) {
        console.error("Error fetching table data:", error);        
    }
}

function sortTable(column) {
    currentSortBy = column;
    currentSortOrder = currentSortOrder === "asc" ? "desc" : "asc";
    currentPage = 1;
    get_table_data();
};

// nahyeh
$(document).ready(function () {
    $("#table_column").on("change", function () {
        get_table_data();
    });
});


// -----------------------------------------------------------------------------
// Delete Record
// -----------------------------------------------------------------------------
function showDeleteModal(id) {
    deleteID = id;
    $("#deleteModal").modal("show");
};


$("#confirmDelete").on("click", function () {
    if (deleteID) {
        $.ajax({
            url: `/api/table/delete/${deleteID}`,
            type: "DELETE",
            success: function () {
                $("#deleteModal").modal("hide");
                get_table_data();
            },
        });
    }
});

// -----------------------------------------------------------------------------
// Update Record
// -----------------------------------------------------------------------------

function showEditModal(id) {
    const search = $("#search").val();
    $.get(`/api/table/data`, { search: search, page: currentPage }, function(response) {
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
        household_risk: $('#editHouseholdRisk').val(),
        bakers_risk: $('#editBakersRisk').val(),
        flour_types: $('#editTypeFlour').val(),
        bread_types: $('#editTypeBread').val(),
        bread_rations: $('#editBreadRations').val(),
    };
    $.ajax({
        url: `/api/table/update/${id}`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(updatedData),
        success: function() {
            $('#editModal').modal('hide');
            get_table_data();
        }
    });
});



$(document).ready(function () {
    get_table_headers();
    get_table_data();

    $("#search").on("input", function () {
        currentPage = 1;
        get_table_data();
    });
    
    $("#prev-page").on("click", function () {
        if (currentPage > 1) {
            currentPage--;
            get_table_data();
        }
    });
    
    $("#next-page").on("click", function () {
        if (currentPage < totalCountPage) {
            currentPage++;
            get_table_data();
        }
    });
});