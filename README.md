# Jammertest 2025 GNSS Interference Dataset

This repository contains a curated GNSS interference dataset recorded during **Jammertest 2025** in Andøya, Norway. Jammertest is an authority-controlled outdoor measurement campaign that enables safely managed GNSS jamming, spoofing, and meaconing experiments under realistic propagation conditions.

The dataset is intended for research on GNSS interference monitoring, including interference detection, modulation/waveform classification, interference characterization, multi-source interference analysis, receiver-aware impact assessment, domain-shift evaluation, and direction finding / array-based interference analysis.

---

## Repository structure

The dataset is stored as a sequence of HDF5 files in the `dataset/` directory. Each file contains a consecutive range of samples from one test area.

```text
fraunhoferIIS_jammertest2025/
├── README.md
└── dataset/
    ├── Sample_Area1_0000000_0024999.h5
    ├── Sample_Area1_0025000_0049999.h5
    ├── Sample_Area1_0050000_0074999.h5
    ├── Sample_Area1_0075000_0099999.h5
    ├── Sample_Area1_0100000_0124999.h5
    ├── Sample_Area1_0125000_0149999.h5
    ├── Sample_Area1_0150000_0174999.h5
    ├── Sample_Area1_0175000_0199999.h5
    ├── Sample_Area1_0200000_0224999.h5
    ├── Sample_Area1_0225000_0249999.h5
    ├── Sample_Area1_0250000_0274999.h5
    ├── Sample_Area1_0275000_0299999.h5
    ├── Sample_Area1_0300000_0324999.h5
    └── ...
```

The file naming convention is:

```text
Sample_<Area>_<StartIndex>_<EndIndex>.h5
```

where `<Area>` identifies the test area (`Area1` or `Area2`), `<StartIndex>` is the first sample index contained in the file, and `<EndIndex>` is the last sample index contained in the file. The chunked structure keeps file sizes manageable and enables partial loading during model training and evaluation.

---

## Measurement campaign

The data were recorded during **Jammertest 2025** in Andøya, Norway. The campaign provides a controlled outdoor test environment with a predefined transmission plan specifying when, where, and which signal type was transmitted.

We recorded data at two official outdoor test sites.

### Test Area 1

Test Area 1 is centered around the Bleik community house and its nearby surroundings. It contains a mixture of open outdoor space and nearby structures, enabling realistic propagation effects such as multipath and obstruction.

### Test Area 2

Test Area 2 is a dedicated open-air measurement setup at a parking lot. It is structured around surveyed reference points and fixed geometries, making it suitable for repeatable jammer placements and controlled multi-emitter configurations.

Recordings were performed in parallel in both areas during the campaign schedule.

---

## Receiver setups

The dataset contains recordings from two receiver/antenna configurations.

### Innosense receiver

The first setup is a compact receiver module referred to as `Innosense`. It is equipped with a 3G+C antenna and a dual-band E1/E5 receiver front end.

| Property | Value |
|---|---|
| Receiver type | Compact E1/E5 receiver module |
| Antenna | 3G+C antenna |
| Evaluated bands | E1 and E5, depending on recording |
| Quantization | 8-bit |
| Bandwidth | 40.5 MHz |
| Sampling rate | 81 MHz |
| Power supply | USB |
| Supply voltage | 5 V |
| Power consumption | 2 W |

### CRPA receiver

The second setup uses a controlled reception pattern antenna (`CRPA`) consisting of a 2 x 2 patch array. This setup enables array-based and direction-finding analysis in addition to standard single-receiver interference classification.

| Property | Value |
|---|---|
| Receiver type | CRPA array receiver |
| Antenna | 2 x 2 patch array |
| Bandwidth | 100 MHz |
| Sampling | Quadrature sampled |
| Snapshot duration | 10 microseconds |
| Main use | Wideband and array-based interference analysis |

---

## Signal types and scenarios

The dataset contains a broad set of GNSS interference and deception scenarios. The transmitted events include both single-source and multi-source configurations.

### Area 1 scenarios

Area 1 contains:

