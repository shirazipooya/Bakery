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
                        <td>${bakery.city}</td>
                        <td>${bakery.region}</td>
                        <td>${bakery.district}</td>
                        <td>${bakery.lat}</td>
                        <td>${bakery.lon}</td>
                        <td>${bakery.household_risk}</td>
                        <td>${bakery.bakers_risk}</td>
                        <td>${bakery.type_flour}</td>
                        <td>${bakery.type_bread}</td>
                        <td>${bakery.bread_rations}</td>
                    </tr>
                `);
            });

            $("#page-info").text(`صفحه ${page} از ${totalCountPage}`);
        }
    );
};

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
        $('#editTypeFlour').val(bakery.type_flour).change();
        $('#editTypeBread').val(bakery.type_bread).change();
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
        type_flour: $('#editTypeFlour').val(),
        type_bread: $('#editTypeBread').val(),
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
