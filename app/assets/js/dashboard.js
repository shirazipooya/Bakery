"use strict";

(function () {

    // =========================================================================
    // Utile
    // =========================================================================
    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }


    // =========================================================================
    // Get Element by ID
    // =========================================================================

    // -------------------------------------------------------------------------
    // Form Control
    // -------------------------------------------------------------------------
    const ostan = document.getElementById("ostan");
    const shahrestan = document.getElementById("shahrestan");
    const bakhsh = document.getElementById("bakhsh");
    const shahrRosta = document.getElementById("shahrRosta");
    const mantagheh = document.getElementById("mantagheh");
    const nahyeh = document.getElementById("nahyeh");

    // -------------------------------------------------------------------------
    // Cards
    // -------------------------------------------------------------------------
    const number_of_bakeries = document.getElementById('number_of_bakeries')
    const number_of_households = document.getElementById('number_of_households')
    const area = document.getElementById('area')
    const population = document.getElementById('population')
    const population_male = document.getElementById('population_male')
    const population_female = document.getElementById('population_female')
    const population_number_of_bakeries_1 = document.getElementById('population_number_of_bakeries_1')
    const population_number_of_bakeries_2 = document.getElementById('population_number_of_bakeries_2')
    const households_number_of_bakeries_1 = document.getElementById('households_number_of_bakeries_1')
    const households_number_of_bakeries_2 = document.getElementById('households_number_of_bakeries_2')
    const area_number_of_bakeries_1 = document.getElementById('area_number_of_bakeries_1')
    const area_number_of_bakeries_2 = document.getElementById('area_number_of_bakeries_2')
    const population_bread_rations_1 = document.getElementById('population_bread_rations_1')
    const population_bread_rations_2 = document.getElementById('population_bread_rations_2')


    // =========================================================================
    // Load Dashboard Data
    // =========================================================================     
    load_dashboard_data();

    async function load_dashboard_data() {
        let selectedOstan = ostan.value;
        let selectedShahrestan = shahrestan.value;
        let selectedBakhsh = bakhsh.value;
        let selectedShahrRosta = shahrRosta.value;
        let selectedMantagheh = mantagheh.value;
        let selectedNahyeh = nahyeh.value;

        if (!selectedOstan) {
            selectedOstan = "999";
        }
        if (!selectedShahrestan) {
            selectedShahrestan = "999";
        }
        if (!selectedBakhsh) {
            selectedBakhsh = "999";
        }
        if (!selectedShahrRosta) {
            selectedShahrRosta = "999";
        }
        if (!selectedMantagheh) {
            selectedMantagheh = "999";
        }
        if (!selectedNahyeh) {
            selectedNahyeh = "999";
        }

        const response = await fetch(`/api/dashboard/data/${selectedOstan}/${selectedShahrestan}/${selectedBakhsh}/${selectedShahrRosta}/${selectedMantagheh}/${selectedNahyeh}`);
        const data = await response.json();
        updateCards(data);
    }


    // =========================================================================
    // Update Cards
    // =========================================================================
    function updateCards(data) {
        number_of_bakeries.innerHTML = numberWithCommas(data.number_of_bakeries);
        number_of_households.innerHTML = numberWithCommas(data.number_of_households);
        area.innerHTML = numberWithCommas(data.area);
        population.innerHTML = numberWithCommas(data.population);
        population_male.innerHTML = numberWithCommas(data.population_male);
        population_female.innerHTML = numberWithCommas(data.population_female);
        population_number_of_bakeries_1.innerHTML = numberWithCommas(data.population_number_of_bakeries);
        population_number_of_bakeries_2.innerHTML = numberWithCommas(data.population_number_of_bakeries);
        households_number_of_bakeries_1.innerHTML = numberWithCommas(data.households_number_of_bakeries);
        households_number_of_bakeries_2.innerHTML = numberWithCommas(data.households_number_of_bakeries);
        area_number_of_bakeries_1.innerHTML = numberWithCommas(data.area_number_of_bakeries);
        area_number_of_bakeries_2.innerHTML = numberWithCommas(data.area_number_of_bakeries);
        population_bread_rations_1.innerHTML = numberWithCommas(data.population_bread_rations);
        population_bread_rations_2.innerHTML = numberWithCommas(data.population_bread_rations);

        breadTypesCard(data);
        flourTypesCard(data);
        secondFuelCard(data);
    };

    // -------------------------------------------------------------------------
    // Bread Types Card
    // -------------------------------------------------------------------------
    function breadTypesCard(data) {            
        data.bread_types_data_updated.forEach((item) => {
            const count = item.count || 0;
            const percent = item.percent.toFixed(0);
            document.getElementById(`BreadType_${item.code}_Count`).innerHTML = count;
            document.getElementById(`BreadType_${item.code}_Percent`).innerHTML = `(${percent}%)`;
            document.getElementById(`BreadType_${item.code}_Bar`).style.width = `${percent}%`;
        });
    }


    // -------------------------------------------------------------------------
    // Flour Types Card
    // -------------------------------------------------------------------------
    function flourTypesCard(data) {            
        data.flour_types_data_updated.forEach((item) => {
            const count = item.count || 0;
            const percent = item.percent.toFixed(0);
            document.getElementById(`FlourType_${item.code}_Count`).innerHTML = count;
            document.getElementById(`FlourType_${item.code}_Percent`).innerHTML = `(${percent}%)`;
            document.getElementById(`FlourType_${item.code}_Bar`).style.width = `${percent}%`;
        });
    }


    // -------------------------------------------------------------------------
    // Seconf Fuel
    // -------------------------------------------------------------------------
    function secondFuelCard(data) {            
        data.second_fuel_data_updated.forEach((item) => {
            const count = item.count || 0;
            const percent = item.percent.toFixed(0);
            document.getElementById(`SecondFuel_${item.code}_Count`).innerHTML = count;
            document.getElementById(`SecondFuel_${item.code}_Percent`).innerHTML = `(${percent}%)`;
            document.getElementById(`SecondFuel_${item.code}_Bar`).style.width = `${percent}%`;
        });
    }
    

    // =========================================================================
    // Form Control
    // =========================================================================
    document.addEventListener("DOMContentLoaded", function () {

        // ---------------------------------------------------------------------
        // Load Functions
        // ---------------------------------------------------------------------       
        get_ostan_options();


        // ---------------------------------------------------------------------
        // Get Ostan Options
        // ---------------------------------------------------------------------
        async function get_ostan_options() {
            const response = await fetch('/api/dashboard/ostan');
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
            shahrRosta.innerHTML = '<option value="">انتخاب کنید ...</option>';
            mantagheh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            nahyeh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            if (ostan.value) {
                fetch(`/api/dashboard/shahrestan/${ostan.value}`)
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
            shahrRosta.innerHTML = '<option value="">انتخاب کنید ...</option>';
            mantagheh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            nahyeh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            if (shahrestan.value) {
                fetch(`/api/dashboard/bakhsh/${shahrestan.value}/${ostan.value}`)
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
        // Get ShahrRosta Options
        // ---------------------------------------------------------------------
        bakhsh.addEventListener('change', function () {
            shahrRosta.innerHTML = '<option value="">انتخاب کنید ...</option>';
            mantagheh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            nahyeh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            if (bakhsh.value) {
                fetch(`/api/dashboard/shahrrosta/${bakhsh.value}/${shahrestan.value}/${ostan.value}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            let option = document.createElement('option');
                            option.value = item;
                            option.textContent = item;
                            shahrRosta.appendChild(option);
                        });
                    });
            }
        });

        // ---------------------------------------------------------------------
        // Get Mantagheh Options
        // ---------------------------------------------------------------------
        shahrRosta.addEventListener('change', function () {
            mantagheh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            nahyeh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            if (shahrRosta.value) {
                fetch(`/api/dashboard/mantagheh/${shahrRosta.value}/${bakhsh.value}/${shahrestan.value}/${ostan.value}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            let option = document.createElement('option');
                            option.value = item;
                            option.textContent = item;
                            mantagheh.appendChild(option);
                        });
                    });
            }
        });

        // ---------------------------------------------------------------------
        // Get Nahyeh Options
        // ---------------------------------------------------------------------
        mantagheh.addEventListener('change', function () {
            nahyeh.innerHTML = '<option value="">انتخاب کنید ...</option>';
            if (mantagheh.value) {
                fetch(`/api/dashboard/nahyeh/${mantagheh.value}/${shahrRosta.value}/${bakhsh.value}/${shahrestan.value}/${ostan.value}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(item => {
                            let option = document.createElement('option');
                            option.value = item;
                            option.textContent = item;
                            nahyeh.appendChild(option);
                        });
                    });
            }
        });

        // ---------------------------------------------------------------------
        // Handle the Change Event
        // ---------------------------------------------------------------------
        // Ostan
        $(document).ready(function () {
            $("#ostan").on("change", function () {
                load_dashboard_data();
                if (shahrRosta.value == "روستایی") {
                    mantagheh.disabled = true;
                    nahyeh.disabled = true;
                } else {
                    mantagheh.disabled = false;
                    nahyeh.disabled = false;
                }
            });
        });

        // Sharestan
        $(document).ready(function () {
            $("#shahrestan").on("change", function () {
                load_dashboard_data();
                if (shahrRosta.value == "روستایی") {
                    mantagheh.disabled = true;
                    nahyeh.disabled = true;
                } else {
                    mantagheh.disabled = false;
                    nahyeh.disabled = false;
                }
            });
        });

        // Bakhsh
        $(document).ready(function () {
            $("#bakhsh").on("change", function () {
                load_dashboard_data();
                if (shahrRosta.value == "روستایی") {
                    mantagheh.disabled = true;
                    nahyeh.disabled = true;
                } else {
                    mantagheh.disabled = false;
                    nahyeh.disabled = false;
                }
            });
        });

        // shahrRosta
        $(document).ready(function () {
            $("#shahrRosta").on("change", function () {
                load_dashboard_data();
                if (shahrRosta.value == "روستایی") {
                    mantagheh.disabled = true;
                    nahyeh.disabled = true;
                } else {
                    mantagheh.disabled = false;
                    nahyeh.disabled = false;
                }
            });
        });

        // mantagheh
        $(document).ready(function () {
            $("#mantagheh").on("change", function () {
                load_dashboard_data();
            });
        });

        // nahyeh
        $(document).ready(function () {
            $("#nahyeh").on("change", function () {
                load_dashboard_data();
            });
        });

    });

    // =========================================================================
    // /Form Control
    // =========================================================================

    // document.getElementById('apply_filter').addEventListener('click', function () {
    //     let citySelect = document.getElementById('city').value;
    //     let regionSelect = document.getElementById('region').value;
    //     let districtSelect = document.getElementById('district').value;
    //     let typeBreadSelect = document.getElementById('typeBread').value;
    //     let typeFlourSelect = document.getElementById('typeFlour').value;
    //     let secondFuelSelect = document.getElementById('secondFuel').value;

    //     if (!citySelect) {
    //         citySelect = "999";
    //     }
    //     if (!regionSelect) {
    //         regionSelect = "999";
    //     }
    //     if (!districtSelect) {
    //         districtSelect = "999";
    //     }
    //     if (!typeBreadSelect) {
    //         typeBreadSelect = "999";
    //     }
    //     if (!typeFlourSelect) {
    //         typeFlourSelect = "999";
    //     }
    //     if (!secondFuelSelect) {
    //         secondFuelSelect = "999";
    //     }

    //     fetch(`/api/dashboard/map/filter/${citySelect}/${regionSelect}/${districtSelect}/${typeBreadSelect}/${typeFlourSelect}/${secondFuelSelect}`)
    //     .then(response => response.json())
    //     .then(data => {
    //         addMarkers(data.data);
    //     });
    // });

    // document.getElementById('clear_filter').addEventListener('click', function () {
    //     document.getElementById('region').innerHTML = '<option value="">منطقه را انتخاب کنید ...</option>';
    //     document.getElementById('district').innerHTML = '<option value="">ناحیه را انتخاب کنید ...</option>';
    //     get_all_data();
    // });

    // load_data();

    // async function load_data() {
    //     const selectedRegion = document.getElementById("selectedRegion").value;
    //     const response = await fetch("/api/dashboard/data/" + selectedRegion);
    //     const data = await response.json();

    //     updateUI(data);
    // }

    // function updateUI(data) {
    //     // Number of Bakers
    //     if (data.number_of_row && data.number_of_row !== undefined) {
    //         document.getElementById("numberBakers").innerHTML =
    //         numberWithCommas(data.number_of_row);
    //     } else {
    //         document.getElementById("numberBakers").innerHTML = "-";
    //     }

    //     // TypeBread
    //     updateTypeBread(data);
    //     // TypeFlour
    //     updateTypeFlour(data);
    //     // BreadRations
    //     updateBreadRations(data);
    //     // BakersRisk
    //     updateBakersRiskChart(data);
    //     // HouseholdRisk
    //     updateHouseholdRiskChart(data);
    //     // RegionInformation
    //     updateRegionInformation(data);
    // }

    // function numberWithCommas(x) {
    //     return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    // }

    // function updateRegionInformation(data) {
    //     document.getElementById('region_info_population').innerHTML = numberWithCommas(data.region_info[0].population);
    //     document.getElementById('region_info_population_male').innerHTML = numberWithCommas(data.region_info[0].population_male);
    //     document.getElementById('region_info_population_female').innerHTML = numberWithCommas(data.region_info[0].population_female);
    //     document.getElementById('region_info_n_households').innerHTML = numberWithCommas(data.region_info[0].n_households);
    //     document.getElementById('region_info_number_bakers').innerHTML = numberWithCommas(data.number_of_row);
    //     document.getElementById('region_info_area').innerHTML = numberWithCommas(data.region_info[0].area);
    //     document.getElementById('region_info_population_bakery_1').innerHTML = numberWithCommas(Math.floor(data.region_info[0].population / data.number_of_row));
    //     document.getElementById('region_info_population_bakery_2').innerHTML = numberWithCommas(Math.floor(data.region_info[0].population / data.number_of_row));
    //     document.getElementById('region_info_area_bakery_1').innerHTML = numberWithCommas(Math.floor(data.region_info[0].area / data.number_of_row));
    //     document.getElementById('region_info_area_bakery_2').innerHTML = numberWithCommas(Math.floor(data.region_info[0].area / data.number_of_row));
    //     document.getElementById('region_info_households_bakery_1').innerHTML = numberWithCommas(Math.floor(data.region_info[0].n_households / data.number_of_row));
    //     document.getElementById('region_info_households_bakery_2').innerHTML = numberWithCommas(Math.floor(data.region_info[0].n_households / data.number_of_row));
    //     document.getElementById('region_info_ration_population_1').innerHTML = numberWithCommas(Math.floor(100 * data.region_bread_rations / data.region_info[0].population));
    //     document.getElementById('region_info_ration_population_2').innerHTML = numberWithCommas(Math.floor(100 * data.region_bread_rations / data.region_info[0].population));
    // }

    // function updateTypeBread(data) {
    //     const breadTypes = ["سنگک", "بربری", "تافتون", "لواش"];
    //     breadTypes.forEach((type, index) => {
    //         const count = data.bread_types_cat[type] || 0;
    //         const tmp = ((count * 100) / (data.number_of_row || 1)).toFixed(0); // avoid division by zero
    //         document.getElementById(
    //             `TypeBread_${String.fromCharCode(65 + index)}_Count`
    //         ).innerHTML = count;
    //         document.getElementById(
    //             `TypeBread_${String.fromCharCode(65 + index)}_Percent`
    //         ).innerHTML = `(${tmp}%)`;
    //         document.getElementById(
    //             `TypeBread_${String.fromCharCode(65 + index)}_Bar`
    //         ).style.width = `${tmp}%`;
    //     });
    // }

    // function updateTypeFlour(data) {
    //     const flourTypes = ["1", "2", "3", "4", "5", "6"];
    //     flourTypes.forEach((type, index) => {
    //         const count = data.flour_types_cat[type] || 0;
    //         const tmp = ((count * 100) / (data.number_of_row || 1)).toFixed(0);
    //         document.getElementById(
    //             `TypeFlour_${String.fromCharCode(65 + index)}_Count`
    //         ).innerHTML = count;
    //         document.getElementById(
    //             `TypeFlour_${String.fromCharCode(65 + index)}_Percent`
    //         ).innerHTML = `(${tmp}%)`;
    //         document.getElementById(
    //             `TypeFlour_${String.fromCharCode(65 + index)}_Bar`
    //         ).style.width = `${tmp}%`;
    //     });
    // }

    // function updateBreadRations(data) {
    //     const rations = ["0", "1", "2", "3", "4", "5"];
    //     rations.forEach((ration, index) => {
    //         const count = data.bread_rations_cat[ration] || 0;
    //         const tmp = ((count * 100) / (data.number_of_row || 1)).toFixed(0);
    //         document.getElementById(
    //             `BreadRations_${String.fromCharCode(65 + index)}_Count`
    //         ).innerHTML = count;
    //         document.getElementById(
    //             `BreadRations_${String.fromCharCode(65 + index)}_Percent`
    //         ).innerHTML = `(${tmp}%)`;
    //         document.getElementById(
    //             `BreadRations_${String.fromCharCode(65 + index)}_Bar`
    //         ).style.width = `${tmp}%`;
    //     });
    // }

    // let bakersRiskChart;
    // let householdRiskBarChart;

    // let ChartConfig = {
    //     chart: {
    //         height: 200,
    //         type: "bar",
    //         toolbar: {
    //             show: false,
    //         },
    //     },
    //     plotOptions: {
    //         bar: {
    //             barHeight: "60%",
    //             columnWidth: "60%",
    //             startingShape: "rounded",
    //             endingShape: "rounded",
    //             borderRadius: 4,
    //             distributed: true,
    //         },
    //     },
    //     grid: {
    //         show: false,
    //         padding: {
    //             top: -20,
    //             bottom: 0,
    //             left: -10,
    //             right: -10,
    //         },
    //     },
    //     colors: [
    //         config.colors.danger,
    //         config.colors_label.primary,
    //         config.colors_label.primary,
    //         config.colors.success,
    //     ],
    //     dataLabels: {
    //         enabled: false,
    //     },
    //     series: [
    //         {
    //             name: "",
    //             data: [],
    //         },
    //     ],
    //     legend: {
    //         show: false,
    //     },
    //     xaxis: {
    //         categories: [],
    //         axisBorder: {
    //             show: false,
    //         },
    //         axisTicks: {
    //             show: false,
    //         },
    //         labels: {
    //             style: {
    //                 colors: config.colors.dark,
    //                 fontSize: "13px",
    //                 fontFamily: "iranyekan",
    //             },
    //         },
    //     },
    //     yaxis: {
    //         labels: {
    //             show: false,
    //         },
    //     },
    //     tooltip: {
    //         enabled: false,
    //     },
    //     dataLabels: {
    //         enabled: true,
    //         formatter: function (val) {
    //             return val;
    //         },
    //         offsetY: 0,
    //         style: {
    //             fontSize: "16px",
    //             fontFamily: "iranyekan",
    //             colors: ["#000"],
    //         },
    //     },
    // };

    // function initBakersRiskChart() {
    //   bakersRiskChart = new ApexCharts(
    //         document.querySelector("#bakersRiskBarChart"),
    //         ChartConfig
    //     );
    //     bakersRiskChart.render();
    // }

    // function initHouseholdRiskChart() {
    //     householdRiskBarChart = new ApexCharts(
    //         document.querySelector("#householdRiskBarChart"),
    //         ChartConfig
    //     );
    //     householdRiskBarChart.render();
    // }

    // function updateBakersRiskChart(data) {
    //     const sortedDataBakersRisk = Object.entries(data.bakers_risk_cat).sort(
    //         (a, b) => b[1] - a[1]
    //     );

    //     bakersRiskChart.updateOptions({
    //         series: [
    //             {
    //                 name: "ریسک نانوا",
    //                 data: sortedDataBakersRisk.map((item) => item[1]),
    //             },
    //         ],
    //         xaxis: {
    //             categories: sortedDataBakersRisk.map((item) => item[0]),
    //         },
    //     });
    // }

    // function updateHouseholdRiskChart(data) {
    //     const sortedDataHouseholdRisk = Object.entries(
    //         data.household_risk_cat
    //     ).sort((a, b) => b[1] - a[1]);

    //     householdRiskBarChart.updateOptions({
    //         series: [
    //             {
    //                 name: "ریسک خانوار",
    //                 data: sortedDataHouseholdRisk.map((item) => item[1]),
    //             },
    //         ],
    //         xaxis: {
    //             categories: sortedDataHouseholdRisk.map((item) => item[0]),
    //         },
    //     });
    // }

    // initBakersRiskChart();
    // initHouseholdRiskChart();


})();
