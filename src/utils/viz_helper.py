

def plot_brain_wave(brain_wave_epochs, brain_wave="all", title='Brain Wave Signal'):
    """
    Plots brain wave signals from segmented epochs data.

    Parameters:
        brain_wave_epochs (dict): Dictionary mapping brain wave names ('Delta', 'Theta', 'Alpha', 'Beta')
                                 to their corresponding epochs objects.
        brain_wave (str, optional): Specific brain wave to plot ('Delta', 'Theta', 'Alpha', 'Beta').
                                   If 'all', plots all available brain waves. Default is 'all'.
        title (str, optional): Title for the plot. Default is 'Brain Wave Signal'.

    Raises:
        ValueError: If the specified brain wave is not found in `brain_wave_epochs`.

    Notes:
        Each plot displays the average signal for the selected brain wave band.
    """
    brain_wave_freqs = [("Delta", 0, 4), ("Theta", 4, 8), ("Alpha", 8, 12), ("Beta", 12, 40)]

    if brain_wave == "all":
        # Loop through all brain wave frequencies
        for wave_name, low_freq, high_freq in brain_wave_freqs:
            epochs = brain_wave_epochs[wave_name]
            evoked = epochs.average()
            fig = evoked.plot()
            fig.axes[0].set_title(f"{wave_name} Band ({low_freq}-{high_freq} Hz)")
    else:
        # Plot only the specified brain wave
        if brain_wave in brain_wave_epochs:
            epochs = brain_wave_epochs[brain_wave]
            evoked = epochs.average()
            fig = evoked.plot()
            fig.axes[0].set_title(f"{brain_wave} Band")
        else:
            raise ValueError(f"Brain wave '{brain_wave}' not found in the provided epochs.")
