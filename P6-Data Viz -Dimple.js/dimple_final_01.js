"use strict";
// Getting the data
d3.csv("airline_dimple_01.csv",
  // Formatting the column names for better readability
  function(d) {
  var format = d3.time.format("%Y");
  return {
    'Year': format.parse(d.year),
    'Carrier Name': d.carrier_name,
    'On Time': +d.on_time,
    'Arrivals': +d.arrivals,
    'Carrier Delay': +d.carrier_delay,
    'Weather Delay': +d.wthr_delay,
    'NAS Delay': +d.ns_delay,
    'Security Delay': +d.sec_delay,
    'Late Aircraft Delay': +d.lt_air_delay,
  };
},

// Creating the canvas, Setting up the axis & drawing the chart
function(data) {

//**  ***************************** On Time Percentage *********************************** **//
      /*
        D3.js setup code
      */

      // Adding a header title to the graph by selecting the selction tag using #id
          d3.select('#content_02')
          .append('h3')
          .attr('id', 'title')
          .text('On Time Arrivals Performance of U.S. Airlines, 2003 - 2017');

          // Setting margin, height & width value
          var margin = 50,
              width = 1000 - margin,
              height = 500 - margin;

          // Constructing the canvas
          var svg = d3.select("#content_02")
          .append("svg")
          .attr("width", width + margin)
          .attr("height", height + margin)
          .append('g')
          .attr('class','chart');

      /*
        Dimple.js Chart construction code
      */
          // Setting limit for y axis, by providing the minimum and maximum values
          var y_min = 0.70;
          var y_max = 0.90;
          
          // Chart Contruction
          var myChart = new dimple.chart(svg, data);
          var x = myChart.addTimeAxis("x", "Year"); 
          var y = myChart.addMeasureAxis('y', 'On Time');

          // Formatting x-axis to year format
          x.tickFormat = '%Y';

          // Setting x-axis interval to 1 year
          x.timeInterval = 1;

          // Formatting y-axis to Percentage format
          y.tickFormat = '%';

          // Overriding y-minimum & maximum values
          y.overrideMin = y_min;
          y.overrideMax = y_max;

          // Drawing the graph
          myChart.addSeries('Carrier Name', dimple.plot.scatter);
          myChart.addSeries('Carrier Name', dimple.plot.line);
          myChart.addLegend(width*0.95, height*0.8, 50, 70, "right");

          // Drawing the graph
          myChart.draw();

          // handle mouse events on gridlines
          y.gridlineShapes.selectAll('line')
          .style('opacity', 0.25)
          .on('mouseover', function(e) {
                d3.select(this)
                .style('opacity', 1);
                }).on('mouseleave', function(e) {
                  d3.select(this)
                  .style('opacity', 0.25);
                  });

          // handle mouse events on paths
          d3.selectAll('path')
          .style('opacity', 0.25)
          .on('mouseover', function(e) {
            d3.select(this)
              .style('stroke-width', '8px')
              .style('opacity', 1)
              .attr('z-index', '1');
        }).on('mouseleave', function(e) {
            d3.select(this)
              .style('stroke-width', '2px')
              .style('opacity', 0.25)
              .attr('z-index', '0');
        });

      });