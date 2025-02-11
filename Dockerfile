# Use an official PyTorch image with CPU support
FROM pytorch/pytorch

# Set the working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    libglx-mesa0 \
    libgl1 \
    libglib2.0-0 \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Clone the YOLOX repository
COPY . /workspace/YOLOX

# Set the working directory to the YOLOX directory
WORKDIR /workspace/YOLOX

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install pycocotools
RUN pip install --no-cache-dir pycocotools

# Install YOLOX package
RUN pip install --no-cache-dir -e .

# Install watchdog for file monitoring
RUN pip install --no-cache-dir watchdog

# Copy the file-watching script into the container
COPY process_new_files.py /workspace/YOLOX/process_new_files.py

COPY yolox_s.pth /workspace/YOLOX/

# Set the default command to run the file-watching script
CMD ["python", "process_new_files.py"]
