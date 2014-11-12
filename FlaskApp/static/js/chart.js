google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(function(){
    $.get("static/csv/data.csv", function(data){
        plotIt(data);
    });
});

function plotIt(csv){
    rows = csv.split("\n")
        .filter(function(row){return row.length > 0;});

    rows = rows.map(function(row, index){
        var splitted = row.split(", ");
        if(index == 0){
            return splitted;
        }
        else{
            return splitted.map(parseFloat);
        }
    });
    var dataTable = google.visualization.arrayToDataTable(rows);
    var chart = new google.visualization.ScatterChart(document.getElementById('chartDiv'));
    var options = {
        title: 'cross-validation performance as a function of document length',
        backgroundColor: $("body").css('background-color'),
        colors: [
            'rgb(100, 200, 100)',
            'rgb(200, 100, 100)',
            'rgb(100, 100, 200)'],
        hAxis: {title: 'length of comment in characters'},
        vAxis: {title: 'probability of correct guess among 200 subreddits'},
        legend: {position: 'top'}
    };
    chart.draw(dataTable, options);
    window.onresize = function(){chart.draw(dataTable, options);};
}

