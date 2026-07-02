# Hash-Based-Grayscale-Image-Integrity-Framework-for-Tamper-Detection-and-Recovery
A Python-based framework for grayscale image tamper detection and recovery using SHA-256 hashing, Sudoku-based block mapping, LSB embedding, and AWS S3 cloud storage. The framework detects unauthorized image modifications, reconstructs tampered regions, and evaluates recovery quality using PSNR, MSE, and SSIM.

## Project Overview

This project presents a secure framework for detecting and recovering tampered regions in grayscale images using cryptographic hashing, Sudoku-based block mapping, Least Significant Bit (LSB) embedding, and AWS S3 cloud storage. The framework authenticates image integrity, localizes tampered regions, reconstructs altered image blocks, and evaluates recovery quality using PSNR, MSE, and SSIM.

## Features

- SHA-256 based image authentication
- Block-wise tamper detection using 8×8 image blocks
- Sudoku-based block mapping for secure recovery data distribution
- LSB embedding for self-recovery information
- AWS S3 integration for recovery data storage
- Recovery of tampered image regions
- Performance evaluation using PSNR, MSE, and SSIM

## Technologies Used

- Python
- OpenCV
- NumPy
- Pillow
- Scikit-image
- SHA-256
- AWS S3 Cloud Storage
- Image Processing

## Project Workflow
  
```text
Original Image
      │
      ▼
Generate SHA-256 Hash
      │
      ▼
Sudoku Block Mapping
      │
      ▼
LSB Embedding
      │
      ▼
Embedded Image
      │
      ▼
Tampering
      │
      ▼
Tamper Detection
      │
      ▼
Image Recovery
      │
      ▼
Performance Evaluation
```

## Sample Results

### Original Image

![Original Image](images/Original Image.png)

### Embedded Image

![Embedded Image](images/Embedded Image.png)

### Tampered Image

![Tampered Image](images/Tampered Image.png)

### Tamper Detection

![Tamper Detection](images/Detection.png)

### Recovered Image

![Recovered Image](images/Recovered Image.png)

## Installation

```bash
git clone https://github.com/Sahithi305/Hash-Based-Grayscale-Image-Integrity-Framework-for-Tamper-Detection-and-Recovery.git
cd Hash-Based-Grayscale-Image-Integrity-Framework-for-Tamper-Detection-and-Recovery
pip install -r requirements.txt
```

## Usage

1. Update the image paths according to your system.
2. Run Embedding.py to generate the embedded image.
3. Run Attacks.py to simulate tampering.
4. Run bounding_box.py to detect tampered regions.
5. Run Recovery.py to recover the tampered image.
6. Run metrics.py to evaluate PSNR, MSE, and SSIM.

## Project Documents

The complete project documentation and experimental results are available below:

- 📄 **Project Report:** [Report.pdf](Report.pdf)
- 📊 **Experimental Results:** [Experimental_Results.pdf](Experimental_Results.pdf)
  
## Applications

- Medical image authentication
- Digital forensics
- Military surveillance
- Secure multimedia communication
- Image integrity verification

## Future Enhancements

- Support for color images
- Deep learning based tamper localization
- Real-time cloud deployment
- Enhanced recovery algorithms

## Requirements

- Python 3.9 or later
- NumPy
- OpenCV
- Pillow
- scikit-image
- boto3 (AWS SDK)

> **Note:** Before running the scripts, update all input and output image paths according to your local system.

## Author

**Sahithi**

Mini Project: Hash-Based Grayscale Image Integrity Framework for Tamper Detection and Recovery

  
