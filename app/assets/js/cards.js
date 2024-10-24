"use strict";

(function () {
    load_data();

    async function load_data() {
        const selectedRegion = document.getElementById("selectedRegion").value;
        const response = await fetch("/api/dashboard/data/" + selectedRegion);
        const data = await response.json();
        updateUI(data);
    }

    function updateUI(data) {
        // Number of Bakers
        if (data.number_of_row && data.number_of_row !== undefined) {
            document.getElementById("numberBakers").innerHTML =
                data.number_of_row;
        } else {
            document.getElementById("numberBakers").innerHTML = "-";
        }

        // TypeBread
        updateTypeBread(data);
        // TypeFlour
        updateTypeFlour(data);
        // BreadRations
        updateBreadRations(data);
        // BakersRisk
        updateBakersRiskChart(data);
        // HouseholdRisk
        updateHouseholdRiskChart(data);
    }

    function updateTypeBread(data) {
        const breadTypes = ["سنگک", "بربری", "تافتون", "لواش"];
        breadTypes.forEach((type, index) => {
            const count = data.type_bread_cat[type] || 0;
            const tmp = ((count * 100) / (data.number_of_row || 1)).toFixed(0); // avoid division by zero
            document.getElementById(
                `TypeBread_${String.fromCharCode(65 + index)}_Count`
            ).innerHTML = count;
            document.getElementById(
                `TypeBread_${String.fromCharCode(65 + index)}_Percent`
            ).innerHTML = `(${tmp}%)`;
            document.getElementById(
                `TypeBread_${String.fromCharCode(65 + index)}_Bar`
            ).style.width = `${tmp}%`;
        });
    }

    function updateTypeFlour(data) {
        const flourTypes = ["1", "2", "3", "4", "5", "6"];
        flourTypes.forEach((type, index) => {
            const count = data.type_flour_cat[type] || 0;
            const tmp = ((count * 100) / (data.number_of_row || 1)).toFixed(0);
            document.getElementById(
                `TypeFlour_${String.fromCharCode(65 + index)}_Count`
            ).innerHTML = count;
            document.getElementById(
                `TypeFlour_${String.fromCharCode(65 + index)}_Percent`
            ).innerHTML = `(${tmp}%)`;
            document.getElementById(
                `TypeFlour_${String.fromCharCode(65 + index)}_Bar`
            ).style.width = `${tmp}%`;
        });
    }

    function updateBreadRations(data) {
        const rations = ["0", "1", "2", "3", "4", "5"];
        rations.forEach((ration, index) => {
            const count = data.bread_rations_cat[ration] || 0;
            const tmp = ((count * 100) / (data.number_of_row || 1)).toFixed(0);
            document.getElementById(
                `BreadRations_${String.fromCharCode(65 + index)}_Count`
            ).innerHTML = count;
            document.getElementById(
                `BreadRations_${String.fromCharCode(65 + index)}_Percent`
            ).innerHTML = `(${tmp}%)`;
            document.getElementById(
                `BreadRations_${String.fromCharCode(65 + index)}_Bar`
            ).style.width = `${tmp}%`;
        });
    }

    let bakersRiskChart;
    let householdRiskBarChart;

    let ChartConfig = {
        chart: {
            height: 200,
            type: "bar",
            toolbar: {
                show: false,
            },
        },
        plotOptions: {
            bar: {
                barHeight: "60%",
                columnWidth: "60%",
                startingShape: "rounded",
                endingShape: "rounded",
                borderRadius: 4,
                distributed: true,
            },
        },
        grid: {
            show: false,
            padding: {
                top: -20,
                bottom: 0,
                left: -10,
                right: -10,
            },
        },
        colors: [
            config.colors.danger,
            config.colors_label.primary,
            config.colors_label.primary,
            config.colors.success,
        ],
        dataLabels: {
            enabled: false,
        },
        series: [
            {
                name: "",
                data: [],
            },
        ],
        legend: {
            show: false,
        },
        xaxis: {
            categories: [],
            axisBorder: {
                show: false,
            },
            axisTicks: {
                show: false,
            },
            labels: {
                style: {
                    colors: config.colors.dark,
                    fontSize: "13px",
                    fontFamily: "iranyekan",
                },
            },
        },
        yaxis: {
            labels: {
                show: false,
            },
        },
        tooltip: {
            enabled: false,
        },
        dataLabels: {
            enabled: true,
            formatter: function (val) {
                return val;
            },
            offsetY: 0,
            style: {
                fontSize: "16px",
                fontFamily: "iranyekan",
                colors: ["#000"],
            },
        },
    };

    function initBakersRiskChart() {
      bakersRiskChart = new ApexCharts(
            document.querySelector("#bakersRiskBarChart"),
            ChartConfig
        );
        bakersRiskChart.render();
    }

    function initHouseholdRiskChart() {
        householdRiskBarChart = new ApexCharts(
            document.querySelector("#householdRiskBarChart"),
            ChartConfig
        );
        householdRiskBarChart.render();
    }

    function updateBakersRiskChart(data) {
        const sortedDataBakersRisk = Object.entries(data.bakers_risk_cat).sort(
            (a, b) => b[1] - a[1]
        );

        bakersRiskChart.updateOptions({
            series: [
                {
                    name: "ریسک نانوا",
                    data: sortedDataBakersRisk.map((item) => item[1]),
                },
            ],
            xaxis: {
                categories: sortedDataBakersRisk.map((item) => item[0]),
            },
        });
    }

    function updateHouseholdRiskChart(data) {
        const sortedDataHouseholdRisk = Object.entries(
            data.household_risk_cat
        ).sort((a, b) => b[1] - a[1]);

        householdRiskBarChart.updateOptions({
            series: [
                {
                    name: "ریسک خانوار",
                    data: sortedDataHouseholdRisk.map((item) => item[1]),
                },
            ],
            xaxis: {
                categories: sortedDataHouseholdRisk.map((item) => item[0]),
            },
        });
    }

    initBakersRiskChart();
    initHouseholdRiskChart();

    $(document).ready(function () {
        $(".select2").select2({
            placeholder: "منطقه را انتخاب کنید ...",
        });

        $("#selectedRegion").on("change", function () {
            load_data();
        });
    });
})();
