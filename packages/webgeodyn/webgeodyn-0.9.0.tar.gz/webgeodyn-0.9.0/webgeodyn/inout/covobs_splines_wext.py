import os
import glob
import numpy as np
from .covobs_splines import build_gnm_from_file


def load(dataDirectory, dataModel, keepRealisations=False):
    """ Loading function for splines files (COV-OBS-like).  Also adds the data to the dataModel.

    :param dataDirectory: directory where the data is located
    :type dataDirectory: str (path)
    :param dataModel: Model to which the data should be added
    :type dataModel: Model
    :param keepRealisations: indicating if realisations should be kept or averaged (not used)
    :type keepRealisations: bool (default: False)
    :return: 0 if everything went well, -1 otherwise
    :rtype: int
    """
    measures = {"MF": 'models', "EF": 'models_ext'}

    for measureName, measureFolder in measures.items():
        generic_model_path = os.path.join(dataDirectory, measureFolder, 'mod*')
        model_files = glob.glob(str(generic_model_path))
        if len(model_files) == 0:
            print('No spline files were found in {} ! Aborting loading...'.format(dataDirectory))
            return -1

        # Load the latest model in the directory
        model_files.sort(reverse=True)
        print(os.path.basename(model_files[0]))
        times, gnm = build_gnm_from_file(model_files[0])
        Nb = gnm.shape[1]
        if Nb == 1:
            lmax = 1
        else:
            Lb = np.sqrt(Nb+1) - 1
            lmax = int(Lb)
            # Assert that Nb gives an integer Lb
            assert Lb == lmax

        if measureName == "SV":
            units = "nT/yr"
        elif measureName.endswith("F"):
            units = "nT"
        else:
            units = None

        if measureName == 'EF':
            gnm = (-1) * gnm + 20
        dataModel.addMeasure(measureName, measureName, lmax, units, gnm, times=times)

    return 0
