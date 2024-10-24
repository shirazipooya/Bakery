"use strict";



(function () {

  load_data();

  async function load_data() {
    const selectedRegion = document.getElementById("selectedRegion").value;
    const response = await fetch("/api/dashboard/data/" + selectedRegion);
    const data = await response.json(); 
    
    // Number of Bakers
    if (data.number_of_row && data.number_of_row !== undefined) {
        document.getElementById("numberBakers").innerHTML =
          data.number_of_row;
      } else {
        document.getElementById("numberBakers").innerHTML = "-";
      }


    // BakersRisk

    const sortedDataBakersRisk = Object.entries(data.bakers_risk_cat)
    .sort((a, b) => b[1] - a[1]);

    const bakersRiskBarChartConfig = {
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
          name: "ریسک نانوا",
          data: sortedDataBakersRisk.map(item => item[1]),
        },
      ],
      legend: {
        show: false,
      },
      xaxis: {
        categories: sortedDataBakersRisk.map(item => item[0]),
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

    const barChart = new ApexCharts(
        document.querySelector("#bakersRiskBarChart"),
        bakersRiskBarChartConfig
    );

    barChart.render();


  }

  function selectFirstOption() {
    var dropdown = document.getElementById("selectedRegion");
    dropdown.selectedIndex = 0;
    load_data();
  }
  document.addEventListener("DOMContentLoaded", selectFirstOption);

})();
