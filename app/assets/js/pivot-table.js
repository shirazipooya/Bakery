$(document).ready(function() {
    // Fetch data from the API
    $.get('/api/pivot_table', function(data) {
        // Create the pivot table
        $("#pivot-table").pivotUI(data, {
            rows: ["TypeBread"], // Default rows, can be customized
            cols: ["Region"],    // Default columns, can be customized
            vals: ["BreadRations"], // Default values, can be customized
            aggregatorName: "Sum", // Default aggregator
            renderers: {
                "Table": $($.pivotUtilities.renderers).get("Table")
            },
            onRefresh: function(config) {
                // This function will be called on each refresh (dragging/dropping)
                console.log("Pivot table configuration:", config);
            }
        });
    });
});
