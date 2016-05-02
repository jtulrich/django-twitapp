$(document).ready(function() {
    var test_data = {
        "most_retweeted": {"text": "Once #Onlywatch, now #Overwatch. #finally"},
        "tweets_grouped": [
            {"date": "2016-04-01 00:00:00", "count": 5,
                "top_tweet": { "text": "Test 1", "coordinates": {"lat":-42,"lng":32}}},
            {"date": "2016-04-01 01:00:00", "count": 1,
                "top_tweet": { "text": "Test 2", "coordinates": {"lat":-42,"lng":22}}},
            {"date": "2016-04-01 02:00:00", "count": 3,
                "top_tweet": { "text": "Test 3", "coordinates": {"lat":-42,"lng":12}}},
            {"date": "2016-04-01 03:00:00", "count": 10,
                "top_tweet": { "text": "Test 4", "coordinates": {"lat":-42,"lng":2}}},
            {"date": "2016-04-01 04:00:00", "count": 8,
                "top_tweet": { "text": "Test 5", "coordinates": {"lat":-42,"lng":-12}}},
            {"date": "2016-04-01 05:00:00", "count": 4,
                "top_tweet": { "text": "Test 6", "coordinates": {"lat":-42,"lng":-22}}}
        ]
    };

    //getTweetList();
    updateMostRetweeted(test_data);
    updateHistogram(test_data.tweets_grouped);
    updateMap(test_data.tweets_grouped);
});

function getTweetList() {
    $.ajax({ 
        url: "/twit/tweet/", 
        success: function(result) {
            updateMostRetweeted(result.most_retweeted);
            updateHistogram(result.tweets_grouped);
            updateMap(result.tweets_grouped);
        },
        error: function(error) {
            alert('unable to retrieve data from backend.');
        }
    });
}

function updateMostRetweeted(most_retweeted) {
    $("#most-retweeted").html(most_retweeted.text);
}

function updateHistogram(data) {

    var margin = {top:20, right:20, bottom:20, left:20},
        width = $(".graph-histogram").width() - 40,
        height = $(".graph-histogram").height() - 40;

    var x = d3.time.scale()
        .domain([new Date(data[0].date), d3.time.day.offset(new Date(data[data.length - 1].date), 1)])
        .rangeRound([0, width - margin.left - margin.right]);

    var y = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return d.count; })])
        .range([height - margin.top - margin.bottom, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient('bottom')
        .ticks(data.length, 1)
        .tickFormat(d3.time.format('%a %d  %H'))
        .tickSize(0)
        .tickPadding(8);

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient('left')
        .tickPadding(8);

    var svg = d3.select('body').append('svg')
        .attr('class', 'chart')
        .attr('width', width)
        .attr('height', height)
      .append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

    svg.selectAll('.graph-histogram')
        .data(data)
      .enter().append('rect')
        .attr('class', 'bar')
        .attr('x', function(d) { return x(new Date(d.date)); })
        .attr('y', function(d) { return height - margin.top - margin.bottom -
            (height - margin.top - margin.bottom - y(d.count)) })
        .attr('width', 10)
        .attr('height', function(d) { return height - margin.top - margin.bottom - y(d.count) });

    svg.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0, ' + (height - margin.top - margin.bottom) + ')')
        .call(xAxis);

    svg.append('g')
      .attr('class', 'y axis')
      .call(yAxis);
}

function updateMap(data) {
    var map = new google.maps.Map($("#graph-geographic"), {
        center: {lat: 0, lng: 0},
        scrollwheel: false,
        zoom: 4
    });

    var marker_list = [];
    for (var i = 0; i < data.length; i++) {
        var marker = new google.maps.Marker({
            position: data[i].top_tweet.coordinates,
            map: map,
            title: data[i].top_tweet.text
        });
        marker_list.push(marker);
    }
}