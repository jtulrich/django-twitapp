$(document).ready(function() {

    // var test_data = {
    //     "most_retweeted": {
    //         "text": "Once #Onlywatch, now #Overwatch. #finally",
    //         "author": "SahuginDagon"
    //     },
    //     "tweets_grouped": [
    //         {"date": "2016-04-01T00:00:00", "count": 5,
    //             "top_tweet": { "text": "Test 1", "coordinates": {"lat":-42,"lng":32}}}
    //     ]
    // };

    getMostRetweeted();
    getTweetList();
});

function getMostRetweeted() {
    $.ajax({
        url: "/data/most_retweeted/",
        success: function(result) {
            // TODO: Update SQL to return a single record as its data type.
            updateMostRetweeted(result[0]);
        },
        error: function(error) {
            alert('unable to retrieve data from backend.');
        }
    });
}

function getTweetList() {
    $.ajax({ 
        url: "/data/",
        success: function(result) {
            updateHistogram(result);
            updateMap(result);
        },
        error: function(error) {
            alert('unable to retrieve data from backend.');
        }
    });
}

function updateMostRetweeted(tweet) {
    $("#most-retweeted-text").html("\"" + tweet.tweet_text + "\"");
    $("#most-retweeted-author").html("&mdash;  @" + tweet.user_screen_name)
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
            .domain([new Date(data[0].tweet_hour), d3.time.day.offset(new Date(data[data.length - 1].tweet_hour), 1)])
            .rangeRound([0, width - margin.left - margin.right]);

        var y = d3.scale.linear()
            .domain([0, d3.max(data, function(d) { return d.tweet_hour_count; })])
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
            .attr('x', function(d) { return x(new Date(d.tweet_hour)); })
            .attr('y', function(d) { return height - margin.top - margin.bottom -
                (height - margin.top - margin.bottom - y(d.tweet_hour_count)) })
            .attr('width', 10)
            .attr('height', function(d) { return height - margin.top - margin.bottom - y(d.tweet_hour_count) });

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
                position: {
                    lat: data[i].tweet_latitude,
                    lng: data[i].tweet_longitude
                },
                map: map,
                title: data[i].tweet_text
            });
            marker_list.push(marker);
        }
    }
    catch (ex)
    {
        console.log('MAP ' + ex);
    }
}