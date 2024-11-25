
FROM python:3.8-slim
WORKDIR /usr/src/app

# Copy the necessary files into the container
COPY fw.bin .
COPY rom.bin .
COPY sram.bin .


# Install Unicorn Engine and any other dependencies
RUN pip install unicorn

# Copy the script that will run the emulation
COPY get_key.py .

# Command to run when the container starts
CMD ["python", "./get_key.py"]