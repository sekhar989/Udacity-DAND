d3.csv("airline_dimple_01.csv",
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
function(data) {

//**  ***************************** Carrier Delay *********************************** **//
"use strict";
          // Set the dimensions of the canvas / graph
          var margin_01 = {top: 5, right: 1, bottom: 5, left: 1},
          width_01 = 600 - margin_01.left - margin_01.right,
          height_01 = 500 - margin_01.top - margin_01.bottom;
          
          // d3.select('#content_01')
          // .append('h3')
          // .attr('id', 'title')
          // .text('U.S. Airlines Delay (Carrier)');

          // Adds the svg canvas
          var chart_01 = d3.select("#content_01")
          .append("svg")
          .attr("width", width_01 + margin_01.left + margin_01.right)
          .attr("height", height_01 + margin_01.top + margin_01.bottom)
          .append("g")
          .attr("transform", "translate(" + margin_01.left + "," + margin_01.top + ")");

      /*Dimple.js Chart construction code*/          
          var y_min = 0;
          var y_max = 0.6;
          
          var myChart = new dimple.chart(chart_01, data);
          var x = myChart.addTimeAxis("x", "Year"); 
          // var x = myChart.addTimeAxis("x", "year"); 
          var y = myChart.addMeasureAxis('y', 'Carrier Delay');
          // var y = myChart.addMeasureAxis('y', 'on_time');

          // x.dateParseFormat = "%Y"
          x.tickFormat = '%Y';
          x.timeInterval = 1;
          // x.title = 'Year';

          y.tickFormat = '%';
          y.overrideMin = y_min;
          y.overrideMax = y_max;
          // y.title = 'On Time';

          myChart.addSeries('Carrier Name', dimple.plot.line);
          myChart.addSeries('Carrier Name', dimple.plot.scatter);
          myChart.addLegend(width_01*0.95, height_01*0.075, 50, 80, "right");
          // myChart.addSeries('carrier_name', dimple.plot.line);
          // myChart.addSeries('carrier_name', dimple.plot.scatter);
          myChart.draw();

//**  ***************************** Weather Delay *********************************** **//

          // d3.select('#content_02')
          // .append('h3')
          // .attr('id', 'title')
          // .text('U.S. Airlines Delay (Weather)');

          // Adds the svg canvas
          var chart_02 = d3.select("#content_02")
          .append("svg")
          .attr("width", width_01 + margin_01.left + margin_01.right)
          .attr("height", height_01 + margin_01.top + margin_01.bottom)
          .append("g")
          .attr("transform", "translate(" + margin_01.left + "," + margin_01.top + ")");

      /*Dimple.js Chart construction code*/          
          var y_min = 0;
          var y_max = 0.25;
          
          var myChart = new dimple.chart(chart_02, data);
          var x = myChart.addTimeAxis("x", "Year"); 
          // var x = myChart.addTimeAxis("x", "year"); 
          var y = myChart.addMeasureAxis('y', 'Weather Delay');
          // var y = myChart.addMeasureAxis('y', 'on_time');

          // x.dateParseFormat = "%Y"
          x.tickFormat = '%Y';
          x.timeInterval = 1;
          // x.title = 'Year';

          y.tickFormat = '%';
          y.overrideMin = y_min;
          y.overrideMax = y_max;
          // y.title = 'On Time';

          myChart.addSeries('Carrier Name', dimple.plot.line);
          myChart.addSeries('Carrier Name', dimple.plot.scatter);
          myChart.addLegend(width_01*0.95, height_01*0.075, 50, 80, "right");
          // myChart.addSeries('carrier_name', dimple.plot.line);
          // myChart.addSeries('carrier_name', dimple.plot.scatter);
          myChart.draw();


//**  ***************************** NAS Delay **************************************** **//

          // d3.select('#content_03')
          // .append('h3')
          // .attr('id', 'title')
          // .text('U.S. Airlines Delay (NAS)');

          // Adds the svg canvas
          var chart_03 = d3.select("#content_03")
          .append("svg")
          .attr("width", width_01 + margin_01.left + margin_01.right)
          .attr("height", height_01 + margin_01.top + margin_01.bottom)
          .append("g")
          .attr("transform", "translate(" + margin_01.left + "," + margin_01.top + ")");

      /*Dimple.js Chart construction code*/          
          var y_min = 0;
          var y_max = 0.7;
          
          var myChart = new dimple.chart(chart_03, data);
          var x = myChart.addTimeAxis("x", "Year"); 
          // var x = myChart.addTimeAxis("x", "year"); 
          var y = myChart.addMeasureAxis('y', 'NAS Delay');
          // var y = myChart.addMeasureAxis('y', 'on_time');

          // x.dateParseFormat = "%Y"
          x.tickFormat = '%Y';
          x.timeInterval = 1;
          // x.title = 'Year';

          y.tickFormat = '%';
          y.overrideMin = y_min;
          y.overrideMax = y_max;
          // y.title = 'On Time';

          myChart.addSeries('Carrier Name', dimple.plot.line);
          myChart.addSeries('Carrier Name', dimple.plot.scatter);
          myChart.addLegend(width_01*0.95, height_01*0.075, 50, 80, "right");
          // myChart.addSeries('carrier_name', dimple.plot.line);
          // myChart.addSeries('carrier_name', dimple.plot.scatter);
          myChart.draw();

//**  ***************************** Late Aircraft Delay ****************************** **//
          
          // d3.select('#content_04')
          // .append('h3')
          // .attr('id', 'title')
          // .text('U.S. Airlines Delay (Late Aircraft Delay)');

          // Adds the svg canvas
          var chart_04 = d3.select("#content_04")
          .append("svg")
          .attr("width", width_01 + margin_01.left + margin_01.right)
          .attr("height", height_01 + margin_01.top + margin_01.bottom)
          .append("g")
          .attr("transform", "translate(" + margin_01.left + "," + margin_01.top + ")");

      /*Dimple.js Chart construction code*/          
          var y_min = 0;
          var y_max = 0.7;
          
          var myChart = new dimple.chart(chart_04, data);
          var x = myChart.addTimeAxis("x", "Year"); 
          // var x = myChart.addTimeAxis("x", "year"); 
          var y = myChart.addMeasureAxis('y', 'Late Aircraft Delay');
          // var y = myChart.addMeasureAxis('y', 'on_time');

          // x.dateParseFormat = "%Y"
          x.tickFormat = '%Y';
          x.timeInterval = 1;
          // x.title = 'Year';

          y.tickFormat = '%';
          y.overrideMin = y_min;
          y.overrideMax = y_max;
          // y.title = 'On Time';

          myChart.addSeries('Carrier Name', dimple.plot.line);
          myChart.addSeries('Carrier Name', dimple.plot.scatter);
          myChart.addLegend(width_01*0.95, height_01*0.075, 50, 80, "right");
          // myChart.addSeries('carrier_name', dimple.plot.line);
          // myChart.addSeries('carrier_name', dimple.plot.scatter);
          myChart.draw();

//**  ***************************** Security Delay *********************************** **//
          
          // d3.select('#content_05')
          // .append('h3')
          // .attr('id', 'title')
          // .text('U.S. Airlines Delay (Security Delay)');

          // Adds the svg canvas
          var chart_05 = d3.select("#content_05")
          .append("svg")
          .attr("width", width_01 + margin_01.left + margin_01.right)
          .attr("height", height_01 + margin_01.top + margin_01.bottom)
          .append("g")
          .attr("transform", "translate(" + margin_01.left + "," + margin_01.top + ")");

      /*Dimple.js Chart construction code*/          
          var y_min = 0;
          var y_max = 0.02;
          
          var myChart = new dimple.chart(chart_05, data);
          var x = myChart.addTimeAxis("x", "Year"); 
          // var x = myChart.addTimeAxis("x", "year"); 
          var y = myChart.addMeasureAxis('y', 'Security Delay');
          // var y = myChart.addMeasureAxis('y', 'on_time');

          // x.dateParseFormat = "%Y"
          x.tickFormat = '%Y';
          x.timeInterval = 1;
          // x.title = 'Year';

          y.tickFormat = '%';
          y.overrideMin = y_min;
          y.overrideMax = y_max;
          // y.title = 'On Time';

          myChart.addSeries('Carrier Name', dimple.plot.line);
          myChart.addSeries('Carrier Name', dimple.plot.scatter);
          myChart.addLegend(width_01*0.95, height_01*0.075, 50, 80, "right");
          // myChart.addSeries('carrier_name', dimple.plot.line);
          // myChart.addSeries('carrier_name', dimple.plot.scatter);
          myChart.draw();


//**  ***************************** On Time Percentage *********************************** **//

      /*
        D3.js setup code
      */
          d3.select('#content_06')
          .append('h3')
          .attr('id', 'title')
          .text('U.S. Airlines On Time Arrivals Percantage');

          "use strict";
          var margin = 50,
              width = 1200 - margin,
              height = 600 - margin;

          // debugger;

          var svg = d3.select("#content_06")
            .append("svg")
              .attr("width", width + margin)
              .attr("height", height + margin)
            .append('g')
                .attr('class','chart');

      /*
        Dimple.js Chart construction code
      */
          

          var y_min = 0.70;
          var y_max = 0.90;
          
          var myChart = new dimple.chart(svg, data);
          var x = myChart.addTimeAxis("x", "Year"); 
          // var x = myChart.addTimeAxis("x", "year"); 
          var y = myChart.addMeasureAxis('y', 'On Time');
          // var y = myChart.addMeasureAxis('y', 'on_time');

          // x.dateParseFormat = "%Y"
          x.tickFormat = '%Y';
          x.timeInterval = 1;
          // x.title = 'Year';

          y.tickFormat = '%';
          y.overrideMin = y_min;
          y.overrideMax = y_max;
          // y.title = 'On Time';

          myChart.addSeries('Carrier Name', dimple.plot.line);
          myChart.addSeries('Carrier Name', dimple.plot.scatter);
          // myChart.addLegend(width*0.80, 90, width*0.25, 60);
          myChart.addLegend(width*0.95, height*0.8, 50, 60, "right")

          // myChart.addSeries('carrier_name', dimple.plot.line);
          // myChart.addSeries('carrier_name', dimple.plot.scatter);
          myChart.draw();

        });



