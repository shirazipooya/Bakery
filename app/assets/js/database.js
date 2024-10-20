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
    $.get(`/api/bakeries`, { search: search, page: currentPage }, function(response) {
        const bakery = response.data.find(b => b.ID === id);
        $('#editID').val(bakery.ID);
        $('#editFirstName').val(bakery.FirstName);
        $('#editLastName').val(bakery.LastName);
        $('#editNID').val(bakery.NID);
        $('#editCity').val(bakery.City).change();
        $('#editRegion').val(bakery.Region).change();
        $('#editDistrict').val(bakery.District).change();
        $('#editLat').val(bakery.Lat);
        $('#editLon').val(bakery.Lon);
        $('#editHouseholdRisk').val(bakery.HouseholdRisk).change();
        $('#editBakersRisk').val(bakery.BakersRisk).change();
        $('#editTypeFlour').val(bakery.TypeFlour).change();
        $('#editTypeBread').val(bakery.TypeBread).change();
        $('#editBreadRations').val(bakery.BreadRations).change();
        $('#editModal').modal('show');
    });
};

$('#editForm').on('submit', function(event) {
    event.preventDefault();
    const id = $('#editID').val();
    const updatedData = {
        FirstName: $('#editFirstName').val(),
        LastName: $('#editLastName').val(),
        NID: $('#editNID').val(),
        City: $('#editCity').val(),
        Region: $('#editRegion').val(),
        District: $('#editDistrict').val(),
        Lat: $('#editLat').val(),
        Lon: $('#editLon').val(),
        HouseholdRisk: $('#editHouseholdRisk').val(),
        BakersRisk: $('#editBakersRisk').val(),
        TypeFlour: $('#editTypeFlour').val(),
        TypeBread: $('#editTypeBread').val(),
        BreadRations: $('#editBreadRations').val(),
    };

    $.ajax({
        url: `/api/bakeries/${id}`,
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
