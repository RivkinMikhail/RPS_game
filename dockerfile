FROM python:3.8

WORKDIR /code

COPY ./ /code/

RUN apt -y update
RUN apt -y upgrade
RUN apt -y install libusb-1.0-0-dev
RUN apt -y install ffmpeg libsm6 libxext6

RUN pip install --no-cache-dir -r /code/requirements.txt

EXPOSE 8000


CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
# docker run -it --name NAME_FOR_CONTAINER -p 8000:8000 IMAGE_ID
# docker run --privileged=True --device=/dev/video2:/dev/video0 -it -p 8888:8000 test_app
