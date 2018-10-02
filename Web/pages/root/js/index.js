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
        $.getJSON('/api/data/' + name,    function (data) {

            seriesOptions[i] = {
                name: name,
                data: data
            };
            seriesCounter += 1;

            if (seriesCounter === variables.length) {
                createChart(chart_name, seriesOptions);
            }
        });
    });
}