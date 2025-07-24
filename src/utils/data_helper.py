from pathlib import Path

import mne
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci

def load_eegbci_data(subjects: list[int], runs: list[int], path=None) -> list[str]:
    """
    Load EEG BCI data from the dataset EEG BCI for given subjects and runs. This function also loads the correct montage.

    Parameters
    ----------
    subjects : list of int
        List of subject numbers to load data for.
    runs : list of int
        List of run numbers to load data for.
    path : str or Path, optional
        Path to save or load the data. If None, uses default path.
    Returns
    -------
    raw : raw object
        The raw loaded EEG data concatenated from all subjects and runs.
    """
    if path is None:
        path = Path(r"C:\Users\erik\IES_codebase\pythonProjects\EEG_Exoskeleton\data\raw_data")

    raw_fnames = []
    for subject in subjects:
        fnames = eegbci.load_data(subject, runs, path=path)
        raw_fnames.extend(fnames)

    raws = [read_raw_edf(f, preload=True) for f in raw_fnames]
    raw = concatenate_raws(raws)

    # Should this be here?
    # Maybe this should be part of the input? So that the user can choose which channels to keep?
    raw.annotations.rename(dict(T1="hands", T2="feet"))

    montage = mne.channels.make_standard_montage("standard_1005")

    mne.datasets.eegbci.standardize(raw)  # set channel names
    raw.set_montage(montage, verbose=False)

    return raw

def create_epochs_from_raw(raw, tmin=-1.0, tmax=4.0, event_id=None, baseline=None):
    """
    Create epochs from raw EEG data.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw EEG data.
    tmin : float
        Start time before event in seconds.
    tmax : float
        End time after event in seconds.
    event_id : dict or None
        Dictionary mapping event names to event IDs. If None, all events are used. (Needs to match up with the naming when loading the data.)
    baseline : tuple of float or None
        Baseline correction interval. If None, no baseline correction is applied.

    Returns
    -------
    epochs : mne.Epochs
        The epochs created from the raw data.
    """
    epochs = mne.Epochs(raw, event_id=event_id, tmin=tmin, tmax=tmax,
                        baseline=baseline, preload=True)
    return epochs

def create_train_set(epochs, tmin=1.0, tmax=2.0):
    """
    Create a training dataset from epochs by cropping the time interval and extracting data and labels.

    Parameters
    ----------
    epochs : mne.Epochs
        The input epochs containing EEG data and event information.
    tmin : float, optional
        Start time of the interval to crop in seconds. Default is 1.0.
    tmax : float, optional
        End time of the interval to crop in seconds. Default is 2.0.

    Returns
    -------
    X : ndarray
        The cropped EEG data as a NumPy array of shape (n_epochs, n_channels, n_times).
    y : ndarray
        The labels corresponding to the events, adjusted by subtracting 2.
    """
    epochs_train = epochs.copy().crop(tmin=tmin, tmax=tmax)
    X = epochs_train.get_data(copy=False)

    # This should not be static.
    y = epochs.events[:, -1] - 2

    return X, y

def seperate_brain_waves(epochs):
    """
    Separate EEG epochs into different brain wave frequency bands.

    Parameters
    ----------
    epochs : mne.Epochs
        The input EEG epochs to be filtered into frequency bands.

    Returns
    -------
    brain_wave_epochs : dict
        Dictionary where keys are brain wave names ('Delta', 'Theta', 'Alpha', 'Beta')
        and values are filtered mne.Epochs objects for each frequency band.
    """
    brain_wave_epochs = {}
    brain_wave_freqs = [("Delta", 0, 4), ("Theta", 4, 8), ("Alpha", 8, 12), ("Beta", 12, 40)]

    for name, fmin, fmax in brain_wave_freqs:
        filtered_epochs = epochs.copy().filter(l_freq=fmin, h_freq=fmax, verbose='error')
        brain_wave_epochs[name] = filtered_epochs

    return brain_wave_epochs