- continuous-wave (`CW`) interference,
- frequency sweep (`Sweep`) signals,
- pseudo-random-noise-modulated (`PRN`) jamming,
- meaconing (`Meaconing`),
- spoofing (`Spoofing`),
- mixed meaconing and jamming events,
- mixed meaconing and spoofing events,
- power-step experiments with changing interference strength,
- single-band and multi-band GNSS configurations.

Typical bandwidths include approximately 0.1 MHz for CW interference, 10-20 MHz for PRN interference, and 20 MHz for sweep signals. Pure meaconing and spoofing entries have no nominal jamming bandwidth.

### Area 2 scenarios

Area 2 contains a broader set of waveform families, including `Chirp`, `ChirpB`, `ChirpM`, `ChirpMS`, `Triang`, `FmS`, `Mod`, `PRN`, `CW`, spoofing, and multi-emitter configurations.

Typical bandwidths range from narrowband CW events to wideband chirp and triangular waveforms, including approximately 0.1 MHz, 2 MHz, 20 MHz, 26-30 MHz, 70 MHz, 77-81 MHz, 85-87 MHz, and up to approximately 100 MHz-class events.

---

## Labels and metadata

The dataset is designed for supervised learning and benchmarking. Each recording is associated with campaign metadata such as:

- test area,
- recording day,
- jammer ID,
- signal type,
- GNSS band(s),
- nominal bandwidth,
- power setting,
- start time,
- end time.

These metadata enable time-aligned ground-truth labels for machine learning tasks.

Typical labels used in our experiments include:

| Label | Description |
|---|---|
| `type` | Interference waveform or scenario type, e.g., CW, PRN, Sweep, Chirp, Spoofing |
| `band` | GNSS band(s) affected by the transmission |
| `bandwidth` | Nominal occupied bandwidth in MHz |
| `power` | Transmit-power setting from the campaign metadata |
| `area` | Test Area 1 or Test Area 2 |
| `receiver` | Innosense or CRPA |
| `sample_index` | Sample index within the released file sequence |

The released HDF5 files are intended to be used together with the metadata in this repository and/or the official Jammertest transmission plan.

The /data dataset contains 8-bit quantized raw IQ samples. The samples are stored in interleaved IQ format, i.e., I0, Q0, I1, Q1, and so on. We did not use automatic gain control during the recordings. Instead, we set a defined VGA value for each recording, which is also included in the labels.

The /label dataset has five columns, with the following meaning:
1. Jammer type
2. Signal strength in dBm
3. Jammer bandwidth in MHz
4. VGA value, meaning the Variable-Gain Amplifier setting
5. E-band

We recorded only on the E1 and E5a bands, and this information is represented in the E-band label column.

For the jammer type column, the numeric labels correspond to the following mapping:
jammer_map = {
    "CW": 0,
    "Sweep": 1,
    "Prn": 2,
    "Meac": 3,
    "Spoof": 4,
    "Chirp": 5,
    "ChirpB": 6,
    "Triang": 7,
    "Meac,Prn": 8,
    "Meac,Spoof": 9,
    "Mod": 10,
    "ChirpM": 11,
    "ChirpMS": 12,
    "FmS": 13,
    "Chirp,Spoof": 14,
    "Chirp,Prn": 15,
    "Chirp,Prn,Triang": 16
}

Comma-separated names indicate scenarios with multiple emitters. Please note, however, that there are also scenarios with multiple emitters of the same jammer type, which are not separately labeled. The signal strength is defined as emitted by the jammer. Since different jammers were placed at different distances from our receiver, the received signal strength can vary accordingly. There is no additional metadata file required to interpret the HDF5 labels. The dataset can be used as is.

Official transmission plan repository:

```text
https://github.com/NPRA/jammertest-plan
```

---

## Suggested machine-learning tasks

This dataset supports multiple research tasks.

### 1. Interference classification

Predict the waveform/scenario class from IQ samples, magnitude time series, or spectrograms.

Example classes include CW, Sweep, PRN, Meaconing, Spoofing, Chirp, ChirpB, Triang, Mod, and FmS.

### 2. Interference characterization

Estimate physically meaningful interference attributes, such as modulation/waveform type, occupied bandwidth, signal strength, and affected GNSS band(s).

### 3. Multi-source interference detection

Detect and localize multiple simultaneous interference sources in a spectrogram. This can be formulated as an object-detection task in the time-frequency plane.

