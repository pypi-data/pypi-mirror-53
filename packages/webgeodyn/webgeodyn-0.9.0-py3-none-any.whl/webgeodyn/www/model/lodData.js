/**
 * Class handling the requests for LOD data
 */
class LodData extends GenericData {
    /**
     * Sets the requestURI to /getloddata.
     */
    constructor() {
        super();
        this.ajaxRequestURI = "/getloddata";
    }

    /**
     * Requests the LOD data to the server and recover it using GenericData.ajaxDataRequest.
     *
     * @param {array} selecteddata - list of the selected models
     * @param {boolean} removemean - whether the temporal mean should be removed or not
     * @returns {Promise<JSON>} JSON containing the request data if success or info on the error otherwise
     */
    getData(selecteddata, removemean) {
        const thisLodData = this;
        return new Promise((resolve, reject) => {
            thisLodData.ajaxDataRequest({
                selecteddata: selecteddata,
                removemean: removemean
            }).then(function (response) {
                console.log("Got Lod Data Response", response);
                if (response.SUCCESS) {
                    resolve(response);
                } else {
                    console.log(response.ERROR);
                    reject(response.ERROR);
                }
            })
                .catch(function (error_msg) {
                    reject(error_msg);
                });
        });
    }
}