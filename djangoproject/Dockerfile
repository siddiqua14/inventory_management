FROM python:3.11.4-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1



# Install system dependencies
RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin \
    && apt-get clean

# Create and set working directory
WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app/

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

# Command to run the application
CMD ["sh", "./start.sh"]

EXPOSE 8000
