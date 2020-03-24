FROM python:3

# mongo results fetching
ADD fetch_results.py /
RUN pip install pymongo

# web server
COPY index.html /
EXPOSE 7000
CMD nohup python fetch_results.py & \
    python -m http.server 7000