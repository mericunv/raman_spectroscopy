import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# -------------------------------------------------------------------------
# Load Data
# -------------------------------------------------------------------------
def load_raman_shift(filename):
    """Load Raman shift values (one per line)."""
    with open(filename, 'r') as f:
        return np.array([float(line.strip()) for line in f])

def load_spectra(filename):
    """Load spectral intensities (multiple samples per line, comma-separated)."""
    return np.loadtxt(filename, delimiter=',', skiprows=1)

def load_dataset(filename):
    """Load dataset with names in the first column."""
    df = pd.read_csv(filename)
    names = df.iloc[:, 0].values  # First column contains names
    spectra = df.iloc[:, 1:].values  # Remaining columns contain spectral data
    return names, spectra

# -------------------------------------------------------------------------
# Process Data
# -------------------------------------------------------------------------
try:
    raman_shift = load_raman_shift("raman_shift.csv")
    spectra = load_spectra("spectra.csv")
    dataset_names, dataset_spectra = load_dataset("data_set.csv")
    
    # Verify dimensions
    num_samples, num_intensity_points = spectra.shape
    if num_intensity_points != len(raman_shift):
        raise ValueError(f"Mismatch: {len(raman_shift)} Raman shifts vs. {num_intensity_points} intensity points per sample.")
    
    # Ask user for sample indices
    selected_samples = input("Enter the sample indices to average (comma-separated): ")
    selected_samples = [int(i.strip()) for i in selected_samples.split(',')]
    
    if any(i >= num_samples or i < 0 for i in selected_samples):
        raise ValueError("Selected sample indices are out of range.")
    
    selected_spectra = spectra[selected_samples]
    average_spectrum = np.mean(selected_spectra, axis=0)

    # Compare with dataset_spectra
    distances = np.linalg.norm(dataset_spectra - average_spectrum, axis=1)
    closest_indices = np.argsort(distances)[:5]
    closest_names = dataset_names[closest_indices]
    
    print("Closest 5 spectra in dataset:")
    for name in closest_names:
        print(name)

except FileNotFoundError as e:
    print(f"Error: File not found - {e.filename}")
except ValueError as e:
    print(f"Data Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")

# -------------------------------------------------------------------------
# Plot Results
# -------------------------------------------------------------------------
else:
    plt.figure(figsize=(12, 6))
    
    # Plot selected samples
    for i, sample_index in enumerate(selected_samples):
        plt.plot(raman_shift, spectra[sample_index], linewidth=0.5, alpha=0.5, label=f"Sample {sample_index + 1}")
    
    # Plot averaged spectrum
    plt.plot(raman_shift, average_spectrum, color='black', linewidth=2, label="Averaged Spectrum")
    
    plt.xlabel("Raman Shift (cm⁻¹)", fontsize=12)
    plt.ylabel("Intensity (counts)", fontsize=12)
    plt.title("Raman Spectra (Selected Samples and Average)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()
