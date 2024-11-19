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
                window.location.href = "/table";
            },
        });
    }
});


// document.getElementById('fileInput').addEventListener('change', function() {
//     const fileName = this.files[0] ? this.files[0].name : 'هیچ فایلی انتخاب نشده';
//     document.getElementById('fileName').value = fileName;
// });

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('fileInput').addEventListener('change', function() {
        const fileName = this.files[0] ? this.files[0].name : 'هیچ فایلی انتخاب نشده';
        document.getElementById('fileName').value = fileName;
    });
});


const socket = io();

socket.on('validation_message', function(message) {
    const textarea = document.getElementById('element-Status');
    textarea.value += message + "\n";
    textarea.scrollTop = textarea.scrollHeight;  // Auto-scroll to the bottom
});