### 4. Receiver-aware impact estimation

Use the recorded spectra and estimated interference power to compute navigation-relevant degradation metrics such as the spectral separation coefficient (SSC), jamming resistance factor Q, effective carrier-to-noise density ratio `(C_s/N_0)_eff`, and C/N0 degradation.

### 5. Domain-shift evaluation

Evaluate robustness across Area 1 vs. Area 2, Innosense vs. CRPA, E1 vs. E5, weak vs. strong interference, single-source vs. multi-source interference, and jamming vs. spoofing/meaconing scenarios.

---

## Loading HDF5 files

The dataset is stored in HDF5 format. The exact internal key structure may depend on the exported version. A typical inspection workflow in Python is:

```python
import h5py
import numpy as np

path = "dataset/Sample_Area1_0000000_0024999.h5"

with h5py.File(path, "r") as f:
    # Replace these keys with the keys shown by f.keys()
    samples = np.array(f["samples"])
    labels = np.array(f["labels"])

print(samples.shape)
print(labels.shape)
```

---

## Recommended splits

For benchmarking, we recommend reporting results under several splits:

1. **Random split within one area**: train and test on the same area using a random train/test split.
2. **Area transfer**: train on Area 1 and test on Area 2, and vice versa.
3. **Joint-area training**: train on Area 1 + Area 2 and test separately on each area.
4. **Receiver transfer**: train on one receiver setup and test on the other, where applicable.
5. **Weak-jammer filtering**: evaluate with and without very weak jammer events below a predefined power threshold.

These splits help quantify domain shift across site, receiver, band, and interference strength.

---

## Notes on interpretation

The dataset contains realistic field measurements and therefore includes environmental multipath, varying jammer-receiver geometry, varying signal strength, receiver-specific front-end effects, different bandwidth limitations, heterogeneous class frequencies, and multi-source interference events.

Class distributions are not balanced, because they follow the actual campaign transmission plan. This imbalance is intentional and reflects realistic operational conditions.

---

## Citation

For more information of the dataset and results, see our publication. If you use our dataset for your research, please consider citing:

```
@inproceedings{heublein_ion_gnss2026,
  author = {Lucas Heublein and {I\~{n}igo} Cort\'{e}s Vidal and Tobias Feigl and Alexander Rügamer and Felix Ott},
  title = {{Analyzing and Characterizing Multi-Source Interference Effects at Jammertest Norway 2025}},
  booktitle = {{Proc. of the Intl. Technical Meeting of the Satellite Division of the Institute of Navigation (ION GNSS+)}},
  month = sep,
  year = 2026,
  address = {Orlando, Florida}
}
```

## Acknowledgment

This work has been carried out within the DARCII project, funding code 50NA2401, and the PaiL project, funding code 50NP2506, sponsored by the German Federal Ministry for Economic Affairs and Climate Action (BMWK) and the German Federal Ministry for Transport (BMV), and supported by the German Space Agency at DLR, the Bundesnetzagentur (BNetzA), and the Federal Agency for Cartography and Geodesy (BKG).

## License

This work is licensed under a CC BY-NC-SA 4.0: Creative Commons Attribution-Noncommercial-ShareAlike, see [https://creativecommons.org/licenses/by-nc-sa/4.0/]()

## Contact

If you have any questions or tips to improve the datasets, contact us:

Lucas Heublein: [lucas.heublein@iis.fraunhofer.de]()

Felix Ott: [felix.ott@iis.fraunhofer.de]()

Nordostpark 84, 90411 Nürnberg, Germany, [GoogleMaps](https://www.google.de/maps/place/Fraunhofer-Institut+f%C3%BCr+Integrierte+Schaltungen+IIS,+Standort+N%C3%BCrnberg/@49.486235,11.1276616,17z/data=!4m13!1m7!3m6!1s0x47a1fd54eca9e61f:0xa0f77e8f8bf3c17d!2sNordostpark+84,+90411+N%C3%BCrnberg!3b1!8m2!3d49.4860832!4d11.1290145!3m4!1s0x47a1fd548f392167:0xbf6afa9178ff23d9!8m2!3d49.4861809!4d11.1286658)

Fraunhofer Institute for Integrated Circuits IIS, Nürnberg, Germany
