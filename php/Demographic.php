<?php
session_start();
echo $_SESSION['choice'];
$topic = $_SESSION['choice'];
?>

<!DOCTYPE html>
<meta charset="utf-8">
<style>

    .main text{
        font: 1px font-weight;
    }

    .states {
        fill: none;
        stroke: #fff;
        stroke-linejoin: round;
    }

    div.tooltip{
        position: absolute;
        text-align:center;
        width: 150px;
        height: 45px;
        padding:2px;
        font-size:11px;
        background: black;
        border:1px;
        border-radius:3px;
        pointer-events: none;
        color: white;
    }

    .tile{
        shape-rendering: crispEdges;
        stroke-width: 2px;
    }


</style>
<svg width="1000" height="600"></svg>
<script src="lib/d3.v3.min.js"></script>
<script src="lib/d3.tip.v0.6.3.js"></script>
<script src="lib/d3-queue.v3.min.js"></script>
<script src="lib/topojson.v1.min.js"></script>

<script>

    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height");


    var div = d3.select("body")
        .append("div")
        .attr("class","tooltip")
        .style("opacity",0);

    var earnings = d3.map();

    var path = d3.geo.path();

    var x = d3.scale.linear()
        .domain([-1,-0.6,-0.2,0.2,0.6,1])
        .range([600, 860]);

    var color = d3.scale.threshold()
        .domain([-1,-0.6,-0.2,0.2,0.6,1])
        .range(["#e1eee1","#9bc99b","#82bb82","#68ad68","#468146","#315b31"]);

    var colorarray = ["#e1eee1","#9bc99b","#82bb82","#68ad68","#468146","#315b31"];

    var g = svg.append("g")
        .attr("class", "key")

    g.selectAll("rect")
        .data(color.range().map(function(d) {
            d = color.invertExtent(d);
            return d;
        }))
        .enter().append("rect")
        .attr("height", 20)
        .attr("x", function (d) { return 870;})
        .attr("y",function (d,i) {
            return 400+i*20;
        })
        .attr("width", function(d,i) {
            return 20;
        })
        .attr("fill", function(d,i) {
            return colorarray[i];
        });

    svg.append("text")
        .attr("class","label")
        .attr("x",350)
        .attr("y",70)
        .attr("font-size","28px","bold")
        .text("US's feeling on $topic");


    var legend = [-1,-1,-0.6,-0.2,0.2,0.6,1];

    svg.selectAll("text")
        .data(legend)
        .enter()
        .append("text")
        .attr("font-weight","5px")
        .attr("fill","black")

        .attr("x",895)
        .attr("y",function (d,i) {
            return 400+i*20;
        })
        .text(function(d,i){
            return legend[i];
        });


    d3.queue()
        .defer(d3.json, "us.json")
        .defer(d3.json, "sentiment_fake.json")
        .defer(d3.json, "population.json")
        .defer(d3.json, "income.json")
        .defer(d3.json, "female.json")
        .defer(d3.json, "education.json")
        .await(ready);

    var svg3 = svg.append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("x",0)
        .attr("y",100);

    function ready(error, us, sentiment, population, income, female, education) {
        if (error) throw error;

        var sentimentById = {};

        sentiment.forEach(function (d) {
            sentimentById[d.id] = [];
            sentimentById[d.id].push({"id": d.id,"sentiment_fake":d.sentiment_fake,"state":d.state, "rank":d.rank});
            d.rank=+d.rank;
        });

        var populationById = {};

        population.forEach(function (d) {
            populationById[d.id] = [];
            d.population = +d.population;
            d.rank = +d.rank;
        });

        population.forEach(function (d) {

            populationById[d.id].push({"id": d.id,"population":d.population,"state":d.state, "rank":d.rank});

        });

        var incomeById = {};

        income.forEach(function (d) {
            incomeById[d.id] = [];
            d.income = +d.income;
            d.rank = +d.rank;
        });

        income.forEach(function (d) {
            incomeById[d.id].push({"id": d.id,"income":d.income,"state":d.state, "rank":d.rank});
        });

        var femaleById = {};

        female.forEach(function (d) {
            femaleById[d.id] = [];
            d.Female = +d.Female;
            d.rank = +d.rank;
        });

        female.forEach(function (d) {
            femaleById[d.id].push({"id": d.id,"Female":d.Female,"state":d.state, "rank":d.rank});
        });

        var educationById = {};

        education.forEach(function (d) {
            educationById[d.id] = [];
            d.education = +d.education;
            d.rank = +d.rank;
        });

        education.forEach(function (d) {
            educationById[d.id].push({"id": d.id,"education":d.education,"state":d.state, "rank":d.rank});
        });



        var map = svg3.append("g")
            .attr("class", "states")
            .selectAll("path")
            .data(topojson.feature(us, us.objects.states).features)
            .enter().append("path")
            .attr("fill", function(d) {
//                if(d.id==56){
//                    return "red";
//                }
                return color(sentimentById[d.id][0].sentiment_fake);
            })
            .attr("d", path);


        map.on("click", function (d){


            //yellow background

                svg.append("rect")
                    .attr("class","info")
                    .attr("height", 250)
                    .attr("x", 300)
                    .attr("y",230)
                    .attr("width", 400)
                    .attr("fill", "#FFFFE0")
                    .on("click", function (d){

                        svg.selectAll(".info").remove();

                    });

                svg.append("text")
                    .attr("class","info")
                    .attr("x",460)
                    .attr("y",260)
                    .attr("font-size","20px","bold")
                    .text(function () {
                        return populationById[d.id][0].state;
                    });

                svg.append("text")
                    .attr("class","info")
                    .attr("x",330)
                    .attr("y",295)
                    .attr("font-size","16px")
                    .text("Sentiment ");

                svg.append("text")
                    .attr("class","info")
                    .attr("x",640)
                    .attr("y",295)
                    .attr("font-size","14px")
                    .text("+1");

                svg.append("text")
                    .attr("class","info")
                    .attr("x",450)
                    .attr("y",295)
                    .attr("font-size","14px")
                    .text("-1");

                //sentiment rectangle
                svg.append("rect")
                    .attr("class","info")
                    .attr("height", 25)
                    .attr("x",470)
                    .attr("y", 280)
                    .attr("width",160)
                    .attr("stroke","lightgrey")
                    .attr("fill", "white");

                var SentiRect = svg.append("rect")
                    .attr("class","info")
                    .attr("height", 25)
                    .attr("x",470)
                    .attr("y", 280)
                    .attr("width",function () {
                        if(sentimentById[d.id][0].sentiment_fake>=0){
                            return 160*((sentimentById[d.id][0].sentiment_fake+1)/2);
                        }else{
                            return 160*(Math.abs(sentimentById[d.id][0].sentiment_fake)/2);
                        }
                    })
                    .attr("stroke","lightgrey")
                    .attr("fill", "pink")
                    .on("mouseover",function () {
                        d3.select(this)
                            .transition()
                            .duration(10).style("opacity", 10);
                        div.transition()
                            .duration(10)
                            .style("opacity", 10)
                        div.html(function(){

                            return  "<br/>" + "Sentiment Degree is: " + sentimentById[d.id][0].sentiment_fake + "<br/>"
                                + "Rank in US is:" + sentimentById[d.id][0].rank ;

                        })
                            .attr("fill","white")
                            .style("left", (d3.event.pageX) + "px")
                            .style("top", (d3.event.pageY -10) + "px");

                    })
                    .on("mouseout", function(d) {
                        div.transition()
                            .duration(10)
                            .style("opacity", 0);
                    });

                //population rectangle
                var popmin = d3.min(population,function (d) {
                    if(d.population!=0){
                        return d.population;
                    }
                });
                var popmax = d3.max(population,function (d) {
                    return d.population;
                });

                svg.append("text")
                    .attr("class","info")
                    .attr("x",330)
                    .attr("y",335)
                    .attr("font-size","16px")
                    .text("Population");

                svg.append("text")
                    .attr("class","info")
                    .attr("x",640)
                    .attr("y",335)
                    .attr("font-size","14px")
                    .text(function () {
                        return (popmax/1000).toFixed(0) + "K";
                    });

                svg.append("text")
                    .attr("class","info")
                    .attr("x",430)
                    .attr("y",335)
                    .attr("font-size","14px")
                    .text(function () {
                        return (popmin/1000).toFixed(0) + "K";
                    });

                svg.append("rect")
                    .attr("class","info")
                    .attr("height", 25)
                    .attr("x",470)
                    .attr("y", 320)
                    .attr("width",160)
                    .attr("stroke","lightgrey")
                    .attr("fill", "white");

                var PopuRect = svg.append("rect")
                    .attr("class","info")
                    .attr("height", 25)
                    .attr("x",470)
                    .attr("y", 320)
                    .attr("width",function () {
                        return 160*((populationById[d.id][0].population-popmin)/(popmax-popmin));
                    })
                    .attr("stroke","lightgrey")
                    .attr("fill", "pink")
                    .on("mouseover",function () {
                        d3.select(this)
                            .transition()
                            .duration(10).style("opacity", 10);
                        div.transition()
                            .duration(10)
                            .style("opacity", 10)
                        div.html(function(){

                            return  "<br/>" + "Population is: " + populationById[d.id][0].population + "<br/>"
                                + "Rank in US is: " + populationById[d.id][0].rank;

                        })
                            .attr("fill","white")
                            .style("left", (d3.event.pageX) + "px")
                            .style("top", (d3.event.pageY -10) + "px");

                    })
                    .on("mouseout", function(d) {
                        div.transition()
                            .duration(10)
                            .style("opacity", 0);
                    });


                //income rectangle
                var incomeMin = d3.min(income,function (d) {
                    if(d.income!=0){
                        return d.income;
                    }
                });
                var incomeMax = d3.max(income,function (d) {
                    return d.income;
                });

                svg.append("text")
                    .attr("class","info")
                    .attr("x",330)
                    .attr("y",375)
                    .attr("font-size","16px")
                    .text("Income");

                svg.append("text")
                    .attr("class","info")
                    .attr("x",640)
                    .attr("y",375)
                    .attr("font-size","14px")
                    .text(function () {
                        return (incomeMax/1000).toFixed(0)+"K";
                    });

                svg.append("text")
                    .attr("class","info")
                    .attr("x",437)
                    .attr("y",375)
                    .attr("font-size","14px")
                    .text(function () {
                        return (incomeMin/1000).toFixed(0)+"K";
                    });

                svg.append("rect")
                    .attr("class","info")
                    .attr("height", 25)
                    .attr("x",470)
                    .attr("y", 360)
                    .attr("width",160)
                    .attr("stroke","lightgrey")
                    .attr("fill", "white");

                var IncomeRect = svg.append("rect")
                    .attr("class","info")
                    .attr("height", 25)
                    .attr("x",470)
                    .attr("y", 360)
                    .attr("width",function () {
                        return 160*((incomeById[d.id][0].income-incomeMin)/(incomeMax-incomeMin));
                    })
                    .attr("stroke","lightgrey")
                    .attr("fill", "pink")
                    .on("mouseover",function () {
                        d3.select(this)
                            .transition()
                            .duration(10).style("opacity", 10);
                        div.transition()
                            .duration(10)
                            .style("opacity", 10)
                        div.html(function(){

                            return  "<br/>" + "Income is: " + incomeById[d.id][0].income + "<br/>"
                                + "Rank in US is: " + incomeById[d.id][0].rank;

                        })
                            .attr("fill","white")
                            .style("left", (d3.event.pageX) + "px")
                            .style("top", (d3.event.pageY -10) + "px");

                    })
                    .on("mouseout", function(d) {
                        div.transition()
                            .duration(10)
                            .style("opacity", 0);
                    });

                //femalerectangle
                var femaleMin = d3.min(female,function (d) {
                    if(d.Female!=0){
                        return d.Female;
                    }
                });
                var femaleMax = d3.max(female,function (d) {
                    return d.Female;
                });

                svg.append("text")
                    .attr("class","info")
                    .attr("x",330)
                    .attr("y",415)
                    .attr("font-size","16px")
                    .text("Female");

                svg.append("text")
                    .attr("class","info")
                    .attr("x",640)
                    .attr("y",415)
                    .attr("font-size","14px")
                    .text(function () {
                        return femaleMax;
                    });

                svg.append("text")
                    .attr("class","info")
                    .attr("x",436)
                    .attr("y",415)
                    .attr("font-size","14px")
                    .text(function () {
                        return femaleMin;
                    });

                svg.append("rect")
                    .attr("class","info")
                    .attr("height", 25)
                    .attr("x",470)
                    .attr("y", 400)
                    .attr("width",160)
                    .attr("stroke","lightgrey")
                    .attr("fill", "white");

                var FemaleRect = svg.append("rect")
                    .attr("class","info")
                    .attr("height", 25)
                    .attr("x",470)
                    .attr("y", 400)
                    .attr("width",function () {
                        return 160*((femaleById[d.id][0].Female-femaleMin)/(femaleMax-femaleMin));
                    })
                    .attr("stroke","lightgrey")
                    .attr("fill", "pink")
                    .on("mouseover",function () {
                        d3.select(this)
                            .transition()
                            .duration(10).style("opacity", 10);
                        div.transition()
                            .duration(10)
                            .style("opacity", 10)
                        div.html(function(){

                            return  "<br/>" + "Female percentage is: " + femaleById[d.id][0].Female + "<br/>"
                                + "Rank in US is: " + femaleById[d.id][0].rank;
                        })
                            .attr("fill","white")
                            .style("left", (d3.event.pageX) + "px")
                            .style("top", (d3.event.pageY -10) + "px");

                    })
                    .on("mouseout", function(d) {
                        div.transition()
                            .duration(10)
                            .style("opacity", 0);
                    });

                //femalerectangle
                var educationMin = d3.min(education,function (d) {
                    if(d.education!=0){
                        return d.education;
                    }
                });
                var educationMax = d3.max(education,function (d) {
                    return d.education;
                });

                svg.append("text")
                    .attr("class","info")
                    .attr("x",330)
                    .attr("y",455)
                    .attr("font-size","16px")
                    .text("Education");

                svg.append("text")
                    .attr("class","info")
                    .attr("x",640)
                    .attr("y",455)
                    .attr("font-size","14px")
                    .text(function () {
                        return educationMax;
                    });

                svg.append("text")
                    .attr("class","info")
                    .attr("x",436)
                    .attr("y",455)
                    .attr("font-size","14px")
                    .text(function () {
                        return educationMin;
                    });

                svg.append("rect")
                    .attr("class","info")
                    .attr("height", 25)
                    .attr("x",470)
                    .attr("y", 440)
                    .attr("width",160)
                    .attr("stroke","lightgrey")
                    .attr("fill", "white");

                var EducationRect = svg.append("rect")
                    .attr("class","info")
                    .attr("height", 25)
                    .attr("x",470)
                    .attr("y", 440)
                    .attr("width",function () {
                        return 160*((educationById[d.id][0].education-educationMin)/(educationMax-educationMin));
                    })
                    .attr("stroke","lightgrey")
                    .attr("fill", "pink")
                    .on("mouseover",function () {
                        d3.select(this)
                            .transition()
                            .duration(10).style("opacity", 10);
                        div.transition()
                            .duration(10)
                            .style("opacity", 10)
                        div.html(function(){

                            return  "<br/>" + "Education level is: " + educationById[d.id][0].education + "<br/>"
                                + "Rank in US is: " + educationById[d.id][0].rank;

                        })
                            .attr("fill","white")
                            .style("left", (d3.event.pageX) + "px")
                            .style("top", (d3.event.pageY -10) + "px");

                    })
                    .on("mouseout", function(d) {
                        div.transition()
                            .duration(10)
                            .style("opacity", 0);
                    });



            });



    };

</script>
