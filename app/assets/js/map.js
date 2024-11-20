'use strict';


(function () {


    // =========================================================================
    // 0. Create Map
    // =========================================================================
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

    L.control.scale({
        metric: true,
        imperial: false,
        position: 'bottomleft'
    }).addTo(map)

    L.Control.Watermark = L.Control.extend({
        onAdd:function(map){
            var img = L.DomUtil.create('img');
            img.src = "assets/img/HydroCode.png";
            img.style.width = "65px";
            return img
        },
        onRemove: function(map){},
    })

    L.control.watermark = function(opts){
        return new L.Control.Watermark(opts);
    }

    L.control.watermark({position:'bottomleft'}).addTo(map);



    L.easyPrint({
        title: 'پرینت',
        sizeModes: ['Current'],
        filename: 'Map',
        exportOnly: true,
        hideControlContainer: true,
        position: 'topright',
        defaultSizeTitles: {Current: 'سایز نقشه',},
    }).addTo(map);

    const markerClusters = L.markerClusterGroup();

    map.addLayer(markerClusters);

    async function addMarkers(data) {
        markerClusters.clearLayers();
        const bounds = L.latLngBounds();
        data.forEach(row => {
            const marker = L.marker([row.lat, row.lon]);
            marker.bindPopup(
                `
                    <h4 class="pb-2" style="text-align: center !important;">${row.first_name} ${row.last_name}</h4>
                    <div class="table-responsive medium">
                        <table class="table table-striped table-sm">
                            <tbody>
                                <tr>
                                    <th>شماره خبازی</th>
                                    <td>${row.bakery_id}</td>
                                </tr>
                                <tr>
                                    <th>نوع پخت</th>
                                    <td>${row.bread_types}</td>
                                </tr>
                                <tr>
                                    <th>نوع آرد</th>
                                    <td>${row.flour_types}</td>
                                </tr>
                                <tr>
                                    <th>سهمیه</th>
                                    <td>${row.bread_rations} کیسه</td>
                                </tr>
                                 <tr>
                                    <th>نوع ملک نانوایی</th>
                                    <td>${row.ownership_status}</td>
                                </tr>
                                 <tr>
                                    <th>سوخت دوم</th>
                                    <td>${row.second_fuel}</td>
                                </tr>
                                 <tr>
                                    <th>تعداد تخلفات نانوایی</th>
                                    <td>${row.number_violations}</td>
                                </tr>
                                <tr>
                                    <th>ریسک خانوار</th>
                                    <td>${row.household_risk}</td>
                                </tr>
                                <tr>
                                    <th>ریسک نانوا</th>
                                    <td>${row.bakers_risk}</td>
                                </tr>
                                 <tr>
                                    <th>موقعیت</th>
                                    <td>
                                        ${row.shahr === 'روستایی' 
                                            ? `استان ${row.ostan}, شهرستان ${row.shahrestan}, بخش ${row.bakhsh}, روستایی`
                                            : `استان ${row.ostan}, شهرستان ${row.shahrestan}, بخش ${row.bakhsh}, شهر ${row.shahr}, منطقه ${row.region}, ناحیه ${row.district}`
                                        }
                                    </td>
                                </tr>
                                <tr>
                                    <th>مختصات</th>
                                    <td>${Number(row.lon.toFixed(2)).toString().replace('.', '/')} شمالی - ${Number(row.lat.toFixed(2)).toString().replace('.', '/')} شرقی</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                `
            );
            markerClusters.addLayer(marker);
            bounds.extend([row.lat, row.lon]);        
        });
        if (data.length > 0) {
            map.fitBounds(bounds);        
        }
    }

    // =========================================================================
    // 1. Get Element by ID
    // =========================================================================

    // Form Control: Select Region
    const ostan = document.getElementById("ostan");
    const shahrestan = document.getElementById("shahrestan");
    const bakhsh = document.getElementById("bakhsh");
    const shahr = document.getElementById("shahr");
    const region = document.getElementById("region");
    const district = document.getElementById("district");

    // Form Control: Select Parameters 
    const bread_types = document.getElementById("bread_types");
    const flour_types = document.getElementById("flour_types");
    const second_fuel = document.getElementById("second_fuel");
    const bakers_risk = document.getElementById("bakers_risk");
    const household_risk = document.getElementById("household_risk");
    const ownership_status = document.getElementById("ownership_status");


    // Form Control: Select Layers
    const ostan_layer_switch = document.getElementById("ostan_layer_switch");
    const shahrestan_layer_switch = document.getElementById("shahrestan_layer_switch");
    const bakhsh_layer_switch = document.getElementById("bakhsh_layer_switch");
    const shahr_layer_switch = document.getElementById("shahr_layer_switch");
    const region_layer_switch = document.getElementById("region_layer_switch");
    const district_layer_switch = document.getElementById("district_layer_switch");

    const region_choropleth_map = document.getElementById("region_choropleth_map");
    const district_choropleth_map = document.getElementById("district_choropleth_map");


    // =========================================================================
    // 2. Load Map Data
    // =========================================================================     
    load_map_data();

    async function load_map_data() {

        let selected_ostan = ostan.value;
        let selected_shahrestan = shahrestan.value;
        let selected_bakhsh = bakhsh.value;
        let selected_shahr = shahr.value;
        let selected_region = region.value;
        let selected_district = district.value;
        let selected_bread_types = bread_types.value;
        let selected_flour_types = flour_types.value;
        let selected_second_fuel = second_fuel.value;
        let selected_bakers_risk = bakers_risk.value;
        let selected_household_risk = household_risk.value;
        let selected_ownership_status = ownership_status.value;

        if (!selected_ostan) {
            selected_ostan = "999";
        }
        if (!selected_shahrestan) {
            selected_shahrestan = "999";
        }
        if (!selected_bakhsh) {
            selected_bakhsh = "999";
        }
        if (!selected_shahr) {
            selected_shahr = "999";
        }
        if (!selected_region) {
            selected_region = "999";
        }
        if (!selected_district) {
            selected_district = "999";
        }
        if (!selected_bread_types) {
            selected_bread_types = "999";
        }
        if (!selected_flour_types) {
            selected_flour_types = "999";
        }
        if (!selected_second_fuel) {
            selected_second_fuel = "999";
        }
        if (!selected_bakers_risk) {
            selected_bakers_risk = "999";
        }
        if (!selected_household_risk) {
            selected_household_risk = "999";
        }
        if (!selected_ownership_status) {
            selected_ownership_status = "999";
        }

        const response = await fetch(`/api/map/data/${selected_ostan}/${selected_shahrestan}/${selected_bakhsh}/${selected_shahr}/${selected_region}/${selected_district}/${selected_bread_types}/${selected_flour_types}/${selected_second_fuel}/${selected_bakers_risk}/${selected_household_risk}/${selected_ownership_status}`);
        const data = await response.json();
        addMarkers(data.data);
    }


    // =========================================================================
    // 3. Form Control
    // =========================================================================
    document.addEventListener("DOMContentLoaded", function () {
        
        // ---------------------------------------------------------------------
        // Select Region  
        // ---------------------------------------------------------------------
        get_ostan_options();
        get_bread_types_options();
        get_flour_types_options();
        get_second_fuel_options();
        get_bakers_risk_options();
        get_household_risk_options();
        get_ownership_status_options();

        // ---------------------------------------------------------------------
        // Get Ostan Options
        // ---------------------------------------------------------------------
        async function get_ostan_options() {
            const response = await fetch('/api/map/ostan');
            const data = await response.json();
            data.forEach(item => {
                let option = document.createElement('option');                
                option.value = item;
                option.textContent = item;
                ostan.appendChild(option);
            });
        };

        // ---------------------------------------------------------------------
        // Get Shahrestan Options
        // ---------------------------------------------------------------------
        ostan.addEventListener('change', function () {
            shahrestan.innerHTML = '<option value="">انتخاب کنید ...</option>';
            bakhsh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            shahr.innerHTML = '<option value="">انتخاب کنید ...</option>';
            region.innerHTML = '<option value="">انتخاب کنید ...</option>';
            district.innerHTML = '<option value="">انتخاب کنید ...</option>';
            if (ostan.value) {
                fetch(`/api/map/shahrestan/${ostan.value}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            let option = document.createElement('option');
                            option.value = item;
                            option.textContent = item;
                            shahrestan.appendChild(option);
                        });
                    });
            }
        });

        // ---------------------------------------------------------------------
        // Get Bakhsh Options
        // ---------------------------------------------------------------------
        shahrestan.addEventListener('change', function () {
            bakhsh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            shahr.innerHTML = '<option value="">انتخاب کنید ...</option>';
            region.innerHTML = '<option value="">انتخاب کنید ...</option>';
            district.innerHTML = '<option value="">انتخاب کنید ...</option>';
            if (shahrestan.value) {
                fetch(`/api/map/bakhsh/${shahrestan.value}/${ostan.value}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            let option = document.createElement('option');
                            option.value = item;
                            option.textContent = item;
                            bakhsh.appendChild(option);
                        });
                    });
            }
        });

        // ---------------------------------------------------------------------
        // Get Shahr Options
        // ---------------------------------------------------------------------
        bakhsh.addEventListener('change', function () {
            shahr.innerHTML = '<option value="">انتخاب کنید ...</option>';
            region.innerHTML = '<option value="">انتخاب کنید ...</option>';
            district.innerHTML = '<option value="">انتخاب کنید ...</option>';
            if (bakhsh.value) {
                fetch(`/api/map/shahr/${bakhsh.value}/${shahrestan.value}/${ostan.value}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            let option = document.createElement('option');
                            option.value = item;
                            option.textContent = item;
                            shahr.appendChild(option);
                        });
                    });
            }
        });

        // ---------------------------------------------------------------------
        // Get Region Options
        // ---------------------------------------------------------------------
        shahr.addEventListener('change', function () {
            region.innerHTML = '<option value="">انتخاب کنید ...</option>';
            district.innerHTML = '<option value="">انتخاب کنید ...</option>';
            if (shahr.value) {
                fetch(`/api/map/region/${shahr.value}/${bakhsh.value}/${shahrestan.value}/${ostan.value}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            let option = document.createElement('option');
                            option.value = item;
                            option.textContent = item;
                            region.appendChild(option);
                        });
                    });
            }
        });

        // ---------------------------------------------------------------------
        // Get District Options
        // ---------------------------------------------------------------------
        region.addEventListener('change', function () {
            district.innerHTML = '<option value="">انتخاب کنید ...</option>';
            if (region.value) {
                fetch(`/api/map/district/${region.value}/${shahr.value}/${bakhsh.value}/${shahrestan.value}/${ostan.value}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            let option = document.createElement('option');
                            option.value = item;
                            option.textContent = item;
                            district.appendChild(option);
                        });
                    });
            }
        });

        // ---------------------------------------------------------------------
        // Get Bread Types Options
        // ---------------------------------------------------------------------
        async function get_bread_types_options() {
            const response = await fetch('/api/map/bread_types');
            const data = await response.json();
            data.forEach(item => {
                let option = document.createElement('option');                
                option.value = item;
                option.textContent = item;
                bread_types.appendChild(option);
            });
        };

        // ---------------------------------------------------------------------
        // Get Flour Types Options
        // ---------------------------------------------------------------------
        async function get_flour_types_options() {
            const response = await fetch('/api/map/flour_types');
            const data = await response.json();
            data.forEach(item => {
                let option = document.createElement('option');                
                option.value = item;
                option.textContent = item;
                flour_types.appendChild(option);
            });
        };

        // ---------------------------------------------------------------------
        // Get Second Fuel Options
        // ---------------------------------------------------------------------
        async function get_second_fuel_options() {
            const response = await fetch('/api/map/second_fuel');
            const data = await response.json();
            data.forEach(item => {
                let option = document.createElement('option');                
                option.value = item;
                option.textContent = item;
                second_fuel.appendChild(option);
            });
        };

        // ---------------------------------------------------------------------
        // Get Bakers Risk Options
        // ---------------------------------------------------------------------
        async function get_bakers_risk_options() {
            const response = await fetch('/api/map/bakers_risk');
            const data = await response.json();
            data.forEach(item => {
                let option = document.createElement('option');                
                option.value = item;
                option.textContent = item;
                bakers_risk.appendChild(option);
            });
        };

        // ---------------------------------------------------------------------
        // Get Household Risk Options
        // ---------------------------------------------------------------------
        async function get_household_risk_options() {
            const response = await fetch('/api/map/household_risk');
            const data = await response.json();
            data.forEach(item => {
                let option = document.createElement('option');                
                option.value = item;
                option.textContent = item;
                household_risk.appendChild(option);
            });
        };

        // ---------------------------------------------------------------------
        // Get Ownership Status Options
        // ---------------------------------------------------------------------
        async function get_ownership_status_options() {
            const response = await fetch('/api/map/ownership_status');
            const data = await response.json();
            data.forEach(item => {
                let option = document.createElement('option');                
                option.value = item;
                option.textContent = item;
                ownership_status.appendChild(option);
            });
        };

        // ---------------------------------------------------------------------
        // Handle the Change Event
        // ---------------------------------------------------------------------
        // Ostan
        $(document).ready(function () {
            $("#ostan").on("change", function () {
                load_map_data();
                if (shahr.value == "روستایی") {
                    region.disabled = true;
                    district.disabled = true;
                } else {
                    region.disabled = false;
                    district.disabled = false;
                }
            });
        });

        // Sharestan
        $(document).ready(function () {
            $("#shahrestan").on("change", function () {
                load_map_data();
                if (shahr.value == "روستایی") {
                    region.disabled = true;
                    district.disabled = true;
                } else {
                    region.disabled = false;
                    district.disabled = false;
                }
            });
        });

        // Bakhsh
        $(document).ready(function () {
            $("#bakhsh").on("change", function () {
                load_map_data();
                if (shahr.value == "روستایی") {
                    region.disabled = true;
                    district.disabled = true;
                } else {
                    region.disabled = false;
                    district.disabled = false;
                }
            });
        });

        // Shahr
        $(document).ready(function () {
            $("#shahr").on("change", function () {
                load_map_data();
                if (shahr.value == "روستایی") {
                    region.disabled = true;
                    district.disabled = true;
                } else {
                    region.disabled = false;
                    district.disabled = false;
                }
            });
        });

        // Region
        $(document).ready(function () {
            $("#region").on("change", function () {
                load_map_data();
            });
        });

        // District
        $(document).ready(function () {
            $("#district").on("change", function () {
                load_map_data();
            });
        });

        // Bread Types
        $(document).ready(function () {
            $("#bread_types").on("change", function () {
                load_map_data();
            });
        });

        // Flour Types
        $(document).ready(function () {
            $("#flour_types").on("change", function () {
                load_map_data();
            });
        });

        // Second Fuel
        $(document).ready(function () {
            $("#second_fuel").on("change", function () {
                load_map_data();
            });
        });

        // Bakers Risk
        $(document).ready(function () {
            $("#bakers_risk").on("change", function () {
                load_map_data();
            });
        });

        // Household Risk
        $(document).ready(function () {
            $("#household_risk").on("change", function () {
                load_map_data();
            });
        });

        // Ownership Status
        $(document).ready(function () {
            $("#ownership_status").on("change", function () {
                load_map_data();
            });
        });

    });

    document.getElementById('clear-parameter-form').addEventListener('click', function () {
        bread_types.value = "";
        flour_types.value = "";
        second_fuel.value = "";
        bakers_risk.value = "";
        household_risk.value = "";
        ownership_status.value = "";
        load_map_data();
    });

    document.getElementById('clear-region-form').addEventListener('click', function () {
        ostan.value = "";
        shahrestan.value = "";
        bakhsh.value = "";
        shahr.value = "";
        region.value = "";
        district.value = "";
        load_map_data();
    });


    // -------------------------------------------------------------------------
    // Layers
    // -------------------------------------------------------------------------

    const getLayer = async (api, func) => {
        try {
            const response = await fetch(api);
            if (!response.ok) {
                throw new Error(`Error fetching data: ${response.statusText}`);
            }
            const data = await response.json();
            func(data);
        } catch (error) {
            console.error("Error in getLayer:", error);
        }
    };

    // Ostan
    let ostan_layer = null;

    function addOstanLayer(data) {
        ostan_layer = L.geoJSON(data, {
            style: function (feature) {
                return {
                    color: "#3388ff",
                    weight: 5,
                    opacity: 1,
                    fillColor: "#3388ff",
                    fillOpacity: 0.2
                };
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(
                    `
                    <h6 class="" style="text-align: center !important;">استان ${feature.properties.ostan}</h6>
                    <div class="table-responsive medium">
                    </div>
                    `
                );
            }
        });
    }

    getLayer('/assets/data/geodatabase/Ostan.geojson', addOstanLayer);

    document.getElementById('ostan_layer_switch').addEventListener('change', function() {
        if (this.checked) {           
            if (ostan_layer) {
                ostan_layer.addTo(map);
                map.fitBounds(ostan_layer.getBounds());
            }
        } else {
            if (ostan_layer) {
                map.removeLayer(ostan_layer);
            }
        }
    })


    // Shahrestan
    let shahrestan_layer = null;

    function addSahrestanLayer(data) {
        shahrestan_layer = L.geoJSON(data, {
            style: function (feature) {
                return {
                    color: "#3388ff",
                    weight: 5,
                    opacity: 1,
                    fillColor: "#3388ff",
                    fillOpacity: 0.2
                };
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(
                    `
                    <h6 class="" style="text-align: center !important;">شهرستان ${feature.properties.shahrestan}</h6>
                    <div class="table-responsive medium">
                        <table class="table table-striped table-sm">
                            <tbody>
                                <tr>
                                    <th>استان</th>
                                    <td>${feature.properties.ostan}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    `
                );
            }
        });
    }

    getLayer('/assets/data/geodatabase/Shahrestan.geojson', addSahrestanLayer);

    document.getElementById('shahrestan_layer_switch').addEventListener('change', function() {
        if (this.checked) {           
            if (shahrestan_layer) {
                shahrestan_layer.addTo(map);
                map.fitBounds(shahrestan_layer.getBounds());
            }
        } else {
            if (shahrestan_layer) {
                map.removeLayer(shahrestan_layer);
            }
        }
    })

    
    // Bakhsh
    let bakhsh_layer = null;

    function addBakhshLayer(data) {
        bakhsh_layer = L.geoJSON(data, {
            style: function (feature) {
                return {
                    color: "#3388ff",
                    weight: 5,
                    opacity: 1,
                    fillColor: "#3388ff",
                    fillOpacity: 0.2
                };
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(
                    `
                    <h6 class="" style="text-align: center !important;">بخش ${feature.properties.bakhsh}</h6>
                    <div class="table-responsive medium">
                        <table class="table table-striped table-sm">
                            <tbody>
                                <tr>
                                    <th>شهرستان</th>
                                    <td>${feature.properties.shahrestan}</td>
                                </tr>
                                <tr>
                                    <th>استان</th>
                                    <td>${feature.properties.ostan}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    `
                );
            }
        });
    }

    getLayer('/assets/data/geodatabase/Bakhsh.geojson', addBakhshLayer);

    document.getElementById('bakhsh_layer_switch').addEventListener('change', function() {
        if (this.checked) {           
            if (bakhsh_layer) {
                bakhsh_layer.addTo(map);
                map.fitBounds(bakhsh_layer.getBounds());
            }
        } else {
            if (bakhsh_layer) {
                map.removeLayer(bakhsh_layer);
            }
        }
    })


    // Shahr
    let shahr_layer = null;

    function addShahrLayer(data) {
        shahr_layer = L.geoJSON(data, {
            style: function (feature) {
                return {
                    color: "#3388ff",
                    weight: 5,
                    opacity: 1,
                    fillColor: "#3388ff",
                    fillOpacity: 0.2
                };
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(
                    `
                    <h6 class="" style="text-align: center !important;">شهر ${feature.properties.shahr}</h6>
                    <div class="table-responsive medium">
                        <table class="table table-striped table-sm">
                            <tbody>
                                <tr>
                                    <th>بخش</th>
                                    <td>${feature.properties.bakhsh}</td>
                                </tr>
                                <tr>
                                    <th>شهرستان</th>
                                    <td>${feature.properties.shahrestan}</td>
                                </tr>
                                <tr>
                                    <th>استان</th>
                                    <td>${feature.properties.ostan}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    `
                );
            }
        });
    }

    getLayer('/assets/data/geodatabase/Shahr.geojson', addShahrLayer);

    document.getElementById('shahr_layer_switch').addEventListener('change', function() {
        if (this.checked) {           
            if (shahr_layer) {
                shahr_layer.addTo(map);
                map.fitBounds(shahr_layer.getBounds());
            }
        } else {
            if (shahr_layer) {
                map.removeLayer(shahr_layer);
            }
        }
    })

    // Region
    let region_layer = null;

    function addRegionLayer(data) {
        region_layer = L.geoJSON(data, {
            style: function (feature) {
                return {
                    color: "#3388ff",
                    weight: 5,
                    opacity: 1,
                    fillColor: "#3388ff",
                    fillOpacity: 0.2
                };
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(
                    `
                    <h6 class="" style="text-align: center !important;">منطقه ${feature.properties.region}</h6>
                    <div class="table-responsive medium">
                        <table class="table table-striped table-sm">
                            <tbody>
                                <tr>
                                    <th>شهر</th>
                                    <td>${feature.properties.shahr}</td>
                                </tr>
                                <tr>
                                    <th>بخش</th>
                                    <td>${feature.properties.bakhsh}</td>
                                </tr>
                                <tr>
                                    <th>شهرستان</th>
                                    <td>${feature.properties.shahrestan}</td>
                                </tr>
                                <tr>
                                    <th>استان</th>
                                    <td>${feature.properties.ostan}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    `
                );
            }
        });
    }

    getLayer('/assets/data/geodatabase/Region.geojson', addRegionLayer);

    document.getElementById('region_layer_switch').addEventListener('change', function() {
        if (this.checked) {           
            if (region_layer) {
                region_layer.addTo(map);
                map.fitBounds(region_layer.getBounds());
            }
        } else {
            if (region_layer) {
                map.removeLayer(region_layer);
            }
        }
    })

    // District
    let district_layer = null;

    function addDistrictLayer(data) {
        district_layer = L.geoJSON(data, {
            style: function (feature) {
                return {
                    color: "#3388ff",
                    weight: 5,
                    opacity: 1,
                    fillColor: "#3388ff",
                    fillOpacity: 0.2
                };
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(
                    `
                    <h6 class="" style="text-align: center !important;">ناحیه ${feature.properties.district}</h6>
                    <div class="table-responsive medium">
                        <table class="table table-striped table-sm">
                            <tbody>
                                <tr>
                                    <th>منطقه</th>
                                    <td>${feature.properties.region}</td>
                                </tr>
                                <tr>
                                    <th>شهر</th>
                                    <td>${feature.properties.shahr}</td>
                                </tr>
                                <tr>
                                    <th>بخش</th>
                                    <td>${feature.properties.bakhsh}</td>
                                </tr>
                                <tr>
                                    <th>شهرستان</th>
                                    <td>${feature.properties.shahrestan}</td>
                                </tr>
                                <tr>
                                    <th>استان</th>
                                    <td>${feature.properties.ostan}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    `
                );
            }
        });
    }

    getLayer('/assets/data/geodatabase/District.geojson', addDistrictLayer);

    document.getElementById('district_layer_switch').addEventListener('change', function() {
        if (this.checked) {           
            if (district_layer) {
                district_layer.addTo(map);
                map.fitBounds(district_layer.getBounds());
            }
        } else {
            if (district_layer) {
                map.removeLayer(district_layer);
            }
        }
    })


    // Region Choropleth Map
    let region_choropleth_layer = null;

    fetch('/api/map/choropleth/region')
        .then(response => response.json())
        .then(data => {
            // Load GeoJSON
            
            fetch('/assets/data/geodatabase/Region.geojson')
                .then(response => response.json())
                .then(geojson => {

                    // Define a style function
                    function style(feature) {
                        const regionData = data.find(d =>
                            d.ostan == feature.properties.ostan &&
                            d.shahrestan == feature.properties.shahrestan &&
                            d.bakhsh == feature.properties.bakhsh &&
                            d.shahr == feature.properties.shahr &&
                            d.region == feature.properties.region
                        );
                        const population_per_bakery = regionData ? regionData.population_per_bakery : 0;
                        const ration_per_population_per_100 = regionData ? regionData.ration_per_population_per_100 : 0;
                        return {
                            fillColor: getColor(population_per_bakery),
                            weight: 2,
                            opacity: 1,
                            color: 'white',
                            dashArray: '3',
                            fillOpacity: 0.7
                        };
                    }

                    function highlightFeature(e) {
                        const layer = e.target;
                
                        layer.setStyle({
                            weight: 5,
                            color: '#666',
                            dashArray: '',
                            fillOpacity: 0.7
                        });
                
                        layer.bringToFront();
                
                    }

                    function resetHighlight(e) {
                        region_choropleth_layer.resetStyle(e.target);
                    }

                    function zoomToFeature(e) {
                        map.fitBounds(e.target.getBounds());
                    }

                    // Function to get color based on ratio
                    function getColor(population_per_bakery) {
                        return population_per_bakery > 4000 ? '#fff5f0' :
                            population_per_bakery > 3500 ? '#fee0d2' :
                            population_per_bakery > 3000  ? '#fcbba1' :
                            population_per_bakery > 2500 ? '#fc9272' :
                            population_per_bakery > 2000   ? '#fb6a4a' :
                            population_per_bakery > 1500   ? '#ef3b2c' :
                            population_per_bakery > 1000    ? '#cb181d' :
                                            '#99000d';
                    }                    

                    // Add GeoJSON layer
                    region_choropleth_layer = L.geoJson(geojson, {
                        style: style,
                        onEachFeature: function(feature, layer) {
                            layer.bindTooltip(
                            // layer.bindPopup(
                                '<b>منطقه: ' + feature.properties.region + '</b><br>' +
                                '- به ازای هر  ' + (Math.floor(data.find(d => 
                                    d.ostan == feature.properties.ostan &&
                                    d.shahrestan == feature.properties.shahrestan &&
                                    d.bakhsh == feature.properties.bakhsh &&
                                    d.shahr == feature.properties.shahr &&
                                    d.region == feature.properties.region
                                )?.population_per_bakery) || 'N/A') + ' نفر، یک عدد نانوایی<br>' +
                                '- به ازای هر 100 نفر،  ' + (Math.floor(data.find(d => 
                                    d.ostan == feature.properties.ostan &&
                                    d.shahrestan == feature.properties.shahrestan &&
                                    d.bakhsh == feature.properties.bakhsh &&
                                    d.shahr == feature.properties.shahr &&
                                    d.region == feature.properties.region
                                )?.ration_per_population_per_100) || 'N/A') + ' عدد کیسه آرد'
                            );
                            layer.on({
                                mouseover: highlightFeature,
                                mouseout: resetHighlight,
                                click: zoomToFeature
                            });
                        }
                    });

                    region_choropleth_map.addEventListener('change', function() {
                        if (this.checked) {           
                            if (region_choropleth_layer) {
                                region_choropleth_layer.addTo(map);
                                map.fitBounds(region_choropleth_layer.getBounds());
                            }
                        } else {
                            if (region_choropleth_layer) {
                                map.removeLayer(region_choropleth_layer);
                            }
                        }
                    })
                });
        })

    // District Choropleth Map
    let district_choropleth_layer = null;

    fetch('/api/map/choropleth/district')
        .then(response => response.json())
        .then(data => {
            // Load GeoJSON
            
            fetch('/assets/data/geodatabase/District.geojson')
                .then(response => response.json())
                .then(geojson => {

                    // Define a style function
                    function style(feature) {
                        const districtData = data.find(d =>
                            d.ostan == feature.properties.ostan &&
                            d.shahrestan == feature.properties.shahrestan &&
                            d.bakhsh == feature.properties.bakhsh &&
                            d.shahr == feature.properties.shahr &&
                            d.region == feature.properties.region &&
                            d.district == feature.properties.district
                        );
                        const population_per_bakery = districtData ? districtData.population_per_bakery : 0;
                        const ration_per_population_per_100 = districtData ? districtData.ration_per_population_per_100 : 0;
                        return {
                            fillColor: getColor(population_per_bakery),
                            weight: 2,
                            opacity: 1,
                            color: 'white',
                            dashArray: '3',
                            fillOpacity: 0.7
                        };
                    }

                    function highlightFeature(e) {
                        const layer = e.target;
                
                        layer.setStyle({
                            weight: 5,
                            color: '#666',
                            dashArray: '',
                            fillOpacity: 0.7
                        });
                
                        layer.bringToFront();
                
                    }

                    function resetHighlight(e) {
                        district_choropleth_layer.resetStyle(e.target);
                    }

                    function zoomToFeature(e) {
                        map.fitBounds(e.target.getBounds());
                    }

                    // Function to get color based on ratio
                    function getColor(population_per_bakery) {
                        return population_per_bakery > 4000 ? '#fff5f0' :
                            population_per_bakery > 3500 ? '#fee0d2' :
                            population_per_bakery > 3000  ? '#fcbba1' :
                            population_per_bakery > 2500 ? '#fc9272' :
                            population_per_bakery > 2000   ? '#fb6a4a' :
                            population_per_bakery > 1500   ? '#ef3b2c' :
                            population_per_bakery > 1000    ? '#cb181d' :
                                            '#99000d';
                    }                    

                    // Add GeoJSON layer
                    district_choropleth_layer = L.geoJson(geojson, {
                        style: style,
                        onEachFeature: function(feature, layer) {
                            layer.bindTooltip(
                            // layer.bindPopup(
                                '<b>منطقه: ' + feature.properties.region + ' ناحیه: ' + feature.properties.district + '</b><br>' +
                                '- به ازای هر  ' + (Math.floor(data.find(d => 
                                    d.ostan == feature.properties.ostan &&
                                    d.shahrestan == feature.properties.shahrestan &&
                                    d.bakhsh == feature.properties.bakhsh &&
                                    d.shahr == feature.properties.shahr &&
                                    d.region == feature.properties.region &&
                                    d.district == feature.properties.district
                                )?.population_per_bakery) || 'N/A') + ' نفر، یک عدد نانوایی<br>' +
                                '- به ازای هر 100 نفر،  ' + (Math.floor(data.find(d => 
                                    d.ostan == feature.properties.ostan &&
                                    d.shahrestan == feature.properties.shahrestan &&
                                    d.bakhsh == feature.properties.bakhsh &&
                                    d.shahr == feature.properties.shahr &&
                                    d.region == feature.properties.region &&
                                    d.district == feature.properties.district
                                )?.ration_per_population_per_100) || 'N/A') + ' عدد کیسه آرد'
                            );
                            layer.on({
                                mouseover: highlightFeature,
                                mouseout: resetHighlight,
                                click: zoomToFeature
                            });
                        }
                    });

                    district_choropleth_map.addEventListener('change', function() {
                        if (this.checked) {           
                            if (district_choropleth_layer) {
                                district_choropleth_layer.addTo(map);
                                map.fitBounds(district_choropleth_layer.getBounds());
                            }
                        } else {
                            if (district_choropleth_layer) {
                                map.removeLayer(district_choropleth_layer);
                            }
                        }
                    })
                });
        })


 


    // =========================================================================
    // /Form Control
    // =========================================================================


    
    // let region_choropleth_layer;

    // fetch('/api/dashboard/map/region_ratio')
    //     .then(response => response.json())
    //     .then(data => {
    //         // Load GeoJSON
    //         fetch('/assets/data/geodatabase/Region.geojson')
    //             .then(response => response.json())
    //             .then(geojson => {
    //                 // Define a style function
    //                 function style(feature) {
    //                     const regionData = data.find(d => d.region == feature.properties.region);
    //                     const ratio = regionData ? regionData.ratio : 0;
    //                     return {
    //                         fillColor: getColor(ratio),
    //                         weight: 2,
    //                         opacity: 1,
    //                         color: 'white',
    //                         dashArray: '3',
    //                         fillOpacity: 0.7
    //                     };
    //                 }

    //                 // Function to get color based on ratio
    //                 function getColor(ratio) {
    //                     return ratio > 4000 ? '#fff5f0' :
    //                         ratio > 3500 ? '#fee0d2' :
    //                         ratio > 3000  ? '#fcbba1' :
    //                         ratio > 2500 ? '#fc9272' :
    //                         ratio > 2000   ? '#fb6a4a' :
    //                         ratio > 1500   ? '#ef3b2c' :
    //                         ratio > 1000    ? '#cb181d' :
    //                                         '#99000d';
    //                 }                    

    //                 // Add GeoJSON layer
    //                 region_choropleth_layer = L.geoJson(geojson, {
    //                     style: style,
    //                     onEachFeature: function(feature, layer) {
    //                         layer.bindPopup(
    //                             '<b>منطقه: ' + feature.properties.region + '</b><br>' +
    //                             '- به ازای هر  ' + (Math.floor(data.find(d => d.region == feature.properties.region)?.ratio) || 'N/A') + ' نفر، یک عدد نانوایی<br>' +
    //                             '- به ازای هر 100 نفر،  ' + (Math.floor(data.find(d => d.region == feature.properties.region)?.ration) || 'N/A') + ' عدد کیسه آرد');
    //                     }
    //                 }).addTo(map);

    //                 const toggleLayerCheckbox = document.getElementById('showRatioRegion');
    //                 toggleLayerCheckbox.addEventListener('change', function() {
    //                     if (this.checked) {
    //                         map.addLayer(region_choropleth_layer); // Add layer when checked
    //                     } else {
    //                         map.removeLayer(region_choropleth_layer); // Remove layer when unchecked
    //                     }
    //                 });
    //             });
    //     })


    //     let ratio_map_district;

    //     fetch('/api/dashboard/map/district_ratio')
    //         .then(response => response.json())
    //         .then(data => {
    //             // Load GeoJSON
    //             fetch('/assets/data/geodatabase/District.geojson')
    //                 .then(response => response.json())
    //                 .then(geojson => {
    //                     // Define a style function
    //                     function style(feature) {
                            
                            
    //                         const regionData = data.find(d => d.region == feature.properties.region && d.district == feature.properties.district);                            
    //                         const ratio = regionData ? regionData.ratio : 0;
    //                         return {
    //                             fillColor: getColor(ratio),
    //                             weight: 2,
    //                             opacity: 1,
    //                             color: 'white',
    //                             dashArray: '3',
    //                             fillOpacity: 0.7
    //                         };
    //                     }
    
    //                     // Function to get color based on ratio
    //                     function getColor(ratio) {
    //                         return ratio > 4000 ? '#fff5f0' :
    //                             ratio > 3500 ? '#fee0d2' :
    //                             ratio > 3000  ? '#fcbba1' :
    //                             ratio > 2500 ? '#fc9272' :
    //                             ratio > 2000   ? '#fb6a4a' :
    //                             ratio > 1500   ? '#ef3b2c' :
    //                             ratio > 1000    ? '#cb181d' :
    //                                             '#99000d';
    //                     }                    
    
    //                     // Add GeoJSON layer
    //                     ratio_map_district = L.geoJson(geojson, {
    //                         style: style,
    //                         onEachFeature: function(feature, layer) {
    //                             layer.bindPopup(
    //                                 '<b>منطقه: ' + feature.properties.region + ' ناحیه: ' + feature.properties.district + '</b><br>' +
    //                                 '- به ازای هر  ' + (Math.floor(data.find(d => d.region == feature.properties.region && d.district == feature.properties.district)?.ratio) || 'N/A') + ' نفر، یک عدد نانوایی<br>' +
    //                                 '- به ازای هر 100 نفر،  ' + (Math.floor(data.find(d => d.region == feature.properties.region && d.district == feature.properties.district)?.ration) || 'N/A') + ' عدد کیسه آرد');
    //                         }
    //                     }).addTo(map);
    
    //                     const toggleLayerCheckboxDistrict = document.getElementById('showRatioDistrict');
    //                     toggleLayerCheckboxDistrict.addEventListener('change', function() {
    //                         if (this.checked) {
    //                             map.addLayer(ratio_map_district); // Add layer when checked
    //                         } else {
    //                             map.removeLayer(ratio_map_district); // Remove layer when unchecked
    //                         }
    //                     });
    //                 });
    //         })




})();
