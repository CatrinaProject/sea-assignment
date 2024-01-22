FROM python
WORKDIR /
COPY . /
RUN pip3 install Flask
CMD ["flask", "run", "--host", "0.0.0.0"]
