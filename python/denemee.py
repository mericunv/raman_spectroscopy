import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------
# Load Data
# -------------------------------------------------------------------------
def load_raman_shift(filename):
    """Load Raman shift values (one per line)."""
    with open(filename, 'r') as f:
        return np.array([float(line.strip()) for line in f])

def load_spectra(filename):
    """Load spectral intensities (multiple samples per line, comma-separated)."""
    spectra = []
    with open(filename, 'r') as f:
        for line in f:
            # Split line by commas and convert to floats
            intensities = [float(x) for x in line.strip().split(",")]
            spectra.append(intensities)
    return np.array(spectra)

# -------------------------------------------------------------------------
# Process Data
# -------------------------------------------------------------------------
try:
    raman_shift = load_raman_shift("raman_shift.csv")
    spectra = load_spectra("spectra.csv")
    
    # Verify dimensions
    num_samples, num_intensity_points = spectra.shape
    if num_intensity_points != len(raman_shift):
        raise ValueError(f"Mismatch: {len(raman_shift)} Raman shifts vs. {num_intensity_points} intensity points per sample.")

    # Average all samples (25 samples per patient as per README)
    average_spectrum = np.mean(spectra, axis=0)

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
    # Plot individual samples (first 5 for demonstration)
    plt.figure(figsize=(12, 6))
    for i in range(min(5, num_samples)):
        plt.plot(raman_shift, spectra[i], linewidth=0.5, alpha=0.5, label=f"Sample {i+1}" if i < 3 else None)
    
    # Plot averaged spectrum
    plt.plot(raman_shift, average_spectrum, color='black', linewidth=2, label="Averaged Spectrum")
    
    plt.xlabel("Raman Shift (cm⁻¹)", fontsize=12)
    plt.ylabel("Intensity (counts)", fontsize=12)
    plt.title("Raman Spectra (Individual Samples and Average)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()