/**
 * Class that handles the selection of models through checkboxes.
 */
class ModelSelector {
    /**
     * @param {Object} config - Configuration of the selector
     * @param {boolean} draw - indicates if the selector should be drawn directly (default: true)
     */
    constructor(config, draw = true) {
        this.config = config;

        this.datalist = Object.keys(this.config.data).sort();

        if (this.config.showremovemean == null) {
            this.config.showremovemean = true;
        }
        if (this.config.removemean == null) {
            this.config.removemean = false;
        }

        if (draw) {
            this.draw();
        }
    }

    /**
     * Draws the selector: empties everything and recreates the selector using HTML elements and the measures in datalist.
     */
    draw() {
        let thismodelSelector = this;
        this.config.parentDiv.empty();
        this.config.parentDiv.hide();
        this.config.parentDiv.show();

        let $modelsDiv = $("<div>").addClass("measuresdiv");

        // Add title div
        if (thismodelSelector.config.title != null) {
            $('<div class="ui bottom pointing blue basic label"style="width: 100%; text-align:center;  margin-bottom:0.8rem;">' + thismodelSelector.config.title + '</div>').appendTo(this.config.parentDiv);
        }

        // Reset checkboxes
        thismodelSelector.config.parentDiv.find(".checkbox").off();

        let newDataModel = true;
        let possible_choices = 0;

        let checkBoxType = this.config.exclusive ? "radio" : "checkbox";

        // Create a checkBox for each model in datalist
        for (let modelName of this.datalist) {
            newDataModel = true;
            for (let measureName in thismodelSelector.config.data[modelName].notSH_measures) {
                let measure = thismodelSelector.config.data[modelName].notSH_measures[measureName];
                // Add only the measure given by config.measure
                if (measure.type === thismodelSelector.config.measure) {
                    if (newDataModel) {
                        newDataModel = false;
                        $('<div class="ui divider" style="margin:0.3rem 0"></div>').appendTo($modelsDiv);
                        $('<div class="ui tiny header" style="margin:0">' + modelName + '</div>').appendTo($modelsDiv);
                    }
                    possible_choices += 1;
                    let $checkboxDiv = $('<div>')
                        .addClass('ui checkbox')
                        .css('width', '100%')
                        .attr({
                            dataname: modelName,
                            measurename: measureName
                        });

                    if(this.config.exclusive) {
                        $checkboxDiv.addClass('radio');
                    }

                    $checkboxDiv.append($('<input>')
                        .attr({
                            type: checkBoxType
                        }));
                    $checkboxDiv.append($('<label>').text(measureName));

                    $checkboxDiv.appendTo($modelsDiv).checkbox({
                        onChange: function () {
                            console.log('onChange called', $(this), $(this).checkbox("is checked"));
                            thismodelSelector.config.selectedData = [];
                            thismodelSelector.config.parentDiv.find(".checkbox:not(.removemeancheckbox)").each(function (index) {
                                if ($(this).checkbox("is checked")) {
                                    thismodelSelector.config.selectedData.push({
                                        "dataname": $(this).attr("dataname"),
                                        "measurename": $(this).attr("measurename"),
                                    });
                                }
                            });
                            console.log("SELECTED DATA", thismodelSelector.config.selectedData);
                            if (thismodelSelector.config.onChangeData) {
                                thismodelSelector.config.onChangeData.bind(thismodelSelector)();
                            }
                        }
                    });
                }
            }
        }

        // If no possible choices, inform the user
        if (possible_choices === 0) {
            $('<div class="ui tiny header" style="margin-top:0.5rem; marg">no available measure</div>').appendTo($modelsDiv);
        }
        // If only one choice, pick it automatically
        else if (possible_choices === 1) {
            setTimeout(function () {
                $modelsDiv.find(".checkbox:not(.removemeancheckbox)").checkbox("check");
            }, 500)
        }

        // Add the "Remove temporal mean" checkbox
        if (thismodelSelector.config.showremovemean) {
            var $removemeancheckbox = $("<div>")
                .attr("class", "ui checkbox removemeancheckbox");
            $("<input>").attr("type", "checkbox").attr("name", "removemean").appendTo($removemeancheckbox);
            $("<label>").text("Remove temporal mean").appendTo($removemeancheckbox);
            $('<div class="ui divider" style="margin:0.3rem 0 0.3rem 0"></div>').appendTo($modelsDiv);
            $removemeancheckbox.appendTo($modelsDiv);

            $removemeancheckbox.checkbox({
                onChange: function () {
                    thismodelSelector.config.removemean = $(this).parent(".checkbox").checkbox("is checked");
                    if (thismodelSelector.config.onChangeData) {
                        thismodelSelector.config.onChangeData.bind(thismodelSelector)();
                    }
                }
            }).checkbox((thismodelSelector.config.removemean ? "set checked" : "set unchecked"));
        }

        $modelsDiv.appendTo(this.config.parentDiv);

    }

}
