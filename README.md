# Bioinformatics Project: DNA sequence analysis

## Overview
This is a Django-based web application designed for bioinformatics analysis. It allows users to upload DNA sequences and perform various computational operations to extract biological insights.

## Features
* **Nucleotide composition analysis:** Calculates the percentage of A, T, C, and G.
* **Motif detection:** Identifies specific patterns or sequences within a larger DNA strand.
* **ML Logic integration:** Includes algorithms for sequence processing and biological data interpretation.
* **Responsive web interface:** Built with Django templates for easy interaction.

## Tech stack
* **Backend:** Python 3.11, Django
* **Bioinformatics logic:** Custom algorithms (NumPy / Biopython compatible)
* **Database:** SQLite (local development)
* **Frontend:** HTML5, CSS3

## Installation and setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/Kamila27-pixel/Bioinformatics_project.git](https://github.com/Kamila27-pixel/Bioinformatics_project.git)
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```
