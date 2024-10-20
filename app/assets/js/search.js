document.addEventListener('DOMContentLoaded', function () {

    // function searchDatabase(query = '') {
    //     fetch(`/database?query=${query}`)
    //         .then(response => response.json())
    //         .then(data => {
    //             addMarkers(data.data);
    //             document.getElementById('totalCitiesSelected').textContent = data.count;
    //         })
    //         .catch(error => console.log(error));
    // }

    // // Load all cities initially
    // fetchCities();

    // Handle search form submission
    document.getElementById('search-form').onsubmit = function(event) {
        event.preventDefault();
        const query = event.target.query.value;
        searchDatabase(query);
    };

});