window.addEventListener("DOMContentLoaded", () => {
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top'
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Position (m)'
        },
        ticks: {
          callback: function(value, index, ticks) {
            const label = this.getLabelForValue(value);
            return parseFloat(label).toFixed(2);
          }
        }
      },
      y: {
        title: {
          display: true,
          text: ''  
        }
      }
    }
  };

  // ✅ Shear Force Diagram (SFD)
  if (typeof xData !== "undefined" && typeof vData !== "undefined") {
    const shearCanvas = document.getElementById("sfdChart");
    if (shearCanvas) {
      new Chart(shearCanvas.getContext("2d"), {
        type: "line",
        data: {
          labels: xData,
          datasets: [{
            label: "Shear Force (kN)",
            data: vData,
            borderColor: "rgba(255, 99, 132, 1)",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            fill: true,
            tension: 0
          }]
        },
        options: {
          ...chartOptions,
          plugins: {
            ...chartOptions.plugins,
            title: {
              display: true,
              text: "Shear Force Diagram (SFD)"
            }
          },
          scales: {
            ...chartOptions.scales,
            y: {
              title: {
                display: true,
                text: "Shear Force (kN)"
              }
            }
          }
        }
      });
    }
  }

  // ✅ Bending Moment Diagram (BMD)
  if (typeof xData !== "undefined" && typeof mData !== "undefined") {
    const momentCanvas = document.getElementById("bmdChart");
    if (momentCanvas) {
      new Chart(momentCanvas.getContext("2d"), {
        type: "line",
        data: {
          labels: xData,
          datasets: [{
            label: "Bending Moment (kN·m)",
            data: mData,
            borderColor: "rgba(54, 162, 235, 1)",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            fill: true,
            tension: 0.2
          }]
        },
        options: {
          ...chartOptions,
          plugins: {
            ...chartOptions.plugins,
            title: {
              display: true,
              text: "Bending Moment Diagram (BMD)"
            }
          },
          scales: {
            ...chartOptions.scales,
            y: {
              title: {
                display: true,
                text: "Bending Moment (kN·m)"
              }
            }
          }
        }
      });
    }
  }

  // ✅ Deflection Diagram
  if (typeof xData !== "undefined" && typeof deflection_vals !== "undefined" && deflection_vals.length > 0) {
    const deflectionCanvas = document.getElementById("deflectionChart");
    if (deflectionCanvas) {
      new Chart(deflectionCanvas.getContext("2d"), {
        type: "line",
        data: {
          labels: xData,
          datasets: [{
            label: "Deflection (mm)",
            data: deflection_vals,
            borderColor: "rgba(255, 206, 86, 1)",
            backgroundColor: "rgba(255, 206, 86, 0.2)",
            fill: true,
            tension: 0.3
          }]
        },
        options: {
          ...chartOptions,
          plugins: {
            ...chartOptions.plugins,
            title: {
              display: true,
              text: "Deflection Diagram"
            }
          },
          scales: {
            ...chartOptions.scales,
            y: {
              title: {
                display: true,
                text: "Deflection (mm)"
              },
              reverse: true  
            }
          }
        }
      });
    }
  }
});

  // ✅ Stress Distribution Chart
  // if (typeof stress_profile !== "undefined" && stress_profile.depths && stress_profile.stresses) {
  //   const ctx = document.getElementById("stressChart").getContext("2d");

  //   new Chart(ctx, {
  //     type: "line",
  //     data: {
  //       labels: stress_profile.depths.map(d => `${d.toFixed(0)} mm`),
  //       datasets: [{
  //         label: "Stress (MPa)",
  //         data: stress_profile.stresses,
  //         backgroundColor: "rgba(153, 102, 255, 0.2)",
  //         borderColor: "rgba(153, 102, 255, 1)",
  //         borderWidth: 2,
  //         pointRadius: 3,
  //         tension: 0.3,
  //         fill: true
  //       }]
  //     },
  //     options: {
  //       responsive: true,
  //       maintainAspectRatio: false,
  //       indexAxis: 'y',  // Vertical layout
  //       plugins: {
  //         title: {
  //           display: true,
  //           text: "Stress Distribution in Beam Cross Section"
  //         },
  //         legend: {
  //           display: false
  //         }
  //       },
  //       scales: {
  //         x: {
  //           title: {
  //             display: true,
  //             text: "Stress (MPa)"
  //           }
  //         },
  //         y: {
  //           title: {
  //             display: true,
  //             text: "Depth from Top (mm)"
  //           },
  //           reverse: true
  //         }
  //       }
  //     }
  //   });
  // }
