// initiate the dropdown button
function dropdown_select() {
    Plotly.d3.json('/names', function(error, response){
        if (error) throw error;
        for (var i = 0; i < response.length; i++){
            Plotly.d3.select("#dataselect").append("option").attr("value",response[i]).text(response[i]);
        }
    })
}

// Create the table for each sample
function load_table(sample){
    var url = '/metadata' + sample;

    Plotly.d3.json(url, function(error, response) {
        if (error) throw error;
        var table = Plotly.d3.select('#table')

        //remove the previous table
        table.selectAll('tr').remove();
        table.selectAll('td').remove();
        table.selectAll('thread').remove();
        table.append('thread').text('Sample Metadata').style('box-body');

        for (var item in response) {
            var cell = response[item];
            var row = table.append('tr');
            row.append('td').text(key);
            row.append('td').text(cell);
        }
    })
}

function intialize_page(){
    dropdown_select()

    var first_val = "BB_940";
    load_table(first_val);


    var otu_val = [];
    var otu_id = [];
    var otu_desc = [];

    var url = '/samples/' + first_val;

    Plotly.d3.json(url, function(error, response){
        if (error) throw error;

        for(var i = 0; i<10; i++){
            otu_val.push(response[first_val][i]);
            otu_id.push(response['otu_id'][i]);
        }
    });

    url = "/otu_desc"
    Plotly.d3.json(url, function(error, response){
        if (error) throw error;
        for(var i = 0; i<10; i++){
            otu_desc.push(response[otu_id[i]]);
        }
    });

    var bio_data = [{
        values:otu_values,
        labels:otu_ids,
        text:otu_descriptions,
        hoverinfo:'text',
        hole: .4,
        type: 'pie'
    )];

    var layout = {
        title: "OTU Values Frequency",
        height: 400,
        width: 877
    };
    Plotly.plot('pieplot', bio_data, layout);

    bio_data = [{
        y:otu_values,
        x:otu_ids,
        mode: 'markers',
          marker:{
            color:otu_ids,
            size:otu_values
          }
      }];

    layout={
        title:"OTU Values for each OTU ID",
        height: 400,
        width: 1010,
        xaxis:{
            title:"OTU ID"
        },
        yaxis:{
            title:"Values"
        }
    };
    Plotly.plot('bubbleplot', bio_data, layout);
}


function intialize_page(){
    dropdown_select()

    var first_val = "BB_940";
    load_table(first_val);


    var otu_val = [];
    var otu_id = [];
    var otu_desc = [];

    var url = '/samples/' + first_val;

    Plotly.d3.json(url, function(error, response){
        if (error) throw error;

        for(var i = 0; i<10; i++){
            otu_val.push(response[first_val][i]);
            otu_id.push(response['otu_id'][i]);
        }
    });

    url = "/otu_desc"
    Plotly.d3.json(url, function(error, response){
        if (error) throw error;
        for(var i = 0; i<10; i++){
            otu_desc.push(response[otu_id[i]]);
        }
    });

    var bio_data = [(
        values: otu_val,
        labels: otu_id,
        text: otu_desc,
        hoverinfo: 'text',
        hole: .4,
        type: 'pie'
    )];

    var layout = {
        title: "OTU Values Frequency",
        height: 400,
        width: 877
    };
    Plotly.plot('pieplot', bio_data, layout);

    bio_data = [(
        y: otu_val,
        x: otu_id,
        mode: 'markers',
        marker:{
            color:otu_id,
            size:otu_val
        }
    )];

    layout={
        title:"OTU Values for each OTU ID",
        height: 400,
        width: 1010,
        xaxis:{
            title:"OTU ID"
        },
        yaxis:{
            title:"Values"
        }
    };
    Plotly.plot('bubbleplot', bio_data, layout);
}