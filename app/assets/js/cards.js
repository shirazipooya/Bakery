// Maps Leaflet

"use strict";

(function () {
  // Get All Data From `/get_all_data`

  get_all_data();

  async function get_all_data() {
    const response = await fetch("/get_all_data");
    const data = await response.json(); 
    
    // Number of Bakers
    if (data.number_of_row && data.number_of_row !== undefined) {
        document.getElementById("numberBakers").innerHTML =
          data.number_of_row;
      } else {
        document.getElementById("numberBakers").innerHTML = "-";
      }


    // TypeBread

    if (data.type_bread_cat && data.type_bread_cat["سنگک"] !== undefined) {
      var tmp = (
        (data.type_bread_cat["سنگک"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("TypeBread_A_Count").innerHTML =
        data.type_bread_cat["سنگک"];
      document.getElementById("TypeBread_A_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("TypeBread_A_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("TypeBread_A_Count").innerHTML = "-";
      document.getElementById("TypeBread_A_Percent").innerHTML = "(0%)";
      document.getElementById("TypeBread_A_Bar").style.width = "0%";
    }

    if (data.type_bread_cat && data.type_bread_cat["بربری"] !== undefined) {
      var tmp = (
        (data.type_bread_cat["بربری"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("TypeBread_B_Count").innerHTML =
        data.type_bread_cat["بربری"];
      document.getElementById("TypeBread_B_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("TypeBread_B_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("TypeBread_B_Count").innerHTML = "-";
      document.getElementById("TypeBread_B_Percent").innerHTML = "(0%)";
      document.getElementById("TypeBread_B_Bar").style.width = "0%";
    }

    if (data.type_bread_cat && data.type_bread_cat["تافتون"] !== undefined) {
      var tmp = (
        (data.type_bread_cat["تافتون"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("TypeBread_C_Count").innerHTML =
        data.type_bread_cat["تافتون"];
      document.getElementById("TypeBread_C_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("TypeBread_C_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("TypeBread_C_Count").innerHTML = "-";
      document.getElementById("TypeBread_C_Percent").innerHTML = "(0%)";
      document.getElementById("TypeBread_C_Bar").style.width = "0%";
    }

    if (data.type_bread_cat && data.type_bread_cat["لواش"] !== undefined) {
      var tmp = (
        (data.type_bread_cat["لواش"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("TypeBread_D_Count").innerHTML =
        data.type_bread_cat["لواش"];
      document.getElementById("TypeBread_D_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("TypeBread_D_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("TypeBread_D_Count").innerHTML = "-";
      document.getElementById("TypeBread_D_Percent").innerHTML = "(0%)";
      document.getElementById("TypeBread_D_Bar").style.width = "0%";
    }

    // TypeFlour

    if (data.type_flour_cat && data.type_flour_cat["1"] !== undefined) {
      var tmp = ((data.type_flour_cat["1"] * 100) / data.number_of_row).toFixed(
        0
      );
      document.getElementById("TypeFlour_A_Count").innerHTML =
        data.type_flour_cat["1"];
      document.getElementById("TypeFlour_A_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("TypeFlour_A_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("TypeFlour_A_Count").innerHTML = "-";
      document.getElementById("TypeFlour_A_Percent").innerHTML = "(0%)";
      document.getElementById("TypeFlour_A_Bar").style.width = "0%";
    }

    if (data.type_flour_cat && data.type_flour_cat["2"] !== undefined) {
      var tmp = ((data.type_flour_cat["2"] * 100) / data.number_of_row).toFixed(
        0
      );
      document.getElementById("TypeFlour_B_Count").innerHTML =
        data.type_flour_cat["2"];
      document.getElementById("TypeFlour_B_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("TypeFlour_B_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("TypeFlour_B_Count").innerHTML = "-";
      document.getElementById("TypeFlour_B_Percent").innerHTML = "(0%)";
      document.getElementById("TypeFlour_B_Bar").style.width = "0%";
    }

    if (data.type_flour_cat && data.type_flour_cat["3"] !== undefined) {
      var tmp = ((data.type_flour_cat["3"] * 100) / data.number_of_row).toFixed(
        0
      );
      document.getElementById("TypeFlour_C_Count").innerHTML =
        data.type_flour_cat["3"];
      document.getElementById("TypeFlour_C_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("TypeFlour_C_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("TypeFlour_C_Count").innerHTML = "-";
      document.getElementById("TypeFlour_C_Percent").innerHTML = "(0%)";
      document.getElementById("TypeFlour_C_Bar").style.width = "0%";
    }

    if (data.type_flour_cat && data.type_flour_cat["4"] !== undefined) {
      var tmp = ((data.type_flour_cat["4"] * 100) / data.number_of_row).toFixed(
        0
      );
      document.getElementById("TypeFlour_D_Count").innerHTML =
        data.type_flour_cat["4"];
      document.getElementById("TypeFlour_D_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("TypeFlour_D_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("TypeFlour_D_Count").innerHTML = "-";
      document.getElementById("TypeFlour_D_Percent").innerHTML = "(0%)";
      document.getElementById("TypeFlour_D_Bar").style.width = "0%";
    }

    if (data.type_flour_cat && data.type_flour_cat["5"] !== undefined) {
      var tmp = ((data.type_flour_cat["5"] * 100) / data.number_of_row).toFixed(
        0
      );
      document.getElementById("TypeFlour_E_Count").innerHTML =
        data.type_flour_cat["5"];
      document.getElementById("TypeFlour_E_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("TypeFlour_E_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("TypeFlour_E_Count").innerHTML = "-";
      document.getElementById("TypeFlour_E_Percent").innerHTML = "(0%)";
      document.getElementById("TypeFlour_E_Bar").style.width = "0%";
    }

    if (data.type_flour_cat && data.type_flour_cat["6"] !== undefined) {
      var tmp = ((data.type_flour_cat["6"] * 100) / data.number_of_row).toFixed(
        0
      );
      document.getElementById("TypeFlour_F_Count").innerHTML =
        data.type_flour_cat["6"];
      document.getElementById("TypeFlour_F_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("TypeFlour_F_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("TypeFlour_F_Count").innerHTML = "-";
      document.getElementById("TypeFlour_F_Percent").innerHTML = "(0%)";
      document.getElementById("TypeFlour_F_Bar").style.width = "0%";
    }

    // BreadRations

    if (data.bread_rations_cat && data.bread_rations_cat["50"] !== undefined) {
      var tmp = (
        (data.bread_rations_cat["50"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("BreadRations_A_Count").innerHTML =
        data.bread_rations_cat["50"];
      document.getElementById("BreadRations_A_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("BreadRations_A_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("BreadRations_A_Count").innerHTML = "-";
      document.getElementById("BreadRations_A_Percent").innerHTML = "(0%)";
      document.getElementById("BreadRations_A_Bar").style.width = "0%";
    }

    if (data.bread_rations_cat && data.bread_rations_cat["100"] !== undefined) {
      var tmp = (
        (data.bread_rations_cat["100"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("BreadRations_B_Count").innerHTML =
        data.bread_rations_cat["100"];
      document.getElementById("BreadRations_B_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("BreadRations_B_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("BreadRations_B_Count").innerHTML = "-";
      document.getElementById("BreadRations_B_Percent").innerHTML = "(0%)";
      document.getElementById("BreadRations_B_Bar").style.width = "0%";
    }

    if (data.bread_rations_cat && data.bread_rations_cat["150"] !== undefined) {
      var tmp = (
        (data.bread_rations_cat["150"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("BreadRations_C_Count").innerHTML =
        data.bread_rations_cat["150"];
      document.getElementById("BreadRations_C_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("BreadRations_C_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("BreadRations_C_Count").innerHTML = "-";
      document.getElementById("BreadRations_C_Percent").innerHTML = "(0%)";
      document.getElementById("BreadRations_C_Bar").style.width = "0%";
    }

    if (data.bread_rations_cat && data.bread_rations_cat["200"] !== undefined) {
      var tmp = (
        (data.bread_rations_cat["200"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("BreadRations_D_Count").innerHTML =
        data.bread_rations_cat["200"];
      document.getElementById("BreadRations_D_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("BreadRations_D_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("BreadRations_D_Count").innerHTML = "-";
      document.getElementById("BreadRations_D_Percent").innerHTML = "(0%)";
      document.getElementById("BreadRations_D_Bar").style.width = "0%";
    }

    if (data.bread_rations_cat && data.bread_rations_cat["250"] !== undefined) {
      var tmp = (
        (data.bread_rations_cat["250"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("BreadRations_E_Count").innerHTML =
        data.bread_rations_cat["250"];
      document.getElementById("BreadRations_E_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("BreadRations_E_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("BreadRations_E_Count").innerHTML = "-";
      document.getElementById("BreadRations_E_Percent").innerHTML = "(0%)";
      document.getElementById("BreadRations_E_Bar").style.width = "0%";
    }

    if (data.bread_rations_cat && data.bread_rations_cat["300"] !== undefined) {
      var tmp = (
        (data.bread_rations_cat["300"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("BreadRations_F_Count").innerHTML =
        data.bread_rations_cat["300"];
      document.getElementById("BreadRations_F_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("BreadRations_F_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("BreadRations_F_Count").innerHTML = "-";
      document.getElementById("BreadRations_F_Percent").innerHTML = "(0%)";
      document.getElementById("BreadRations_F_Bar").style.width = "0%";
    }

    if (data.bread_rations_cat && data.bread_rations_cat["350"] !== undefined) {
      var tmp = (
        (data.bread_rations_cat["350"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("BreadRations_G_Count").innerHTML =
        data.bread_rations_cat["350"];
      document.getElementById("BreadRations_G_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("BreadRations_G_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("BreadRations_G_Count").innerHTML = "-";
      document.getElementById("BreadRations_G_Percent").innerHTML = "(0%)";
      document.getElementById("BreadRations_G_Bar").style.width = "0%";
    }

    if (data.bread_rations_cat && data.bread_rations_cat["400"] !== undefined) {
      var tmp = (
        (data.bread_rations_cat["400"] * 100) /
        data.number_of_row
      ).toFixed(0);
      document.getElementById("BreadRations_H_Count").innerHTML =
        data.bread_rations_cat["400"];
      document.getElementById("BreadRations_H_Percent").innerHTML = `(${tmp}%)`;
      document.getElementById("BreadRations_H_Bar").style.width = `${tmp}%`;
    } else {
      document.getElementById("BreadRations_H_Count").innerHTML = "-";
      document.getElementById("BreadRations_H_Percent").innerHTML = "(0%)";
      document.getElementById("BreadRations_H_Bar").style.width = "0%";
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



    // HouseholdRisk

    const sortedDataHouseholdRisk = Object.entries(data.household_risk_cat)
            .sort((a, b) => b[1] - a[1]);

    const householdRiskBarChartConfig = {
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
          name: "ریسک خانوار",
        //   data: Object.values(data.household_risk_cat),
          data: sortedDataHouseholdRisk.map(item => item[1]),
        },
      ],
      legend: {
        show: false,
      },
      xaxis: {
        // categories: Object.keys(data.household_risk_cat),
        categories: sortedDataHouseholdRisk.map(item => item[0]),
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

    const householdRiskBarChart = new ApexCharts(
        document.querySelector("#householdRiskBarChart"),
        householdRiskBarChartConfig
    );

    householdRiskBarChart.render();


  }
})();
