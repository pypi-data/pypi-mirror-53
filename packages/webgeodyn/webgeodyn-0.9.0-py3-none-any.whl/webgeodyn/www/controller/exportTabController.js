/** Controller of the export tab */
class ExportTabController{
    /** Creates an array containing the long nmaes of the measures and the format of files to export.
     * @param {MainController} mainController - The main controller of the page
     */
    constructor(mainController){
        console.log("Building ExportTabController...");
        this.mc = mainController;
        this.dataDropdown = null;

        this.longNames = {MF:'Reanalysed magnetic field',
                          SV:'Reanalysed secular variation',
                          DIFF:'Diffusion',
                          U:'Core flow',
                          ER:'Subgrid errors',
                          DIVHU:'Horizontal divergence of the core flow',
                          LOD: 'Length of day variation'};


        this.getExportFileInfo();
    }

    /**
     * Initiates the HTML components of the controller. Called in documentReady
     * */
    initExport(){
        var thisETC = this;
        $('.optionscontainer').show();
        // Remove everything in the option menu
        var optionMenu = $('.menuoptionsdiv');
        optionMenu.empty();

        // Creates the title in the main div
        $("<h2>").attr({"class":"ui _centered _flexfixedsize",
                        "id":"model_title",
                        "style":"text-align:center",
                        })
                        .css("margin","0.5rem; ")
                        .insertBefore($('#infodiv'));

        // Creates a new div for the dataDropdown
        $("<div>")
            .attr("class","ui segment _flexfixedsize")
            .css("margin","0.5rem 0!important;")
            .attr('id','dataselectdiv')
            .appendTo(optionMenu);

        // Creates the dropdown to put in the div just created
        this.dataDropdown = new DataDropdown(
            {
                data : this.export_file_info,
                parentDiv : $("#dataselectdiv"),
                onChangeData : function(){
                    thisETC.initExportData();
                }
            }
        );

    }

    /**
     * Updates the list of measures that can be exported. Called when the model was changed in the dropdown
     * */
    initExportData(){
        const thisETC = this;

        // Change the model title
        $('#model_title').html('Model <b>' + thisETC.dataDropdown.config.value + '</b>');

        // Build descriptions of the models
        thisETC.buildDescription();

        // Creates a new div for the measures to download if not present
        if ($('#downloaddiv').length === 0){
            $("<div>")
                .attr("class","ui segment _flexfixedsize")
                .css("margin","0.5rem 0!important;")
                .attr('id',"downloaddiv")
                .insertBefore($('#infodiv'));
        }
        // Else empty it
        else {
            $('#downloaddiv').empty();
        }

        // Build the download links for the current model
        thisETC.buildDownloadLinks();
    }

    /**
     * Build the description of the model fetched from home.html
     * */
    buildDescription() {
        const thisETC = this;

        var desc_div = $('#descdiv');

        // Build the desc_div if not present
        if (desc_div.length === 0){
            desc_div = $('<div>',{
            'class': 'ui segment _flexfixedsize',
            id : 'descdiv',
            });
            desc_div.insertBefore($('#infodiv'));
        }
        // Else empty it
        else {
            desc_div.empty();
        }

        // Creates the title in the description div
        $('<h3>').attr('class','ui')
        .text('Model description')
        .appendTo(desc_div);

        // Creates a subdiv that will receive the description
        $('<div>',{
            'class': 'ui _flexfixedsize',
            id : 'subdescdiv',
        }).appendTo(desc_div);

        // Load the description fetched from coreflowDesc.html into the subdiv of descdiv
        $('#subdescdiv').load('view/coreflowDesc.html #'+thisETC.dataDropdown.config.value);

        // README
        $('<div>')
            .attr('class','ui _flexfixedsize')
            .html('Further information can be found in the README file provided with the model.')
            .appendTo(desc_div);
    }


    /**
     * Builds the different download links according to the files available for download
     * */
    buildDownloadLinks() {
        const thisETC = this;
        var download_div = $('#downloaddiv');

        // Set title
        $('<h3>').attr('class','ui').text('Provided files').appendTo(download_div);

        // Get model info
        const model_name = thisETC.dataDropdown.config.value;
        const current_model_file_info = thisETC.export_file_info[model_name];
        const current_model = thisETC.mc.datalist[model_name];

        // Add the measures of the model as list
        var list = $('<div id=measure_list>').attr('class','ui list');

        // Sort the measure names by alphabetical order
        let sorted_keys = Object.keys(current_model.measures).sort();
        // If no SH measure, give other type of measures instead
        if(sorted_keys.length === 0) {
            sorted_keys = Object.keys(current_model.notSH_measures).sort();
        }
        let measure = null;
        let list_member = null;

        for (var i_measure in sorted_keys) {
            measure = sorted_keys[i_measure];
            // Skip DivHU for export
            if(measure === 'DIVHU') {continue;}

            // Create a container for the measure name and the download links
            list_member = $('<div>')
                .html('<b style="margin-right:auto">- ' + thisETC.longNames[measure] + ' (' + measure + ')</b>')
                .attr('class','_flexcontainer _vcentered indented');

            //Append to the list
            list.append(list_member);
        }

        console.log('list', list);

        // Create a download link for all measures
        // Append a divider to the list
        $('<div>').attr('class','ui divider').appendTo(list);

        list_member = $('<div>')
            .attr('class','_flexcontainer _vcentered indented')
            .css({'margin-top':'1em'});

        let full_download_link = $('<a>',{
                href: model_name+'/'+model_name+'.zip'
            });
            $('<input>',{
                type: 'button',
                'class': 'ui primary button _flexfixedsize',
                value: 'Download',
                style: 'background-color:#660000;',
            }).appendTo(full_download_link);

        list_member.append(full_download_link);
        list.append(list_member);

        // Closing the list and appending to download_div
        download_div.append(list);
    }

    /**
     * Get the info of the files to export using a JSON
     * */
    getExportFileInfo() {
        var thisETC = this;
        $.getJSON("/getexportfileinfo")
            .done(function(response) {
                thisETC.export_file_info = response.exportfileinfo;
                console.log("File info response", response, "--->", response.exportfileinfo);
            })
            .fail(function(jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Server request failed:" + err);
            });
    }


    documentReady() {
       this.initExport();
    }

}