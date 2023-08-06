class LodTabController{
    /** Creates the controller of the Length-of-Day tab
     *
     * @param {mainController} mainController - The main controller of the page
     */
    constructor(mainController){
        console.log("Building LodTabController...");

        this.mc = mainController;
        this.lodSelector = null;
        this.lodData = new LodData();
        this.chartSeries = [];
    }

    /**
     * Initiates the chart with proper options. Called in documentReady.
     * */
    initChart() {
        this.chart = Highcharts.chart('lodplotdiv', {
            chart: {
                zoomType: 'xy',
                animation: false,
            },
            title: {
              text: "Length-of-day variation",
              useHTML: true
            },
            credits: {
                enabled: false
            },
            xAxis: {
                title: {
                    text: "Years",
                    style: {
                      "fontSize":"1rem",
                    },
                },
                labels: {
                  style: {
                    "fontSize":"1rem",
                  },
                },
                tickInterval: 1,
            },
            yAxis: {
                title: {
                    text: "LOD variation (ms)",
                    // If useHTML set to true, the label is not rotated on export (https://github.com/highcharts/highcharts/issues/5393)
                    useHTML: false,
                    rotation: 270,
                    style: {
                      "fontSize":"1rem",
                    },
                },
                labels: {
                  style: {
                    "fontSize":"1rem",
                  },
                },
            },
            tooltip: {
                enabled: true,
            },
            series: this.chartSeries,
            legend: {
              useHTML: true,
              itemStyle: {
                  "fontSize":"0.9rem",
                  "fontWeight": "normal",
                  "line-height" : "1.3rem"
              },
              verticalAlign: 'top',
              align: 'right',
              layout: 'vertical',
              symbolWidth: 32,
              x:-32,
              y:50,
              itemMarginTop:3,
              itemMarginBottom:3,
            },
            exporting: {
              fallbackToExportServer: true,
              allowHTML: true,
              sourceWidth : $('#lodplotdiv').innerWidth(),
              sourceHeight : $('#lodplotdiv').innerHeight(),
              buttons: {
                contextButton: {
                  menuItems: ['downloadPNG',
                              'downloadJPEG',
                              'downloadPDF',
                              'downloadSVG',
                              'separator',
                              'downloadCSV']
                }
              }
            },
        });
    }

    /** Clears the chart */
    clearChart() {
        const thisLTC = this;
        if (thisLTC.isChartClear) {return;}
            thisLTC.isChartClear = true;
            while (thisLTC.chart.series.length > 0) {
                thisLTC.chart.series[0].remove();
            }
            thisLTC.chart.title.update({'text': 'Please select a model'});
            thisLTC.chart.zoom();
            thisLTC.chart.redraw();
    }

    /**
     * Updates the chart with the series stored in chartSeries. Also update the title and axis labels.
     */
    updateChart()
     {
        const thisLTC = this;

        this.clearChart();
        this.isChartClear = false;
        for (let serie of thisLTC.chartSeries) {
            thisLTC.chart.addSeries(serie);
        }
        thisLTC.chart.title.update({'text': 'Length-of-day variation'});
        this.chart.reflow();
        thisLTC.chart.exporting.update({filename: thisLTC.chart.title.textStr.replace(/<.*?>/g, "")});
    }

    /**
     * Updated the exporting dimensions of the chart. Called by mainController when the window is resized
     * */
    onResize(){
        let lodPlotDiv = $('#lodplotdiv');
        // Update export size
        this.chart.options.exporting.sourceWidth = lodPlotDiv.innerWidth();
        this.chart.options.exporting.sourceHeight = lodPlotDiv.innerHeight();
        // Resize chart according to container size
        this.chart.reflow();
    }

    /**
     * Initialises the modelSelector. Called in documentReady.
     */
    initLodData() {
        console.log('initLodData');
        const thisLTC = this;

        //Clear option div and chart
        let optionDiv = $('.menuoptionsdiv');
        $('.optionscontainer').show();
        optionDiv.empty();
        thisLTC.clearChart();

        // Create a div for the modelSelector
        let $selectorDiv = $("<div>")
            .addClass("ui segment _flexfixedsize")
            .css("margin","0.5rem 0!important;")
            .attr('id','selector_div');
        $selectorDiv.appendTo(optionDiv);

        this.lodSelector = new ModelSelector(
            {
                data: thisLTC.mc.datalist,
                measure: "LOD",
                showremovemean: true,
                parentDiv: $selectorDiv,
                title: "Select data",
                onChangeData: function () {
                    thisLTC.clearChart();
                    if (this.config.selectedData.length === 0) {
                        return;
                    }
                    thisLTC.getLodData().then(function (data) {
                        for (let modelName in data) {
                            if(modelName === 'SUCCESS' || modelName === 'ERROR') {
                                continue;
                            }
                            thisLTC.toHighchartSeries(data[modelName], modelName);
                        }
                        thisLTC.updateChart();
                    });
                }
            });
    }

    /**
     * Requests the LOD data from the server with parameters from the selector.
     *
     * @returns {Promise<JSON>} The Promise from LodData.
     */
    getLodData() {
        const thisLTC = this;
        let removemean = this.lodSelector.config.removemean;

        thisLTC.chartSeries = [];
        return thisLTC.lodData.getData(thisLTC.lodSelector.config.selectedData, removemean)
    }

    /**
     * Convert the lodSeries (mean + RMS) in Highchart Series that are then appended to the chart.
     *
     * @param {Object} lodSeries - Object containing the time series of LOD for a model
     * @param {number[]} lodSeries.times - Array of LOD times
     * @param {number[]} lodSeries.data - Array of LOD mean data
     * @param {number[]} lodSeries.rmsdata - Array of LOD rms data
     * @param {string} modelName - Name of the model
     */
    toHighchartSeries(lodSeries, modelName) {
        const thisLTC = this;

        console.log("RECEIVED LodData", lodSeries);
        let linedata = [];
        let areadata = [];

        for (let itime in lodSeries.times) {
            linedata.push([lodSeries.times[itime], lodSeries.data[itime]]);
            areadata.push([lodSeries.times[itime],
                lodSeries.data[itime] - lodSeries.rmsdata[itime],
                lodSeries.data[itime] + lodSeries.rmsdata[itime]
            ]);
        }

        this.chartSeries.push({
            allowPointSelect: true,
            name: modelName + " - LOD",
            data: linedata, // [[x,y],[x,y]...]
            animation: false,
            color: thisLTC.mc.datalist[modelName].color,
            zIndex: 1,
            marker: {
                enabled: false,
            },

            lineWidth: 2.5,
            fillOpacity: 0.8,
        });
        this.chartSeries.push({
            allowPointSelect: false,
            enableMouseTracking: false,
            name: "&plusmn;RMS" + modelName + " - LOD",
            data: areadata,// [[x,y-,y+],[x,y-,y+],...]
            type: 'arearange',
            lineWidth: 0,
            linkedTo: ':previous',
            color: this.mc.datalist[modelName].color,
            fillOpacity: 0.2,
            animation: false,
            zIndex: 0,
            marker: {
                enabled: false
            },
        });
    }

    /**
     * Initiates the chart and the LOD option divs (in that order).
     */
    documentReady() {
        this.initChart();
        this.initLodData();
    }

}