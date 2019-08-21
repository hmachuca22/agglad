// Morris-JS.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -



$(document).on('nifty.ready', function () {

    // MORRIS AREA CHART
    // =================================================================
    // Require MorrisJS Chart
    // -----------------------------------------------------------------
    // http://morrisjs.github.io/morris.js/
    // =================================================================

    var chart = Morris.Area({
        element: 'demo-morris-area',
        data: [{
            period: 'Atlántida',
            dl: 400,
           
            }, {
            period: 'Choluteca',
            dl: 127,
            
            }, {
            period: 'Colón',
            dl: 115,
           
            }, {
            period: 'Comayagua',
            dl: 239,
           
            }, {
            period: 'Copán',
            dl: 420,
           
            }, {
            period: 'Cortes',
            dl: 300,
            
            }, {
            period: 'El Paraíso',
            dl: 400,
           
            }, {
            period: 'Francisco Morazán',
            dl: 200,
            
            }, {
            period: 'Gracias a Dios',
            dl: 239,
            
            }, {
            period: 'Intibucá',
            dl: 200,
            
            }, {
            period: 'Islas de la Bahía',
            dl: 189,
            
            }, {
            period: 'La Paz',
            dl: 150,
           
            }, {
            period: 'Lempira',
            dl: 245,
           
            }, {
            period: 'Ocotepeque',
            dl: 127,
            
            }, {
            period: 'Olancho',
            dl: 115,
            
            }, {
            period: 'Santa Bárbara',
            dl: 239,
           
            }, {
            period: 'Valle',
            dl: 460,
            
            }, {
            period: 'Yoro',
            dl: 974,
            
            }],
        gridEnabled: true,
        gridLineColor: 'rgba(0,0,0,.1)',
        gridTextColor: '#8f9ea6',
        gridTextSize: '11px',
        behaveLikeLine: true,
        smooth: true,
        xkey: 'period',
        ykeys: ['dl'],
        labels: ['Capacitados'],
        lineColors: ['#fcbf71', '#78c855'],
        pointSize: 0,
        pointStrokeColors : ['#045d97'],
        lineWidth: 0,
        resize:true,
        hideHover: 'auto',
        fillOpacity: 0.9,
        parseTime:false
    });

    chart.options.labels.forEach(function(label, i){
        var legendItem = $('<div class=\'morris-legend-items\'></div>').text(label);
        $('<span></span>').css('background-color', chart.options.lineColors[i]).prependTo(legendItem);
        $('#demo-morris-area-legend').append(legendItem)
    })



    // MORRIS LINE CHART
    // =================================================================
    // Require MorrisJS Chart
    // -----------------------------------------------------------------
    // http://morrisjs.github.io/morris.js/
    // =================================================================
    var day_data = [
        {'elapsed': '18 Años', 'value': 18},
        {'elapsed': '19 Años', 'value': 24},
        {'elapsed': '20 Años', 'value': 9},
        {'elapsed': '21 Años', 'value': 12},
        {'elapsed': '22 Años', 'value': 13},
        {'elapsed': '23 Años', 'value': 22},
        {'elapsed': '25 Años', 'value': 11},
        {'elapsed': '26 Años', 'value': 26},
        {'elapsed': '27 Años', 'value': 12},
        {'elapsed': '28 Años', 'value': 19},
        {'elapsed': '29 Años', 'value': 15},
        {'elapsed': '30 Años', 'value': 24},
        {'elapsed': '31 Años', 'value': 9},
        {'elapsed': '32 Años', 'value': 12},
        {'elapsed': '33 Años', 'value': 13},
        {'elapsed': '34 Años', 'value': 35},
        {'elapsed': '35 Años', 'value': 15},
        {'elapsed': '36 Años', 'value': 26},
        {'elapsed': '37 Años', 'value': 12},
        {'elapsed': '38 Años', 'value': 19},
        {'elapsed': '40 Años', 'value': 50},
        {'elapsed': '41 Años', 'value': 19}
    ];
    Morris.Line({
        element: 'demo-morris-line',
        data: day_data,
        xkey: 'elapsed',
        ykeys: ['value'],
        labels: ['Capacitados'],
        gridEnabled: true,
        gridLineColor: 'rgba(0,0,0,.1)',
        gridTextColor: '#8f9ea6',
        gridTextSize: '11px',
        lineColors: ['#177bbb'],
        lineWidth: 2,
        parseTime: false,
        resize:true,
        hideHover: 'auto'
    });




    // MORRIS AREA CHART
    // =================================================================
    // Require MorrisJS Chart
    // -----------------------------------------------------------------
    // http://morrisjs.github.io/morris.js/
    // =================================================================

    var chart = Morris.Area({
        element: 'demo-morris-area-full',
        data: [{
            period: 'Atlántida',
            dl: 77,
            up: 25
            }, {
            period: 'Choluteca',
            dl: 127,
            up: 58
            }, {
            period: 'Colón',
            dl: 115,
            up: 46
            }, {
            period: 'Comayagua',
            dl: 239,
            up: 57
            }, {
            period: 'Copán',
            dl: 46,
            up: 75
            }, {
            period: 'Cortes',
            dl: 97,
            up: 57
            }, {
            period: 'El Paraíso',
            dl: 105,
            up: 70
            }, {
            period: 'Francisco Morazán',
            dl: 115,
            up: 106
            }, {
            period: 'Gracias a Dios',
            dl: 239,
            up: 187
            }, {
            period: 'Intibucá',
            dl: 97,
            up: 57
            }, {
            period: 'Islas de la Bahía',
            dl: 189,
            up: 70
            }, {
            period: 'La Paz',
            dl: 65,
            up: 30
            }, {
            period: 'Lempira',
            dl: 35,
            up: 90
            }, {
            period: 'Ocotepeque',
            dl: 127,
            up: 58
            }, {
            period: 'Olancho',
            dl: 115,
            up: 46
            }, {
            period: 'Santa Bárbara',
            dl: 239,
            up: 57
            }, {
            period: 'Valle',
            dl: 46,
            up: 75
            }, {
            period: 'Yoro',
            dl: 97,
            up: 57
            }],
        gridEnabled: true,
        gridLineColor: 'rgba(0,0,0,.1)',
        behaveLikeLine: true,
        smooth: false,
        axes:false,
        xkey: 'period',
        ykeys: ['dl', 'up'],
        labels: ['Femenino', 'Masculino'],
        lineColors: ['#b5bfc5', '#9B59B6'],
        pointSize: 0,
        pointStrokeColors : ['#045d97'],
        lineWidth: 0,
        resize:true,
        hideHover: 'auto',
        fillOpacity: 0.9,
        parseTime:false
    });

    chart.options.labels.forEach(function(label, i){
        var legendItem = $('<div class=\'morris-legend-items\'></div>').text(label);
        $('<span></span>').css('background-color', chart.options.lineColors[i]).prependTo(legendItem);
        $('#demo-morris-area-legend-full').append(legendItem)
    })




    // MORRIS BAR CHART
    // =================================================================
    // Require MorrisJS Chart
    // -----------------------------------------------------------------
    // http://morrisjs.github.io/morris.js/
    // =================================================================
    Morris.Bar({
        element: 'demo-morris-bar',
        data: [
            { y: '1', a: 100, b: 90 },
            { y: '2', a: 75,  b: 65 },
            { y: '3', a: 20,  b: 15 },
            { y: '5', a: 50,  b: 40 },
            { y: '6', a: 75,  b: 95 },
            { y: '7', a: 15,  b: 65 },
            { y: '8', a: 70,  b: 100 },
            { y: '9', a: 100, b: 70 },
            { y: '10', a: 50, b: 70 },
            { y: '11', a: 20, b: 10 },
            { y: '12', a: 40, b: 90 },
            { y: '13', a: 70, b: 30 },
            { y: '14', a: 50, b: 50 },
            { y: '15', a: 100, b: 90 }
        ],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Series A', 'Series B'],
        gridEnabled: true,
        gridLineColor: 'rgba(0,0,0,.1)',
        gridTextColor: '#8f9ea6',
        gridTextSize: '11px',
        barColors: ['#1abc9c', '#d8e8e5'],
        resize:true,
        hideHover: 'auto'
    });


    // MORRIS DONUT CHART
    // =================================================================
    // Require MorrisJS Chart
    // -----------------------------------------------------------------
    // http://morrisjs.github.io/morris.js/
    // =================================================================
    Morris.Donut({
        element: 'demo-morris-donut',
        data: [
            {label: 'Download Sales', value: 12},
            {label: 'In-Store Sales', value: 30},
            {label: 'Mail-Order Sales', value: 20}
        ],
        colors: [
            '#ec407a',
            '#03a9f4',
            '#d8dfe2'
        ],
        resize:true
    });
});
