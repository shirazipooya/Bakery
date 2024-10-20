// Maps Leaflet


'use strict';


(function () {


    // Get All Data From `/get_all_data`

    get_all_data();

    async function get_all_data() {
        const response = await fetch('/get_all_data');
        const data = await response.json();
        await addMarkers(data.data);    
    };


    // Create Map

    const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    });

    const imagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19,
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    });

    const terrain = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenTopoMap contributors'
    });

    const map = L.map('map', {
        center: [32.7, 52.4],
        zoom: 5,
        layers: [osm]
    });

    const baseLayers = {
        "OpenStreetMap": osm,
        "Terrain": terrain,
        "Imagery": imagery
    };

    L.control.layers(baseLayers).addTo(map);




    // Region
    let geojsonLayerRegion = null;

    function addGeoJSONLayerRegion(geojsonData) {
        geojsonLayerRegion = L.geoJSON(geojsonData, {
            style: function (feature) {
                return {
                    color: "#3388ff",  // Outline color
                    weight: 2,
                    opacity: 1,
                    fillColor: "#3388ff",
                    fillOpacity: 0.2
                };
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(
                    `${feature.properties.Region}`
                );
                layer.on('click', function() {
                    fetch(`/region/${feature.properties.Region}`)
                        .then(response => response.json())
                        .then(data => {
                            console.log(data.n);
                            
                        })
                });
            }
        }).addTo(map);
    }

    fetch('/assets/data/geodatabase/Region.geojson')
        .then(response => response.json())
        .then(geojsonData => {           
            addGeoJSONLayerRegion(geojsonData);
        })
        .catch(error => {
            console.error("Error loading the GeoJSON file:", error);
        })
    
    document.getElementById('showRegion').addEventListener('change', function() {
        if (this.checked) {           
            if (geojsonLayerRegion) {
                geojsonLayerRegion.addTo(map);
            }
        } else {
            if (geojsonLayerRegion) {
                map.removeLayer(geojsonLayerRegion);
            }
        }
    })



    // // District
    // let geojsonLayerDistrict = null;

    // function addGeoJSONLayerDistrict(geojsonData) {       
    //     geojsonLayerDistrict = L.geoJSON(geojsonData, {
    //         style: function () {
    //             return {
    //                 color: "#3388ff", 
    //                 weight: 2,
    //                 opacity: 1,
    //                 fillColor: "#3388ff",
    //                 fillOpacity: 0.2
    //             };
    //         },
    //     }).addTo(map);
    //     geojsonLayerDistrict = L.geoJSON(geojsonData).addTo(map);
    // }

    // fetch('/assets/data/geodatabase/District.geojson')
    //     .then(response => response.json())
    //     .then(geojsonData => {                      
    //         addGeoJSONLayerDistrict(geojsonData);
    //     })
    //     .catch(error => {
    //         console.error("Error loading the GeoJSON file:", error);
    //     })
    
    // document.getElementById('showDistrict').addEventListener('change', function() {
    //     if (this.checked) {                    
    //         if (geojsonLayerDistrict) {
    //             geojsonLayerDistrict.addTo(map);
    //         }
    //     } else {
    //         if (geojsonLayerDistrict) {
    //             map.removeLayer(geojsonLayerDistrict);
    //         }
    //     }
    // })


    const markerClusters = L.markerClusterGroup();

    map.addLayer(markerClusters);


    // Function to Add Markers to the Map

    async function addMarkers(data) {
        markerClusters.clearLayers();
        const bounds = L.latLngBounds();
        data.forEach(row => {
            const marker = L.marker([row.Lat, row.Lon]);
            marker.bindPopup(
                `
                    <h4 class="pb-2" style="text-align: center !important;">${row.FirstName} ${row.LastName}</h4>
                    <div class="table-responsive medium">
                        <table class="table table-striped table-sm">
                            <tbody>
                                 <tr>
                                    <th>کد ملی</th>
                                    <td>${row.NID}</td>
                                </tr>
                                <tr>
                                    <th>نوع آرد</th>
                                    <td>${row.TypeFlour}</td>
                                </tr>
                                <tr>
                                    <th>نوع پخت</th>
                                    <td>${row.TypeBread}</td>
                                </tr>
                                <tr>
                                    <th>سهمیه (تعداد کیسه)</th>
                                    <td>${row.BreadRations}</td>
                                </tr>
                                <tr>
                                    <th>ریسک خانوار</th>
                                    <td>${row.HouseholdRisk}</td>
                                </tr>
                                <tr>
                                    <th>ریسک نانوا</th>
                                    <td>${row.BakersRisk}</td>
                                </tr>
                                 <tr>
                                    <th>شهر</th>
                                    <td>${row.City}</td>
                                </tr>
                                 <tr>
                                    <th>منطقه</th>
                                    <td>${row.Region}</td>
                                </tr>
                                 <tr>
                                    <th>ناحیه</th>
                                    <td>${row.District}</td>
                                </tr>
                                <tr>
                                    <th>طول جغرافیایی</th>
                                    <td>${Number((row.Lon).toFixed(2))}</td>
                                </tr>
                                <tr>
                                    <th>عرض جغرافیایی</th>
                                    <td>${Number((row.Lat).toFixed(2))}</td>
                                </tr>
                            </tbody>
                `
            );
            markerClusters.addLayer(marker);
            bounds.extend([row.Lat, row.Lon]);        
        });
        if (data.length > 0) {
            map.fitBounds(bounds);        
        }
    }

    document.getElementById('apply_filter').addEventListener('click', function () {
        let citySelect = document.getElementById('city').value;
        let regionSelect = document.getElementById('region').value;
        let districtSelect = document.getElementById('district').value;
        let typeBreadSelect = document.getElementById('typeBread').value;

        if (!citySelect) {
            citySelect = "999";
        }
        if (!regionSelect) {
            regionSelect = "999";
        }
        if (!districtSelect) {
            districtSelect = "999";
        }
        if (!typeBreadSelect) {
            typeBreadSelect = "999";
        }

        fetch(`/api/filtered/${citySelect}/${regionSelect}/${districtSelect}/${typeBreadSelect}`)
        .then(response => response.json())
        .then(data => {
            addMarkers(data.data);
        });
    });

    document.getElementById('clear_filter').addEventListener('click', function () {
        document.getElementById('region').innerHTML = '<option value="">منطقه را انتخاب کنید ...</option>';
        document.getElementById('district').innerHTML = '<option value="">ناحیه را انتخاب کنید ...</option>';
        get_all_data();
    });

})();
