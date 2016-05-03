$(document).ready(function() {
    var test_data = {
        "most_retweeted": {
            "text": "Once #Onlywatch, now #Overwatch. #finally",
            "author": "SahuginDagon"
        },
        "tweets_grouped": [
            {"date": "2016-04-01T00:00:00", "count": 5,
                "top_tweet": { "text": "Test 1", "coordinates": {"lat":-42,"lng":32}}},
            {"date": "2016-04-01T01:00:00", "count": 1,
                "top_tweet": { "text": "Test 2", "coordinates": {"lat":-42,"lng":22}}},
            {"date": "2016-04-01T02:00:00", "count": 3,
                "top_tweet": { "text": "Test 3", "coordinates": {"lat":-42,"lng":12}}},
            {"date": "2016-04-01T03:00:00", "count": 10,
                "top_tweet": { "text": "Test 4", "coordinates": {"lat":-42,"lng":2}}},
            {"date": "2016-04-01T04:00:00", "count": 8,
                "top_tweet": { "text": "Test 5", "coordinates": {"lat":-42,"lng":-12}}},
            {"date": "2016-04-03T05:00:00", "count": 4,
                "top_tweet": { "text": "Test 6", "coordinates": {"lat":-42,"lng":-22}}},
            {"date": "2016-04-03T00:00:00", "count": 5,
                "top_tweet": { "text": "Test 1", "coordinates": {"lat":-32,"lng":32}}},
            {"date": "2016-04-03T01:00:00", "count": 1,
                "top_tweet": { "text": "Test 2", "coordinates": {"lat":-32,"lng":22}}},
            {"date": "2016-04-03T02:00:00", "count": 3,
                "top_tweet": { "text": "Test 3", "coordinates": {"lat":-32,"lng":12}}},
            {"date": "2016-04-03T03:00:00", "count": 10,
                "top_tweet": { "text": "Test 4", "coordinates": {"lat":-32,"lng":2}}},
            {"date": "2016-04-03T04:00:00", "count": 8,
                "top_tweet": { "text": "Test 5", "coordinates": {"lat":-32,"lng":-12}}},
            {"date": "2016-04-03T05:00:00", "count": 4,
                "top_tweet": { "text": "Test 6", "coordinates": {"lat":-32,"lng":-22}}},
            {"date": "2016-04-05T00:00:00", "count": 5,
                "top_tweet": { "text": "Test 1", "coordinates": {"lat":-22,"lng":32}}},
            {"date": "2016-04-05T01:00:00", "count": 1,
                "top_tweet": { "text": "Test 2", "coordinates": {"lat":-22,"lng":22}}},
            {"date": "2016-04-05T02:00:00", "count": 3,
                "top_tweet": { "text": "Test 3", "coordinates": {"lat":-22,"lng":12}}},
            {"date": "2016-04-05T03:00:00", "count": 10,
                "top_tweet": { "text": "Test 4", "coordinates": {"lat":-22,"lng":2}}},
            {"date": "2016-04-05T04:00:00", "count": 8,
                "top_tweet": { "text": "Test 5", "coordinates": {"lat":-22,"lng":-12}}},
            {"date": "2016-04-05T05:00:00", "count": 4,
                "top_tweet": { "text": "Test 6", "coordinates": {"lat":-22,"lng":-22}}},
            {"date": "2016-04-07T00:00:00", "count": 5,
                "top_tweet": { "text": "Test 1", "coordinates": {"lat":-12,"lng":32}}},
            {"date": "2016-04-07T01:00:00", "count": 1,
                "top_tweet": { "text": "Test 2", "coordinates": {"lat":-12,"lng":22}}},
            {"date": "2016-04-07T02:00:00", "count": 3,
                "top_tweet": { "text": "Test 3", "coordinates": {"lat":-12,"lng":12}}},
            {"date": "2016-04-07T03:00:00", "count": 10,
                "top_tweet": { "text": "Test 4", "coordinates": {"lat":-12,"lng":2}}},
            {"date": "2016-04-07T04:00:00", "count": 8,
                "top_tweet": { "text": "Test 5", "coordinates": {"lat":-12,"lng":-12}}},
            {"date": "2016-04-07T05:00:00", "count": 4,
                "top_tweet": { "text": "Test 6", "coordinates": {"lat":-12,"lng":-22}}}
        ]
    };

    //getTweetList();
    updateMostRetweeted(test_data.most_retweeted);
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

function updateMostRetweeted(tweet) {
    $("#most-retweeted-text").html("\"" + tweet.text + "\"");
    $("#most-retweeted-author").html("&mdash;  @" + tweet.author)
}

function updateHistogram(data) {
    try
    {
        var target_string = "#graph-histogram";
        var target_object = $("#graph-histogram");

        var margin = {top:50, right:50, bottom:50, left:50},
            width = target_object.width(),
            height = target_object.height();

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
            .tickFormat(d3.time.format('%d-%H'))
            .tickSize(0)
            .tickPadding(8);

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient('left')
            .tickPadding(8);

        var svg = d3.select(target_string).append('svg')
            .attr('class', 'chart')
            .attr('width', width)
            .attr('height', height)
          .append('g')
            .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

        svg.selectAll(target_string)
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
            .call(xAxis)
            .selectAll("text")
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-65)" );

        svg.append('g')
          .attr('class', 'y axis')
          .call(yAxis);
    }
    catch (ex)
    {
        console.log('HISTOGRAM ' + ex);
    }
}

function updateMap(data) {
    try
    {
        var map = new google.maps.Map(document.getElementById("graph-geographic"), {
            center: {lat: 0, lng: 0},
            scrollwheel: false,
            zoom: 1
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
    catch (ex)
    {
        console.log('MAP ' + ex);
    }
}