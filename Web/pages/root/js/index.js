let DataStack = {};

function toggleCountOn() {
    goCount = true;
    $('.fa-play').addClass('no-display');
    $('.fa-pause').addClass('no-display')
        .removeClass('no-display');
}

function toggleCountOff() {
    goCount = false;
    $('.fa-pause').addClass('no-display');
    $('.fa-play').addClass('no-display')
        .removeClass('no-display');
}

// Collect Data
function preload(callback) {
    let elements = ["workerCount", "totalPoint", "totalHashrate", "difficulty"],
        count = elements.length;

    /* $.each(elements, function(i, name){
        $.getJSON('/api/data/' + name, function(data){
            DataStack[name] = data;

            if(!--count) {
                callback();
            }
        })
    }); */

    $.getJSON('/api/data/' + elements.join(","), function(data){
       $.each(elements, function(i, name){
           DataStack[name] = data[name];

           if(count === i+1) callback();
       });
    });
}

function createChart(chart_name, seriesOptions) {
        Highcharts.stockChart(chart_name, {
            time: {
                timezone: 'Asia/Seoul'
            },
            rangeSelector: {
                selected: 4
            },
            yAxis: {
                labels: {
                    formatter: function () {
                        return (this.value > 0 ? ' + ' : '') + this.value + '%';
                    }
                },
                plotLines: [{
                    value: 0,
                    width: 2,
                    color: 'silver'
                }]
            },
            plotOptions: {
                series: {
                    compare: 'percent',
                    showInNavigator: true
                }
            },
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                valueDecimals: 2,
                split: true
            },
            series: seriesOptions
        });
    }

function build(chart_name, variables) {
    var seriesCounter = 0,
        seriesOptions=[];

    $.each(variables, function (i, name) {
        if(DataStack[name] === undefined) {
            console.log("Fetching " + name);
            $.getJSON('/api/data/' + name,    function (data) {
                DataStack[name] = data;
            });
        }

        seriesOptions[i] = {
            name: name,
            data: DataStack[name]
        };
        seriesCounter += 1;

        if (seriesCounter === variables.length) {
            createChart(chart_name, seriesOptions);
        }
    });
}
